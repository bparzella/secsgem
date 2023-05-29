#####################################################################
# multi_passive_connection.py
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
"""Hsms multi passive connection."""

import socket

from .connection import HsmsConnection


class HsmsMultiPassiveConnection(HsmsConnection):  # pragma: no cover
    """
    Connection class for single connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`.

    Handles connections incoming connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        """
        Initialize a passive client connection.

        :param address: IP address of target host
        :type address: string
        :param port: TCP port of target host
        :type port: integer
        :param session_id: session / device ID to use for connection
        :type session_id: integer
        :param delegate: target for messages
        :type delegate: object

        Example:

            # TODO: create example

        """
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)

        # initially not enabled
        self.enabled = False

    def on_connected(self, sock, address):
        """
        Connect callback for :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`.

        :param sock: Socket for new connection
        :type sock: :class:`Socket`
        :param address: IP address of remote host
        :type address: string
        """
        del address  # unused parameter

        # setup socket
        self.__sock = sock
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # make socket nonblocking
        self._sock.setblocking(0)

        # start the receiver thread
        self._start_receiver()

    def enable(self):
        """
        Enable the connection.

        Starts the connection process to the passive remote.
        """
        self.enabled = True

    def disable(self):
        """
        Disable the connection.

        Stops all connection attempts, and closes the connection
        """
        self.enabled = False
        if self._connected:
            self.disconnect()
