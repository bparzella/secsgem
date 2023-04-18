#####################################################################
# active_connection.py
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
"""Hsms active connection."""

import socket
import threading
import time

from .connection import HsmsConnection


class HsmsActiveConnection(HsmsConnection):  # pragma: no cover
    """Client class for single active (outgoing) connection."""

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        """
        Initialize a active hsms connection.

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

        # reconnect thread required for active connection
        self.connection_thread = None
        self.stop_connection_thread = False

        # flag if this is the first connection since enable
        self.first_connection = True

    def _on_hsms_connection_close(self, data):
        """
        Signal from super that the connection was closed.

        This is required to initiate the reconnect if the connection is still enabled
        """
        if self.enabled:
            self.__start_connect_thread()

    def enable(self):
        """
        Enable the connection.

        Starts the connection process to the passive remote.
        """
        # only start if not already enabled
        if not self.enabled:
            # reset first connection to eliminate reconnection timeout
            self.first_connection = True

            # mark connection as enabled
            self.enabled = True

            # start the connection thread
            self.__start_connect_thread()

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
            if self.connection_thread and self.connection_thread.is_alive():
                self.stop_connection_thread = True

            # wait for connection thread to stop
            while self.stop_connection_thread:
                time.sleep(0.2)

            # disconnect super class
            self.disconnect()

    def __idle(self, timeout):
        """
        Wait until timeout elapsed or connection thread is stopped.

        :param timeout: number of seconds to wait
        :type timeout: float
        :returns: False if thread was stopped
        :rtype: boolean
        """
        for _ in range(int(timeout) * 5):
            time.sleep(0.2)

            # check if connection was disabled
            if self.stop_connection_thread:
                self.stop_connection_thread = False
                return False

        return True

    def __start_connect_thread(self):
        self.connection_thread = threading.Thread(
            target=self.__connect_thread,
            name=f"secsgem_HsmsActiveConnection_connectThread_{self._remote_address}")
        self.connection_thread.start()

    def __connect_thread(self):
        """
        Thread function to (re)connect active connection to remote host.

        .. warning:: Do not call this directly, for internal use only.
        """
        # wait for timeout if this is not the first connection
        if not self.first_connection:
            if not self.__idle(self.timeouts.t5):
                return

        self.first_connection = False

        # try to connect to remote
        while not self.__connect():
            if not self.__idle(self.timeouts.t5):
                return

    def __connect(self):
        """
        Open connection to remote host.

        :returns: True if connection was established, False if connection failed
        :rtype: boolean
        """
        # create socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # setup socket
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        self._logger.debug("connecting to %s:%d", self._remote_address, self._remote_port)

        # try to connect socket
        try:
            self._sock.connect((self._remote_address, self._remote_port))
        except socket.error:
            self._logger.debug("connecting to %s:%d failed", self._remote_address, self._remote_port)
            return False

        # make socket nonblocking
        self._sock.setblocking(0)

        # start the receiver thread
        self._start_receiver()

        return True
