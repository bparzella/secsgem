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

    def __init__(self, address, port=5000, session_id=0, delegate=None):
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

        # initially not enabled
        self.enabled = False

        # reconnect thread required for passive connection
        self.serverThread = None
        self.stopServerThread = False
        self.serverSock = None

    def _on_hsms_connection_close(self, data):
        """
        Signal from super that the connection was closed.

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__start_server_thread()

    def enable(self):
        """
        Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self.enabled:
            # mark connection as enabled
            self.enabled = True

            # start the connection thread
            self.__start_server_thread()

    def disable(self):
        """
        Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        # only stop if enabled
        if self.enabled:
            # mark connection as disabled
            self.enabled = False

            # stop connection thread if it is running
            if self.serverThread and self.serverThread.is_alive():
                self.stopServerThread = True

                if self.serverSock:
                    self.serverSock.close()

                # wait for connection thread to stop
                while self.stopServerThread:
                    time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __start_server_thread(self):
        self.serverThread = threading.Thread(target=self.__server_thread,
                                             name="secsgem_HsmsPassiveConnection_serverThread_{}"
                                             .format(self.remoteAddress))
        self.serverThread.start()

    def __server_thread(self):
        """
        Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not secsgem.common.is_windows():
            self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverSock.bind(('', self.remotePort))
        self.serverSock.listen(1)

        while not self.stopServerThread:
            try:
                select_result = select.select([self.serverSock], [], [], self.select_timeout)
            except Exception:  # pylint: disable=broad-except
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
