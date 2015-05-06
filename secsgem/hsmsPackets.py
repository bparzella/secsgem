#####################################################################
# hsmsPackets.py
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


class hsmsHeader:
    """Generic HSMS header

    Base for different specific headers

    :param system: message ID
    :type system: integer
    :param sessionID: device / session ID
    :type sessionID: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsHeader(3, 100)
        secsgem.hsmsPackets.hsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 3, 'sessionID': 100, 'requireResponse': False, 'sType': 1})

    """
    def __init__(self, system, sessionID):
        self.sessionID = sessionID
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x01
        self.system = system

    def __str__(self):
        return '{sessionID:0x%04x, stream:%02d, function:%02d, pType:0x%02x, sType:0x%02x, system:0x%08x, requireResponse:%01d}' % \
            (self.sessionID, self.stream, self.function, self.pType, self.sType, self.system, self.requireResponse)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class hsmsSelectReqHeader(hsmsHeader):
    """Header for Select Request

    Header for message with SType 1.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsSelectReqHeader(14)
        secsgem.hsmsPackets.hsmsSelectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 14, 'sessionID': 65535, 'requireResponse': False, 'sType': 1})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x01
        self.system = system


class hsmsSelectRspHeader(hsmsHeader):
    """Header for Select Response

    Header for message with SType 2.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsSelectRspHeader(24)
        secsgem.hsmsPackets.hsmsSelectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 24, 'sessionID': 65535, 'requireResponse': False, 'sType': 2})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x02
        self.system = system


class hsmsDeselectReqHeader(hsmsHeader):
    """Header for Deselect Request

    Header for message with SType 3.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsDeselectReqHeader(1)
        secsgem.hsmsPackets.hsmsDeselectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 3})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x03
        self.system = system


class hsmsDeselectRspHeader(hsmsHeader):
    """Header for Deselect Response

    Header for message with SType 4.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsDeselectRspHeader(1)
        secsgem.hsmsPackets.hsmsDeselectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 4})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x04
        self.system = system


class hsmsLinktestReqHeader(hsmsHeader):
    """Header for Linktest Request

    Header for message with SType 5.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsLinktestReqHeader(2)
        secsgem.hsmsPackets.hsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x05
        self.system = system


class hsmsLinktestRspHeader(hsmsHeader):
    """Header for Linktest Response

    Header for message with SType 6.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsLinktestRspHeader(10)
        secsgem.hsmsPackets.hsmsLinktestRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 10, 'sessionID': 65535, 'requireResponse': False, 'sType': 6})

    """
    def __init__(self, system):
        self.sessionID = 0xFFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x06
        self.system = system


class hsmsSeparateReqHeader(hsmsHeader):
    """Header for Separate Request

    Header for message with SType 9.

    :param system: message ID
    :type system: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsSeparateReqHeader(17)
        secsgem.hsmsPackets.hsmsSeparateReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 17, 'sessionID': 65535, 'requireResponse': False, 'sType': 9})

    """
    def __init__(self, system):
        self.sessionID = 0x0FFFF
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x09
        self.system = system


class hsmsStreamFunctionHeader(hsmsHeader):
    """Header for SECS message

    Header for message with SType 0.

    :param system: message ID
    :type system: integer
    :param stream: messages stream
    :type stream: integer
    :param function: messages function
    :type function: integer
    :param requireResponse: is response expected from remote
    :type requireResponse: boolean
    :param sessionID: device / session ID
    :type sessionID: integer

    **Example**::

        >>> secsgem.hsmsPackets.hsmsStreamFunctionHeader(22, 1, 1, True, 100)
        secsgem.hsmsPackets.hsmsStreamFunctionHeader({'function': 1, 'stream': 1, 'pType': 0, 'system': 22, 'sessionID': 100, 'requireResponse': True, 'sType': 0})

    """
    def __init__(self, system, stream, function, requireResponse, sessionID):
        self.sessionID = sessionID
        self.requireResponse = requireResponse
        self.stream = stream
        self.function = function
        self.pType = 0x00
        self.sType = 0x00
        self.system = system


class hsmsPacket:
    """Class for hsms packet.

    Contains all required data and functions.

    :param header: header used for this packet
    :type header: :class:`secsgem.hsmsPackets.hsmsHeader` and derived
    :param data: data part used for streams and functions (SType 0)
    :type data: string

    **Example**::

        >>> secsgem.hsmsPackets.hsmsPacket(secsgem.hsmsPackets.hsmsLinktestReqHeader(2))
        secsgem.hsmsPackets.hsmsPacket({'header': secsgem.hsmsPackets.hsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

    """
    def __init__(self, header=None, data=""):
        if header is None:
            self.header = hsmsHeader()
        else:
            self.header = header

        self.data = data

    def __str__(self):
        data = "header: " + self.header.__str__()
        return data

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def encode(self):
        """Encode packet data to hsms packet

        :returns: encoded packet
        :rtype: string

        **Example**::

            >>> packet = secsgem.hsmsPackets.hsmsPacket(secsgem.hsmsPackets.hsmsLinktestReqHeader(2))
            >>> secsgem.common.formatHex(packet.encode())
            '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

        """
        length = 10 + len(self.data)
        dataLengthText = str(len(self.data))+"s"

        headerStream = self.header.stream
        if self.header.requireResponse:
            headerStream |= 0b10000000

        return struct.pack(">LHBBBBL"+dataLengthText, length, self.header.sessionID, headerStream, self.header.function, self.header.pType, self.header.sType, self.header.system, self.data)

    @staticmethod
    def decode(text):
        """Decode byte array hsms packet to hsmsPacket object

        :returns: received packet object
        :rtype: :class:`secsgem.hsmsPackets.hsmsPacket`

        **Example**::

            >>> secsgem.formatHex(packetData)
            '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

            >>> secsgem.hsmsPackets.hsmsPacket.decode(packetData)
            secsgem.hsmsPackets.hsmsPacket({'header': secsgem.hsmsPackets.hsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

        """
        dataLength = len(text) - 14
        dataLengthText = str(dataLength)+"s"

        res = struct.unpack(">LHBBBBL"+dataLengthText, text)

        result = hsmsPacket(hsmsHeader(res[6], res[1]))
        result.header.requireResponse = (((res[2] & 0b10000000) >> 7) == 1)
        result.header.stream = res[2] & 0b01111111
        result.header.function = res[3]
        result.header.pType = res[4]
        result.header.sType = res[5]
        result.data = res[7]

        return result
