#####################################################################
# header.py
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
"""Header for the hsms packets."""

import struct


class HsmsHeader:
    """
    Generic HSMS header.

    Base for different specific headers
    """

    def __init__(self, system, session_id):
        """
        Initialize a hsms header.

        :param system: message ID
        :type system: integer
        :param session_id: device / session ID
        :type session_id: integer

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsHeader(3, 100)
            HsmsHeader({sessionID:0x0064, stream:00, function:00, pType:0x00, sType:0x01, system:0x00000003, \
requireResponse:False})
        """
        self.sessionID = session_id
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x01
        self.system = system

    def __str__(self):
        """Generate string representation for an object of this class."""
        return '{sessionID:0x%04x, stream:%02d, function:%02d, pType:0x%02x, sType:0x%02x, system:0x%08x, ' \
               'requireResponse:%r}' % \
            (self.sessionID, self.stream, self.function, self.pType, self.sType, self.system, self.requireResponse)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return "%s(%s)" % (self.__class__.__name__, self.__str__())

    def encode(self):
        """
        Encode header to hsms packet.

        :returns: encoded header
        :rtype: string

        **Example**::

            >>> import secsgem.hsms
            >>> import secsgem.common
            >>>
            >>> header = secsgem.hsms.HsmsLinktestReqHeader(2)
            >>> secsgem.common.format_hex(header.encode())
            'ff:ff:00:00:00:05:00:00:00:02'

        """
        header_stream = self.stream
        if self.requireResponse:
            header_stream |= 0b10000000

        return struct.pack(">HBBBBL", self.sessionID, header_stream, self.function, self.pType, self.sType, self.system)
