#####################################################################
# base.py
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
"""SECS variable base type."""


class Base:
    """
    Base class for SECS variables.

    Due to the python types, wrapper classes for variables are required.
    If constructor is called with Base or subclass only the value is copied.
    """

    format_code = -1

    def __init__(self):
        """Initialize a secs variable."""
        self.value = None

    def set(self, value):
        """
        Set the internal value to the provided value.

        :param value: new value
        :type value: various
        """
        raise NotImplementedError("Function set not implemented on " + self.__class__.__name__)

    def encode_item_header(self, length):
        """
        Encode item header depending on the number of length bytes required.

        :param length: number of bytes in data
        :type length: integer
        :returns: encoded item header bytes
        :rtype: string
        """
        if length < 0:
            raise ValueError("Encoding {} not possible, data length too small {}"
                             .format(self.__class__.__name__, length))
        if length > 0xFFFFFF:
            raise ValueError("Encoding {} not possible, data length too big {}"
                             .format(self.__class__.__name__, length))

        if length > 0xFFFF:
            length_bytes = 3
            format_byte = (self.format_code << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0xFF0000) >> 16, (length & 0x00FF00) >> 8,
                                    (length & 0x0000FF))))
        if length > 0xFF:
            length_bytes = 2
            format_byte = (self.format_code << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0x00FF00) >> 8, (length & 0x0000FF))))

        length_bytes = 1
        format_byte = (self.format_code << 2) | length_bytes
        return bytes(bytearray((format_byte, (length & 0x0000FF))))

    def decode_item_header(self, data, text_pos=0):
        """
        Encode item header depending on the number of length bytes required.

        :param data: encoded data
        :type data: string
        :param text_pos: start of item header in data
        :type text_pos: integer
        :returns: start position for next item, format code, length item of data
        :rtype: (integer, integer, integer)
        """
        if len(data) == 0:
            raise ValueError("Decoding for {} without any text".format(self.__class__.__name__))

        # parse format byte
        format_byte = bytearray(data)[text_pos]

        format_code = (format_byte & 0b11111100) >> 2
        length_bytes = (format_byte & 0b00000011)

        text_pos += 1

        # read 1-3 length bytes
        length = 0
        for _ in range(length_bytes):
            length <<= 8
            length += bytearray(data)[text_pos]

            text_pos += 1

        if 0 <= self.format_code != format_code:
            raise ValueError("Decoding data for {} ({}) has invalid format {}"
                             .format(self.__class__.__name__, self.format_code, format_code))

        return text_pos, format_code, length

    @property
    def is_dynamic(self) -> bool:
        """Check if this instance is Dynamic or derived."""
        return False
