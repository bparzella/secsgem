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

import secsgem.common


class HsmsHeader(secsgem.common.Header):
    """
    Generic HSMS header.

    Base for different specific headers
    """

    def __init__(
            self, 
            system: int, 
            session_id: int, 
            stream: int = 0, 
            function: int = 0,
            requires_response: bool = False,
            p_type: int = 0x00,
            s_type: int = 0x01):
        """
        Initialize a hsms header.

        :param system: message ID
        :type system: integer
        :param session_id: device / session ID
        :type session_id: integer
        :param stream: stream
        :type stream: integer
        :param function: function
        :type function: integer
        :param requires_response: is response required
        :type requires_response: bool
        :param p_type: P-Type
        :type p_type: integer
        :param s_type: S-Type
        :type s_type: integer

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsHeader(3, 100)
            HsmsHeader({session_id:0x0064, stream:00, function:00, p_type:0x00, s_type:0x01, system:0x00000003, \
require_response:False})
        """
        super().__init__(system, session_id, stream, function)
        self._require_response = requires_response
        self._p_type = p_type
        self._s_type = s_type

    def __str__(self):
        """Generate string representation for an object of this class."""
        return f'{{session_id:0x{self.session_id:04x}, ' \
               f'stream:{self.stream:02d}, ' \
               f'function:{self.function:02d}, ' \
               f'p_type:0x{self.p_type:02x}, ' \
               f's_type:0x{self.s_type:02x}, ' \
               f'system:0x{self.system:08x}, ' \
               f'require_response:{self.require_response!r}}}'

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}({self.__str__()})"

    @property
    def require_response(self) -> bool:
        """Get require response flag."""
        return self._require_response

    @property
    def p_type(self) -> int:
        """Get P-type."""
        return self._p_type

    @property
    def s_type(self) -> int:
        """Get S-type."""
        return self._s_type

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
        if self.require_response:
            header_stream |= 0b10000000

        return struct.pack(
            ">HBBBBL",
            self.session_id,
            header_stream,
            self.function,
            self.p_type,
            self.s_type,
            self.system
        )
