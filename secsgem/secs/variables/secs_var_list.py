#####################################################################
# secs_var_list.py
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
"""SECS list variable types."""

from collections import OrderedDict
import inspect

from .secs_var import SecsVar

from ...common import indent_block


class SecsVarList(SecsVar):
    """List variable type. List with items of different types."""

    format_code = 0
    text_code = 'L'
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

            raise StopIteration()

    def __init__(self, data_format, value=None):
        """
        Initialize a secs list variable.

        :param data_format: internal data values
        :type data_format: OrderedDict
        :param value: initial value
        :type value: dict/list
        :param count: number of fields in the list
        :type count: integer
        """
        super(SecsVarList, self).__init__()

        self.name = "DATA"

        self.data = self._generate(data_format)

        if value is not None:
            self.set(value)

        self._object_intitialized = True

    @staticmethod
    def get_format(data_format, showname=False):
        """
        Gets the format of the variable.

        :returns: returns the string representation of the function
        :rtype: string
        """
        if showname:
            arrayName = "{}: ".format(SecsVarList.get_name_from_format(data_format))
        else:
            arrayName = ""

        if isinstance(data_format, list):
            items = []
            for item in data_format:
                if isinstance(item, str):
                    continue
                if isinstance(item, list):
                    if len(item) == 1:
                        items.append(indent_block(SecsVarArray.get_format(item[0], True), 4))
                    else:
                        items.append(indent_block(SecsVarList.get_format(item, True), 4))
                else:
                    items.append(indent_block(item.get_format(), 4))
            return arrayName + "{\n" + "\n".join(items) + "\n}"
        return None

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        if len(self.data) == 0:
            return "<{}>".format(self.text_code)

        data = ""

        for field_name in self.data:
            data += "{}\n".format(indent_block(self.data[field_name].__repr__()))

        return "<{} [{}]\n{}\n>".format(self.text_code, len(self.data), data)

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
        return SecsVarList._SecsVarListIter(self.data.keys())

    def __setitem__(self, index, value):
        """Set an item using the indexer operator."""
        if isinstance(index, int):
            index = list(self.data.keys())[index]

        if isinstance(value, (type(self.data[index]), self.data[index].__class__.__bases__)):
            self.data[index] = value
        elif isinstance(value, SecsVar):
            raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__,
                                                                     self.data[index].__class__.__name__))
        else:
            self.data[index].set(value)

    def _generate(self, data_format):
        if data_format is None:
            return None

        result_data = OrderedDict()
        for item in data_format:
            if isinstance(item, str):
                self.name = item
                continue

            item_value = generate(item)
            if isinstance(item_value, SecsVarArray):
                result_data[item_value.name] = item_value
            elif isinstance(item_value, SecsVarList):
                result_data[SecsVarList.get_name_from_format(item)] = item_value
            elif isinstance(item_value, SecsVar):
                result_data[item_value.name] = item_value
            else:
                raise TypeError("Can't handle item of class {}".format(data_format.__class__.__name__))

        return result_data

    def __getattr__(self, item):
        """Get an item as member of the object."""
        try:
            return self.data.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Set an item as member of the object."""
        if '_object_intitialized' not in self.__dict__:
            dict.__setattr__(self, item, value)
            return

        if item in self.data:
            if isinstance(value, (type(self.data[item]), self.data[item].__class__.__bases__)):
                self.data[item] = value
            elif isinstance(value, SecsVar):
                raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__,
                                                                         self.data[item].__class__.__name__))
            else:
                self.data[item].set(value)
        else:
            self.__dict__.__setattr__(item, value)

    @staticmethod
    def get_name_from_format(data_format):
        """
        Generates a name for the passed data_format.

        :param data_format: data_format to get name for
        :type data_format: list/SecsVar based class
        :returns: name for data_format
        :rtype: str
        """
        if not isinstance(data_format, list):
            raise TypeError("Can't generate item name of class {}".format(data_format.__class__.__name__))

        if isinstance(data_format[0], str):
            return data_format[0]

        return "DATA"

    def set(self, value):
        """
        Set the internal value to the provided value.

        :param value: new value
        :type value: dict/list
        """
        if isinstance(value, dict):
            for field_name in value:
                self.data[field_name].set(value[field_name])
        elif isinstance(value, list):
            if len(value) > len(self.data):
                raise ValueError("Value has invalid field count (expected: {}, actual: {})"
                                 .format(len(self.data), len(value)))

            counter = 0
            for itemvalue in value:
                self.data[list(self.data.keys())[counter]].set(itemvalue)
                counter += 1
        else:
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

    def get(self):
        """
        Return the internal value.

        :returns: internal value
        :rtype: list
        """
        data = {}
        for field_name in self.data:
            data[field_name] = self.data[field_name].get()

        return data

    def encode(self):
        """
        Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for field_name in self.data:
            result += self.data[field_name].encode()

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
        for i in range(length):
            field_name = list(self.data.keys())[i]
            text_pos = self.data[field_name].decode(data, text_pos)

        return text_pos


class SecsVarArray(SecsVar):
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
        :type data_format: :class:`secs.variables.SecsVar`
        :param value: initial value
        :type value: list
        :param count: number of fields in the list
        :type count: integer
        """
        super(SecsVarArray, self).__init__()

        self.item_decriptor = data_format
        self.count = count
        self.data = []
        if isinstance(data_format, list):
            self.name = SecsVarList.get_name_from_format(data_format)
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
                arrayName = arrayName.format(SecsVarList.get_name_from_format(data_format))
            else:
                arrayName = arrayName.format(data_format.__name__)
        else:
            arrayName = ""

        if isinstance(data_format, list):
            return "{}[\n{}\n    ...\n]".format(arrayName, indent_block(SecsVarList.get_format(data_format), 4))

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
        return SecsVarArray._SecsVarArrayIter(self.data)

    def __setitem__(self, key, value):
        """Set an item using the indexer operator."""
        if isinstance(value, (type(self.data[key]), self.data[key].__class__.__bases__)):
            self.data[key] = value
        elif isinstance(value, SecsVar):
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
        new_object = generate(self.item_decriptor)
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
            new_object = generate(self.item_decriptor)
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
            new_object = generate(self.item_decriptor)
            text_pos = new_object.decode(data, text_pos)
            self.data.append(new_object)

        return text_pos


def generate(data_format):
    """
    Generate actual variable from data format.

    :param data_format: data format to create variable for
    :type data_format: list/SecsVar based class
    :returns: created variable
    :rtype: SecsVar based class
    """
    if data_format is None:
        return None

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return SecsVarArray(data_format[0])
        return SecsVarList(data_format)
    if inspect.isclass(data_format):
        if issubclass(data_format, SecsVar):
            return data_format()
        raise TypeError("Can't generate item of class {}".format(data_format.__name__))
    raise TypeError("Can't handle item of class {}".format(data_format.__class__.__name__))


def get_format(data_format, showname=False):
    """
    Gets the format of the function.

    :returns: returns the string representation of the function
    :rtype: string
    """
    del showname  # unused variable
    if data_format is None:
        return None

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return SecsVarArray.get_format(data_format[0])
        return SecsVarList.get_format(data_format)

    if inspect.isclass(data_format):
        if issubclass(data_format, SecsVar):
            return data_format.get_format()
        raise TypeError("Can't generate data_format for class {}".format(data_format.__name__))

    raise TypeError("Can't handle item of class {}".format(data_format.__class__.__name__))
