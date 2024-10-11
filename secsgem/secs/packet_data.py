#####################################################################
# packet_data.py
#
# (c) Copyright 2024, Benjamin Parzella. All rights reserved.
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
"""Packet data class."""

from __future__ import annotations


class PacketData:
    r"""Wrapper for packet data that allows iterating over the data bytes.

    Example:
        >>> from secsgem.secs.packet_data import PacketData
        >>>
        >>> packet_data = PacketData(b"\x01\x02\x03\x04")
        >>> packet_data.peek()
        1
        >>> packet_data.get_one()
        1
        >>> packet_data.get(2)
        b'\x02\x03'
        >>> packet_data.get()
        b'\x04'

    """

    def __init__(self, data: bytes):
        """Initialize packet data.

        Args:
            data: packet raw data

        """
        self._data = data

    def peek(self) -> int:
        """Get the next packet byte without incrementing the pointer.

        Returns:
            requested data

        """
        return self._data[0]

    def get_one(self) -> int:
        """Get one packet byte.

        Returns:
            single packet byte

        """
        result = self._data[0]

        self._data = self._data[1:]

        return result

    def get(self, length: int = 1) -> bytes:
        """Get the next packet bytes.

        Args:
            length: number of bytes

        Returns:
            requested data

        """
        result = self._data[:length]

        self._data = self._data[length:]

        return result


