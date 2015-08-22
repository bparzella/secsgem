#####################################################################
# handler.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
"""Contains class to create model for hsms endpoints."""

import logging
import time
import threading

from secsgem.common import EventProducer
from secsgem.common.fysom import Fysom

from connections import HsmsActiveConnection, HsmsPassiveConnection, hsmsSTypes
from packets import HsmsPacket, HsmsRejectReqHeader, HsmsStreamFunctionHeader, HsmsSelectReqHeader, \
    HsmsSelectRspHeader, HsmsLinktestReqHeader, HsmsLinktestRspHeader, HsmsDeselectReqHeader, HsmsDeselectRspHeader, \
    HsmsSeparateReqHeader


class HsmsHandler(EventProducer):
    """Baseclass for creating Host/Equipment models. This layer contains the HSMS functionality. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`

    **Example**::

        import secsgem

        def onConnect(event, data):
            print "Connected"

        client = secsgem.HsmsHandler("10.211.55.33", 5000, True, 0, "test", event_handler=secsgem.EventHandler(events={'hsms_connected': onConnect}))

        client.enable()

        time.sleep(3)

        client.disable()

    """
    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        EventProducer.__init__(self, event_handler)

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.address = address
        self.port = port
        self.active = active
        self.sessionID = session_id
        self.name = name

        self.connected = False

        # repeating linktest variables
        self.linktestTimer = None
        self.linktestTimeout = 30

        # event and packet queues
        self.eventQueue = []
        self.packetQueue = []

        # hsms connection state fsm
        self.connectionState = Fysom({
            'initial': 'NOT_CONNECTED',
            'events': [
                {'name': 'connect', 'src': 'NOT_CONNECTED', 'dst': 'CONNECTED'},
                {'name': 'disconnect', 'src': ['CONNECTED', 'NOT_SELECTED', 'SELECTED'], 'dst': 'NOT_CONNECTED'},
                {'name': 'select', 'src': ['CONNECTED', 'NOT_SELECTED'], 'dst': 'SELECTED'},
                {'name': 'deselect', 'src': 'SELECTED', 'dst': 'NOT_SELECTED'},
                {'name': 'timeoutT7', 'src': ['CONNECTED', 'NOT_SELECTED'], 'dst': 'NOT_CONNECTED'},
            ],
            'callbacks': {
                'onNOT_SELECTED': self._on_state_connect,
                'onNOT_CONNECTED': self._on_state_disconnect,
                'onSELECTED': self._on_state_select,
            },
            'autoforward': [
                {'src': 'CONNECTED', 'dst': 'NOT_SELECTED'}
            ]
        })

        # setup connection
        if self.active:
            if custom_connection_handler is None:
                self.connection = HsmsActiveConnection(self.address, self.port, self.sessionID, self)
            else:
                self.connection = custom_connection_handler.create_connection(self.address, self.port, self.sessionID, self)
        else:
            if custom_connection_handler is None:
                self.connection = HsmsPassiveConnection(self.address, self.port, self.sessionID, self)
            else:
                self.connection = custom_connection_handler.create_connection(self.address, self.port, self.sessionID, self)

    def _on_state_connect(self, _):
        """Connection state model got event connect

        :param data: event attributes
        :type data: object
        """
        # start linktest timer
        self.linktestTimer = threading.Timer(self.linktestTimeout, self._on_linktest_timer)
        self.linktestTimer.start()

        # start select process if connection is active
        if self.active:
            system_id = self.send_select_req()
            self.waitfor_select_rsp(system_id)

    def _on_state_disconnect(self, _):
        """Connection state model got event disconnect

        :param data: event attributes
        :type data: object
        """
        # stop linktest timer
        if self.linktestTimer:
            self.linktestTimer.cancel()

        self.linktestTimer = None

    def _on_state_select(self, _):
        """Connection state model got event select

        :param data: event attributes
        :type data: object
        """
        # send event
        self.fire_event('hsms_selected', {'connection': self})

        # notify hsms handler of selection
        if hasattr(self, '_on_hsms_select') and callable(getattr(self, '_on_hsms_select')):
            self._on_hsms_select()

    def _on_linktest_timer(self):
        """Linktest time timed out, so send linktest request"""
        # send linktest request and wait for response
        system_id = self.send_linktest_req()
        self.waitfor_linktest_rsp(system_id)

        # restart the timer
        self.linktestTimer = threading.Timer(self.linktestTimeout, self._on_linktest_timer)
        self.linktestTimer.start()

    def on_connection_established(self, _):
        """Connection was established"""
        # update connection state
        self.connectionState.connect()

        self.connected = True

        self.fire_event("hsms_connected", {'connection': self})

    def on_connection_before_closed(self, _):
        """Connection is about to be closed"""
        # send separate request
        self.send_separate_req()

    def on_connection_closed(self, _):
        """Connection was closed"""
        # update connection state
        self.connected = False
        self.connectionState.disconnect()

        self.fire_event("hsms_disconnected", {'connection': self})

    def _queue_packet(self, packet):
        """Add packet to event queue

        :param packet: received data packet
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        # add to event queue
        self.packetQueue.append(packet)

        # notify all that new event arrived
        for event in self.eventQueue:
            event.set()

    def on_connection_packet_received(self, _, packet):
        """Packet received by connection

        :param packet: received data packet
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        if packet.header.sType > 0:
            self.logger.info("< %s\n  %s", packet, hsmsSTypes[packet.header.sType])

            # check if it is a select request
            if packet.header.sType == 0x01:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.send_reject_rsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.send_select_rsp(packet.header.system)

                    # update connection state
                    self.connectionState.select()

            # check if it is a select response
            elif packet.header.sType == 0x02:
                # update connection state
                self.connectionState.select()

                # queue packet to notify waiting threads
                self._queue_packet(packet)

            # check if it is a deselect request
            elif packet.header.sType == 0x03:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.send_reject_rsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.send_deselect_rsp(packet.header.system)
                    # update connection state
                    self.connectionState.deselect()

            elif packet.header.sType == 0x04:
                # update connection state
                self.connectionState.deselect()

                # queue packet to notify waiting threads
                self._queue_packet(packet)

            # check if it is a linktest request
            elif packet.header.sType == 0x05:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.send_reject_rsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.send_linktest_rsp(packet.header.system)

            else:
                # queue packet if not handeled
                self._queue_packet(packet)
        else:
            if not self.connectionState.isstate("SELECTED"):
                self.logger.info("< %s", packet)
                self.logger.warning("received message when not selected")
                self.connection.send_packet(HsmsPacket(HsmsRejectReqHeader(packet.header.system, packet.header.sType, 4)))

                return True

            # redirect packet to hsms handler
            if hasattr(self, '_on_hsms_packet_received') and callable(getattr(self, '_on_hsms_packet_received')):
                self._on_hsms_packet_received(packet)
            else:
                self.logger.info("< %s", packet)

    def _serialize_data(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {'address': self.address, 'port': self.port, 'active': self.active, 'sessionID': self.sessionID, 'name': self.name, 'connected': self.connected}

    def enable(self):
        """Enables the connection"""
        self.connection.enable()

    def disable(self):
        """Disables the connection"""
        self.connection.disable()

    def waitfor_stream_function(self, stream, function, is_control=False):
        """Wait for an incoming stream and function and return the receive data

        :param stream: number of stream to wait for
        :type stream: integer
        :param function: number of function to wait for
        :type function: integer
        :param is_control: is it a control packet
        :type is_control: bool
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        if is_control:
            # setup timeout to T6
            timeout = time.time() + self.connection.T6
        else:
            # setup timeout to T3
            timeout = time.time() + self.connection.T3

        # setup event for new item in queue
        event = threading.Event()
        self.eventQueue.append(event)

        found_packet = None

        while found_packet is None:
            for packet in self.packetQueue:
                if (packet.header.stream == stream) and (packet.header.function == function):
                    self.packetQueue.remove(packet)
                    found_packet = packet
                    break

            if found_packet is None:
                if event.wait(1):
                    event.clear()
                elif not self.connected or self.connection.disconnecting or time.time() > timeout:
                    return None

        self.eventQueue.remove(event)

        return found_packet

    def send_stream_function(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        """
        out_packet = HsmsPacket(HsmsStreamFunctionHeader(self.connection.get_next_system_counter(), packet.stream, packet.function, True, self.sessionID), packet.encode())
        self.connection.send_packet(out_packet)

    def waitfor_system(self, system, is_control=False):
        """Wait for an message with supplied system

        :param system: number of system to wait for
        :type system: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        if not self.connected:
            self.logger.warning("handler not connected waiting for response for system {0}".format(system))
            return None

        if is_control:
            # setup timeout to T6
            timeout = time.time() + self.connection.T6
        else:
            # setup timeout to T3
            timeout = time.time() + self.connection.T3

        event = threading.Event()
        self.eventQueue.append(event)

        found_packet = None

        while found_packet is None:
            for packet in self.packetQueue:
                if packet.header.system == system:
                    self.packetQueue.remove(packet)
                    found_packet = packet
                    break

            if found_packet is None:
                if event.wait(1):
                    event.clear()
                elif not self.connected or self.connection.disconnecting or time.time() > timeout:
                    self.logger.warning("response for system {0} not received within timeout".format(system))
                    return None

        self.eventQueue.remove(event)

        return found_packet

    def send_and_waitfor_response(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        out_packet = HsmsPacket(HsmsStreamFunctionHeader(self.connection.get_next_system_counter(), packet.stream, packet.function, True, self.sessionID), packet.encode())
        self.connection.send_packet(out_packet)

        return self.waitfor_system(out_packet.header.system, (packet.stream == 0))

    def send_response(self, function, system):
        """Send response function for system

        :param function: function to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :param system: system to reply to
        :type system: integer
        """
        out_packet = HsmsPacket(HsmsStreamFunctionHeader(system, function.stream, function.function, False, self.sessionID), function.encode())
        self.connection.send_packet(out_packet)

    def send_select_req(self):
        """Send a Select Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.connection.get_next_system_counter()

        packet = HsmsPacket(HsmsSelectReqHeader(system_id))
        self.connection.send_packet(packet)

        return system_id

    def send_select_rsp(self, system_id):
        """Send a Select Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsSelectRspHeader(system_id))
        self.connection.send_packet(packet)

    def waitfor_select_rsp(self, system_id):
        """Wait for an incoming Select Response

        :param system_id: System of the request to reply for
        :type system_id: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        result = self.waitfor_system(system_id, True)

        return result

    def send_linktest_req(self):
        """Send a Linktest Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.connection.get_next_system_counter()

        packet = HsmsPacket(HsmsLinktestReqHeader(system_id))
        self.connection.send_packet(packet)

        return system_id

    def send_linktest_rsp(self, system_id):
        """Send a Linktest Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsLinktestRspHeader(system_id))
        self.connection.send_packet(packet)

    def waitfor_linktest_rsp(self, system_id):
        """Wait for an incoming Linktest Response

        :param system_id: System of the request to reply for
        :type system_id: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        return self.waitfor_system(system_id, True)

    def send_deselect_req(self):
        """Send a Deselect Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.connection.get_next_system_counter()

        packet = HsmsPacket(HsmsDeselectReqHeader(system_id))
        self.connection.send_packet(packet)

        return system_id

    def send_deselect_rsp(self, system_id):
        """Send a Deselect Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsDeselectRspHeader(system_id))
        self.connection.send_packet(packet)

    def waitfor_deselect_rsp(self, system_id):
        """Wait for an incoming Deselect Response

        :param system_id: System of the request to reply for
        :type system_id: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        result = self.waitfor_system(system_id, True)

        return result

    def send_reject_rsp(self, system_id, s_type, reason):
        """Send a Reject Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        :param s_type: s_type of rejected message
        :type s_type: integer
        :param reason: reason for rejection
        :type reason: integer
        """
        packet = HsmsPacket(HsmsRejectReqHeader(system_id, s_type, reason))
        self.connection.send_packet(packet)

    def send_separate_req(self):
        """Send a Separate Request to the remote host"""
        system_id = self.connection.get_next_system_counter()

        packet = HsmsPacket(HsmsSeparateReqHeader(system_id))
        self.connection.send_packet(packet)

        return system_id
