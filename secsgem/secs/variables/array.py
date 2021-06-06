#####################################################################
# array.py
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
"""SECS array variable type."""

from . import list_type  # pylint: disable=cyclic-import
from . import functions  # pylint: disable=cyclic-import

from .base import Base

from ...common import indent_block


class Array(Base):
    """List variable type. List with items of same type."""

    format_code = 0
    text_code = 'L'
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

            raise StopIteration()

    def __init__(self, data_format, value=None, count=-1):
        """
        Initialize a secs array variable.

        :param data_format: internal data definition/sample
        :type data_format: :class:`secs.variables.Base`
        :param value: initial value
        :type value: list
        :param count: number of fields in the list
        :type count: integer
        """
        super(Array, self).__init__()

        self.item_decriptor = data_format
        self.count = count
        self.data = []
        if isinstance(data_format, list):
            self.name = list_type.List.get_name_from_format(data_format)
        elif hasattr(data_format, "__name__"):
            self.name = data_format.__name__
        else:
            self.name = "UNKNOWN"

        if value is not None:
            self.set(value)

    @staticmethod
    def get_format(data_format, showname=False):
        """
        Gets the format of the variable.

        :returns: returns the string representation of the function
        :rtype: string
        """
        if showname:
            arrayName = "{}: "
            if isinstance(data_format, list):
                arrayName = arrayName.format(list_type.List.get_name_from_format(data_format))
            else:
                arrayName = arrayName.format(data_format.__name__)
        else:
            arrayName = ""

        if isinstance(data_format, list):
            return "{}[\n{}\n    ...\n]".format(arrayName,
                                                indent_block(list_type.List.get_format(data_format), 4))

        return "{}[\n{}\n    ...\n]".format(arrayName, indent_block(data_format.get_format(not showname), 4))

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.data) == 0:
            return "<{}>".format(self.text_code)

        data = ""

        for value in self.data:
            data += "{}\n".format(indent_block(value.__repr__()))

        return "<{} [{}]\n{}\n>".format(self.text_code, len(self.data), data)

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
            raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__,
                                                                     self.data[key].__class__.__name__))
        else:
            self.data[key].set(value)

    def append(self, data):
        """
        Append data to the internal list.

        :param value: new value
        :type value: various
        """
        new_object = functions.generate(self.item_decriptor)
        new_object.set(data)
        self.data.append(new_object)

    def set(self, value):
        """
        Set the internal value to the provided value.

        :param value: new value
        :type value: list
        """
        if not isinstance(value, list):
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if self.count >= 0:
            if not len(value) == self.count:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})"
                                 .format(self.count, len(value)))

        self.data = []

        for item in value:
            new_object = functions.generate(self.item_decriptor)
            new_object.set(item)
            self.data.append(new_object)

    def get(self):
        """
        Return the internal value.

        :returns: internal value
        :rtype: list
        """
        data = []
        for item in self.data:
            data.append(item.get())

        return data

    def encode(self):
        """
        Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for item in self.data:
            result += item.encode()

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

        # list
        self.data = []

        for _ in range(length):
            new_object = functions.generate(self.item_decriptor)
            text_pos = new_object.decode(data, text_pos)
            self.data.append(new_object)

        return text_pos
