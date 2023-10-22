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
"""Contains hsms packet class."""
from __future__ import annotations

import struct
import typing

import secsgem.common
from secsgem.common.header import Header

from .header import SecsIHeader


class SecsIPacket(secsgem.common.Packet):
    """
    Class for SECS I packet.

    Contains all required data and functions.
    """

    def __init__(self, header: typing.Optional[SecsIHeader] = None, data: bytes = b""):
        """
        Initialize a SECS I packet.

        Args:
            header: header used for this packet
            data: data part used for streams and functions (SType 0)

        Example:
            >>> import secsgem.secsi
            >>>
            >>> secsgem.secsi.SecsIPacket()
            HsmsPacket({'header': HsmsLinktestReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, \
s_type:0x05, system:0x00000002, require_response:False}), 'data': ''})

        """
        self._header = SecsIHeader(0, 0) if header is None else header

        self._data = data

    @property
    def header(self) -> Header:
        """Get the header."""
        return self._header

    @property
    def data(self) -> bytes:
        """Get the data."""
        return self._data

    def __str__(self) -> str:
        """Generate string representation for an object of this class."""
        data = "'header': " + self.header.__str__()
        return data

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}" \
               f"({{'header': {self.header.__repr__()}, 'data': '{self.data.decode('utf-8')}'}})"

    def encode(self) -> bytes:
        """
        Encode packet data to SECS I packet.

        Returns:
            byte-encoded packet

        Example:

            >>> import secsgem.secsi
            >>> import secsgem.common
            >>>
            >>> packet = secsgem.secsi.SecsIPacket()
            >>> secsgem.common.format_hex(packet.encode())
            '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

        """
        headerdata = self._header.encode()

        length = len(headerdata) + len(self.data)

        return struct.pack(">L", length) + headerdata + self.data

    @staticmethod
    def decode(data: bytes) -> SecsIPacket:
        r"""
        Decode byte array SECS I packet to SecsIPacket object.

        Args:
            data: byte-encode packet data
        
        Returns:
            received packet object

        Example:
            >>> import secsgem.common
            >>> import secsgem.secsi
            >>>
            >>> packetData = b"\x00\x00\x00\x0b\xff\xff\x00\x00\x00\x05\x00\x00\x00\x02"
            >>>
            >>> secsgem.common.format_hex(packetData)
            '00:00:00:0b:ff:ff:00:00:00:05:00:00:00:02'
            >>>
            >>> secsgem.secsi.SecsIPacket.decode(packetData)
            SecsIPacket({'header': HsmsHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x05, system:0x00000002, require_response:False}), 'data': ''})

        """   # noqa pylint: disable=line-too-long
        data_length = len(data) - SecsIHeader.length

        header = SecsIHeader.decode(data[:SecsIHeader.length])
        res = struct.unpack(f">{data_length}s", data[SecsIHeader.length:])

        result = SecsIPacket(header, res[0])

        return result
