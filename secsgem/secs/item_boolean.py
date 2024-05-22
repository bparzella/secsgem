#####################################################################
# item_boolean.py
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
"""Boolean SECS data."""
from __future__ import annotations

import typing

from .item import Item, PacketData

if typing.TYPE_CHECKING:
    from .sml import SMLParser


class ItemBOOLEAN(Item):
    """SECS boolean data type wrapper."""

    _sml_type = "BOOLEAN"
    _hsms_type = 0o11
    _minimum_value = 0
    _maximum_value = 1

    def _validate_list_value(self, value: typing.Any) -> list[bool]:
        values = []
        for data_item in value:
            if isinstance(data_item, int):
                values.append(self._verify_value_in_bounds(data_item) == 1)
            elif isinstance(data_item, bool):
                values.append(data_item)
            else:
                raise self._invalid_type_exception(data_item)

        return values

    def validate_value(self, value: typing.Any) -> list[bool]:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        if isinstance(value, list):
            return self._validate_list_value(value)
        if isinstance(value, int):
            return [self._verify_value_in_bounds(value) == 1]
        if isinstance(value, bool):
            return [value]

        raise self._invalid_type_exception(value)

    @classmethod
    def _is_valid_list(cls, value: typing.Any) -> bool:
        for item in value:
            if isinstance(item, int):
                if not cls._is_value_in_bounds(item):
                    return False
            elif not isinstance(item, bool):
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
        if isinstance(value, bool):
            return True
        if isinstance(value, ItemBOOLEAN):
            return True

        return False

    @classmethod
    def _read_sml_token(cls, parser: SMLParser) -> list[bool]:
        data = []

        while parser.peek_token().value != ">":
            item = parser.get_token()

            value = int(item.value, 0)
            value = int(cls._verify_value_in_bounds(value, item))
            data.append(value == 1)

        parser.get_token()

        return data

    @staticmethod
    def _format_value(value: bool) -> str:
        return "0x1" if value else "0x0"

    def encode(self) -> bytes:
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        result = self.encode_item_header(len(self._value))

        for counter, _ in enumerate(self._value):
            value = self._value[counter]
            if value:
                result += b"\1"
            else:
                result += b"\0"

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

        result = [char > 0 for char in data.get(length)]

        return cls(result)
