#####################################################################
# boolean.py
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
"""SECS boolean variable type."""

from .base import Base


class Boolean(Base):
    """Secs type for boolean data."""

    format_code = 0o11
    text_code = "BOOLEAN"
    preferred_types = [bool]

    _true_strings = ["TRUE", "YES"]
    _false_strings = ["FALSE", "NO"]

    def __init__(self, value=None, count=-1):
        """Initialize a boolean secs variable.

        :param value: initial value
        :type value: list/boolean
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
        if isinstance(value, bool):
            return True

        if isinstance(value, int):
            return 0 <= value <= 1

        if isinstance(value, str):
            return bool(value.upper() in self._true_strings or value.upper() in self._false_strings)

        return False

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
        if 0 < self.count < len(value):
            return False

        return all(self._check_single_item_support(item) for item in value)

    def _supports_value_bytearray(self, value) -> bool:
        if 0 < self.count < len(value):
            return False

        return all(0 <= char <= 1 for char in value)

    def __convert_single_item(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            if not 0 <= value <= 1:
                raise ValueError(f"Value {value} out of bounds")

            return bool(value)

        if isinstance(value, str):
            if value.upper() in self._true_strings:
                return True

            if value.upper() in self._false_strings:
                return False

            raise ValueError(f"Value {value} out of bounds")

        raise ValueError(f"Can't convert value {value}")

    def set(self, value):
        """Set the internal value to the provided value.

        :param value: new value
        :type value: list/boolean
        """
        if isinstance(value, (list, tuple)):
            if 0 <= self.count < len(value):
                raise ValueError(f"Value longer than {self.count} chars")

            self.value = [self.__convert_single_item(item) for item in value]
        elif isinstance(value, bytearray):
            if 0 <= self.count < len(value):
                raise ValueError(f"Value longer than {self.count} chars")

            new_value = []
            for char in value:
                if not 0 <= char <= 1:
                    raise ValueError(f"Value {char} out of bounds")

                new_value.append(char)

            self.value = new_value
        else:
            self.value = [self.__convert_single_item(value)]

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: list/boolean
        """
        if len(self.value) == 1:
            return self.value[0]

        return self.value

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        for value in self.value:
            if value:
                result += b"\1"
            else:
                result += b"\0"

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

        for _ in range(length):
            if bytearray(data)[text_pos] == 0:
                result.append(False)
            else:
                result.append(True)

            text_pos += 1

        self.set(result)

        return text_pos
