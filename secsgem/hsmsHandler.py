#####################################################################
# hsmsHandler.py
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

from hsmsConnections import hsmsActiveConnection, hsmsPassiveConnection, hsmsSTypes
from hsmsPackets import hsmsPacket, hsmsRejectReqHeader, hsmsStreamFunctionHeader, hsmsSelectReqHeader, \
    hsmsSelectRspHeader, hsmsLinktestReqHeader, hsmsLinktestRspHeader, hsmsDeselectReqHeader, hsmsDeselectRspHeader, \
    hsmsSeparateReqHeader

from common import EventProducer

from fysom import Fysom

# TODO: cesetup after S1F13/14 handling


class hsmsHandler(EventProducer):
    """Baseclass for creating Host/Equipment models. This layer contains the HSMS functionality. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    :param connectionHandler: object for connection handling (ie multi server)
    :type connectionHandler: object

    **Example**::

        import secsgem

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(event, data):
            print "Connected"

        client = secsgem.hsmsHandler("10.211.55.33", 5000, True, 0, "test", eventHandler=secsgem.EventHandler(events={'RemoteConnected': onConnect}))
        client.registerCallback(1, 1, S1F1Handler)

        client.enable()

        time.sleep(3)

        client.disable()

    """
    def __init__(self, address, port, active, sessionID, name, eventHandler=None, customConnectionHandler=None):
        EventProducer.__init__(self, eventHandler)

        self.address = address
        self.port = port
        self.active = active
        self.sessionID = sessionID
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
                {'name': 'select', 'src': 'NOT_SELECTED', 'dst': 'SELECTED'},
                {'name': 'deselect', 'src': 'SELECTED', 'dst': 'NOT_SELECTED'},
                {'name': 'timeoutT7', 'src': 'NOT_SELECTED', 'dst': 'NOT_CONNECTED'},
            ],
            'callbacks': {
                'onNOT_SELECTED': self._onStateConnect,
                'onNOT_CONNECTED': self._onStateDisconnect,
                'onSELECTED': self._onStateSelect,
            },
            'autoforward': [
                {'src': 'CONNECTED', 'dst': 'NOT_SELECTED'}
            ]
        })

        # setup connection
        if self.active:
            self.connection = hsmsActiveConnection(self.address, self.port, self.sessionID, self)
        else:
            if customConnectionHandler is None:
                self.connection = hsmsPassiveConnection(self.address, self.port, self.sessionID, self)
            else:
                self.connection = customConnectionHandler.createConnection(self.address, self.port, self.sessionID, self)

    def _onStateConnect(self, data):
        """Connection state model got event connect

        :param data: event attributes
        :type data: object
        """
        # start linktest timer
        self.linktestTimer = threading.Timer(self.linktestTimeout, self._onLinktestTimer)
        self.linktestTimer.start()

        # start select process if connection is active
        if self.active:
            systemID = self.sendSelectReq()
            self.waitforSelectRsp(systemID)

    def _onStateDisconnect(self, data):
        """Connection state model got event disconnect

        :param data: event attributes
        :type data: object
        """
        # stop linktest timer
        if self.linktestTimer:
            self.linktestTimer.cancel()

        self.linktestTimer = None

    def _onStateSelect(self, data):
        """Connection state model got event select

        :param data: event attributes
        :type data: object
        """
        # send event
        self.fireEvent('HsmsSelected', {'connection': self})

        # notify hsms handler of selection
        if hasattr(self, '_onHsmsSelect') and callable(getattr(self, '_onHsmsSelect')):
            self._onHsmsSelect()

    def _onLinktestTimer(self):
        """Linktest time timed out, so send linktest request"""
        # send linktest request and wait for response
        systemID = self.sendLinktestReq()
        self.waitforLinktestRsp(systemID)

        # restart the timer
        self.linktestTimer = threading.Timer(self.linktestTimeout, self._onLinktestTimer)
        self.linktestTimer.start()

    def _onConnectionEstablished(self):
        """Connection was established

        :param data: event attributes
        :type data: object
        """
        # update connection state
        self.connectionState.connect()

        self.fireEvent("HsmsConnected", {'connection': self})

    def _onBeforeConnectionClosed(self):
        """Connection is about to be closed

        :param data: event attributes
        :type data: object
        """
        # send separate request
        self.sendSeparateReq()

    def _onConnectionClosed(self):
        """Connection was closed

        :param data: event attributes
        :type data: object
        """
        # update connection state
        self.connectionState.disconnect()

        self.fireEvent("HsmsDisconnected", {'connection': self})

    def _queuePacket(self, packet):
        # add to event queue
        self.packetQueue.append(packet)

        # notify all that new event arrived
        for event in self.eventQueue:
            event.set()

    def _onConnectionPacketReceived(self, packet):
        """Packet received by connection

        :param packet: received data packet
        :type packet: object
        """
        if packet.header.sType > 0:
            logging.info("< %s\n  %s", packet, hsmsSTypes[packet.header.sType])

            # check if it is a select request
            if packet.header.sType == 0x01:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.sendRejectRsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.sendSelectRsp(packet.header.system)

                    # update connection state
                    self.connectionState.select()

            # check if it is a select response
            elif packet.header.sType == 0x02:
                # update connection state
                self.connectionState.select()

                # queue packet to notify waiting threads
                self._queuePacket(packet)

            # check if it is a deselect request
            elif packet.header.sType == 0x03:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.sendRejectRsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.sendDeselectRsp(packet.header.system)
                    # update connection state
                    self.connectionState.deselect()

            elif packet.header.sType == 0x04:
                # update connection state
                self.connectionState.deselect()

                # queue packet to notify waiting threads
                self._queuePacket(packet)

            # check if it is a linktest request
            elif packet.header.sType == 0x05:
                # if we are disconnecting send reject else send response
                if self.connection.disconnecting:
                    self.sendRejectRsp(packet.header.system, packet.header.sType, 4)
                else:
                    self.sendLinktestRsp(packet.header.system)

            else:
                # queue packet if not handeled
                self._queuePacket(packet)
        else:
            if not self.connectionState.isstate("SELECTED"):
                logging.info("< %s", packet)
                logging.warning("received message when not selected")
                self.connection.sendPacket(hsmsPacket(hsmsRejectReqHeader(packet.header.system, packet.header.sType, 4)))

                return True

            #redirect packet to hsms handler
            if hasattr(self, '_onHsmsPacketReceived') and callable(getattr(self, '_onHsmsPacketReceived')):
                self._onHsmsPacketReceived(packet)
            else:
                logging.info("< %s", packet)

    def _serializeData(self):
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

    def waitforStreamFunction(self, stream, function, isControl=False):
        """Wait for an incoming stream and function and return the receive data

        :param stream: number of stream to wait for
        :type stream: integer
        :param function: number of function to wait for
        :type function: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        if isControl:
            # setup timeout to T6
            timeout = time.time() + self.connection.T6
        else:
            # setup timeout to T3
            timeout = time.time() + self.connection.T3

        # setup event for new item in queue
        event = threading.Event()
        self.eventQueue.append(event)

        foundPacket = None

        while foundPacket is None:
            for packet in self.packetQueue:
                if (packet.header.stream == stream) and (packet.header.function == function):
                    self.packetQueue.remove(packet)
                    foundPacket = packet
                    break

            if foundPacket is None:
                if event.wait(1) == True:
                    event.clear()
                elif not self.connected or self.connection.disconnecting or time.time() > timeout:
                    return None

        self.eventQueue.remove(event)

        return packet

    def sendStreamFunction(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secsFunctionBase.secsStreamFunction`
        """
        outPacket = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), packet._stream, packet._function, True, self.sessionID), packet.encode())
        self.connection.sendPacket(outPacket)

    def waitforSystem(self, system, isControl=False):
        """Wait for an message with supplied system

        :param system: number of system to wait for
        :type system: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        if isControl:
            # setup timeout to T6
            timeout = time.time() + self.connection.T6
        else:
            # setup timeout to T3
            timeout = time.time() + self.connection.T3

        event = threading.Event()
        self.eventQueue.append(event)

        foundPacket = None

        while foundPacket is None:
            for packet in self.packetQueue:
                if (packet.header.system == system):
                    self.packetQueue.remove(packet)
                    foundPacket = packet
                    break

            if foundPacket is None:
                if event.wait(1) == True:
                    event.clear()
                elif not self.connected or self.connection.disconnecting or time.time() > timeout:
                    return None

        self.eventQueue.remove(event)

        return packet

    def sendAndWaitForResponse(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secsFunctionBase.secsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        outPacket = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), packet._stream, packet._function, True, self.sessionID), packet.encode())
        self.connection.sendPacket(outPacket)

        return self.waitforSystem(outPacket.header.system, (packet._stream == 0))

    def sendResponse(self, packet, system):
        """Send response packet for system

        :param packet: packet to be sent
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        :param system: system to reply to
        :type system: integer
        """
        outPacket = hsmsPacket(hsmsStreamFunctionHeader(system, packet._stream, packet._function, False, self.sessionID), packet.encode())
        self.connection.sendPacket(outPacket)

    def sendSelectReq(self):
        """Send a Select Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        systemID = self.connection.getNextSystemCounter()

        packet = hsmsPacket(hsmsSelectReqHeader(systemID))
        self.connection.sendPacket(packet)

        return systemID

    def sendSelectRsp(self, systemID):
        """Send a Select Response to the remote host

        :param systemID: System of the request to reply for
        :type systemID: integer
        """
        packet = hsmsPacket(hsmsSelectRspHeader(systemID))
        self.connection.sendPacket(packet)

    def waitforSelectRsp(self, systemID):
        """Wait for an incoming Select Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        result = self.waitforSystem(systemID, True)

        return result

    def sendLinktestReq(self):
        """Send a Linktest Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        systemID = self.connection.getNextSystemCounter()

        packet = hsmsPacket(hsmsLinktestReqHeader(systemID))
        self.connection.sendPacket(packet)

        return systemID

    def sendLinktestRsp(self, systemID):
        """Send a Linktest Response to the remote host

        :param systemID: System of the request to reply for
        :type systemID: integer
        """
        packet = hsmsPacket(hsmsLinktestRspHeader(systemID))
        self.connection.sendPacket(packet)

    def waitforLinktestRsp(self, systemID):
        """Wait for an incoming Linktest Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        return self.waitforSystem(systemID, True)

    def sendDeselectReq(self):
        """Send a Deselect Request to the remote host

        :returns: System of the sent request
        :rtype: integer
        """
        systemID = self.connection.getNextSystemCounter()

        packet = hsmsPacket(hsmsDeselectReqHeader(systemID))
        self.connection.sendPacket(packet)

        return systemID

    def sendDeselectRsp(self, systemID):
        """Send a Deselect Response to the remote host

        :param systemID: System of the request to reply for
        :type systemID: integer
        """
        packet = hsmsPacket(hsmsDeselectRspHeader(systemID))
        self.connection.sendPacket(packet)

    def waitforDeselectRsp(self, systemID):
        """Wait for an incoming Deselect Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        result = self.waitforSystem(systemID)

        return result

    def sendRejectRsp(self, systemID, sType, reason):
        """Send a Reject Response to the remote host

        :param systemID: System of the request to reply for
        :type systemID: integer
        :param sType: sType of rejected message
        :type sType: integer
        :param reason: reason for rejection
        :type reason: integer
        """
        packet = hsmsPacket(hsmsRejectReqHeader(systemID, sType, reason))
        self.connection.sendPacket(packet)

    def sendSeparateReq(self):
        """Send a Separate Request to the remote host"""
        systemID = self.connection.getNextSystemCounter()

        packet = hsmsPacket(hsmsSeparateReqHeader(systemID))
        self.connection.sendPacket(packet)

        return systemID
