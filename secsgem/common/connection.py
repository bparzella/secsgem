#####################################################################
# connection.py
#
# (c) Copyright 2023, Benjamin Parzella. All rights reserved.
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
"""Connection base function."""

import abc

from .events import Event
from .settings import Settings


class Connection(abc.ABC):
    """Abstract base class for a connection."""

    def __init__(self, settings: Settings) -> None:
        """Initialize connection object."""
        super().__init__()

        self._settings = settings

        self._on_connected = Event()
        self._on_data = Event()
        self._on_disconnecting = Event()
        self._on_disconnected = Event()

        self._connected = False
        self._disconnecting = False

    @property
    def on_connected(self) -> Event:
        """Get the connected event.

        Callbacks to this event are called, when a connection was established.

        """
        return self._on_connected

    @property
    def on_data(self) -> Event:
        """Get the data received event.

        Callbacks to this event are called, when data was received.

        """
        return self._on_data

    @property
    def on_disconnecting(self) -> Event:
        """Get the disconnecting event.

        Callbacks to this event are called, before the connection is separated.

        """
        return self._on_disconnecting

    @property
    def on_disconnected(self) -> Event:
        """Get the disconnect event.

        Callbacks to this event are called, after the connection was separated.

        """
        return self._on_disconnected

    @property
    def connected(self) -> bool:
        """Get the connected flag.

        This flag is True, when a connection is established.

        """
        return self._connected

    @property
    def disconnecting(self) -> bool:
        """Get the disconnecting flag.

        This flag is True, when the connection is about to be separated.

        """
        return self._disconnecting

    @abc.abstractmethod
    def enable(self):
        """Enable the connection.

        Open port and start receiver thread.
        """
        raise NotImplementedError("Connection.enable missing implementation")

    @abc.abstractmethod
    def disable(self):
        """Disable the connection.

        Close port and stop receiver thread.
        """
        raise NotImplementedError("Connection.disable missing implementation")

    @abc.abstractmethod
    def send_data(self, data: bytes) -> bool:
        """Send data to the remote host.

        Args:
            data: encoded data.

        Returns:
            True if succeeded, False if failed

        """
        raise NotImplementedError("Connection.send_data missing implementation")
