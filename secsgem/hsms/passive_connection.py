#####################################################################
# passive_connection.py
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
"""Hsms passive connection."""

import select
import socket
import threading
import time

import secsgem.common

from .connection import HsmsConnection


class HsmsPassiveConnection(HsmsConnection):  # pragma: no cover
    """
    Server class for single passive (incoming) connection.

    Creates a listening socket and waits for one incoming connection on this socket.
    After the connection is established the listening socket is closed.
    """

    def __init__(self, address, port=5000, session_id=0, delegate=None, bind_ip=''):
        """
        Initialize a passive hsms connection.

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
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)
        self._bind_ip = bind_ip

        # initially not enabled
        self._enabled = False

        # reconnect thread required for passive connection
        self._server_thread = None
        self._stop_server_thread = False
        self._server_sock = None

    def _on_hsms_connection_close(self, data):
        """
        Signal from super that the connection was closed.

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self._enabled:
            self.__start_server_thread()

    def enable(self):
        """
        Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self._enabled:
            # mark connection as enabled
            self._enabled = True

            # start the connection thread
            self.__start_server_thread()

    def disable(self):
        """
        Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        # only stop if enabled
        if self._enabled:
            # mark connection as disabled
            self._enabled = False

            # stop connection thread if it is running
            if self._server_thread and self._server_thread.is_alive():
                self._stop_server_thread = True

                if self._server_sock:
                    self._server_sock.close()

                # wait for connection thread to stop
                while self._stop_server_thread:
                    time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __start_server_thread(self):
        self._server_thread = threading.Thread(
            target=self.__server_thread,
            name=f"secsgem_HsmsPassiveConnection_serverThread_{self._remote_address}")
        self._server_thread.start()

    def __server_thread(self):
        """
        Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not secsgem.common.is_windows():
            self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._server_sock.bind((self._bind_ip, self._remote_port))
        self._server_sock.listen(1)

        while not self._stop_server_thread:
            try:
                select_result = select.select([self._server_sock], [], [], self.select_timeout)
            except Exception:  # pylint: disable=broad-except
                continue

            if not select_result[0]:
                # select timed out
                continue

            accept_result = self._server_sock.accept()
            if accept_result is None:
                continue

            (self._sock, (_, _)) = accept_result

            # setup socket
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # make socket nonblocking
            self._sock.setblocking(0)

            # start the receiver thread
            self._start_receiver()

            self._server_sock.shutdown(socket.SHUT_RDWR)
            self._server_sock.close()

            return

        self._stop_server_thread = False
