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
        """
        Initialize a boolean secs variable.

        :param value: initial value
        :type value: list/boolean
        :param count: number of items this value
        :type count: integer
        """
        super(Boolean, self).__init__()

        self.value = []
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.value) == 0:
            return "<{}>".format(self.text_code)

        data = ""

        for boolean in self.value:
            data += "{} ".format(boolean)

        return "<{} {}>".format(self.text_code, data)

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

    def __check_single_item_support(self, value):
        if isinstance(value, bool):
            return True

        if isinstance(value, int):
            if 0 <= value <= 1:
                return True
            return False

        if isinstance(value, str):
            if value.upper() in self._true_strings or value.upper() in self._false_strings:
                return True

            return False

        return False

    def supports_value(self, value):
        """
        Check if the current instance supports the provided value.

        :param value: value to test
        :type value: any
        """
        if isinstance(value, (list, tuple)):
            if 0 < self.count < len(value):
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True

        if isinstance(value, bytearray):
            if 0 < self.count < len(value):
                return False
            for char in value:
                if not 0 <= char <= 1:
                    return False
            return True

        return self.__check_single_item_support(value)

    def __convert_single_item(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            if not 0 <= value <= 1:
                raise ValueError("Value {} out of bounds".format(value))

            return bool(value)

        if isinstance(value, str):
            if value.upper() in self._true_strings:
                return True

            if value.upper() in self._false_strings:
                return False

            raise ValueError("Value {} out of bounds".format(value))

        raise ValueError("Can't convert value {}".format(value))

    def set(self, value):
        """
        Set the internal value to the provided value.

        :param value: new value
        :type value: list/boolean
        """
        if isinstance(value, (list, tuple)):
            if 0 <= self.count < len(value):
                raise ValueError("Value longer than {} chars".format(self.count))

            new_value = []
            for item in value:
                new_value.append(self.__convert_single_item(item))

            self.value = new_value
        elif isinstance(value, bytearray):
            if 0 <= self.count < len(value):
                raise ValueError("Value longer than {} chars".format(self.count))

            new_value = []
            for char in value:
                if not 0 <= char <= 1:
                    raise ValueError("Value {} out of bounds".format(char))

                new_value.append(char)

            self.value = new_value
        else:
            self.value = [self.__convert_single_item(value)]

    def get(self):
        """
        Return the internal value.

        :returns: internal value
        :rtype: list/boolean
        """
        if len(self.value) == 1:
            return self.value[0]

        return self.value

    def encode(self):
        """
        Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            if value:
                result += b"\1"
            else:
                result += b"\0"

        return result

    def decode(self, data, start=0):
        """
        Decode the secs byte data to the value.

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