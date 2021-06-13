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
        self.connectionThread = None
        self.stopConnectionThread = False

        # flag if this is the first connection since enable
        self.firstConnection = True

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
            self.firstConnection = True

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
            if self.connectionThread and self.connectionThread.is_alive():
                self.stopConnectionThread = True

            # wait for connection thread to stop
            while self.stopConnectionThread:
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
            if self.stopConnectionThread:
                self.stopConnectionThread = False
                return False

        return True

    def __start_connect_thread(self):
        self.connectionThread = threading.Thread(target=self.__connect_thread,
                                                 name="secsgem_HsmsActiveConnection_connectThread_{}"
                                                 .format(self.remoteAddress))
        self.connectionThread.start()

    def __connect_thread(self):
        """
        Thread function to (re)connect active connection to remote host.

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
        """
        Open connection to remote host.

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
