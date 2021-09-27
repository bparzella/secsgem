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

import struct

from .header import HsmsHeader


class HsmsPacket:
    """
    Class for hsms packet.

    Contains all required data and functions.
    """

    def __init__(self, header=None, data=b""):
        """
        Initialize a hsms packet.

        :param header: header used for this packet
        :type header: :class:`secsgem.hsms.HsmsHeader` and derived
        :param data: data part used for streams and functions (SType 0)
        :type data: string

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
            HsmsPacket({'header': HsmsLinktestReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, \
sType:0x05, system:0x00000002, requireResponse:False}), 'data': ''})
        """
        if header is None:
            self.header = HsmsHeader(0, 0)
        else:
            self.header = header

        self.data = data

    def __str__(self):
        """Generate string representation for an object of this class."""
        data = "'header': " + self.header.__str__()
        return data

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}" \
               f"({{'header': {self.header.__repr__()}, 'data': '{self.data.decode('utf-8')}'}})"

    def encode(self):
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
    def decode(text):
        """
        Decode byte array hsms packet to HsmsPacket object.

        :returns: received packet object
        :rtype: :class:`secsgem.hsms.HsmsPacket`

        **Example**::

            >>> import secsgem.common
            >>> import secsgem.hsms
            >>>
            >>> packetData = b"\\x00\\x00\\x00\\x0b\\xff\\xff\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\x02"
            >>>
            >>> secsgem.common.format_hex(packetData)
            '00:00:00:0b:ff:ff:00:00:00:05:00:00:00:02'
            >>>
            >>> secsgem.hsms.HsmsPacket.decode(packetData)
            HsmsPacket({'header': HsmsHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x05, \
system:0x00000002, requireResponse:False}), 'data': ''})
        """
        data_length = len(text) - 14
        data_length_text = str(data_length) + "s"

        res = struct.unpack(">LHBBBBL" + data_length_text, text)

        result = HsmsPacket(HsmsHeader(res[6], res[1]))
        result.header.requireResponse = (((res[2] & 0b10000000) >> 7) == 1)
        result.header.stream = res[2] & 0b01111111
        result.header.function = res[3]
        result.header.pType = res[4]
        result.header.sType = res[5]
        result.data = res[7]

        return result
