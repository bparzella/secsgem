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
import typing

from .connection import HsmsConnection


class HsmsMultiPassiveConnection(HsmsConnection):
    """Connection class for single connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`.

    Handles connections incoming connection from :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(
            self,
            address: str,
            port: int = 5000,
            session_id: int = 0,
            delegate: typing.Optional[object] = None
    ):
        """Initialize a passive client connection.

        Args:
            address: IP address of target host
            port: TCP port of target host
            session_id: session / device ID to use for connection
            delegate: target for messages

        Example:
            # TODO: create example

        """
        # initialize super class
        HsmsConnection.__init__(self, True, address, port, session_id, delegate)

        # initially not enabled
        self.enabled = False

    def new_connection(self, sock: socket.socket, address: str):
        """Connect callback for :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`.

        Args:
            sock: Socket for new connection
            address: IP address of remote host

        """
        del address  # unused parameter

        # setup socket
        self._sock = sock
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        # make socket nonblocking
        self._socket.setblocking(False)

        # mark connection as connected
        self._connected = True

        # start the receiver thread
        self._start_receiver()

        # send event
        try:
            self.on_connected({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_connected handler")

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
        if self._connected:
            self.disconnect()
