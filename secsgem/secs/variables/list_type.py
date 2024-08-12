#####################################################################
# list_type.py
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
"""SECS list variable type."""

from collections import OrderedDict

import secsgem.common

from .base import Base


class List(Base):
    """List variable type. List with items of different types."""

    format_code = 0
    text_code = "L"
    preferred_types = [dict]

    class _SecsVarListIter:
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):
            """Get an iterator."""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list."""
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]

            raise StopIteration

    def __init__(self, data_format, value=None):
        """Initialize a secs list variable.

        :param data_format: internal data values
        :type data_format: OrderedDict
        :param value: initial value
        :type value: dict/list
        :param count: number of fields in the list
        :type count: integer
        """
        super().__init__()

        self.name = "DATA"

        self.data = self._generate(data_format)

        if value is not None:
            self.set(value)

        self._object_intitialized = True

    @staticmethod
    def get_format(data_format, showname=False):
        """Get the format of the variable.

        :returns: returns the string representation of the function
        :rtype: string
        """
        from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import

        array_name = f"{List.get_name_from_format(data_format)}: " if showname else ""

        if isinstance(data_format, list):
            items = []
            for item in data_format:
                if isinstance(item, str):
                    continue
                if isinstance(item, list):
                    if len(item) == 1:
                        items.append(secsgem.common.indent_block(Array.get_format(item[0], True), 4))
                    else:
                        items.append(secsgem.common.indent_block(List.get_format(item, True), 4))
                else:
                    items.append(secsgem.common.indent_block(item.get_format(), 4))
            return array_name + "{\n" + "\n".join(items) + "\n}"
        return None

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.data) == 0:
            return f"<{self.text_code}>"

        data = ""

        for field_name in self.data:
            data += f"{secsgem.common.indent_block(self.data[field_name].__repr__())}\n"

        return f"<{self.text_code} [{len(self.data)}]\n{data}\n>"

    def __len__(self):
        """Get the length."""
        return len(self.data)

    def __getitem__(self, index):
        """Get an item using the indexer operator."""
        if isinstance(index, int):
            return self.data[list(self.data.keys())[index]]
        return self.data[index]

    def __iter__(self):
        """Get an iterator."""
        return List._SecsVarListIter(self.data.keys())

    def __setitem__(self, index, value):
        """Set an item using the indexer operator."""
        if isinstance(index, int):
            index = list(self.data.keys())[index]

        if isinstance(value, (type(self.data[index]), self.data[index].__class__.__bases__)):
            self.data[index] = value
        elif isinstance(value, Base):
            raise TypeError(
                f"Wrong type {value.__class__.__name__} when expecting {self.data[index].__class__.__name__}")
        else:
            self.data[index].set(value)

    def _generate(self, data_format):
        from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import
        from .functions import generate  # pylint: disable=import-outside-toplevel,cyclic-import

        if data_format is None:
            return None

        result_data = OrderedDict()
        for item in data_format:
            if isinstance(item, str):
                self.name = item
                continue

            item_value = generate(item)
            if isinstance(item_value, Array):
                result_data[item_value.name] = item_value
            elif isinstance(item_value, List):
                result_data[List.get_name_from_format(item)] = item_value
            elif isinstance(item_value, Base):
                result_data[item_value.name] = item_value
            else:
                raise TypeError(f"Can't handle item of class {data_format.__class__.__name__}")

        return result_data

    def __getattr__(self, item):
        """Get an item as member of the object."""
        try:
            return self.data.__getitem__(item)
        except KeyError as exc:
            raise AttributeError(item) from exc

    def __setattr__(self, item, value):
        """Set an item as member of the object."""
        if "_object_intitialized" not in self.__dict__:
            dict.__setattr__(self, item, value)
            return

        if item in self.data:
            if isinstance(value, (type(self.data[item]), self.data[item].__class__.__bases__)):
                self.data[item] = value
            elif isinstance(value, Base):
                raise TypeError(
                    f"Wrong type {value.__class__.__name__} when expecting {self.data[item].__class__.__name__}")
            else:
                self.data[item].set(value)
        else:
            self.__dict__.__setattr__(item, value)

    @staticmethod
    def get_name_from_format(data_format):
        """Generate a name for the passed data_format.

        :param data_format: data_format to get name for
        :type data_format: list/Base based class
        :returns: name for data_format
        :rtype: str
        """
        if not isinstance(data_format, list):
            raise TypeError(f"Can't generate item name of class {data_format.__class__.__name__}")

        if isinstance(data_format[0], str):
            return data_format[0]

        return "DATA"

    def set(self, value):
        """Set the internal value to the provided value.

        :param value: new value
        :type value: dict/list
        """
        if isinstance(value, dict):
            for field_name in value:
                self.data[field_name].set(value[field_name])
        elif isinstance(value, list):
            if len(value) > len(self.data):
                raise ValueError(f"Value has invalid field count (expected: {len(self.data)}, actual: {len(value)})")

            for counter, itemvalue in enumerate(value):
                self.data[list(self.data.keys())[counter]].set(itemvalue)
        else:
            raise TypeError(f"Invalid value type {type(value).__name__} for {self.__class__.__name__}")

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: list
        """
        data = {}
        for field_name in self.data:
            data[field_name] = self.data[field_name].get()

        return data

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for field_name in self.data:
            result += self.data[field_name].encode()

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

        # list
        for i in range(length):
            field_name = list(self.data.keys())[i]
            text_pos = self.data[field_name].decode(data, text_pos)

        return text_pos
