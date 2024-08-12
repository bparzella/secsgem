#####################################################################
# base_number.py
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
"""SECS numeric variable base type."""
from __future__ import annotations

import struct

from .base import Base


class BaseNumber(Base):
    """Secs base type for numeric data."""

    format_code = 0
    text_code = ""
    _base_type: type[int] | type[float] = int
    _min: int | float = 0
    _max: int | float = 0
    _bytes = 0
    _struct_code = ""

    def __init__(self, value=None, count=-1):
        """Initialize a numeric secs variable.

        :param value: initial value
        :type value: list/integer/float
        :param count: number of items this value
        :type count: integer
        """
        super().__init__()

        self.value = []
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.value) == 0:
            return f"<{self.text_code}>"

        data = " ".join([str(value) for value in self.value])

        return f"<{self.text_code} {data} >"

    def __len__(self):
        """Get the length."""
        return len(self.value)

    def __getitem__(self, key):
        """Get an item using the indexer operator."""
        return self.value[key]

    def __setitem__(self, key, item):
        """Set an item using the indexer operator."""
        self.value[key] = item

    def __eq__(self, other):
        """Check equality with other object."""
        if isinstance(other, Base):
            if other.is_dynamic:
                return other.value.value == self.value
            return other.value == self.value
        if isinstance(other, list):
            return other == self.value
        return [other] == self.value

    def __hash__(self):
        """Get data item for hashing."""
        return hash(str(self.value))

    def _check_single_item_support(self, value):
        if isinstance(value, float) and self._base_type is int:
            return False

        if isinstance(value, bool):
            return True

        if isinstance(value, (int, float)):
            return not (value < self._min or value > self._max)

        if isinstance(value, (bytes, str)):
            return self._check_single_item_support_str(value)

        return False

    def _check_single_item_support_str(self, value) -> bool:
        try:
            val = self._base_type(value)
        except ValueError:
            return False
        return not (val < self._min or val > self._max)

    def supports_value(self, value) -> bool:
        """Check if the current instance supports the provided value.

        :param value: value to test
        :type value: any
        """
        if isinstance(value, (list, tuple)):
            return self._supports_value_list(value)
        if isinstance(value, bytearray):
            return self._supports_value_bytearray(value)
        return self._check_single_item_support(value)

    def _supports_value_list(self, value) -> bool:
        if 0 <= self.count < len(value):
            return False
        return all(self._check_single_item_support(item) for item in value)

    def _supports_value_bytearray(self, value) -> bool:
        if 0 <= self.count < len(value):
            return False
        return all(not (item < self._min or item > self._max) for item in value)

    def set(self, value):
        """Set the internal value to the provided value.

        :param value: new value
        :type value: list/integer/float
        """
        if isinstance(value, float) and self._base_type is int:
            raise ValueError(f"Invalid value {value}")

        if isinstance(value, (list, tuple)):
            self._set_list(value)
        elif isinstance(value, bytearray):
            self._set_bytearray(value)
        else:
            new_value = self._base_type(value)

            if new_value < self._min or new_value > self._max:
                raise ValueError(f"Invalid value {value}")

            self.value = [new_value]

    def _set_list(self, value):
        if 0 <= self.count < len(value):
            raise ValueError(f"Value longer than {self.count} chars")

        new_list = []
        for item in value:
            item = self._base_type(item)
            if item < self._min or item > self._max:
                raise ValueError(f"Invalid value {item}")

            new_list.append(item)
        self.value = new_list

    def _set_bytearray(self, value):
        if 0 <= self.count < len(value):
            raise ValueError(f"Value longer than {self.count} chars")

        new_list = []
        for item in value:
            if item < self._min or item > self._max:
                raise ValueError(f"Invalid value {item}")
            new_list.append(item)
        self.value = new_list

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: list/integer/float
        """
        if len(self.value) == 1:
            return self.value[0]

        return self.value

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * self._bytes)

        for value in self.value:
            result += struct.pack(f">{self._struct_code}", value)

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value.

        :param data: encoded data bytes
        :type data: string
        :param start: start position of value the data
        :type start: integer
        :returns: new start position
        :rtype: integer
        """
        (text_pos, _, length) = self.decode_item_header(data, start)

        result = []

        for _ in range(length // self._bytes):
            result_text = data[text_pos:text_pos + self._bytes]

            if len(result_text) != self._bytes:
                raise ValueError(
                    f"No enough data found for {self.__class__.__name__} with length {length} at position {start} ")

            result.append(struct.unpack(f">{self._struct_code}", result_text)[0])

            text_pos += self._bytes

        self.set(result)

        return text_pos
