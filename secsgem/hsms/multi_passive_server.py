#####################################################################
# multi_passive_server.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
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
"""Hsms multi passive server."""

import logging
import select
import socket
import threading

import secsgem.common

from .multi_passive_connection import HsmsMultiPassiveConnection


class HsmsMultiPassiveServer:  # pragma: no cover
    """
    Server class for multiple passive (incoming) connection.

    The server creates a listening socket and waits for incoming connections on this socket.
    """

    select_timeout = 0.5
    """ Timeout for select calls ."""

    def __init__(self, port=5000):
        """
        Initialize a passive hsms server.

        :param port: TCP port to listen on
        :type port: integer

        **Example**::

            # TODO: create example

        """
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.listenSock = None

        self.port = port

        self.threadRunning = False
        self.stopThread = False

        self.connections = {}

        self.listenThread = None

    def create_connection(self, address, port=5000, session_id=0, delegate=None):
        """
        Create and remember connection for the server.

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
        """
        Start the server and return.

        It will launch a listener running in background to wait for incoming connections.
        """
        self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not secsgem.common.is_windows():
            self.listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.listenSock.bind(('', self.port))
        self.listenSock.listen(1)
        self.listenSock.setblocking(0)

        self.listenThread = threading.Thread(target=self._listen_thread, args=(),
                                             name="secsgem_hsmsMultiPassiveServer_listenThread_{}".format(self.port))
        self.listenThread.start()

        self.logger.debug("listening")

    def stop(self, terminate_connections=True):
        """
        Stop the server. The background job waiting for incoming connections will be terminated.

        Optionally all connections received will be closed.

        :param terminate_connections: terminate all connection made by this server
        :type terminate_connections: boolean
        """
        self.stopThread = True

        if self.listenThread.is_alive():
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
        """
        Set connection up.

        .. warning:: Do not call this directly, used internally.
        """
        (sock, (source_ip, _)) = accept_result

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        new_connection = None

        # check if connection available with source ip
        if source_ip not in self.connections:
            named_connection_found = False

            # check all connections if connection with hostname can be resolved
            for connection_id in self.connections:
                connection = self.connections[connection_id]
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
        """
        Thread listening for incoming connections.

        .. warning:: Do not call this directly, used internally.
        """
        self.threadRunning = True
        try:
            while not self.stopThread:
                # check for data in the input buffer
                select_result = select.select([self.listenSock], [], [self.listenSock], self.select_timeout)

                if select_result[0]:
                    accept_result = None

                    try:
                        accept_result = self.listenSock.accept()
                    except OSError as exc:
                        if not secsgem.common.is_errorcode_ewouldblock(exc.errno):
                            raise exc

                    if accept_result is None:
                        continue

                    if self.stopThread:
                        continue

                    self.logger.debug("connection from %s:%d", accept_result[1][0], accept_result[1][1])

                    threading.Thread(target=self._initialize_connection_thread, args=(accept_result,),
                                     name="secsgem_hsmsMultiPassiveServer_InitializeConnectionThread_{}:{}"
                                     .format(accept_result[1][0], accept_result[1][1])).start()

        except Exception:  # pylint: disable=broad-except
            self.logger.exception('exception')

        self.threadRunning = False
