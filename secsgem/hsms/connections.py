#####################################################################
# connections.py
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

from __future__ import absolute_import

import logging
import socket
import select
import struct
import time
import threading
import errno

from ..common import is_windows

from .packets import HsmsPacket

# TODO: timeouts (T7, T8)

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
"""Names for hsms header SType"""

def is_errorcode_ewouldblock(errorcode):
    if errorcode == errno.EAGAIN or errorcode == errno.EWOULDBLOCK:
        return True

    return False


class HsmsConnection(object):  # pragma: no cover
    """Connection class used for active and passive hsms connections.

    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: inherited from :class:`secsgem.hsms.handler.HsmsHandler`
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

    def __init__(self, active, address, port, session_id=0, delegate=None):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # set parameters
        self.active = active
        self.remoteAddress = address
        self.remotePort = port
        self.sessionID = session_id
        self.delegate = delegate

        # connection socket
        self.sock = None

        # buffer for received data
        self.receiveBuffer = b""

        # receiving thread flags
        self.threadRunning = False
        self.stopThread = False

        # connected flag
        self.connected = False

        # flag set during disconnection
        self.disconnecting = False

    def _serialize_data(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {
            'active': self.active, 
            'remoteAddress': self.remoteAddress, 
            'remotePort': self.remotePort, 
            'sessionID': self.sessionID, 
            'connected': self.connected }

    def __str__(self):
        """Get the contents of this object as a string"""
        return "{} connection to {}:{} sessionID={}".format(("Active" if self.active else "Passive"), \
            self.remoteAddress, str(self.remotePort), str(self.sessionID))

    def _start_receiver(self):
        """Start the thread for receiving and handling incoming messages. Will also do the initial Select and Linktest requests

        .. warning:: Do not call this directly, will be called from HSMS client/server class.
        .. seealso:: :class:`secsgem.hsms.connections.HsmsActiveConnection`, 
            :class:`secsgem.hsms.connections.HsmsPassiveConnection`, 
            :class:`secsgem.hsms.connections.HsmsMultiPassiveConnection`
        """
        # mark connection as connected
        self.connected = True

        # start data receiving thread
        threading.Thread(target=self.__receiver_thread, args=(), \
            name="secsgem_hsmsConnection_receiver_{}:{}".format(self.remoteAddress, self.remotePort)).start()

        # wait until thread is running
        while not self.threadRunning:
            pass

        # send event
        if self.delegate and hasattr(self.delegate, 'on_connection_established') and callable(getattr(self.delegate, 'on_connection_established')):
            try:
                self.delegate.on_connection_established(self)
            except Exception:
                self.logger.exception('ignoring exception for on_connection_established handler')

    def _on_hsms_connection_close(self, data):
        pass

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

    def send_packet(self, packet):
        """Send the ASCII coded packet to the remote host

        :param packet: encoded data to be transmitted
        :type packet: string / byte array
        """
        # encode the packet
        data = packet.encode()

        # split data into blocks
        blocks = [data[i: i + self.sendBlockSize] for i in range(0, len(data), self.sendBlockSize)]

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
                except socket.error as e:
                    errorcode = e[0]
                    if not is_errorcode_ewouldblock(errorcode):
                        # raise if not EWOULDBLOCK
                        return False
                    # it is EWOULDBLOCK, so retry sending

        return True

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
        response = HsmsPacket.decode(data)

        # redirect packet to hsms handler
        if self.delegate and hasattr(self.delegate, 'on_connection_packet_received') and callable(getattr(self.delegate, 'on_connection_packet_received')):
            try:
                self.delegate.on_connection_packet_received(self, response)
            except Exception:
                self.logger.exception('ignoring exception for on_connection_packet_received handler')

        # return True if more data is available
        if len(self.receiveBuffer) > 0:
            return True

        return False

    def __receiver_thread_read_data(self):
        # check if shutdown requested
        while not self.stopThread:
            # check if data available
            select_result = select.select([self.sock], [], [self.sock], self.selectTimeout)

            # check if disconnection was started
            if self.disconnecting:
                time.sleep(0.2)
                continue

            if select_result[0]:
                try:
                    # get data from socket
                    recv_data = self.sock.recv(1024)

                    # check if socket was closed
                    if len(recv_data) == 0:
                        self.connected = False
                        self.stopThread = True
                        continue

                    # add received data to input buffer
                    self.receiveBuffer += recv_data
                except socket.error as e:
                    errorcode = e[0]
                    if not is_errorcode_ewouldblock(errorcode):
                        raise e

                # handle data in input buffer
                while self._process_receive_buffer():
                    pass

    def __receiver_thread(self):
        """Thread for receiving incoming data and adding it to the receive buffer.

        .. warning:: Do not call this directly, will be called from :func:`secsgem.hsmsConnections.hsmsConnection._startReceiver` method.
        """
        self.threadRunning = True

        try:
            self.__receiver_thread_read_data()
        except Exception:
            self.logger.exception('exception')

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, 'on_connection_before_closed') and callable(getattr(self.delegate, 'on_connection_before_closed')):
            try:
                self.delegate.on_connection_before_closed(self)
            except Exception:
                self.logger.exception('ignoring exception for on_connection_before_closed handler')

        # close the socket
        self.sock.close()

        # notify listeners of disconnection
        if self.delegate and hasattr(self.delegate, 'on_connection_closed') and callable(getattr(self.delegate, 'on_connection_closed')):
            try:
                self.delegate.on_connection_closed(self)
            except Exception:
                self.logger.exception('ignoring exception for on_connection_closed handler')

        # reset all flags
        self.connected = False
        self.threadRunning = False
        self.stopThread = False

        # clear receive buffer
        self.receiveBuffer = b""

        # notify inherited classes of disconnection
        self._on_hsms_connection_close({'connection': self})


class HsmsPassiveConnection(HsmsConnection):  # pragma: no cover
    """Server class for single passive (incoming) connection

    Creates a listening socket and waits for one incoming connection on this socket. After the connection is established the listening socket is closed.

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        # TODO: create example

    """

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)

        # initially not enabled
        self.enabled = False

        # reconnect thread required for passive connection
        self.serverThread = None
        self.stopServerThread = False
        self.serverSock = None

    def _on_hsms_connection_close(self, data):
        """Signal from super that the connection was closed

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__start_server_thread()

    def enable(self):
        """Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self.enabled:
            # mark connection as enabled
            self.enabled = True

            # start the connection thread
            self.__start_server_thread()

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

                if self.serverSock:
                    self.serverSock.close()

                # wait for connection thread to stop
                while self.stopServerThread:
                    time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __start_server_thread(self):
        self.serverThread = threading.Thread(target=self.__server_thread, name="secsgem_HsmsPassiveConnection_serverThread_{}".format(self.remoteAddress))
        self.serverThread.start()

    def __server_thread(self):
        """Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not is_windows():
            self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverSock.bind(('', self.remotePort))
        self.serverSock.listen(1)

        while not self.stopServerThread:
            try:
                select_result = select.select([self.serverSock], [], [], self.selectTimeout)
            except Exception:
                continue

            if not select_result[0]:
                # select timed out
                continue

            accept_result = self.serverSock.accept()
            if accept_result is None:
                continue

            (self.sock, (_, _)) = accept_result

            # setup socket
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # make socket nonblocking
            self.sock.setblocking(0)

            # start the receiver thread
            self._start_receiver()

            self.serverSock.close()

            return

        self.stopServerThread = False


class HsmsMultiPassiveConnection(HsmsConnection):  # pragma: no cover
    """Connection class for single connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`

    Handles connections incoming connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        # TODO: create example

    """

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)

        # initially not enabled
        self.enabled = False

    def on_connected(self, sock, address):
        """Connected callback for :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`

        :param sock: Socket for new connection
        :type sock: :class:`Socket`
        :param address: IP address of remote host
        :type address: string
        """
        del address  # unused parameter

        # setup socket
        self.sock = sock
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # make socket nonblocking
        self.sock.setblocking(0)

        # start the receiver thread
        self._start_receiver()

    def enable(self):
        """Enable the connection.

        Starts the connection process to the passive remote.
        """
        self.enabled = True

    def disable(self):
        """Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        self.enabled = False
        if self.connected:
            self.disconnect()


class HsmsMultiPassiveServer(object):  # pragma: no cover
    """Server class for multiple passive (incoming) connection. The server creates a listening socket and waits for incoming connections on this socket.

    :param port: TCP port to listen on
    :type port: integer

    **Example**::

        # TODO: create example

    """

    selectTimeout = 0.5
    """ Timeout for select calls """

    def __init__(self, port=5000):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.listenSock = None

        self.port = port

        self.threadRunning = False
        self.stopThread = False

        self.connections = {}

        self.listenThread = None

    def create_connection(self, address, port=5000, session_id=0, delegate=None):
        """Create and remember connection for the server

        :param address: IP address of target host
        :type address: string
        :param port: TCP port of target host
        :type port: integer
        :param session_id: session / device ID to use for connection
        :type session_id: integer
        :param delegate: target for messages
        :type delegate: object
        """
        connection = HsmsMultiPassiveConnection(address, port, session_id, delegate)
        connection.handler = self

        self.connections[address] = connection

        return connection

    def start(self):
        """Starts the server and returns. It will launch a listener running in background to wait for incoming connections."""
        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not is_windows():
            self.listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.listenSock.bind(('', self.port))
        self.listenSock.listen(1)
        self.listenSock.setblocking(0)

        self.listenThread = threading.Thread(target=self._listen_thread, args=(), name="secsgem_hsmsMultiPassiveServer_listenThread_{}".format(self.port))
        self.listenThread.start()

        self.logger.debug("listening")

    def stop(self, terminate_connections=True):
        """Stops the server. The background job waiting for incoming connections will be terminated. Optionally all connections received will be closed.

        :param terminate_connections: terminate all connection made by this server
        :type terminate_connections: boolean
        """
        self.stopThread = True

        if self.listenThread.isAlive:
            while self.threadRunning:
                pass

        self.listenSock.close()

        self.stopThread = False

        if terminate_connections:
            for address in self.connections:
                connection = self.connections[address]
                connection.disconnect()

        self.logger.debug("server stopped")

    def _initialize_connection_thread(self, accept_result):
        """Setup connection

        .. warning:: Do not call this directly, used internally.
        """
        (sock, (source_ip, _)) = accept_result

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        new_connection = None

        # check if connection available with source ip
        if source_ip not in self.connections:
            named_connection_found = False

            # check all connections if connection with hostname can be resolved
            for connectionID in self.connections:
                connection = self.connections[connectionID]
                try:
                    if source_ip == socket.gethostbyname(connection.remoteAddress):
                        new_connection = connection
                        named_connection_found = True
                        break
                except socket.gaierror:
                    pass

            if not named_connection_found:
                sock.close()
                return
        else:
            new_connection = self.connections[source_ip]

        if not new_connection.enabled:
            sock.close()
            return

        new_connection.on_connected(sock, source_ip)

    def _listen_thread(self):
        """Thread listening for incoming connections

        .. warning:: Do not call this directly, used internally.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                # check for data in the input buffer
                select_result = select.select([self.listenSock], [], [self.listenSock], self.selectTimeout)

                if select_result[0]:
                    accept_result = None

                    try:
                        accept_result = self.listenSock.accept()
                    except socket.error as e:
                        errorcode = e[0]
                        if not is_errorcode_ewouldblock(errorcode):
                            raise e

                    if accept_result is None:
                        continue

                    if self.stopThread:
                        continue

                    self.logger.debug("connection from %s:%d", accept_result[1][0], accept_result[1][1])

                    threading.Thread(target=self._initialize_connection_thread, args=(accept_result,), \
                        name="secsgem_hsmsMultiPassiveServer_InitializeConnectionThread_{}:{}".format(accept_result[1][0], accept_result[1][1])).start()

        except Exception:
            self.logger.exception('exception')

        self.threadRunning = False


class HsmsActiveConnection(HsmsConnection):  # pragma: no cover
    """Client class for single active (outgoing) connection

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        # TODO: create example

    """

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)

        # initially not enabled
        self.enabled = False

        # reconnect thread required for active connection
        self.connectionThread = None
        self.stopConnectionThread = False

        # flag if this is the first connection since enable
        self.firstConnection = True

    def _on_hsms_connection_close(self, data):
        """Signal from super that the connection was closed

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__start_connect_thread()

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
            self.__start_connect_thread()

    def disable(self):
        """Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        # only stop if enabled
        if self.enabled:
            # mark connection as disabled
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
        for _ in range(int(timeout) * 5):
            time.sleep(0.2)

            # check if connection was disabled
            if self.stopConnectionThread:
                self.stopConnectionThread = False
                return False

        return True

    def __start_connect_thread(self):
        self.connectionThread = threading.Thread(target=self.__connect_thread, name="secsgem_HsmsActiveConnection_connectThread_{}".format(self.remoteAddress))
        self.connectionThread.start()

    def __connect_thread(self):
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

        self.logger.debug("connecting to %s:%d", self.remoteAddress, self.remotePort)

        # try to connect socket
        try:
            self.sock.connect((self.remoteAddress, self.remotePort))
        except socket.error:
            self.logger.debug("connecting to %s:%d failed", self.remoteAddress, self.remotePort)
            return False

        # make socket nonblocking
        self.sock.setblocking(0)

        # start the receiver thread
        self._start_receiver()

        return True
