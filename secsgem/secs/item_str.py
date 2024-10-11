#####################################################################
# item_str.py
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
"""String SECS data."""

from __future__ import annotations

import string
import typing

from .item import Item, PacketData

if typing.TYPE_CHECKING:
    from .sml import SMLParser


class ItemStr(Item):
    """SECS string data type wrapper."""

    _minimum_value = 0
    _maximum_value = 0xFF

    _encoding = ""

    printable_chars = string.printable.replace("\n", "").replace("\r", "")

    def validate_value(self, value: str | bytes) -> str:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        if not isinstance(value, (str, bytes)):
            raise ValueError(f"Value type {type(value)} not allowed, only 'str' or 'bytes'")

        if isinstance(value, bytes):
            return value.decode(self._encoding)

        return value

    @classmethod
    def is_valid(cls, value: typing.Any, length: int | None = None) -> bool:
        """Check if value is valid.

        Args:
            value: value to check
            length: data length if applicable

        Returns:
            True if data is valid

        """
        if isinstance(value, (str, bytes)):
            return not (length is not None and len(value) > length)

        return bool(isinstance(value, cls))

    @classmethod
    def _char_coder(cls, char: int) -> bytes:
        raise NotImplementedError

    @classmethod
    def _read_sml_token(cls, parser: SMLParser) -> bytes:
        data = b""

        while parser.peek_token().value != ">":
            item = parser.get_token()

            if item.value.startswith('"'):
                data += item.value.strip('"').encode(cls._encoding)
            else:
                char = int(item.value, 0)
                char = int(cls._verify_value_in_bounds(char, item))
                data += cls._char_coder(char)

        parser.get_token()

        return data

    def to_sml(self, indent=0):
        """Convert data object to SML string.

        Args:
            indent: indent level in spaces

        Returns:
            SML text

        """
        data = ""
        last_char_printable = False

        for char in self._value:
            output = char
            if char in self.printable_chars:
                if last_char_printable:
                    data += output
                else:
                    data += ' "' + output
                last_char_printable = True
            else:
                if last_char_printable:
                    data += '" ' + hex(ord(output))
                else:
                    data += " " + hex(ord(output))
                last_char_printable = False

        if last_char_printable:
            data += '"'

        return f"{indent * ' '}< {self._sml_type}{data}>"

    def encode(self) -> bytes:
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        result = self.encode_item_header(len(self._value))

        result += self._value.encode(self._encoding)

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

        return cls(data.get(length))


class ItemJ(ItemStr):
    """SECS jis8 string data type wrapper."""

    _sml_type = "J"
    _hsms_type = 0o21
    _encoding = "jis_8"

    @classmethod
    def _char_coder(cls, char: int) -> bytes:
        return bytes([char])

    _minimum_value = 0
    _maximum_value = 0xFF

    printable_chars = string.printable.replace("\n", "").replace("\r", "")


class ItemA(ItemStr):
    r"""SECS latin1 string data type wrapper.

    Example:
        >>> from secsgem.secs.items import ItemA, Item
        >>>
        >>> ItemA("Hello World")
        < A "Hello World">
        >>> ItemA("Hello \0 World")
        < A "Hello " 0x0 " World">
        >>>
        >>> ItemA.is_valid("Hello World")
        True
        >>> ItemA.is_valid(10)
        False
        >>>
        >>> ItemA("Hello World").encode()
        b'A\x0bHello World'
        >>> ItemA.decode(b'A\x0bHello World')
        < A "Hello World">
        >>>
        >>> Item.from_sml('< A "Hello World">')
        < A "Hello World">

    """

    _sml_type = "A"
    _hsms_type = 0o20
    _encoding = "latin1"

    @classmethod
    def _char_coder(cls, char: int) -> bytes:
        return char.to_bytes(1, "big")

    _minimum_value = 0
    _maximum_value = 0xFF

    printable_chars = string.printable.replace("\n", "").replace("\r", "")
