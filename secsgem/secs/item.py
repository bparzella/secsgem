#####################################################################
# item.py
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
"""Secs data classes."""
from __future__ import annotations

import abc
import re
import typing

from .sml import SMLParser, SMLToken

if typing.TYPE_CHECKING:
    import secsgem.common


class InvalidSmlTypeSpecifierError(Exception):
    """Exception for invalid sml type."""

    def __init__(self, typ: str) -> None:
        """Initialize excpetion."""
        super().__init__(f"Invalid SML type '{typ}' selected")


class InvalidYamlTypeSpecifierError(Exception):
    """Exception for invalid yaml type."""

    def __init__(self, typ: str) -> None:
        """Initialize excpetion."""
        super().__init__(f"Invalid Yaml type '{typ}' selected")


class PacketData:
    """Wrapper for packet data that allows iterating over the data bytes."""

    def __init__(self, data: bytes):
        """Initialize packet data.

        Args:
            data: packet raw data

        """
        self._data = data

    def peek(self) -> int:
        """Get the next packet byte without incrementing the pointer.

        Returns:
            requested data

        """
        return self._data[0]

    def get_one(self) -> int:
        """Get one packet byte.

        Returns:
            single packet byte

        """
        result = self._data[0]

        self._data = self._data[1:]

        return result

    def get(self, length: int = 1) -> bytes:
        """Get the next packet bytes.

        Args:
            length: number of bytes

        Returns:
            requested data

        """
        result = self._data[:length]

        self._data = self._data[length:]

        return result


class _ClassProperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class Item(abc.ABC):
    """SECS item data element."""

    _sml_type = ""
    _hsms_type = -1

    _minimum_value: int | float = -0xFFFFFFFFFFFF
    _maximum_value: int | float = -0xFFFFFFFFFFFF

    _subclasses_by_sml: dict[str, type[Item]] = {}
    _subclasses_by_hsms: dict[int, type[Item]] = {}

    @_ClassProperty
    def minimum_value(self):
        """Get the minimum value of the item."""
        return self._minimum_value

    @_ClassProperty
    def maximum_value(self):
        """Get the maximum value of the item."""
        return self._maximum_value

    def __init__(self, value: typing.Any):
        """Initialize data element.

        Args:
            value: new value for the element

        """
        self._import_inherited()
        self._value = self.validate_value(value)

    def __init_subclass__(cls, **kwargs):
        """Initialize a new sub-class."""
        super().__init_subclass__(**kwargs)

        if cls._sml_type:
            cls._subclasses_by_sml[cls._sml_type.upper()] = cls
            cls._subclasses_by_hsms[cls._hsms_type] = cls

    @staticmethod
    def _import_inherited():
        from . import (  # pylint: disable=cyclic-import,import-outside-toplevel
            item_b,
            item_boolean,
            item_l,
            item_number,
            item_str,
        )

        return (item_l, item_b, item_boolean, item_number, item_str)

    def __repr__(self) -> str:
        """Generate string representation of object."""
        return self.to_sml()

    @classmethod
    def _from_value_float(cls, value: float) -> Item:
        for f_type in ["F4", "F8"]:
            typ = cls._subclasses_by_sml[f_type]
            if typ.minimum_value <= value <= typ.maximum_value:
                return typ(value)

        return cls._subclasses_by_sml["F8"](value)

    @classmethod
    def _from_value_int(cls, value: float) -> Item:
        types = ["U1", "U2", "U4", "U8"] if value >= 0 else ["I1", "I2", "I4", "I8"]
        for f_type in types:
            typ = cls._subclasses_by_sml[f_type]
            if typ.minimum_value <= value <= typ.maximum_value:
                return typ(value)

        return cls._subclasses_by_sml["I8"](value)

    @classmethod
    def from_value(cls, value: typing.Any) -> Item:
        """Create a item object from a python type value.

        Args:
            value: value to create item from

        Returns:
            created item object

        """
        result = None

        if isinstance(value, Item):
            result = value
        elif isinstance(value, list):
            result = cls._subclasses_by_sml["L"](value)
        elif isinstance(value, str):
            result = cls._subclasses_by_sml["A"](value)
        elif isinstance(value, bytes):
            result = cls._subclasses_by_sml["B"](value)
        elif isinstance(value, bool):
            result = cls._subclasses_by_sml["BOOLEAN"](value)
        elif isinstance(value, float):
            result = cls._from_value_float(value)
        elif isinstance(value, int):
            result = cls._from_value_int(value)

        if result:
            return result

        raise ValueError(f"Invalid value '{value}' of type '{type(value)}' in 'Item.from_value'")

    @classmethod
    def from_sml(cls, sml: str | SMLParser) -> Item:
        """Create a new data object from sml text or parser.

        Args:
            sml: sml text or parser

        Returns:
            new data object

        """
        if isinstance(sml, str):
            sml = SMLParser(sml)

        cls._import_inherited()

        if cls is Item:
            return cls._read_sml_token(sml)

        if cls is cls._subclasses_by_sml["L"]:
            return cls(cls._read_items(sml, cls._read_sml_token))

        return cls(cls._read_sml_token(sml))

    @classmethod
    def by_sml_type(cls, typ: str) -> type[Item]:
        """Get an item class by sml type.

        Args:
            typ: type name of the selected type

        Returns:
            item type

        """
        if typ not in cls._subclasses_by_sml:
            raise InvalidSmlTypeSpecifierError(typ)

        return cls._subclasses_by_sml[typ]

    @classmethod
    def by_yaml_type(cls, typ: str) -> type[Item]:
        """Get an item class by yaml type.

        Args:
            typ: type name of the selected type

        Returns:
            item type

        """
        _type_map = {
            "Array": "L",
            "Boolean": "BOOLEAN",
            "U1": "U1",
            "U2": "U2",
            "U4": "U4",
            "U8": "U8",
            "I1": "I1",
            "I2": "I2",
            "I4": "I4",
            "I8": "I8",
            "F4": "F4",
            "F8": "F8",
            "String": "A",
            "Binary": "B",
        }

        if typ not in _type_map:
            raise InvalidYamlTypeSpecifierError(typ)

        return cls.by_sml_type(_type_map[typ])

    def to_sml(self, indent=0) -> str:
        """Convert data object to SML string.

        Args:
            indent: indent level in spaces

        Returns:
            SML text

        """
        if len(self._value) == 0:
            return f"{indent * ' '}< {self._sml_type} >"

        values_string = " ".join([self._format_value(value) for value in self._value])
        return f"{indent * ' '}< {self._sml_type} {values_string} >"

    @property
    def value(self) -> typing.Any:
        """Get the item value."""
        return self._value

    @property
    def to_list(self) -> typing.Any:
        """Generate list based tree of this item (and sub-items)."""
        if isinstance(self._value, list):
            results = []
            if len(self._value) == 1 and not isinstance(self._value[0], Item):
                return self._value[0]

            for value in self._value:
                if isinstance(value, Item):
                    results.append(value.to_list)
                else:
                    results.append(value)

            return results

        return self._value

    @staticmethod
    def _format_value(value: typing.Any) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_value(self, value: typing.Any) -> typing.Any:
        """Validate the input value and return possibly converted value.

        Args:
            value: passed value

        Returns:
            converted value

        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def is_valid(cls, value: typing.Any, length: int | None = None) -> typing.Any:
        """Check if value is valid.

        Args:
            value: value to check
            length: data length if applicable

        Returns:
            True if data is valid

        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _read_sml_token(cls, parser: SMLParser) -> typing.Any:
        return cls._read_item(parser)

    @abc.abstractmethod
    def encode(self) -> bytes:
        """Encode the data value to transmittable bytes.

        Return:
            byte array of data

        """
        raise NotImplementedError

    @classmethod
    def _decode_peek_item_type(cls, data: PacketData):
        return (data.peek() & 0b11111100) >> 2

    @classmethod
    def _decode_item_header(cls, data: PacketData) -> tuple[int, int]:
        # parse format byte
        format_byte = data.get_one()

        format_code = (format_byte & 0b11111100) >> 2
        length_bytes = format_byte & 0b00000011

        # read 1-3 length bytes
        length = 0
        for _ in range(length_bytes):
            length <<= 8
            length += data.get_one()

        return format_code, length

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: PacketData | bytes) -> Item:
        """Create a new data object by decoding a secs packet.

        Args:
            data: packet data

        Returns:
            new data object

        """
        if isinstance(data, bytes):
            data = PacketData(data)

        cls._import_inherited()

        data_type = cls._decode_peek_item_type(data)

        if data_type not in cls._subclasses_by_hsms:
            raise TypeError(f"Unknown data type '{data_type}'")

        return cls._subclasses_by_hsms[data_type].decode(data)

    @classmethod
    def _read_item(cls, parser: SMLParser) -> Item:
        start_char = parser.get_token()

        if start_char.value != "<":
            raise start_char.exception(f"expected open character '<', found '{start_char.value}'")

        data_type = parser.get_token()

        if data_type.value.upper() not in cls._subclasses_by_sml:
            raise data_type.exception(f"unknown data type '{data_type.value}'")

        return cls._subclasses_by_sml[data_type.value.upper()].from_sml(parser)

    @classmethod
    def _read_length(cls, parser: SMLParser):
        length = parser.get_token()

        closing = parser.get_token()
        if closing.value != "]":
            raise closing.exception(f"expected length close ']', got '{closing.value}''")

        return length

    @classmethod
    def _read_items(cls, parser: SMLParser, sub_parser: typing.Callable):
        items = []
        length = None
        count = 0

        if parser.peek_token().value == "[":
            parser.get_token()
            length = cls._read_length(parser)

        while parser.peek_token().value not in ">.":
            items.append(sub_parser(parser))
            count += 1

        parser.get_token()

        if length is not None and 0 < int(length.value) != count:
            raise length.exception(f"expected length ({length.value}) doesn't match counted items ({count})")

        return items

    def encode_item_header(self, length: int) -> bytes:
        """Encode item header depending on the number of length bytes required.

        Args:
            length: number of bytes in data

        Returns:
            encoded item header bytes

        """
        if length < 0:
            raise ValueError(f"Encoding {self.__class__.__name__} not possible, data length too small {length}")
        if length > 0xFFFFFF:
            raise ValueError(f"Encoding {self.__class__.__name__} not possible, data length too big {length}")

        if length > 0xFFFF:
            length_bytes = 3
            format_byte = (self._hsms_type << 2) | length_bytes
            return bytes(
                bytearray((format_byte, (length & 0xFF0000) >> 16, (length & 0x00FF00) >> 8, (length & 0x0000FF)))
            )
        if length > 0xFF:
            length_bytes = 2
            format_byte = (self._hsms_type << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0x00FF00) >> 8, (length & 0x0000FF))))

        length_bytes = 1
        format_byte = (self._hsms_type << 2) | length_bytes
        return bytes(bytearray((format_byte, (length & 0x0000FF))))

    @classmethod
    def _verify_value_in_bounds(cls, value: int | float, item: SMLToken | None = None) -> int | float:
        if cls._minimum_value <= value <= cls._maximum_value:
            return value

        if item is not None:
            raise item.exception(
                f"value '{item.value}' out of bounds for {cls._sml_type} ({cls._minimum_value} - {cls._maximum_value})"
            )

        raise ValueError(
            f"value '{value}' out of bounds for {cls._sml_type} ({cls._minimum_value} - {cls._maximum_value})"
        )

    @classmethod
    def _is_value_in_bounds(cls, value: int | float) -> bool:
        if cls._minimum_value <= value <= cls._maximum_value:
            return True

        return False

    @classmethod
    def _invalid_type_exception(cls, data: typing.Any) -> Exception:
        raise TypeError(f"Invalid value '{data}' of '{data.__class__.__name__}' for '{cls.__name__}'")


# TODO(BP): unifi with data_items.StreamsFunctions / data_items.StreamFunction
class Function:
    """Representation of a secs stream function."""

    stream_function_regex = re.compile(r"^[sS](\d*)[fF](\d*)$")

    def __init__(self, stream: int, function: int, w_bit: bool, data: Item | None, header=None):
        """Initialize a secs stream/function.

        Args:
            stream: stream number
            function: function number
            w_bit: answer request
            data: message data
            header: hsms header data

        """
        self.stream = stream
        self.function = function
        self.w_bit = w_bit
        self.data = data
        self.hsms_header = header

    def __repr__(self):
        """Generate a textual representation of an object."""
        return (
            f"S{self.stream}F{self.function} {'W' if self.w_bit else ''}\n"
            f"{self.data.to_sml(4) if self.data else ''} ."
        )

    @classmethod
    def from_sml(cls, text: str):
        """Create a SECSFunction object from SML text.

        Args:
            text: SML text

        Returns:
            generated SECSFunction

        """
        tokens = SMLParser(text)

        stream_function_token = tokens.get_token()
        stream_function_match = cls.stream_function_regex.match(stream_function_token.value)

        if stream_function_match is None:
            raise stream_function_token.exception(
                f"expected stream function descriptor SxxFyy, found '{stream_function_token}"
            )

        stream = int(stream_function_match.group(1))
        function = int(stream_function_match.group(2))

        w_bit = False
        if tokens.peek_token().value.lower() == "w":
            tokens.get_token()
            w_bit = True

        if tokens.peek_token().value == ".":
            return cls(stream, function, w_bit, None)

        data = Item.from_sml(tokens)

        final_token = tokens.get_token()
        if final_token.value != ".":
            raise final_token.exception(f"expected final character '.', found '{final_token.value}'")

        return cls(stream, function, w_bit, data)

    @classmethod
    def from_message(cls, message: secsgem.common.Message) -> Function:
        """Create a SECSFunction object from a received packet.

        Args:
            message: received message

        Returns:
            generated SECSFunction

        """
        return cls(
            message.header.stream,
            message.header.function,
            message.header.require_response,
            Item.decode(PacketData(message.data)),
            message.header,
        )
