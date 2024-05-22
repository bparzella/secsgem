#####################################################################
# item_l.py
#
# (c) Copyright 2023-2024, Benjamin Parzella. All rights reserved.
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
"""SECS data list."""
from __future__ import annotations

import typing

from .item import Item, PacketData

if typing.TYPE_CHECKING:
    from .sml import SMLParser


class ItemL(Item):
    """SECS list data type wrapper."""

    _sml_type = "L"
    _hsms_type = 0o00

    def validate_value(self, value: typing.Any) -> typing.Any:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        if isinstance(value, list):
            return [self.from_value(item) for item in value]

        raise ValueError(f"Invalid value '{value}' for type '{self.__class__.__name__}'")

    @classmethod
    def is_valid(cls, value: typing.Any, _length: int | None = None) -> bool:
        """Check if value is valid.

        Args:
            value: value to check
            _length: data length if applicable

        Returns:
            True if data is valid

        """
        if isinstance(value, list):
            return True

        return False

    @classmethod
    def _read_sml_token(cls, parser: SMLParser) -> Item:
        return cls._read_item(parser)

    def to_sml(self, indent=0):
        """Convert data object to SML string.

        Args:
            indent: indent level in spaces

        Returns:
            SML text

        """
        if len(self._value) == 0:
            return f"{indent * ' '}< {self._sml_type} >"

        values = [f"{value.to_sml(indent + 4)}" for value in self._value]
        values_text = "\n".join(values)
        return (
            f"{indent * ' '}< {self._sml_type} [{len(self._value)}]\n"
            f"{values_text}\n"
            f"{indent * ' '}>"
        )

    def encode(self) -> bytes:
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        result = self.encode_item_header(len(self._value))

        for item in self._value:
            result += item.encode()

        return result

    @classmethod
    def decode(cls, data: PacketData | bytes) -> Item:
        """Create a new data object by decoding a secs packet.

        Args:
            data: packet data

        Returns:
            new data object

        """
        if isinstance(data, bytes):
            data = PacketData(data)

        (_, length) = cls._decode_item_header(data)

        # list
        items = [Item.decode(data) for _ in range(length)]

        return cls(items)
