#####################################################################
# header.py
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
"""Header for the secs messagess."""

from __future__ import annotations

import struct
import typing

import secsgem.common


class SecsIHeader(secsgem.common.Header):
    """Generic SECS I header.

    Base for different specific headers
    """

    length = 10

    def __init__(  # pylint: disable=too-many-arguments
        self,
        system: int,
        session_id: int,
        stream: int = 0,
        function: int = 0,
        block: int = 0,
        from_equipment: bool = False,
        require_response: bool = False,
        last_block: bool = True,
    ):
        """Initialize a SECS I header.

        Args:
            system: message ID
            session_id: device / session ID
            stream: stream
            function: function
            block: block number
            from_equipment: message is send from equipment
            require_response: response requested
            last_block: last block of multi block message

        Example:
            >>> import secsgem.secsi
            >>>
            >>> secsgem.secsi.SecsIHeader(3, 100)
            SecsIHeader({session_id:0x0064, stream:00, function:00, system:0x00000003, block:0x0000, from_host:False, \
require_response:False, last_block:True})

        """
        super().__init__(system, session_id, stream, function, require_response)

        self._block = block
        self._from_equipment = from_equipment
        self._last_block = last_block

    @property
    def block(self) -> int:
        """Get block number."""
        return self._block

    @property
    def from_equipment(self) -> bool:
        """Get if the message is from equipment (True) or host (False).

        This is the reverse bit (r-bit).
        """
        return self._from_equipment

    @property
    def last_block(self) -> bool:
        """Get if the message is the last of a multi-block message.

        This is the end bit (e-bit).
        """
        return self._last_block

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
            "block": self._block,
            "from_equipment": self._from_equipment,
            "require_response": self._require_response,
            "last_block": self._last_block,
        }

    def __str__(self) -> str:
        """Generate string representation for an object of this class."""
        return (
            "{"
            f"session_id:0x{self.session_id:04x}, "
            f"stream:{self.stream:02d}, "
            f"function:{self.function:02d}, "
            f"system:0x{self.system:08x}, "
            f"block:0x{self.block:04x}, "
            f"from_host:{self.from_equipment!r}, "
            f"require_response:{self.require_response!r}, "
            f"last_block:{self.last_block!r}"
            "}"
        )

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}({self.__str__()})"

    def encode(self) -> bytes:
        """Encode header to SECS I message.

        Returns:
            encoded header

        Example:
            >>> import secsgem.secsi
            >>> import secsgem.common
            >>>
            >>> header = secsgem.secsi.SecsIHeader(2, 100)
            >>> secsgem.common.format_hex(header.encode())
            '00:64:00:00:80:00:00:00:00:02'

        """
        session_id = self.session_id
        if self.from_equipment:
            session_id |= 0b1000000000000000

        stream = self.stream
        if self.require_response:
            stream |= 0b10000000

        block = self.block
        if self.last_block:
            block |= 0b1000000000000000

        return struct.pack(
            ">HBBHI",
            session_id,
            stream,
            self.function,
            block,
            self.system,
        )

    @classmethod
    def decode(cls, data: bytes) -> SecsIHeader:
        """Decode data to SecsIHeader object.

        Args:
            data: data to decode

        Returns:
            new header object

        """
        res = struct.unpack(">HBBHI", data)

        return SecsIHeader(
            res[4],
            res[0] & 0b0111111111111111,
            res[1] & 0b01111111,
            res[2],
            res[3] & 0b0111111111111111,
            (((res[0] & 0b1000000000000000) >> 15) == 1),
            (((res[1] & 0b10000000) >> 7) == 1),
            (((res[3] & 0b1000000000000000) >> 15) == 1),
        )
