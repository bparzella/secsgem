#####################################################################
# packet.py
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
"""packet base class."""
from __future__ import annotations

import abc

from .header import Header


class Packet(abc.ABC):
    """Abstract base class for a packet."""

    @property
    @abc.abstractmethod
    def header(self) -> Header:
        """Get the header."""
        raise NotImplementedError("Packet.header missing implementation")

    @property
    @abc.abstractmethod
    def data(self) -> bytes:
        """Get the header."""
        raise NotImplementedError("Packet.data missing implementation")

    @abc.abstractmethod
    def encode(self) -> bytes:
        """
        Encode packet object to transmittable bytes.

        Returns:
            byte-encoded packet

        """
        raise NotImplementedError("Packet.encode missing implementation")

    @staticmethod
    @abc.abstractmethod
    def decode(data: bytes) -> Packet:
        """Decode byte array hsms packet to HsmsPacket object.

        Args:
            data: byte-encode packet data

        Returns
            received packet object

        """
        raise NotImplementedError("Packet.decode missing implementation")
