#####################################################################
# tcp_server_connection.py
#
# (c) Copyright 2021-2023, Benjamin Parzella. All rights reserved.
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
"""TCP server connection."""
from __future__ import annotations

import select
import socket
import threading
import time
import typing

from .helpers import is_windows
from .tcp_connection import TcpConnection

if typing.TYPE_CHECKING:
    from .settings import Settings


class TcpServerConnection(TcpConnection):
    """Server class for TCP server connection.

    Creates a listening socket and waits for one incoming connection on this socket.
    After the connection is established the listening socket is closed.
    """

    def __init__(self, settings: Settings):
        """Initialize a TCP server connection.

        Args:
            settings: protocol and communication settings

        """
        # initialize super class
        TcpConnection.__init__(self, settings)

        # initially not enabled
        self._enabled = False

        # reconnect thread required for server
        self._server_thread = None
        self._stop_server_thread = False
        self._server_sock = None

        self.on_disconnected.register(self._disconnected)

    def _disconnected(self, _: dict[str, typing.Any]):
        """Called when the connection was disconnected.

        This is required to initiate the reconnect if the connection is still enabled

        """
        if self._enabled:
            self.__start_server_thread()

    def enable(self):
        """Enable the connection.

        Starts the connection server process.
        """
        # only start if not already enabled
        if not self._enabled:
            # mark connection as enabled
            self._enabled = True

            # start the connection thread
            self.__start_server_thread()

    def disable(self):
        """Disable the connection.

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
            name=f"secsgem_tcpServerConnection_serverThread_{self._settings.address}")
        self._server_thread.start()

    def __server_thread(self):
        """Thread function to wait for incoming tcp connections.

        .. warning:: Do not call this directly, for internal use only.
        """
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not is_windows():
            self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._server_sock.bind((self._settings.address, self._settings.port))
        self._server_sock.listen(1)

        while not self._stop_server_thread:
            try:
                select_result = select.select([self._server_sock], [], [], self.select_timeout)
            except Exception as exc:  # pylint: disable=broad-except
                self._logger.debug("select exception", exc_info=exc)

            if not select_result[0]:
                # select timed out
                continue

            accept_result = self._server_sock.accept()
            if accept_result is None:
                continue

            (self._sock, (_, _)) = accept_result

            # setup socket
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # make socket nonblocking
            self._socket.setblocking(0)

            # mark connection as connected
            self._connected = True

            # start the receiver thread
            self._start_receiver()

            # send event
            try:
                self.on_connected({"source": self})
            except Exception:  # pylint: disable=broad-except
                self._logger.exception("ignoring exception for on_connection_established handler")

            self._server_sock.shutdown(socket.SHUT_RDWR)
            self._server_sock.close()

            return

        self._stop_server_thread = False
