#####################################################################
# item_number.py
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
"""Numeric SECS data."""
from __future__ import annotations

import struct
import typing

from .item import Item, PacketData

if typing.TYPE_CHECKING:
    from .sml import SMLParser


class ItemNumber(Item):
    """SECS number generic data type wrapper."""

    _bytes = -1
    _struct_code = ""
    _type: type = int

    @classmethod
    def _read_sml_token(cls, parser: SMLParser) -> list:
        data = []

        while parser.peek_token().value != ">":
            item = parser.get_token()

            value = cls._type(item.value)
            value = cls._type(cls._verify_value_in_bounds(value, item))
            data.append(value)

        parser.get_token()

        return data

    @staticmethod
    def _format_value(value: int) -> str:
        return f"{value}"

    def validate_value(self, value: list[int | float] | int | float) -> typing.Any:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        if isinstance(value, list):
            values = []
            for data_item in value:
                if isinstance(data_item, self._type):
                    values.append(self._verify_value_in_bounds(data_item))
                else:
                    raise self._invalid_type_exception(data_item)
            return values

        if isinstance(value, self._type):
            return [self._verify_value_in_bounds(value)]

        raise self._invalid_type_exception(value)

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
            for item in value:
                if not isinstance(item, cls._type):
                    return False

                if not cls._is_value_in_bounds(item):
                    return False
            return True

        if isinstance(value, cls._type):
            return cls._is_value_in_bounds(value)

        if isinstance(value, cls):
            return True

        return False

    def encode(self):
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        result = self.encode_item_header(len(self._value) * self._bytes)

        for counter, _ in enumerate(self._value):
            value = self._value[counter]
            result += struct.pack(f">{self._struct_code}", value)

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
        result = []

        for _ in range(length // cls._bytes):
            result_text = data.get(cls._bytes)

            if len(result_text) != cls._bytes:
                raise ValueError(f"No enough data found for {cls.__name__} with length {length}")

            result.append(struct.unpack(f">{cls._struct_code}", result_text)[0])

        return cls(result)


class ItemI8(ItemNumber):
    """Representation of signed 8 byte integer SECS data."""

    _sml_type = "I8"
    _hsms_type = 0o30
    _bytes = 8
    _struct_code = "q"
    _minimum_value = -9223372036854775808
    _maximum_value = 9223372036854775807
    _type = int


class ItemI1(ItemNumber):
    """Representation of signed 1 byte integer SECS data."""

    _sml_type = "I1"
    _hsms_type = 0o31
    _bytes = 1
    _struct_code = "b"
    _minimum_value = -128
    _maximum_value = 127
    _type = int


class ItemI2(ItemNumber):
    """Representation of signed 2 byte integer SECS data."""

    _sml_type = "I2"
    _hsms_type = 0o32
    _bytes = 2
    _struct_code = "h"
    _minimum_value = -32768
    _maximum_value = 32767
    _type = int


class ItemI4(ItemNumber):
    """Representation of signed 4 byte integer SECS data."""

    _sml_type = "I4"
    _hsms_type = 0o34
    _bytes = 4
    _struct_code = "l"
    _minimum_value = -2147483648
    _maximum_value = 2147483647
    _type = int


class ItemF8(ItemNumber):
    """Representation of 8 byte float SECS data."""

    _sml_type = "F8"
    _hsms_type = 0o40
    _bytes = 8
    _struct_code = "d"
    _minimum_value = -1.79769e+308
    _maximum_value = 1.79769e+308
    _type = float


class ItemF4(ItemNumber):
    """Representation of 4 byte float SECS data."""

    _sml_type = "F4"
    _hsms_type = 0o44
    _bytes = 4
    _struct_code = "f"
    _minimum_value = -3.40282e+38
    _maximum_value = 3.40282e+38
    _type = float


class ItemU8(ItemNumber):
    """Representation of unsigned 8 byte integer SECS data."""

    _sml_type = "U8"
    _hsms_type = 0o50
    _bytes = 8
    _struct_code = "Q"
    _minimum_value = 0
    _maximum_value = 0xFFFFFFFFFFFFFFFF
    _type = int


class ItemU1(ItemNumber):
    """Representation of unsigned 1 byte integer SECS data."""

    _sml_type = "U1"
    _hsms_type = 0o51
    _bytes = 1
    _struct_code = "B"
    _minimum_value = 0
    _maximum_value = 0xFF
    _type = int


class ItemU2(ItemNumber):
    """Representation of unsigned 2 byte integer SECS data."""

    _sml_type = "U2"
    _hsms_type = 0o52
    _bytes = 2
    _struct_code = "H"
    _minimum_value = 0
    _maximum_value = 0xFFFF
    _type = int


class ItemU4(ItemNumber):
    """Representation of unsigned 4 byte integer SECS data."""

    _sml_type = "U4"
    _hsms_type = 0o54
    _bytes = 4
    _struct_code = "L"
    _minimum_value = 0
    _maximum_value = 0xFFFFFFFF
    _type = int
