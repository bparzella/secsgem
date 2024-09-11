#####################################################################
# array.py
#
# (c) Copyright 2021-2023, Benjamin Parzella. All rights reserved.
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
"""SECS array variable type."""

import secsgem.common

from .base import Base
from .list_type import List


class Array(Base):
    """List variable type. List with items of same type."""

    format_code = 0
    text_code = "L"
    preferred_types = [list]

    class _SecsVarArrayIter:
        def __init__(self, values):
            self._values = values
            self._counter = 0

        def __iter__(self):
            """Get an iterator."""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list."""
            if self._counter < len(self._values):
                i = self._counter
                self._counter += 1
                return self._values[i]

            raise StopIteration

    def __init__(self, data_format, value=None, count=-1):
        """Initialize a secs array variable.

        :param data_format: internal data definition/sample
        :type data_format: :class:`secs.variables.Base`
        :param value: initial value
        :type value: list
        :param count: number of fields in the list
        :type count: integer
        """
        super().__init__()

        self.item_decriptor = data_format
        self.count = count
        self.data = []
        if isinstance(data_format, list):
            self.name = List.get_name_from_format(data_format)
        elif hasattr(data_format, "__name__"):
            self.name = data_format.__name__
        else:
            self.name = "UNKNOWN"

        if value is not None:
            self.set(value)

    @staticmethod
    def get_format(data_format, showname=False):
        """Get the format of the variable.

        :returns: returns the string representation of the function
        :rtype: string
        """
        if showname:
            array_name = "{}: "
            if isinstance(data_format, list):
                array_name = array_name.format(List.get_name_from_format(data_format))
            else:
                array_name = array_name.format(data_format.__name__)
        else:
            array_name = ""

        if isinstance(data_format, list):
            return f"{array_name}[\n" f"{secsgem.common.indent_block(List.get_format(data_format), 4)}\n" f"    ...\n]"

        return (
            f"{array_name}[\n" f"{secsgem.common.indent_block(data_format.get_format(not showname), 4)}\n" f"    ...\n]"
        )

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.data) == 0:
            return f"<{self.text_code}>"

        data = ""

        for value in self.data:
            data += f"{secsgem.common.indent_block(value.__repr__())}\n"

        return f"<{self.text_code} [{len(self.data)}]\n{data}\n>"

    def __len__(self):
        """Get the length."""
        return len(self.data)

    def __getitem__(self, key):
        """Get an item using the indexer operator."""
        return self.data[key]

    def __iter__(self):
        """Get an iterator."""
        return Array._SecsVarArrayIter(self.data)

    def __setitem__(self, key, value):
        """Set an item using the indexer operator."""
        if isinstance(value, (type(self.data[key]), self.data[key].__class__.__bases__)):
            self.data[key] = value
        elif isinstance(value, Base):
            raise TypeError(f"Wrong type {value.__class__.__name__} when expecting {self.data[key].__class__.__name__}")
        else:
            self.data[key].set(value)

    def append(self, data):
        """Append data to the internal list.

        :param value: new value
        :type value: various
        """
        from .functions import generate  # pylint: disable=import-outside-toplevel,cyclic-import

        new_object = generate(self.item_decriptor)
        new_object.set(data)
        self.data.append(new_object)

    def set(self, value):
        """Set the internal value to the provided value.

        :param value: new value
        :type value: list
        """
        if not isinstance(value, list):
            raise TypeError(f"Invalid value type {type(value).__name__} for {self.__class__.__name__}")

        if self.count >= 0 and not len(value) == self.count:
            raise ValueError(f"Value has invalid field count (expected: {self.count}, actual: {len(value)})")

        self.data = []

        for item in value:
            from .functions import generate  # pylint: disable=import-outside-toplevel,cyclic-import

            new_object = generate(self.item_decriptor)
            new_object.set(item)
            self.data.append(new_object)

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: list
        """
        return [item.get() for item in self.data]

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for item in self.data:
            result += item.encode()

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
        from .functions import generate  # pylint: disable=import-outside-toplevel,cyclic-import

        (text_pos, _, length) = self.decode_item_header(data, start)

        # list
        self.data = []

        for _ in range(length):
            new_object = generate(self.item_decriptor)
            text_pos = new_object.decode(data, text_pos)
            self.data.append(new_object)

        return text_pos
