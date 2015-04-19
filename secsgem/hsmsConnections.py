#####################################################################
# hsmsConnections.py
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
"""Contains objects and functions to create and handle hsms connection."""

import logging

import socket
import select
import struct

import thread
import threading
import traceback

import time

import errno

from hsmsPackets import *

from common import *

"""Names for hsms header SType"""
hsmsSTypes = {
    1: "Select.req",
    2: "Select.rsp",
    3: "Deselect.req",
    4: "Deselect.rsp",
    5: "Linktest.req",
    6: "Linktest.rsp",
    9: "Separate.req"
}

def isErrorCodeEWouldBlock(errorcode):
    if errorcode == errno.EAGAIN or errorcode == errno.EWOULDBLOCK:
        return True

    return False

class hsmsConnectionState:
    """hsms connection state machine states"""
    NOT_CONNECTED, CONNECTED, NOT_SELECTED, SELECTED = range(4)

class hsmsSingleServer(StreamFunctionCallbackHandler, EventProducer):
    """Server class for single passive (incoming) connection 

    Creates a listening socket and waits for one incoming connection on this socket. After the connection is established the listening socket is closed.

    :param port: TCP port to listen on for incoming connections 
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`

    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        server = secsgem.hsmsConnections.hsmsSingleServer(5000, eventHandler=EventHandler(events={'RemoteInitialized': onConnect}))
        server.registerCallback(1, 1, S1F1Handler)

        connection = server.waitForConnection()

        time.sleep(3)

        connection.disconnect()

    """
    def __init__(self, port = 5000, sessionID = 0, eventHandler=None):
        StreamFunctionCallbackHandler.__init__(self)
        EventProducer.__init__(self, eventHandler)

        self.port = port
        self.sessionID = sessionID

    def waitForConnection(self):
        """Wait for incoming connection

        Opens listening socket and waits (blocking) for the connection. Terminates the listening socket and returns the new connection.

        :returns: the newly established connection
        :rtype: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not isWindows():
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('', self.port))
        sock.listen(1)

        while True:
            accept_result = sock.accept()
            if accept_result == None:
                continue

            (sock,(sourceIP, sourcePort)) = accept_result

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            connection = hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, eventHandler = self.parentEventHandler)

            self.fireEvent("RemoteConnected", {'connection': connection})

            connection.startReceiver()

            self.fireEvent("RemoteInitialized", {'connection': connection})

            return connection

        sock.close()

#start server accepting all connections
class hsmsMultiServer(StreamFunctionCallbackHandler, EventProducer):
    """Server class for multiple passive (incoming) connection. The server creates a listening socket and waits for incoming connections on this socket.

    :param port: TCP port to listen on
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    
    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        server = secsgem.hsmsConnections.hsmsMultiServer(5000, eventHandler=EventHandler(events={'RemoteInitialized': onConnect}))
        server.registerCallback(1, 1, S1F1Handler)

        server.start()

        time.sleep(3)

        server.stop()

    """

    selectTimeout = 0.5
    """ Timeout for select calls """ 

    def __init__(self, port=5000, sessionID=0, eventHandler=None):
        StreamFunctionCallbackHandler.__init__(self)
        EventProducer.__init__(self, eventHandler)

        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not isWindows():
            self.listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sessionID = sessionID
        self.port = port

        self.threadRunning = False
        self.stopThread = False

        self.connections = []
        self.connectionsLock = threading.Lock()

        self.listenThreadIdentifier = None

    def start(self):
        """Starts the server and returns. It will launch a listener running in background to wait for incoming connections."""
        self.listenSock.bind(('', self.port))
        self.listenSock.listen(1)
        self.listenSock.setblocking(0)

        self.listenThreadIdentifier = threading.Thread(target=self._listen_thread, args=())
        self.listenThreadIdentifier.start()

        logging.debug("hsmsMultiServer.start: listening")

    def stop(self, terminateConnections = True):
        """Stops the server. The background job waiting for incoming connections will be terminated. Optionally all connections received will be closed.

        :param terminateConnections: terminate all connection made by this server
        :type terminateConnections: boolean
        """
        self.stopThread = True

        if self.listenThreadIdentifier.isAlive:
            while self.threadRunning:
                pass

        self.listenSock.close()

        self.connectionsLock.acquire()

        if terminateConnections:
            for connection in self.connections:
                if connection.connected:
                    connection.disconnect(separate = True)

        self.connectionsLock.release()

        logging.debug("hsmsMultiServer.stop: server stopped")

    def _listen_thread(self):
        """Thread listening for incoming connections

        .. warning:: Do not call this directly, used internally.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                selectResult = select.select([self.listenSock], [], [self.listenSock], self.selectTimeout)

                if selectResult[0]:
                    accept_result = None

                    try:
                        accept_result = self.listenSock.accept()
                    except socket.error, e:
                        errorcode = e[0]
                        if not isErrorCodeEWouldBlock(errorcode):
                            raise e

                    if accept_result == None:
                        continue

                    if self.stopThread:
                        continue

                    logging.debug("hsmsMultiServer._listen_thread: connection from %s:%d", accept_result[1][0], accept_result[1][1])

                    self.connectionsLock.acquire()
                    (sock,(sourceIP, sourcePort)) = accept_result

                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                    connection = hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, eventHandler=self.parentEventHandler)

                    self.connections.append(connection)
                    self.connectionsLock.release()

                    self.fireEvent("RemoteConnected", {'connection': connection})

                    connection.startReceiver()

                    self.fireEvent("RemoteInitialized", {'connection': connection})

        except Exception, e:
            print "hsmsServer._listen_thread : exception", e
            traceback.print_exc()

        self.threadRunning = False

#single client connection
class hsmsClient(StreamFunctionCallbackHandler, EventProducer):
    """Client class for single active (outgoing) connection 

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`

    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        client = secsgem.hsmsConnections.hsmsClient("127.0.0.1", 5000, eventHandler=EventHandler(events={'RemoteInitialized': onConnect}))
        client.registerCallback(1, 1, S1F1Handler)

        connection = client.connect()

        time.sleep(3)

        connection.disconnect()

    """
    def __init__(self, address, port=5000, sessionID=0, eventHandler=None):
        StreamFunctionCallbackHandler.__init__(self)
        EventProducer.__init__(self, eventHandler)

        self.address = address
        self.port = port
        self.sessionID = sessionID

        self.aborted = False

        self.sock = None
        
    def connect(self):
        """Open connection to remote host

        :returns: the newly established connection, *None* if connection failed
        :rtype: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        logging.debug("hsmsClient.connect: connecting to %s:%d", self.address, self.port)

        try:
            self.sock.connect((self.address, self.port)) 
        except socket.error, v:
            logging.debug("hsmsClient.connect: connecting to %s:%d failed", self.address, self.port)
            return None

        connection = hsmsConnection(self.sock, self.callbacks, True, self.address, self.port, self.sessionID, eventHandler=self.parentEventHandler)

        self.fireEvent("RemoteConnected", {'connection': connection})

        connection.startReceiver()

        self.fireEvent("RemoteInitialized", {'connection': connection})

        return connection

    def cancel(self):
        """Cancel connection to remote host
        """
        self.aborted = True

        self.sock.close()

class hsmsConnection(StreamFunctionCallbackHandler, EventProducer):
    """Connection class used for active and passive connections. Contains the basic HSMS functionality.

    :param sock: Socket of the underlying connection
    :type sock: socket.socket
    :param callbacks: Callbacks used for this connections streams and functions
    :type callbacks: dict
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, sock, callbacks, active, address, port, sessionID = 0, eventHandler=None):
        StreamFunctionCallbackHandler.__init__(self)
        EventProducer.__init__(self, eventHandler)

        self.sock = sock
        self.callbacks = dict(callbacks)
        self.active = active
        self.remoteIP = address
        self.remotePort = port
        self.sessionID = sessionID

        self.receiveBuffer = ""

        self.systemCounter = 1

        self.threadRunning = False
        self.stopThread = False
        
        self.eventQueue = []
        self.packetQueue = []

        self.connected = True

        self.connectionState = hsmsConnectionState.NOT_SELECTED

        #disable blocking
        self.sock.setblocking(0)

    selectTimeout = 0.5
    """ Timeout for select calls """ 

    sendBlockSize = 1024*1024
    """ Block size for outbound data """ 

    def _serializeData(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {'active': self.active, 'remoteIP': self.remoteIP, 'remotePort': self.remotePort, 'sessionID': self.sessionID, 'systemCounter': self.systemCounter, 'connected': self.connected, 'connectionState': self.connectionState}

    def __str__(self):
        return ("Active" if self.active else "Passive") + " connection to " + self.remoteIP + ":" + str(self.remotePort) + " sessionID=" + str(self.sessionID) + ", connectionState=" + str(self.connectionState)

    def startReceiver(self):
        """Start the thread for receiving and handling incoming messages. Will also do the initial Select and Linktest requests

        .. warning:: Do not call this directly, will be called from HSMS client/server class.
        .. seealso:: :class:`secsgem.hsmsConnections.hsmsSingleServer`, :class:`secsgem.hsmsConnections.hsmsMultiServer`, :class:`secsgem.hsmsConnections.hsmsClient`
        """
        thread.start_new_thread(self._receiver_thread, ())

        while not self.threadRunning:
            pass
        
        if self.active:
            self.sendSelectReq()
            self.waitforSelectRsp()
            self.sendLinktestReq()
            self.waitforLinktestRsp()
        else:
            system = self.waitforSelectReq()
            self.sendSelectRsp(system)
            self.sendLinktestReq()
            self.waitforLinktestRsp()

    def disconnect(self, separate = False):
        """Close connection

        :param separate: use Separate instead of Deselect 
        :type separate: boolean
        """
        if separate:
            self.sendSeparateReq()
        else:
            self.sendDeselectReq()
            self.waitforDeselectRsp()

        self.stopThread = True
        
        while self.threadRunning:
            pass

    def sendPacket(self, packet):
        """Send the ASCII coded packet to the remote host

        :param packet: encoded data to be transmitted
        :type packet: string / byte array
        """
        logging.info("> %s", packet)

        data = packet.encode()

        blocks = [data[i:i+self.sendBlockSize] for i in range(0, len(data), self.sendBlockSize)]

        for block in blocks:
            retry = True

            #not sent yet, retry
            while retry:
                #wait until socket is writable
                while not select.select([], [self.sock], [], self.selectTimeout)[1]:
                    pass

                try:
                    #send packet
                    self.sock.send(block)

                    #retry will be cleared if send succeeded
                    retry = False
                except socket.error, e:
                    errorcode = e[0]
                    if not isErrorCodeEWouldBlock(errorcode):
                        # raise if not EWOULDBLOCK
                        raise e
                    #it is EWOULDBLOCK, so retry sending

    def waitforStreamFunction(self, stream, function):
        """Wait for an incoming stream and function and return the receive data

        :param stream: number of stream to wait for
        :type stream: integer
        :param function: number of function to wait for
        :type function: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        event = threading.Event()
        self.eventQueue.append(event)

        foundPacket = None
        
        while foundPacket == None:
            for packet in self.packetQueue:
                if (packet.header.stream == stream) and (packet.header.function == function):
                    self.packetQueue.remove(packet)
                    foundPacket = packet
                    break

            if foundPacket == None:
                if event.wait(1) == True:
                    event.clear()
                    
        self.eventQueue.remove(event)
        
        return packet

    def waitforSystem(self, system):
        """Wait for an message with supplied system

        :param system: number of system to wait for
        :type system: integer
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        event = threading.Event()
        self.eventQueue.append(event)

        foundPacket = None
        
        while foundPacket == None:
            for packet in self.packetQueue:
                if (packet.header.system == system):
                    self.packetQueue.remove(packet)
                    foundPacket = packet
                    break

            if foundPacket == None:
                if event.wait(1) == True:
                    event.clear()
                    
        self.eventQueue.remove(event)
        
        return packet

    def sendAndWaitForResponse(self, packet):
        """Send the packet and wait for the response

        :param packet: packet to be sent
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        outPacket = hsmsPacket(hsmsStreamFunctionHeader(self.getNextSystemCounter(), packet.stream, packet.function, True, self.sessionID), packet.encode())
        self.sendPacket(outPacket)
        
        return self.waitforSystem(outPacket.header.system)

    def sendResponse(self, packet, system):
        """Send response packet for system

        :param packet: packet to be sent
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        :param system: system to reply to
        :type system: integer
        """
        outPacket = hsmsPacket(hsmsStreamFunctionHeader(system, packet.stream, packet.function, False, self.sessionID), packet.encode())
        self.sendPacket(outPacket)

    def sendSelectReq(self):
        """Send a Select Request to the remote host"""
        packet = hsmsPacket(hsmsSelectReqHeader(self.getNextSystemCounter()))
        self.sendPacket(packet)

    def waitforSelectReq(self):
        """Wait for an incoming Select Request

        :returns: System of the incoming request required for response
        :rtype: integer
        """
        result = None

        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        
        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x01):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        result = packet.header.system
                        break
        
        self.eventQueue.remove(event)

        return result

    def sendSelectRsp(self, system = None):
        """Send a Select Response to the remote host

        :param system: System of the request to reply for
        :type system: integer
        """
        packet = hsmsPacket(hsmsSelectRspHeader(system))
        self.sendPacket(packet)

    def waitforSelectRsp(self):
        """Wait for an incoming Select Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        result = -1

        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x02):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        result = packet.header.function
                        break
        
        self.eventQueue.remove(event)

        self.connectionState = hsmsConnectionState.SELECTED

        return result

    def sendLinktestReq(self):
        """Send a Linktest Request to the remote host"""
        packet = hsmsPacket(hsmsLinktestReqHeader(self.getNextSystemCounter()))
        self.sendPacket(packet)

    def waitforLinktestReq(self):
        """Wait for an incoming Linktest Request

        :returns: System of the incoming request required for response
        :rtype: integer
        """
        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        
        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x05):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        break
        
        self.eventQueue.remove(event)

    def sendLinktestRsp(self, system):
        """Send a Linktest Response to the remote host

        :param system: System of the request to reply for
        :type system: integer
        """
        packet = hsmsPacket(hsmsLinktestReqHeader(system))
        self.sendPacket(packet)

    def waitforLinktestRsp(self):
        """Wait for an incoming Linktest Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        
        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x06):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        break
        
        self.eventQueue.remove(event)

    def sendDeselectReq(self):
        """Send a Deselect Request to the remote host"""
        packet = hsmsPacket(hsmsDeselectReqHeader(self.getNextSystemCounter()))
        self.sendPacket(packet)

    def waitforDeselectReq(self):
        """Wait for an incoming Deselect Request

        :returns: System of the incoming request required for response
        :rtype: integer
        """
        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        
        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x03):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        break

        self.eventQueue.remove(event)

    def sendDeselectRsp(self, system):
        """Send a Deselect Response to the remote host

        :param system: System of the request to reply for
        :type system: integer
        """
        packet = hsmsPacket(hsmsDeselectRspHeader(system))
        self.sendPacket(packet)

    def waitforDeselectRsp(self):
        """Wait for an incoming Deselect Response

        :returns: System of the incoming response for validation
        :rtype: integer
        """
        event = threading.Event()
        self.eventQueue.append(event)

        eventReceived = False
        result = -1
        
        while not eventReceived:
            if event.wait(1) == True:
                event.clear()
                for packet in self.packetQueue:
                    if (packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.sType == 0x04):
                        self.packetQueue.remove(packet)
                        eventReceived = True
                        result = packet.header.function
                        break
        
        self.eventQueue.remove(event)

        self.connectionState = hsmsConnectionState.NOT_SELECTED

        return result

    def sendSeparateReq(self):
        """Send a Separate Request to the remote host"""
        packet = hsmsPacket(hsmsSeparateReqHeader(self.getNextSystemCounter()))
        self.sendPacket(packet)

        self.connectionState = hsmsConnectionState.NOT_SELECTED

    def _process_receive_buffer(self):
        """Parse the receive buffer and dispatch callbacks.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection._receiver_thread` method.
        """
        if len(self.receiveBuffer) < 4:
            return False

        length = struct.unpack(">L", self.receiveBuffer[0:4])[0] + 4

        if len(self.receiveBuffer) < length:
            return False

        data = self.receiveBuffer[0:length]
        self.receiveBuffer = self.receiveBuffer[length:]

        response = hsmsPacket.decode(data)
        if response.header.sessionID == 0xffff:
            logging.info("< %s\n  %s", response, hsmsSTypes[response.header.sType])
        else:
            if response.data == None:
                logging.info("< %s", response)
            else:
                logging.info("< %s", response)

        callbackIndex = "s"+str(response.header.stream)+"f"+str(response.header.function)
        if callbackIndex in self.callbacks:
            for callback in self.callbacks[callbackIndex]:
                thread.start_new_thread(callback, (self, response))
        else:
            self.packetQueue.append(response)
            for event in self.eventQueue:
                event.set()

        if len(self.receiveBuffer) > 0:
            return True

        return False

    def _receiver_thread(self):
        """Thread for receiving incoming data and adding it to the receive buffer.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection.startReceiver` method.
        """
        self.threadRunning = True

        try:
            while not self.stopThread:
                selectResult = select.select([self.sock], [], [self.sock], self.selectTimeout)

                if selectResult[0]:
                    try:
                        recvData = self.sock.recv(1024) 

                        if len(recvData) == 0:
                            self.connected = False
                            self.stopThread = True
                            continue

                        self.receiveBuffer += recvData
                    except socket.error, e:
                        errorcode = e[0]
                        if not isErrorCodeEWouldBlock(errorcode):
                            raise e
    
                    while self._process_receive_buffer():
                        pass

        except Exception, e:
            print "hsmsClient.ReceiverThread : exception", e
            print traceback.format_exc()

        self.fireEvent("RemoteDisconnected", {'connection': self})

        self.sock.close()

        self.connected = False

        self.connectionState = hsmsConnectionState.NOT_CONNECTED

        self.threadRunning = False

    def getNextSystemCounter(self):
        """Returns the next System.

        :returns: System for the next command
        :rtype: integer
        """
        self.systemCounter += 1
        return self.systemCounter

    def defaultS0F0Handler(self, connection, packet):
        """Stream/Function callback to autoreply Linktest requests

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`
        """
        if packet.header.sessionID != 0xffff:
            logging.error("S00F00: invalid sessionID")
            return
        
        if packet.header.sType == 0x05:
            responsePacket = hsmsPacket(hsmsLinktestRspHeader(packet.header.system))
            self.sendPacket(responsePacket)
        else:
            logging.error("S00F00: unexpected sType (%s)", packet.header)

