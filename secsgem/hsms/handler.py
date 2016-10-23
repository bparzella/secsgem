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

from __future__ import absolute_import

import random
import threading
import logging
import queue

from ..common.callbacks import CallbackHandler
from ..common.events import EventProducer

from .connections import HsmsActiveConnection, HsmsPassiveConnection, hsmsSTypes
from .packets import HsmsPacket, HsmsRejectReqHeader, HsmsStreamFunctionHeader,\
    HsmsSelectReqHeader, HsmsSelectRspHeader, HsmsLinktestReqHeader, HsmsLinktestRspHeader, \
    HsmsDeselectReqHeader, HsmsDeselectRspHeader, HsmsSeparateReqHeader

from .connectionstatemachine import ConnectionStateMachine

class HsmsHandler(object):
    """Baseclass for creating Host/Equipment models.

    This layer contains the HSMS functionality.
    Inherit from this class and override required functions.

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
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`

    **Example**::

        import secsgem

        def onConnect(event, data):
            print "Connected"

        client = secsgem.HsmsHandler("10.211.55.33", 5000, True, 0, "test")
        client.events.hsms_connected += onConnect

        client.enable()

        time.sleep(3)

        client.disable()

    """

    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        self._eventProducer = EventProducer()
        self._eventProducer.targets += self

        self._callback_handler = CallbackHandler()
        self._callback_handler.target = self

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self.communicationLogger = logging.getLogger("hsms_communication")

        self.address = address
        self.port = port
        self.active = active
        self.sessionID = session_id
        self.name = name

        self.connected = False

        # system id counter
        self.systemCounter = random.randint(0, (2 ** 32) - 1)

        # repeating linktest variables
        self.linktestTimer = None
        self.linktestTimeout = 30

        # select request thread for active connections, to avoid blocking state changes
        self.selectReqThread = None

        # response queues
        self._systemQueues = {}

        # hsms connection state fsm
        self.connectionState = ConnectionStateMachine({"on_enter_CONNECTED": self._on_state_connect,
                                                       "on_exit_CONNECTED": self._on_state_disconnect,
                                                       "on_enter_CONNECTED_SELECTED": self._on_state_select})

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

    @property
    def events(self):
        """Property for event handling""" 
        return self._eventProducer

    @property
    def callbacks(self):
        """Property for callback handling""" 
        return self._callback_handler

    def get_next_system_counter(self):
        """Returns the next System.

        :returns: System for the next command
        :rtype: integer
        """
        self.systemCounter += 1

        if self.systemCounter > ((2 ** 32) - 1):
            self.systemCounter = 0

        return self.systemCounter

    def _sendSelectReqThread(self):
        response = self.send_select_req()
        if response is None:
            self.logger.warning("select request failed")

    def _start_linktest_timer(self):
        self.linktestTimer = threading.Timer(self.linktestTimeout, self._on_linktest_timer)
        self.linktestTimer.daemon = True  # kill thread automatically on main program termination
        self.linktestTimer.name = "secsgem_hsmsHandler_linktestTimer"
        self.linktestTimer.start()

    def _on_state_connect(self):
        """Connection state model got event connect

        :param data: event attributes
        :type data: object
        """
        # start linktest timer
        self._start_linktest_timer()

        # start select process if connection is active
        if self.active:
            self.selectReqThread = threading.Thread(target=self._sendSelectReqThread, name="secsgem_hsmsHandler_sendSelectReqThread")
            self.selectReqThread.daemon = True  # kill thread automatically on main program termination
            self.selectReqThread.start() 

    def _on_state_disconnect(self):
        """Connection state model got event disconnect

        :param data: event attributes
        :type data: object
        """
        # stop linktest timer
        if self.linktestTimer:
            self.linktestTimer.cancel()

        self.linktestTimer = None

    def _on_state_select(self):
        """Connection state model got event select

        :param data: event attributes
        :type data: object
        """
        # send event
        self.events.fire('hsms_selected', {'connection': self})

        # notify hsms handler of selection
        if hasattr(self, '_on_hsms_select') and callable(getattr(self, '_on_hsms_select')):
            self._on_hsms_select()

    def _on_linktest_timer(self):
        """Linktest time timed out, so send linktest request"""
        # send linktest request and wait for response
        self.send_linktest_req()

        # restart the timer
        self._start_linktest_timer()

    def on_connection_established(self, _):
        """Connection was established"""
        self.connected = True

        # update connection state
        self.connectionState.connect()

        self.events.fire("hsms_connected", {'connection': self})

    def on_connection_before_closed(self, _):
        """Connection is about to be closed"""
        # send separate request
        self.send_separate_req()

    def on_connection_closed(self, _):
        """Connection was closed"""
        # update connection state
        self.connected = False
        self.connectionState.disconnect()

        self.events.fire("hsms_disconnected", {'connection': self})

    def __handle_hsms_requests(self, packet):
        self.communicationLogger.info("< %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())

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

            if packet.header.system in self._systemQueues:
                # send packet to request sender
                self._systemQueues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?

        # check if it is a deselect request
        elif packet.header.sType == 0x03:
            # if we are disconnecting send reject else send response
            if self.connection.disconnecting:
                self.send_reject_rsp(packet.header.system, packet.header.sType, 4)
            else:
                self.send_deselect_rsp(packet.header.system)
                # update connection state
                self.connectionState.deselect()

        # check if it is a deselect response
        elif packet.header.sType == 0x04:
            # update connection state
            self.connectionState.deselect()

            if packet.header.system in self._systemQueues:
                # send packet to request sender
                self._systemQueues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?

        # check if it is a linktest request
        elif packet.header.sType == 0x05:
            # if we are disconnecting send reject else send response
            if self.connection.disconnecting:
                self.send_reject_rsp(packet.header.system, packet.header.sType, 4)
            else:
                self.send_linktest_rsp(packet.header.system)

        else:
            if packet.header.system in self._systemQueues:
                # send packet to request sender
                self._systemQueues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?
            
    def on_connection_packet_received(self, _, packet):
        """Packet received by connection

        :param packet: received data packet
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        if packet.header.sType > 0:
            self.__handle_hsms_requests(packet)
        else:
            if hasattr(self, 'secs_decode') and callable(getattr(self, 'secs_decode')):
                message = self.secs_decode(packet)
                self.communicationLogger.info("< %s\n%s", packet, message, extra=self._get_log_extra())
            else:
                self.communicationLogger.info("< %s", packet, extra=self._get_log_extra())

            if not self.connectionState.is_CONNECTED_SELECTED():
                self.logger.warning("received message when not selected")

                out_packet = HsmsPacket(HsmsRejectReqHeader(packet.header.system, packet.header.sType, 4))
                self.communicationLogger.info("> %s\n  %s", out_packet, hsmsSTypes[out_packet.header.sType], extra=self._get_log_extra())
                self.connection.send_packet(out_packet)

                return True

            # someone is waiting for this message
            if packet.header.system in self._systemQueues:
                # send packet to request sender
                self._systemQueues[packet.header.system].put_nowait(packet)
            # redirect packet to hsms handler
            elif hasattr(self, '_on_hsms_packet_received') and callable(getattr(self, '_on_hsms_packet_received')):
                self._on_hsms_packet_received(packet)
            # just log if nobody is interested
            else:
                self.logger.warning("packet unhandled")

    def _get_queue_for_system(self, system_id):
        """Creates a new queue to receive responses for a certain system

        :param system_id: system id to watch
        :type system_id: int
        :returns: queue to receive responses with
        :rtype: queue.Queue
        """
        self._systemQueues[system_id] = queue.Queue()
        return self._systemQueues[system_id]

    def _remove_queue(self, system_id):
        """Remove queue for system id from list

        :param system_id: system id to remove
        :type system_id: int
        """
        del self._systemQueues[system_id]

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        return "{} {}".format(self.__class__.__name__, str(self._serialize_data()))

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

    def send_stream_function(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        """
        out_packet = HsmsPacket( \
            HsmsStreamFunctionHeader(self.get_next_system_counter(), packet.stream, packet.function, True, self.sessionID), \
            packet.encode())

        self.communicationLogger.info("> %s\n%s", out_packet, packet, extra=self._get_log_extra())

        return self.connection.send_packet(out_packet)

    def send_and_waitfor_response(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_packet = HsmsPacket(HsmsStreamFunctionHeader(system_id, packet.stream, packet.function, True, self.sessionID), packet.encode())

        self.communicationLogger.info("> %s\n%s", out_packet, packet, extra=self._get_log_extra())

        if not self.connection.send_packet(out_packet):
            self.logger.error("Sending packet failed")
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.connection.T3)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_response(self, function, system):
        """Send response function for system

        :param function: function to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :param system: system to reply to
        :type system: integer
        """
        out_packet = HsmsPacket(HsmsStreamFunctionHeader(system, function.stream, function.function, False, self.sessionID), function.encode())

        self.communicationLogger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        return self.connection.send_packet(out_packet)

    def send_select_req(self):
        """Send a Select Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsSelectReqHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())

        if not self.connection.send_packet(packet):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.connection.T6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_select_rsp(self, system_id):
        """Send a Select Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsSelectRspHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())
        return self.connection.send_packet(packet)

    def send_linktest_req(self):
        """Send a Linktest Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsLinktestReqHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())

        if not self.connection.send_packet(packet):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.connection.T6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_linktest_rsp(self, system_id):
        """Send a Linktest Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsLinktestRspHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())
        return self.connection.send_packet(packet)

    def send_deselect_req(self):
        """Send a Deselect Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsDeselectReqHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())

        if not self.connection.send_packet(packet):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.connection.T6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_deselect_rsp(self, system_id):
        """Send a Deselect Response to the remote host

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        packet = HsmsPacket(HsmsDeselectRspHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())
        return self.connection.send_packet(packet)

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
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())
        return self.connection.send_packet(packet)

    def send_separate_req(self):
        """Send a Separate Request to the remote host"""
        system_id = self.get_next_system_counter()

        packet = HsmsPacket(HsmsSeparateReqHeader(system_id))
        self.communicationLogger.info("> %s\n  %s", packet, hsmsSTypes[packet.header.sType], extra=self._get_log_extra())

        if not self.connection.send_packet(packet):
            return None

        return system_id

    # helpers

    def _get_log_extra(self):
        return {"address": self.address, "port": self.port, "sessionID": self.sessionID, "remoteName": self.name}
