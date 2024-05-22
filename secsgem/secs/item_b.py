#####################################################################
# item_b.py
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
"""Byte SECS data."""
from __future__ import annotations

import typing

from .item import Item, PacketData

if typing.TYPE_CHECKING:
    from .sml import SMLParser


class ItemB(Item):
    """SECS byte data type wrapper."""

    _sml_type = "B"
    _hsms_type = 0o10
    _minimum_value = 0
    _maximum_value = 0xFF

    def _validate_list_value(self, value: typing.Any) -> bytes:
        values = []
        for data_item in value:
            if isinstance(data_item, int):
                values.append(bytes(int(self._verify_value_in_bounds(data_item))))
            elif isinstance(data_item, bytes):
                values.append(data_item)
            else:
                raise self._invalid_type_exception(data_item)
        return b"".join(values)

    def validate_value(self, value: typing.Any) -> bytes:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        if isinstance(value, list):
            return self._validate_list_value(value)
        if isinstance(value, int):
            return bytes([int(self._verify_value_in_bounds(value))])
        if isinstance(value, bytes):
            return value

        raise self._invalid_type_exception(value)

    @classmethod
    def _is_valid_list(cls, values: typing.Any) -> bool:
        for value in values:
            if isinstance(value, int):
                if not cls._is_value_in_bounds(value):
                    return False
            elif not isinstance(value, bytes):
                return False

        return True
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
            return cls._is_valid_list(value)
        if isinstance(value, int):
            return cls._is_value_in_bounds(value)
        if isinstance(value, bytes):
            return True
        if isinstance(value, ItemB):
            return True

        return False

    @classmethod
    def _read_sml_token(cls, parser: SMLParser) -> bytes:
        data = []

        while parser.peek_token().value != ">":
            item = parser.get_token()

            value = int(item.value, 0)
            value = int(cls._verify_value_in_bounds(value, item))
            data.append(value)

        parser.get_token()

        return bytes(data)

    @staticmethod
    def _format_value(value: int) -> str:
        return hex(value)

    def encode(self) -> bytes:
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        result = self.encode_item_header(len(self._value) if self._value is not None else 0)

        if self._value is not None:
            result += self._value

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

        _, length = cls._decode_item_header(data)

        return cls([data.get(length)])
