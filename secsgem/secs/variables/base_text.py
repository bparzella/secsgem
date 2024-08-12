#####################################################################
# base_text.py
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
"""SECS string variable base type."""

import unicodedata

from .base import Base


class BaseText(Base):
    """Secs type base for any text data."""

    format_code = -1
    text_code = ""
    control_chars = "".join(chr(ch) for ch in range(256) if unicodedata.category(chr(ch))[0] == "C")
    coding = ""

    def __init__(self, value="", count=-1):
        """Initialize a secs text variable.

        :param value: initial value
        :type value: string
        :param count: number of items this value
        :type count: integer
        """
        super().__init__()

        self.value = ""
        self.count = count

        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.value) == 0:
            return f"<{self.text_code}>"

        data = ""
        last_char_printable = False

        for char in self.value:
            output = char

            if char not in self.control_chars:
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

        return f"<{self.text_code}{data}>"

    def __len__(self):
        """Get the length."""
        return len(self.value)

    def __eq__(self, other):
        """Check equality with other object."""
        if isinstance(other, Base):
            if other.is_dynamic:
                return other.value.value == self.value
            return other.value == self.value

        return other == self.value

    def __hash__(self):
        """Get data item for hashing."""
        return hash(self.value)

    @staticmethod
    def _check_single_item_support(value):
        if isinstance(value, bool):
            return True

        if isinstance(value, int):
            return 0 <= value <= 255

        return False

    def supports_value(self, value) -> bool:
        """Check if the current instance supports the provided value.

        :param value: value to test
        :type value: any
        """
        if isinstance(value, (list, tuple, bytearray)):
            return self._supports_value_list(value)

        if isinstance(value, bytes):
            return self._supports_value_bytes(value)

        if isinstance(value, (int, float, complex)):
            return self._supports_value_number(value)

        if isinstance(value, str):
            return self._supports_value_str(value)

        return False

    def _supports_value_list(self, value) -> bool:
        if self.count > 0 and len(value) > self.count:
            return False

        return all(self._check_single_item_support(item) for item in value)

    def _supports_value_bytes(self, value) -> bool:
        return not 0 < self.count < len(value)

    def _supports_value_number(self, value) -> bool:
        return not 0 < self.count < len(str(value))

    def _supports_value_str(self, value) -> bool:
        if 0 < self.count < len(value):
            return False
        try:
            value.encode(self.coding)
        except UnicodeEncodeError:
            return False

        return True

    def set(self, value):
        """Set the internal value to the provided value.

        :param value: new value
        :type value: string/integer
        """
        if value is None:
            raise ValueError(f"{self.__class__.__name__} can't be None")

        if isinstance(value, bytes):
            value = value.decode(self.coding)
        elif isinstance(value, bytearray):
            value = bytes(value).decode(self.coding)
        elif isinstance(value, (list, tuple)):
            value = str(bytes(bytearray(value)).decode(self.coding))
        elif isinstance(value, (int, float, complex)):
            value = str(value)
        elif isinstance(value, str):
            value.encode(self.coding)  # try if it can be encoded as ascii (values 0-127)
        else:
            raise TypeError(f"Unsupported type {type(value).__name__} for {self.__class__.__name__}")

        if 0 < self.count < len(value):
            raise ValueError(f"Value longer than {self.count} chars ({len(value)} chars)")

        self.value = str(value)

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: string
        """
        return self.value

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        result += self.value.encode(self.coding)

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

        # string
        result = ""

        if length > 0:
            result = data[text_pos:text_pos + length].decode(self.coding)

        self.set(result)

        return text_pos + length
