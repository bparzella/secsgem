#####################################################################
# packet.py
#
# (c) Copyright 2015, Benjamin Parzella. All rights reserved.
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

from .header import HsmsHeader


class HsmsPacket(secsgem.common.Packet):
    """
    Class for hsms packet.

    Contains all required data and functions.
    """

    def __init__(self, header: typing.Optional[HsmsHeader] = None, data: bytes = b""):
        """
        Initialize a hsms packet.

        Args:
            header: header used for this packet
            data: data part used for streams and functions (SType 0)

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
            HsmsPacket({'header': HsmsLinktestReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, \
s_type:0x05, system:0x00000002, require_response:False}), 'data': ''})

        """
        self._header = HsmsHeader(0, 0) if header is None else header

        self._data = data

    @property
    def header(self) -> HsmsHeader:
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
        Encode packet data to hsms packet.

        :returns: encoded packet
        :rtype: string

        **Example**::

            >>> import secsgem.hsms
            >>> import secsgem.common
            >>>
            >>> packet = secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
            >>> secsgem.common.format_hex(packet.encode())
            '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

        """
        headerdata = self.header.encode()

        length = len(headerdata) + len(self.data)

        return struct.pack(">L", length) + headerdata + self.data

    @staticmethod
    def decode(text: bytes) -> HsmsPacket:
        r"""
        Decode byte array hsms packet to HsmsPacket object.

        :returns: received packet object
        :rtype: :class:`secsgem.hsms.HsmsPacket`

        **Example**::

            >>> import secsgem.common
            >>> import secsgem.hsms
            >>>
            >>> packetData = b"\x00\x00\x00\x0b\xff\xff\x00\x00\x00\x05\x00\x00\x00\x02"
            >>>
            >>> secsgem.common.format_hex(packetData)
            '00:00:00:0b:ff:ff:00:00:00:05:00:00:00:02'
            >>>
            >>> secsgem.hsms.HsmsPacket.decode(packetData)
            HsmsPacket({'header': HsmsHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x05, system:0x00000002, require_response:False}), 'data': ''})
        """   # noqa pylint: disable=line-too-long
        data_length = len(text) - 14
        data_length_text = str(data_length) + "s"

        res = struct.unpack(">LHBBBBL" + data_length_text, text)

        result = HsmsPacket(HsmsHeader(
            res[6], 
            res[1],
            res[2] & 0b01111111,
            res[3],
            (((res[2] & 0b10000000) >> 7) == 1),
            res[4],
            res[5]
        ), res[7])

        return result
