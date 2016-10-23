#####################################################################
# packets.py
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
"""Contains objects that encapsulate hsms messages"""

import struct


class HsmsHeader:
    """Generic HSMS header

    Base for different specific headers

    :param system: message ID
    :type system: integer
    :param session_id: device / session ID
    :type session_id: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsHeader(3, 100)
        HsmsHeader({sessionID:0x0064, stream:00, function:00, pType:0x00, sType:0x01, system:0x00000003, requireResponse:False})

    """

    def __init__(self, system, session_id):
        self.sessionID = session_id
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x01
        self.system = system

    def __str__(self):
        """Generate string representation for an object of this class"""
        return '{sessionID:0x%04x, stream:%02d, function:%02d, pType:0x%02x, sType:0x%02x, system:0x%08x, requireResponse:%r}' % \
            (self.sessionID, self.stream, self.function, self.pType, self.sType, self.system, self.requireResponse)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        return "%s(%s)" % (self.__class__.__name__, self.__str__())

    def encode(self):
        """Encode header to hsms packet

        :returns: encoded header
        :rtype: string

        **Example**::

            >>> import secsgem
            >>>
            >>> header = secsgem.hsms.packets.HsmsLinktestReqHeader(2)
            >>> secsgem.common.format_hex(header.encode())
            'ff:ff:00:00:00:05:00:00:00:02'

        """
        header_stream = self.stream
        if self.requireResponse:
            header_stream |= 0b10000000

        return struct.pack(">HBBBBL", self.sessionID, header_stream, self.function, self.pType, self.sType, self.system)


class HsmsSelectReqHeader(HsmsHeader):
    """Header for Select Request

    Header for message with SType 1.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsSelectReqHeader(14)
        HsmsSelectReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x01, system:0x0000000e, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x01


class HsmsSelectRspHeader(HsmsHeader):
    """Header for Select Response

    Header for message with SType 2.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsSelectRspHeader(24)
        HsmsSelectRspHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x02, system:0x00000018, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x02


class HsmsDeselectReqHeader(HsmsHeader):
    """Header for Deselect Request

    Header for message with SType 3.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsDeselectReqHeader(1)
        HsmsDeselectReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x03, system:0x00000001, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x03


class HsmsDeselectRspHeader(HsmsHeader):
    """Header for Deselect Response

    Header for message with SType 4.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsDeselectRspHeader(1)
        HsmsDeselectRspHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x04, system:0x00000001, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x04


class HsmsLinktestReqHeader(HsmsHeader):
    """Header for Linktest Request

    Header for message with SType 5.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsLinktestReqHeader(2)
        HsmsLinktestReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x05, system:0x00000002, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x05


class HsmsLinktestRspHeader(HsmsHeader):
    """Header for Linktest Response

    Header for message with SType 6.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsLinktestRspHeader(10)
        HsmsLinktestRspHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x06, system:0x0000000a, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x06


class HsmsRejectReqHeader(HsmsHeader):
    """Header for Reject Request

    Header for message with SType 7.

    :param system: message ID
    :type system: integer
    :param s_type: sType of rejected message
    :type s_type: integer
    :param reason: reason for rejection
    :type reason: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsRejectReqHeader(17, 3, 4)
        HsmsRejectReqHeader({sessionID:0xffff, stream:03, function:04, pType:0x00, sType:0x07, system:0x00000011, requireResponse:False})

    """

    def __init__(self, system, s_type, reason):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = s_type
        self.function = reason
        self.pType = 0x00
        self.sType = 0x07


class HsmsSeparateReqHeader(HsmsHeader):
    """Header for Separate Request

    Header for message with SType 9.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsSeparateReqHeader(17)
        HsmsSeparateReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x09, system:0x00000011, requireResponse:False})

    """

    def __init__(self, system):
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x09


class HsmsStreamFunctionHeader(HsmsHeader):
    """Header for SECS message

    Header for message with SType 0.

    :param system: message ID
    :type system: integer
    :param stream: messages stream
    :type stream: integer
    :param function: messages function
    :type function: integer
    :param require_response: is response expected from remote
    :type require_response: boolean
    :param session_id: device / session ID
    :type session_id: integer

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
        HsmsStreamFunctionHeader({sessionID:0x0064, stream:01, function:01, pType:0x00, sType:0x00, system:0x00000016, requireResponse:True})

    """

    def __init__(self, system, stream, function, require_response, session_id):
        HsmsHeader.__init__(self, system, session_id)
        self.sessionID = session_id
        self.requireResponse = require_response
        self.stream = stream
        self.function = function
        self.pType = 0x00
        self.sType = 0x00
        self.system = system


class HsmsPacket:
    """Class for hsms packet.

    Contains all required data and functions.

    :param header: header used for this packet
    :type header: :class:`secsgem.hsms.packets.HsmsHeader` and derived
    :param data: data part used for streams and functions (SType 0)
    :type data: string

    **Example**::

        >>> import secsgem
        >>>
        >>> secsgem.hsms.packets.HsmsPacket(secsgem.hsms.packets.HsmsLinktestReqHeader(2))
        HsmsPacket({'header': HsmsLinktestReqHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x05, system:0x00000002, requireResponse:False}), 'data': ''})

    """

    def __init__(self, header=None, data=b""):
        if header is None:
            self.header = HsmsHeader(0, 0)
        else:
            self.header = header

        self.data = data

    def __str__(self):
        """Generate string representation for an object of this class"""
        data = "'header': " + self.header.__str__()
        return data

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        return "%s({'header': %s, 'data': '%s'})" % (self.__class__.__name__, self.header.__repr__(), self.data.decode("utf-8"))

    def encode(self):
        """Encode packet data to hsms packet

        :returns: encoded packet
        :rtype: string

        **Example**::

            >>> import secsgem
            >>>
            >>> packet = secsgem.hsms.packets.HsmsPacket(secsgem.hsms.packets.HsmsLinktestReqHeader(2))
            >>> secsgem.common.format_hex(packet.encode())
            '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

        """
        headerdata = self.header.encode()

        length = len(headerdata) + len(self.data)

        return struct.pack(">L", length) + headerdata + self.data

    @staticmethod
    def decode(text):
        """Decode byte array hsms packet to HsmsPacket object

        :returns: received packet object
        :rtype: :class:`secsgem.hsms.packets.HsmsPacket`

        **Example**::

            >>> import secsgem
            >>>
            >>> packetData = b"\\x00\\x00\\x00\\x0b\\xff\\xff\\x00\\x00\\x00\\x05\\x00\\x00\\x00\\x02"
            >>>
            >>> secsgem.format_hex(packetData)
            '00:00:00:0b:ff:ff:00:00:00:05:00:00:00:02'
            >>>
            >>> secsgem.hsms.packets.HsmsPacket.decode(packetData)
            HsmsPacket({'header': HsmsHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x05, system:0x00000002, requireResponse:False}), 'data': ''})


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
