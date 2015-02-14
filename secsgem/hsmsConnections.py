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
import struct

import thread
import threading
import traceback

import time

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

class hsmsConnectionState:
    """hsms connection state machine states"""
    NOT_CONNECTED, CONNECTED, NOT_SELECTED, SELECTED = range(4)

class _callbackHandler:
    """Base class for all connection classes. Provides functionality for registering and unregistering callbacks for streams and functions."""
    def __init__(self):
        self.callbacks = {}

    def registerCallback(self, stream, function, callback):
        """Register the function callback for stream and function. Multiple callbacks can be registered for one function.

        :param stream: stream to register callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to call when stream and functions is received
        :type callback: def callback(connection)
        """
        name = "s"+str(stream)+"f"+str(function)

        if not name in self.callbacks:
            self.callbacks[name] = []

        self.callbacks[name].append(callback)

    def unregisterCallback(self, stream, function, callback):
        """Unregister the function callback for stream and function. Multiple callbacks can be registered for one function, only the supplied callback will be removed.

        :param stream: stream to unregister callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to remove from callback list
        :type callback: def callback(connection)
        """
        name = "s"+str(stream)+"f"+str(function)

        if callback in self.callbacks[name]:
            self.callbacks[name].remove(callback)

class hsmsSingleServer(_callbackHandler):
    """Server class for single passive (incoming) connection 

    Creates a listening socket and waits for one incoming connection on this socket. After the connection is established the listening socket is closed.

    :param port: TCP port to listen on for incoming connections 
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param connectionCallback: method to call when the connection is established
    :type connectionCallback: def connectionCallback(connection)
    :param disconnectionCallback: method to call when the connection is terminated
    :type disconnectionCallback: def disconnectionCallback(connection)

    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        server = secsgem.hsmsConnections.hsmsSingleServer(5000, connectionCallback = onConnect)
        server.registerCallback(1, 1, S1F1Handler)

        connection = server.waitForConnection()

        time.sleep(3)

        connection.disconnect()

    """
    def __init__(self, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
        _callbackHandler.__init__(self)

        self.port = port
        self.connectionCallback = connectionCallback
        self.disconnectionCallback = disconnectionCallback
        self.sessionID = sessionID

    def waitForConnection(self):
        """Wait for incoming connection

        Opens listening socket and waits (blocking) for the connection. Terminates the listening socket and returns the new connection.

        :returns: the newly established connection
        :rtype: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1)

        while True:
            accept_result = sock.accept()
            if accept_result == None:
                continue

            (sock,(sourceIP, sourcePort)) = accept_result

            connection = hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, disconnectionCallback = self.disconnectionCallback)

            if not self.connectionCallback == None:
                self.connectionCallback(connection)

            connection.startReceiver()

            return connection

        sock.close()

#start server accepting all connections
class hsmsMultiServer(_callbackHandler):
    """Server class for multiple passive (incoming) connection. The server creates a listening socket and waits for incoming connections on this socket. When the connection is established the supplied connectionCallback will be called with the new connection class.

    :param port: TCP port to listen on
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param connectionCallback: method to call when the connection is established
    :type connectionCallback: def connectionCallback(connection)
    :param disconnectionCallback: method to call when the connection is terminated
    :type disconnectionCallback: def disconnectionCallback(connection)
    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        server = secsgem.hsmsConnections.hsmsMultiServer(5000, connectionCallback = onConnect)
        server.registerCallback(1, 1, S1F1Handler)

        server.start()

        time.sleep(3)

        server.stop()

    """
    def __init__(self, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
        _callbackHandler.__init__(self)

        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sessionID = sessionID
        self.port = port

        self.threadRunning = False
        self.stopThread = False

        self.connections = []
        self.connectionsLock = threading.Lock()

        self.connectionCallback = connectionCallback
        self.disconnectionCallback = disconnectionCallback

        self.listenThreadIdentifier = None

    def start(self):
        """Starts the server and returns. It will launch a listener running in background to wait for incoming connections."""
        self.listenSock.bind(('', self.port))
        self.listenSock.listen(1)

        self.listenThreadIdentifier = threading.Thread(target=self._listen_thread, args=())
        self.listenThreadIdentifier.start()

    def stop(self, terminateConnections = True):
        """Stops the server. The background job waiting for incoming connections will be terminated. Optionally all connections received will be closed.

        :param terminateConnections: terminate all connection made by this server
        :type terminateConnections: boolean
        """
        self.stopThread = True

        #this is evil madness
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("localhost", self.port))

        self.listenSock.close()

        if self.listenThreadIdentifier.isAlive:
            while self.threadRunning:
                pass

        self.connectionsLock.acquire()

        if terminateConnections:
            for connection in self.connections:
                connection.disconnect()

        self.connectionsLock.release()

    def _listen_thread(self):
        """Thread listening for incoming connections

        .. warning:: Do not call this directly, used internally.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                accept_result = self.listenSock.accept()
                if accept_result == None:
                    continue

                if self.stopThread:
                    continue

                self.connectionsLock.acquire()
                (sock,(sourceIP, sourcePort)) = accept_result

                connection = hsmsConnection(sock, self.callbacks, False, sourceIP, sourcePort, self.sessionID, disconnectionCallback = self.disconnectionCallback)

                self.connections.append(connection)
                self.connectionsLock.release()

                if not self.connectionCallback == None:
                    self.connectionCallback(connection)

                connection.startReceiver()

        except Exception, e:
            print "hsmsServer._listen_thread : exception", e
            traceback.print_exc()

        self.threadRunning = False

#single client connection
class hsmsClient(_callbackHandler):
    """Client class for single active (outgoing) connection 

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param connectionCallback: method to call when the connection is established
    :type connectionCallback: def connectionCallback(connection)
    :param disconnectionCallback: method to call when the connection is terminated
    :type disconnectionCallback: def disconnectionCallback(connection)

    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        client = secsgem.hsmsConnections.hsmsClient("127.0.0.1", 5000, connectionCallback = onConnect)
        client.registerCallback(1, 1, S1F1Handler)

        connection = client.connect()

        time.sleep(3)

        connection.disconnect()

    """
    def __init__(self, address, port = 5000, sessionID = 0, connectionCallback = None, disconnectionCallback = None):
        _callbackHandler.__init__(self)

        self.address = address
        self.port = port
        self.connectionCallback = connectionCallback
        self.disconnectionCallback = disconnectionCallback
        self.sessionID = sessionID
        
    def connect(self):
        """Open connection to remote host

        :returns: the newly established connection, *None* if connection failed
        :rtype: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logging.debug("hsmsClient.connect: connecting to %s:%d", self.address, self.port)

        try:
            sock.connect((self.address, self.port)) 
        except socket.error, v:
            logging.debug("hsmsClient.connect: connecting to %s:%d failed", self.address, self.port)
            return None

        connection = hsmsConnection(sock, self.callbacks, True, self.address, self.port, self.sessionID, disconnectionCallback = self.disconnectionCallback)

        if not self.connectionCallback == None:
            self.connectionCallback(connection)

        connection.startReceiver()

        return connection

class hsmsConnection(_callbackHandler):
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
    :param disconnectionCallback: method to call when the connection is terminated
    :type disconnectionCallback: def disconnectionCallback(connection)
    """
    def __init__(self, sock, callbacks, active, address, port, sessionID = 0, disconnectionCallback = None):
        _callbackHandler.__init__(self)

        self.sock = sock
        self.callbacks = dict(callbacks)
        self.active = active
        self.remoteIP = address
        self.remotePort = port
        self.sessionID = sessionID
        self.disconnectionCallback = disconnectionCallback

        self.systemCounter = 1

        self.threadRunning = False
        self.stopThread = False
        
        self.eventQueue = []
        self.packetQueue = []

        self.connected = True

        self.connectionState = hsmsConnectionState.NOT_SELECTED


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

        time.sleep(0.5)

        self.stopThread = True
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.connected = False

        self.connectionState = hsmsConnectionState.NOT_CONNECTED
        
        while self.threadRunning:
            pass

    def sendPacket(self, packet):
        """Send the ASCII coded packet to the remote host

        :param packet: encoded data to be transmitted
        :type packet: string / byte array
        """
        logging.info("> %s", packet)
        self.sock.send(packet.encode())
                
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

    def sendSelectReq(self):
        """Send a Select Request to the remote host"""
        packet = hsmsPacket(hsmsSelectReqHeader(self.getNextSystemCounter()))
        logging.info("> %s\n  %s", packet, hsmsSTypes[1])

        self.sock.send(packet.encode())

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

        logging.info("> %s\n  %s", packet, hsmsSTypes[2])

        self.sock.send(packet.encode())

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
        logging.info("> %s\n  %s", packet, hsmsSTypes[5])

        self.sock.send(packet.encode())

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
        logging.info("> %s\n  %s", packet, hsmsSTypes[6])

        self.sock.send(packet.encode())

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
        logging.info("> %s\n  %s", packet, hsmsSTypes[3])

        self.sock.send(packet.encode())

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
        logging.info("> %s\n  %s", packet, hsmsSTypes[4])

        self.sock.send(packet.encode())

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
        logging.info("> %s\n  %s", packet, hsmsSTypes[9])

        self.sock.send(packet.encode())

        self.connectionState = hsmsConnectionState.NOT_SELECTED

    def _receiver_thread(self):
        """Start the thread for receiving and handling incoming messages. Will also do the initial Select and Linktest requests.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection.startReceiver` method.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                data = self.sock.recv(4) 
                if len(data) == 0:
                    self.connected = False
                    self.stopThread = True
                    continue

                length = struct.unpack(">L", data)[0]

                while len(data) < length + 4:
                    data += self.sock.recv(length) 
                    if len(data) == 4:
                        self.connected = False
                        self.stopThread = True
                        continue
                    
                response = hsmsPacket.decode(data)
                if response.header.sessionID == 0xffff:
                    logging.info("< %s\n  %s", response, hsmsSTypes[response.header.sType])
                else:
                    if response.data == None:
                        logging.info("< %s", response)
                    else:
                        logging.info("< %s", response)
                
                data = ""

                unhandeled = True
                
                callbackIndex = "s"+str(response.header.stream)+"f"+str(response.header.function)
                if callbackIndex in self.callbacks:
                    unhandeled = False
                    for callback in self.callbacks[callbackIndex]:
                        thread.start_new_thread(callback, (self, response))
                else:
                    self.packetQueue.append(response)
                    for event in self.eventQueue:
                        event.set()
        except Exception, e:
            print "hsmsClient.ReceiverThread : exception", e
            print traceback.format_exc()

        if not self.disconnectionCallback == None:
            self.disconnectionCallback(self)

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
            logging.info("> %s\n  %s", responsePacket, hsmsSTypes[6])

            self.sock.send(responsePacket.encode())
        else:
            logging.error("S00F00: unexpected sType (%s)", packet.header)

