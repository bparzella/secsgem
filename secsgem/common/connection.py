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

from .packet import Packet


class Connection(abc.ABC):
    """Abstract base class for a connection."""

    @property
    @abc.abstractmethod
    def disconnecting(self) -> bool:
        """Get the disconnecting flag."""
        raise NotImplementedError("Connection.disconnecting missing implementation")

    @abc.abstractmethod
    def send_packet(self, packet: Packet) -> bool:
        """
        Send a packet to the remote.

        Args:
            packet: packet to be transmitted

        Returns:
            True if succeeded, False if failed

        """
        raise NotImplementedError("Connection.send_packet missing implementation")
