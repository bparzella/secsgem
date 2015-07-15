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
import time

import threading
import traceback

import errno

from hsmsPackets import hsmsPacket

from common import isWindows

# TODO: timeouts (T7, T8)

"""Names for hsms header SType"""
hsmsSTypes = {
    1: "Select.req",
    2: "Select.rsp",
    3: "Deselect.req",
    4: "Deselect.rsp",
    5: "Linktest.req",
    6: "Linktest.rsp",
    7: "Reject.req",
    9: "Separate.req"
}


def isErrorCodeEWouldBlock(errorcode):
    if errorcode == errno.EAGAIN or errorcode == errno.EWOULDBLOCK:
        return True

    return False


class hsmsConnection(object):
    """Connection class used for active and passive hsms connections.

    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param delegate: target for messages
    :type delegate: object
    """

    selectTimeout = 0.5
    """ Timeout for select calls """

    sendBlockSize = 1024 * 1024
    """ Block size for outbound data """

    T3 = 45.0
    """ Reply Timeout """

    T5 = 10.0
    """ Connect Separation Time """

    T6 = 5.0
    """ Control Transaction Timeout """

    def __init__(self, active, address, port, sessionID=0, delegate=None):
        # set parameters
        self.active = active
        self.remoteAddress = address
        self.remotePort = port
        self.sessionID = sessionID
        self.delegate = delegate

        # connection socket
        self.sock = None

        # buffer for received data
        self.receiveBuffer = ""

        # system id counter
        self.systemCounter = 1

        # receiving thread flags
        self.threadRunning = False
        self.stopThread = False

        # connected flag
        self.connected = False

        # flag set during disconnection
        self.disconnecting = False

    def _serializeData(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {'active': self.active, 'remoteAddress': self.remoteAddress, 'remotePort': self.remotePort, 'sessionID': self.sessionID, 'systemCounter': self.systemCounter, 'connected': self.connected}

    def __str__(self):
        return ("Active" if self.active else "Passive") + " connection to " + self.remoteAddress + ":" + str(self.remotePort) + " sessionID=" + str(self.sessionID)

    def _startReceiver(self):
        """Start the thread for receiving and handling incoming messages. Will also do the initial Select and Linktest requests

        .. warning:: Do not call this directly, will be called from HSMS client/server class.
        .. seealso:: :class:`secsgem.hsmsConnections.hsmsActiveConnection`, :class:`secsgem.hsmsConnections.hsmsPassiveConnection`, :class:`secsgem.hsmsConnections.hsmsMultiPassiveConnection`
        """
        # mark connection as connected
        self.connected = True

        if self.delegate and hasattr(self.delegate, '_onConnectionEstablished') and callable(getattr(self.delegate, '_onConnectionEstablished')):
            self.delegate._onConnectionEstablished()

        # start data receiving thread
        threading.Thread(target=self.__receiver_thread, args=(), name="secsgem_hsmsConnection_receiver_{}:{}".format(self.remoteAddress, self.remotePort)).start()

        # wait until thread is running
        while not self.threadRunning:
            pass

        # send event

    def disconnect(self):
        """Close connection"""
        # return if thread isn't running
        if not self.threadRunning:
            return

        # set disconnecting flag to avoid another select
        self.disconnecting = True

        # set flag to stop the thread
        self.stopThread = True

        # wait until thread stopped
        while self.threadRunning:
            pass

        # clear disconnecting flag, no selects coming any more
        self.disconnecting = False

    def sendPacket(self, packet):
        """Send the ASCII coded packet to the remote host

        :param packet: encoded data to be transmitted
        :type packet: string / byte array
        """
        logging.info("> %s", packet)

        # encode the packet
        data = packet.encode()

        # split data into blocks
        blocks = [data[i:i+self.sendBlockSize] for i in range(0, len(data), self.sendBlockSize)]

        for block in blocks:
            retry = True

            # not sent yet, retry
            while retry:
                # wait until socket is writable
                while not select.select([], [self.sock], [], self.selectTimeout)[1]:
                    pass

                try:
                    # send packet
                    self.sock.send(block)

                    # retry will be cleared if send succeeded
                    retry = False
                except socket.error, e:
                    errorcode = e[0]
                    if not isErrorCodeEWouldBlock(errorcode):
                        # raise if not EWOULDBLOCK
                        raise e
                    # it is EWOULDBLOCK, so retry sending

    def _process_receive_buffer(self):
        """Parse the receive buffer and dispatch callbacks.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection.__receiver_thread` method.
        """
        # check if enough data in input buffer
        if len(self.receiveBuffer) < 4:
            return False

        # unpack length from input buffer
        length = struct.unpack(">L", self.receiveBuffer[0:4])[0] + 4

        # check if enough data in input buffer
        if len(self.receiveBuffer) < length:
            return False

        # extract and remove packet from input buffer
        data = self.receiveBuffer[0:length]
        self.receiveBuffer = self.receiveBuffer[length:]

        # decode received packet
        response = hsmsPacket.decode(data)

        # redirect packet to hsms handler
        if self.delegate and hasattr(self.delegate, '_onConnectionPacketReceived') and callable(getattr(self.delegate, '_onConnectionPacketReceived')):
            self.delegate._onConnectionPacketReceived(response)

        # return True if more data is available
        if len(self.receiveBuffer) > 0:
            return True

        return False

    def __receiver_thread(self):
        """Thread for receiving incoming data and adding it to the receive buffer.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection._startReceiver` method.
        """
        self.threadRunning = True

        try:
            # check if shutdown requested
            while not self.stopThread:
                # check if data available
                selectResult = select.select([self.sock], [], [self.sock], self.selectTimeout)

                # check if disconnection was started
                if self.disconnecting:
                    time.sleep(0.2)
                    continue

                if selectResult[0]:
                    try:
                        # get data from socket
                        recvData = self.sock.recv(1024)

                        # check if socket was closed
                        if len(recvData) == 0:
                            self.connected = False
                            self.stopThread = True
                            continue

                        # add received data to input buffer
                        self.receiveBuffer += recvData
                    except socket.error, e:
                        errorcode = e[0]
                        if not isErrorCodeEWouldBlock(errorcode):
                            raise e

                    # handle data in input buffer
                    while self._process_receive_buffer():
                        pass

        except Exception, e:
            result = 'hsmsClient.ReceiverThread : exception {0}\n'.format(e)
            result += ''.join(traceback.format_stack())
            logging.error(result)

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, '_onBeforeConnectionClosed') and callable(getattr(self.delegate, '_onBeforeConnectionClosed')):
            self.delegate._onBeforeConnectionClosed()

        # close the socket
        self.sock.close()

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, '_onConnectionClosed') and callable(getattr(self.delegate, '_onConnectionClosed')):
            self.delegate._onConnectionClosed()

        # reset all flags
        self.connected = False
        self.threadRunning = False
        self.stopThread = False

        # clear receive buffer
        self.receiveBuffer = ""

        # notify inherited classes of disconnection
        if hasattr(self.__class__, '_onHsmsConnectionClose') and callable(getattr(self.__class__, '_onHsmsConnectionClose')):
            self._onHsmsConnectionClose({'connection': self})

    def getNextSystemCounter(self):
        """Returns the next System.

        :returns: System for the next command
        :rtype: integer
        """
        self.systemCounter += 1
        return self.systemCounter


class hsmsPassiveConnection(hsmsConnection):
    """Server class for single passive (incoming) connection

    Creates a listening socket and waits for one incoming connection on this socket. After the connection is established the listening socket is closed.

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        def S1F1Handler(connection, packet):
            print "S1F1 received"

        def onConnect(connection):
            print "Connected"

        server = secsgem.hsmsConnections.hsmsPassiveConnection(5000, eventHandler=EventHandler(events={'RemoteConnected': onConnect}))
        server.registerCallback(1, 1, S1F1Handler)

        connection = server.waitForConnection()

        time.sleep(3)

        connection.disconnect()

    """
    def __init__(self, address, port=5000, sessionID=0, delegate=None):
        # initialize super class
        hsmsConnection.__init__(self, True, address, port, sessionID, delegate)

        # initially not enabled
        self.enabled = False

        # reconnect thread required for passive connection
        self.serverThread = None
        self.stopServerThread = False

    def _onHsmsConnectionClose(self, data):
        """Signal from super that the connection was closed

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__startServerThread()

    def enable(self):
        """Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self.enabled:
            # mark connection as enabled
            self.enabled = True

            # start the connection thread
            self.__startServerThread()

    def disable(self):
        """Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        # only stop if enabled
        if self.enabled:
            # mark connection as disabled
            self.enabled = False

            # stop connection thread if it is running
            if self.serverThread and self.serverThread.isAlive():
                self.stopServerThread = True

            # wait for connection thread to stop
            while self.stopServerThread:
                time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __startServerThread(self):
        self.serverThread = threading.Thread(target=self.__serverThread, name="secsgem_hsmsPassiveConnection_serverThread_{}".format(self.remoteAddress))
        self.serverThread.start()

    def __serverThread(self):
        """Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not isWindows():
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('', self.remotePort))
        sock.listen(1)

        while True:
            accept_result = sock.accept()
            if accept_result is None:
                continue

            (self.sock, (sourceIP, sourcePort)) = accept_result

            # setup socket
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # make socket nonblocking
            self.sock.setblocking(0)

            # start the receiver thread
            self._startReceiver()

            sock.close()

            return

class hsmsMultiPassiveConnection(hsmsConnection):
    """Connection class for single connection from hsmsMultiPassiveServer

    Handles connections incoming connection from hsmsMultiPassiveServer

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        # TODO: create example

    """
    def __init__(self, address, port=5000, sessionID=0, delegate=None):
        # initialize super class
        hsmsConnection.__init__(self, True, address, port, sessionID, delegate)

        # initially not enabled
        self.enabled = False

    def _onConnected(self, sock, address):
        # setup socket
        self.sock = sock
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # make socket nonblocking
        self.sock.setblocking(0)

        # start the receiver thread
        self._startReceiver()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        if self.connected:
            self.disconnect()


class hsmsMultiPassiveServer(object):
    """Server class for multiple passive (incoming) connection. The server creates a listening socket and waits for incoming connections on this socket.

    :param port: TCP port to listen on
    :type port: integer

    **Example**::

        # TODO: create example

    """

    selectTimeout = 0.5
    """ Timeout for select calls """

    def __init__(self, port=5000):
        self.listenSock = None

        self.port = port

        self.threadRunning = False
        self.stopThread = False

        self.connections = {}

        self.listenThread = None

    def createConnection(self, address, port=5000, sessionID=0, delegate=None):
        """ Create and remember connection for the server

        :param address: IP address of target host
        :type address: string
        :param port: TCP port of target host
        :type port: integer
        :param sessionID: session / device ID to use for connection
        :type sessionID: integer
        :param delegate: target for messages
        :type delegate: object
        """
        connection = hsmsMultiPassiveConnection(address, port, sessionID, delegate)
        connection.handler = self

        self.connections[address] = connection

        return connection

    def start(self):
        """Starts the server and returns. It will launch a listener running in background to wait for incoming connections."""
        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not isWindows():
            self.listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.listenSock.bind(('', self.port))
        self.listenSock.listen(1)
        self.listenSock.setblocking(0)

        self.listenThread = threading.Thread(target=self._listen_thread, args=(), name="secsgem_hsmsMultiPassiveServer_listenThread_{}".format(self.port))
        self.listenThread.start()

        logging.debug("hsmsMultiPassiveServer.start: listening")

    def stop(self, terminateConnections=True):
        """Stops the server. The background job waiting for incoming connections will be terminated. Optionally all connections received will be closed.

        :param terminateConnections: terminate all connection made by this server
        :type terminateConnections: boolean
        """
        self.stopThread = True

        if self.listenThread.isAlive:
            while self.threadRunning:
                pass

        self.listenSock.close()

        self.stopThread = False

        if terminateConnections:
            for address in self.connections:
                connection = self.connections[address]
                connection.disconnect()

        logging.debug("hsmsMultiPassiveServer.stop: server stopped")

    def _initialize_connection_thread(self, accept_result):
        """Setup connection

        .. warning:: Do not call this directly, used internally.
        """
        (sock, (sourceIP, sourcePort)) = accept_result

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        if sourceIP not in self.connections:
            sock.close()
            return

        connection = self.connections[sourceIP]

        if not connection.enabled:
            sock.close()
            return

        connection._onConnected(sock, sourceIP)

    def _listen_thread(self):
        """Thread listening for incoming connections

        .. warning:: Do not call this directly, used internally.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                # check for data in the input buffer
                selectResult = select.select([self.listenSock], [], [self.listenSock], self.selectTimeout)

                if selectResult[0]:
                    accept_result = None

                    try:
                        accept_result = self.listenSock.accept()
                    except socket.error, e:
                        errorcode = e[0]
                        if not isErrorCodeEWouldBlock(errorcode):
                            raise e

                    if accept_result is None:
                        continue

                    if self.stopThread:
                        continue

                    logging.debug("hsmsMultiPassiveServer._listen_thread: connection from %s:%d", accept_result[1][0], accept_result[1][1])

                    threading.Thread(target=self._initialize_connection_thread, args=(accept_result,), name="secsgem_hsmsMultiPassiveServer_InitializeConnectionThread_{}:{}".format(accept_result[1][0], accept_result[1][1])).start()

        except Exception, e:
            result = 'hsmsServer._listen_thread : exception {0}\n'.format(e)
            result += ''.join(traceback.format_stack())
            logging.error(result)

        self.threadRunning = False


class hsmsActiveConnection(hsmsConnection):
    """Client class for single active (outgoing) connection

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        import secsgem

        def S0F0Handler(connection, packet):
            print "S0F0 received:", packet

        def onConnect(event, data):
            print "Connected"
            client = data["connection"]
            packet = secsgem.hsmsPacket(secsgem.hsmsSelectReqHeader(client.getNextSystemCounter()))
            client.sendPacket(packet)

        client = secsgem.hsmsActiveConnection("10.211.55.33", 5000, 0, eventHandler=secsgem.EventHandler(events={'HsmsConnectionEstablished': onConnect}))
        client.registerCallback(0, 0, S0F0Handler)

    """
    def __init__(self, address, port=5000, sessionID=0, delegate=None):
        # initialize super class
        hsmsConnection.__init__(self, True, address, port, sessionID, delegate)

        # initially not enabled
        self.enabled = False

        # reconnect thread required for active connection
        self.connectionThread = None
        self.stopConnectionThread = False

        # flag if this is the first connection since enable
        self.firstConnection = True

    def _onHsmsConnectionClose(self, data):
        """Signal from super that the connection was closed

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__startConnectThread()

    def enable(self):
        """Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self.enabled:
            # reset first connection to eliminate reconnection timeout
            self.firstConnection = True

            # mark connection as enabled
            self.enabled = True

            # start the connection thread
            self.__startConnectThread()

    def disable(self):
        """Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        # only stop if enabled
        if self.enabled:
            #mark connection as disabled
            self.enabled = False

            # stop connection thread if it is running
            if self.connectionThread and self.connectionThread.isAlive():
                self.stopConnectionThread = True

            # wait for connection thread to stop
            while self.stopConnectionThread:
                time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __idle(self, timeout):
        """Wait until timeout elapsed or connection thread is stopped

        :param timeout: number of seconds to wait
        :type timeout: float
        :returns: False if thread was stopped
        :rtype: boolean
        """
        for i in range(int(timeout) * 5):
            time.sleep(0.2)

            # check if connection was disabled
            if self.stopConnectionThread:
                self.stopConnectionThread = False
                return False

        return True

    def __startConnectThread(self):
        self.connectionThread = threading.Thread(target=self.__connectThread, name="secsgem_hsmsActiveConnection_connectThread_{}".format(self.remoteAddress))
        self.connectionThread.start()

    def __connectThread(self):
        """Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        # wait for timeout if this is not the first connection
        if not self.firstConnection:
            if not self.__idle(self.T5):
                return

        self.firstConnection = False

        # try to connect to remote
        while not self.__connect():
            if not self.__idle(self.T5):
                return

    def __connect(self):
        """Open connection to remote host

        :returns: True if connection was established, False if connection failed
        :rtype: boolean
        """
        # create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # setup socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        logging.debug("hsmsClient.connect: connecting to %s:%d", self.remoteAddress, self.remotePort)

        # try to connect socket
        try:
            self.sock.connect((self.remoteAddress, self.remotePort))
        except socket.error:
            logging.debug("hsmsClient.connect: connecting to %s:%d failed", self.remoteAddress, self.remotePort)
            return False

        # make socket nonblocking
        self.sock.setblocking(0)

        # start the receiver thread
        self._startReceiver()

        return True
