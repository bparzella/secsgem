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
"""Header for the hsms messages."""

from __future__ import annotations

import enum
import struct
import typing

import secsgem.common


class HsmsSType(enum.Enum):
    """HSMS SType enum."""

    DATA_MESSAGE = 0
    SELECT_REQ = 1
    SELECT_RSP = 2
    DESELECT_REQ = 3
    DESELECT_RSP = 4
    LINKTEST_REQ = 5
    LINKTEST_RSP = 6
    REJECT_REQ = 7
    SEPARATE_REQ = 9

    @classmethod
    def names(cls) -> dict[HsmsSType, str]:
        """Get the names associated with the scode.

        Returns:
            dictionary of names associated with enum values

        """
        return {
            cls.DATA_MESSAGE: "Data.msg",
            cls.SELECT_REQ: "Select.req",
            cls.SELECT_RSP: "Select.rsp",
            cls.DESELECT_REQ: "Deselect.req",
            cls.DESELECT_RSP: "Deselect.rsp",
            cls.LINKTEST_REQ: "Linktest.req",
            cls.LINKTEST_RSP: "Linktest.rsp",
            cls.REJECT_REQ: "Reject.req",
            cls.SEPARATE_REQ: "Separate.req",
        }

    @property
    def text(self) -> str:
        """Get the text for the item."""
        return self.names()[self]


class HsmsHeader(secsgem.common.Header):
    """Generic HSMS header.

    Base for different specific headers
    """

    length = 10

    def __init__(  # pylint: disable=too-many-arguments
        self,
        system: int,
        session_id: int,
        stream: int = 0,
        function: int = 0,
        requires_response: bool = False,
        p_type: int = 0x00,
        s_type: HsmsSType = HsmsSType.SELECT_REQ,
    ):
        """Initialize a hsms header.

        Args:
            system: message ID
            session_id: device / session ID
            stream: stream
            function: function
            requires_response: is response required
            p_type: P-Type
            s_type: S-Type

        Example:
            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsHeader(3, 100)
            HsmsHeader({session_id:0x0064, stream:00, function:00, p_type:0x00, s_type:0x01, system:0x00000003, \
require_response:False})

        """
        super().__init__(system, session_id, stream, function, requires_response)
        self._p_type = p_type
        self._s_type = s_type

    def __str__(self) -> str:
        """Generate string representation for an object of this class."""
        return (
            f"{{session_id:0x{self.session_id:04x}, "
            f"stream:{self.stream:02d}, "
            f"function:{self.function:02d}, "
            f"p_type:0x{self.p_type:02x}, "
            f"s_type:0x{self.s_type.value:02x}, "
            f"system:0x{self.system:08x}, "
            f"require_response:{self.require_response!r}}}"
        )

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}({self.__str__()})"

    @property
    def p_type(self) -> int:
        """Get P-type."""
        return self._p_type

    @property
    def s_type(self) -> HsmsSType:
        """Get S-type."""
        return self._s_type

    @property
    def _as_dictionary(self) -> dict[str, typing.Any]:
        """Get the data as dictionary.

        Returns:
            Header data as dictionary.

        """
        return {
            "system": self._system,
            "session_id": self._session_id,
            "stream": self._stream,
            "function": self._function,
            "requires_response": self._require_response,
            "p_type": self._p_type,
            "s_type": self._s_type,
        }

    def encode(self) -> bytes:
        """Encode header to hsms message.

        Returns:
            encoded header

        Example:
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
            self.s_type.value,
            self.system,
        )

    @classmethod
    def decode(cls, data: bytes) -> HsmsHeader:
        """Decode data to HsmsHeader object.

        Args:
            data: data to decode

        Returns:
            new header object

        """
        res = struct.unpack(">HBBBBL", data)

        return HsmsHeader(
            res[5],
            res[0],
            res[1] & 0b01111111,
            res[2],
            (((res[1] & 0b10000000) >> 7) == 1),
            res[3],
            HsmsSType(res[4]),
        )
