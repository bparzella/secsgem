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


class HsmsMultiPassiveServer:  # pylint: disable=too-many-instance-attributes
    """
    Server class for multiple passive (incoming) connection.

    The server creates a listening socket and waits for incoming connections on this socket.
    """

    select_timeout = 0.5
    """ Timeout for select calls ."""

    def __init__(self, port=5000, bind_ip=''):
        """
        Initialize a passive hsms server.

        :param port: TCP port to listen on
        :type port: integer

        Example:

            # TODO: create example

        """
        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._listen_sock = None

        self._port = port
        self._bind_ip = bind_ip

        self._thread_running = False
        self._stop_thread = False

        self._connections = {}

        self._listen_thread = None

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

        self._connections[address] = connection

        return connection

    def start(self):
        """
        Start the server and return.

        It will launch a listener running in background to wait for incoming connections.
        """
        self._listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not secsgem.common.is_windows():
            self._listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._listen_sock.bind((self._bind_ip, self._port))
        self._listen_sock.listen(1)
        self._listen_sock.setblocking(0)

        self._listen_thread = threading.Thread(
            target=self._listen_thread_func, args=(),
            name=f"secsgem_hsmsMultiPassiveServer_listenThread_{self._port}")
        self._listen_thread.start()

        self._logger.debug("listening")

    def stop(self, terminate_connections=True):
        """
        Stop the server. The background job waiting for incoming connections will be terminated.

        Optionally all connections received will be closed.

        :param terminate_connections: terminate all connection made by this server
        :type terminate_connections: boolean
        """
        self._stop_thread = True

        if self._listen_thread.is_alive():
            while self._thread_running:
                pass

        self._listen_sock.close()

        self._stop_thread = False

        if terminate_connections:
            for connection in self._connections.values():
                connection.disconnect()

        self._logger.debug("server stopped")

    def _initialize_connection_thread(self, accept_result):
        """
        Set connection up.

        .. warning:: Do not call this directly, used internally.
        """
        (sock, (source_ip, _)) = accept_result

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        new_connection = None

        # check if connection available with source ip
        if source_ip not in self._connections:
            named_connection_found = False

            # check all connections if connection with hostname can be resolved
            for connection in self._connections.values():
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
            new_connection = self._connections[source_ip]

        if not new_connection.enabled:
            sock.close()
            return

        new_connection.connected(sock, source_ip)

    def _listen_thread_func(self):
        """
        Thread listening for incoming connections.

        .. warning:: Do not call this directly, used internally.
        """
        self._thread_running = True
        try:
            while not self._stop_thread:
                # check for data in the input buffer
                select_result = select.select([self._listen_sock], [], [self._listen_sock], self.select_timeout)

                if select_result[0]:
                    accept_result = None

                    try:
                        accept_result = self._listen_sock.accept()
                    except OSError as exc:
                        if not secsgem.common.is_errorcode_ewouldblock(exc.errno):
                            raise exc

                    if accept_result is None:
                        continue

                    if self._stop_thread:
                        continue

                    self._logger.debug("connection from %s:%d", accept_result[1][0], accept_result[1][1])

                    threading.Thread(
                        target=self._initialize_connection_thread, args=(accept_result,),
                        name=f"secsgem_hsmsMultiPassiveServer_InitializeConnectionThread_"
                             f"{accept_result[1][0]}:{accept_result[1][1]}"
                    ).start()

        except Exception:  # pylint: disable=broad-except
            self._logger.exception('exception')

        self._thread_running = False
