#####################################################################
# variables.py
#
# (c) Copyright 2013-2016, Benjamin Parzella. All rights reserved.
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
"""SECS variable types"""

from past.builtins import long, unicode
from builtins import chr  # noqa
from future.utils import implements_iterator

import struct
import inspect
import unicodedata

from collections import OrderedDict

from ..common import indent_block
from ..common.codec_jis_x_0201 import *  # noqa

class SecsVar(object):
    """Base class for SECS variables. 

    Due to the python types, wrapper classes for variables are required. 
    If constructor is called with SecsVar or subclass only the value is copied.
    """

    formatCode = -1

    def __init__(self):
        self.value = None

    @staticmethod
    def generate(dataformat):
        """Generate actual variable from data format

        :param dataformat: dataformat to create variable for
        :type dataformat: list/SecsVar based class
        :returns: created variable
        :rtype: SecsVar based class
        """
        if dataformat is None:
            return None

        if isinstance(dataformat, list):
            if len(dataformat) == 1:
                return SecsVarArray(dataformat[0])
            else:
                return SecsVarList(dataformat)
        elif inspect.isclass(dataformat):
            if issubclass(dataformat, SecsVar):
                return dataformat()
            else:
                raise TypeError("Can't generate item of class {}".format(dataformat.__name__))
        else:
            raise TypeError("Can't handle item of class {}".format(dataformat.__class__.__name__))

    @staticmethod
    def get_format(dataformat, showname=False):
        """Gets the format of the function

        :returns: returns the string representation of the function
        :rtype: string
        """
        del showname  # unused variable
        if dataformat is None:
            return None

        if isinstance(dataformat, list):
            if len(dataformat) == 1:
                return SecsVarArray.get_format(dataformat[0])
            else:
                return SecsVarList.get_format(dataformat)
        elif inspect.isclass(dataformat):
            if issubclass(dataformat, SecsVar):
                return dataformat.get_format()
            else:
                raise TypeError("Can't generate dataformat for class {}".format(dataformat.__name__))
        else:
            raise TypeError("Can't handle item of class {}".format(dataformat.__class__.__name__))

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: various
        """
        raise NotImplementedError("Function set not implemented on " + self.__class__.__name__)

    def encode_item_header(self, length):
        """Encode item header depending on the number of length bytes required.

        :param length: number of bytes in data
        :type length: integer
        :returns: encoded item header bytes
        :rtype: string
        """
        if length < 0:
            raise ValueError("Encoding {} not possible, data length too small {}".format(self.__class__.__name__, length))
        if length > 0xFFFFFF:
            raise ValueError("Encoding {} not possible, data length too big {}".format(self.__class__.__name__, length))

        if length > 0xFFFF:
            length_bytes = 3
            format_byte = (self.formatCode << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0xFF0000) >> 16, (length & 0x00FF00) >> 8, (length & 0x0000FF))))
        elif length > 0xFF:
            length_bytes = 2
            format_byte = (self.formatCode << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0x00FF00) >> 8, (length & 0x0000FF))))
        else:
            length_bytes = 1
            format_byte = (self.formatCode << 2) | length_bytes
            return bytes(bytearray((format_byte, (length & 0x0000FF))))

    def decode_item_header(self, data, text_pos=0):
        """Encode item header depending on the number of length bytes required.

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

        if 0 <= self.formatCode != format_code:
            raise ValueError("Decoding data for {} ({}) has invalid format {}".format(self.__class__.__name__, self.formatCode, format_code))

        return text_pos, format_code, length


class SecsVarDynamic(SecsVar):
    """Variable with interchangable type.

    :param types: list of supported types, default first. empty list means all types are support, SecsVarString default
    :type types: list of :class:`secsgem.secs.variables.SecsVar` classes
    :param value: initial value
    :type value: various
    :param count: max number of items in type
    :type count: integer
    """

    def __init__(self, types, value=None, count=-1):
        super(SecsVarDynamic, self).__init__()

        self.value = None

        self.types = types
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        return self.value.__repr__()

    def __len__(self):
        """Get the lenth"""
        return self.value.__len__()

    def __getitem__(self, key):
        """Get an item using the indexer operator"""
        return self.value.__getitem__(key)

    def __setitem__(self, key, item):
        """Set an item using the indexer operator"""
        self.value.__setitem__(key, item)

    def __eq__(self, other):
        """Check equality with other object"""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value.value
        elif isinstance(other, SecsVar):
            return other.value == self.value.value
        elif isinstance(other, list):
            return other == self.value.value
        else:
            if isinstance(other, (bytes, unicode)) and isinstance(self.value.value, (bytes, unicode)):
                return (unicode(other) == unicode(self.value.value)) 
            else: 
                return [other] == self.value.value

    def __hash__(self):
        """Get data item for hashing"""
        if isinstance(self.value.value, list):
            return hash(self.value.value[0])
        else:
            return hash(self.value.value)

    def __type_supported(self, typ):
        if not self.types:
            return True

        if typ in self.types:
            return True

        return False

    def set(self, value):
        """Set the internal value to the provided value

        In doubt provide the variable wrapped in the matching :class:`secsgem.secs.variables.SecsVar` class, to avoid confusion.

        **Example**::

            >>> import secsgem
            >>>
            >>> var = secsgem.SecsVarDynamic([secsgem.SecsVarString, secsgem.SecsVarU1])
            >>> var.set(secsgem.SecsVarU1(10))
            >>> var
            <U1 10 >

        If no type is provided the default type is used which might not be the expected type.

        :param value: new value
        :type value: various
        """
        if isinstance(value, SecsVar):
            if isinstance(value, SecsVarDynamic):
                if not isinstance(value.value, tuple(self.types)) and self.types:
                    raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}".format(value.value.__class__.__name__, self.types))

                self.value = value.value
            else:
                if not isinstance(value, tuple(self.types)) and self.types:
                    raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}".format(value.__class__.__name__, self.types))

                self.value = value
        else:
            matched_type = self._match_type(value)

            if matched_type is None:
                raise ValueError('Value "{}" of type {} not valid for SecsDynamic with {}'.format(value, value.__class__.__name__, self.types))

            self.value = matched_type(count=self.count)
            self.value.set(value)

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: various
        """
        if self.value is not None:
            return self.value.get()
        else:
            return None

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        return self.value.encode()

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

        :param data: encoded data bytes
        :type data: string
        :param start: start position of value the data
        :type start: integer
        :returns: new start position
        :rtype: integer
        """
        (_, format_code, _) = self.decode_item_header(data, start)

        if format_code == SecsVarArray.formatCode and self.__type_supported(SecsVarArray):
            self.value = SecsVarArray(ANYVALUE)
        elif format_code == SecsVarBinary.formatCode and self.__type_supported(SecsVarBinary):
            self.value = SecsVarBinary(count=self.count)
        elif format_code == SecsVarBoolean.formatCode and self.__type_supported(SecsVarBoolean):
            self.value = SecsVarBoolean(count=self.count)
        elif format_code == SecsVarString.formatCode and self.__type_supported(SecsVarString):
            self.value = SecsVarString(count=self.count)
        elif format_code == SecsVarI8.formatCode and self.__type_supported(SecsVarI8):
            self.value = SecsVarI8(count=self.count)
        elif format_code == SecsVarI1.formatCode and self.__type_supported(SecsVarI1):
            self.value = SecsVarI1(count=self.count)
        elif format_code == SecsVarI2.formatCode and self.__type_supported(SecsVarI2):
            self.value = SecsVarI2(count=self.count)
        elif format_code == SecsVarI4.formatCode and self.__type_supported(SecsVarI4):
            self.value = SecsVarI4(count=self.count)
        elif format_code == SecsVarF8.formatCode and self.__type_supported(SecsVarF8):
            self.value = SecsVarF8(count=self.count)
        elif format_code == SecsVarF4.formatCode and self.__type_supported(SecsVarF4):
            self.value = SecsVarF4(count=self.count)
        elif format_code == SecsVarU8.formatCode and self.__type_supported(SecsVarU8):
            self.value = SecsVarU8(count=self.count)
        elif format_code == SecsVarU1.formatCode and self.__type_supported(SecsVarU1):
            self.value = SecsVarU1(count=self.count)
        elif format_code == SecsVarU2.formatCode and self.__type_supported(SecsVarU2):
            self.value = SecsVarU2(count=self.count)
        elif format_code == SecsVarU4.formatCode and self.__type_supported(SecsVarU4):
            self.value = SecsVarU4(count=self.count)
        else:
            raise ValueError(
                "Unsupported format {} for this instance of SecsVarDynamic, allowed {}".format(
                    format_code,
                    self.types))

        return self.value.decode(data, start)

    def _match_type(self, value):
        var_types = self.types
        #if no types are set use internal order
        if not self.types:
            var_types = [SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
                SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]

        # first try to find the preferred type for the kind of value
        for var_type in var_types:
            if isinstance(value, tuple(var_type.preferredTypes)):
                if var_type(count=self.count).supports_value(value):
                    return var_type

        # when no preferred type was found, then try to match any available type
        for var_type in var_types:
            if var_type(count=self.count).supports_value(value):
                return var_type

        return None


class ANYVALUE(SecsVarDynamic):
    """Dummy data item for generation of unknown types

    :Types:
       - :class:`SecsVarArray <secsgem.secs.variables.SecsVarArray>`
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       - :class:`SecsVarBoolean <secsgem.secs.variables.SecsVarBoolean>`
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`
       - :class:`SecsVarF8 <secsgem.secs.variables.SecsVarF8>`
       - :class:`SecsVarF4 <secsgem.secs.variables.SecsVarF4>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    """

    def __init__(self, value=None):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, \
            SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary], value=value)


class SecsVarList(SecsVar):
    """List variable type. List with items of different types

    :param dataformat: internal data values
    :type dataformat: OrderedDict
    :param value: initial value
    :type value: dict/list
    :param count: number of fields in the list
    :type count: integer
    """

    formatCode = 0
    textCode = 'L'
    preferredTypes = [dict]

    @implements_iterator
    class SecsVarListIter(object):
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):
            """Get an iterator"""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list"""
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]
            else:
                raise StopIteration()

    def __init__(self, dataformat, value=None):
        super(SecsVarList, self).__init__()

        self.name = "DATA"

        self.data = self._generate(dataformat)

        if value is not None:
            self.set(value)

        self._object_intitialized = True

    @staticmethod
    def get_format(dataformat, showname=False):
        """Gets the format of the variable

        :returns: returns the string representation of the function
        :rtype: string
        """
        if showname:
            arrayName = "{}: ".format(SecsVarList.get_name_from_format(dataformat))
        else:
            arrayName = ""

        if isinstance(dataformat, list):
            items = []
            for item in dataformat:
                if isinstance(item, str):
                    continue
                elif isinstance(item, list):
                    if len(item) == 1:
                        items.append(indent_block(SecsVarArray.get_format(item[0], True), 4))
                    else:
                        items.append(indent_block(SecsVarList.get_format(item, True), 4))
                else:
                    items.append(indent_block(item.get_format(), 4))
            return arrayName + "{\n" + "\n".join(items) + "\n}"

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.data) == 0:
            return "<{}>".format(self.textCode)

        data = ""

        for field_name in self.data:
            data += "{}\n".format(indent_block(self.data[field_name].__repr__()))

        return "<{} [{}]\n{}\n>".format(self.textCode, len(self.data), data)

    def __len__(self):
        """Get the lenth"""
        return len(self.data)

    def __getitem__(self, index):
        """Get an item using the indexer operator"""
        if isinstance(index, int):
            return self.data[list(self.data.keys())[index]]
        else:
            return self.data[index]

    def __iter__(self):
        """Get an iterator"""
        return SecsVarList.SecsVarListIter(self.data.keys())

    def __setitem__(self, index, value):
        """Set an item using the indexer operator"""
        if isinstance(index, int):
            index = list(self.data.keys())[index]

        if isinstance(value, type(self.data[index])) or isinstance(value, self.data[index].__class__.__bases__):
            self.data[index] = value
        elif isinstance(value, SecsVar):
            raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__, self.data[index].__class__.__name__))
        else:
            self.data[index].set(value)

    def _generate(self, dataformat):
        if dataformat is None:
            return None

        result_data = OrderedDict()
        for item in dataformat:
            if isinstance(item, str):
                self.name = item
                continue

            itemvalue = SecsVar.generate(item)
            if isinstance(itemvalue, SecsVarArray):
                result_data[itemvalue.name] = itemvalue
            elif isinstance(itemvalue, SecsVarList):
                result_data[SecsVarList.get_name_from_format(item)] = itemvalue
            elif isinstance(itemvalue, SecsVar):
                result_data[itemvalue.name] = itemvalue
            else:
                raise TypeError("Can't handle item of class {}".format(dataformat.__class__.__name__))

        return result_data

    def __getattr__(self, item):
        """Get an item as member of the object"""
        try:
            return self.data.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Set an item as member of the object"""
        if '_object_intitialized' not in self.__dict__:
            return dict.__setattr__(self, item, value)
        elif item in self.data:
            if isinstance(value, type(self.data[item])) or isinstance(value, self.data[item].__class__.__bases__):
                self.data[item] = value
            elif isinstance(value, SecsVar):
                raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__, self.data[item].__class__.__name__))
            else:
                self.data[item].set(value)
        else:
            self.__dict__.__setattr__(item, value)

    @staticmethod
    def get_name_from_format(dataformat):
        """Generates a name for the passed dataformat

        :param dataformat: dataformat to get name for
        :type dataformat: list/SecsVar based class
        :returns: name for dataformat
        :rtype: str
        """
        if not isinstance(dataformat, list):
            raise TypeError("Can't generate item name of class {}".format(dataformat.__class__.__name__))

        if isinstance(dataformat[0], str):
            return dataformat[0]

        return "DATA"

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: dict/list
        """
        if isinstance(value, dict):
            for field_name in value:
                self.data[field_name].set(value[field_name])
        elif isinstance(value, list):
            if len(value) > len(self.data):
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(len(self.data), len(value)))
           
            counter = 0
            for itemvalue in value:
                self.data[list(self.data.keys())[counter]].set(itemvalue)
                counter += 1
        else:
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list
        """
        data = {}
        for field_name in self.data:
            data[field_name] = self.data[field_name].get() 

        return data

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for field_name in self.data:
            result += self.data[field_name].encode()

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

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
    """List variable type. List with items of same type

    :param dataFormat: internal data definition/sample
    :type dataFormat: :class:`secsgem.secs.variables.SecsVar`
    :param value: initial value
    :type value: list
    :param count: number of fields in the list
    :type count: integer
    """

    formatCode = 0
    textCode = 'L'
    preferredTypes = [list]

    @implements_iterator
    class SecsVarArrayIter(object):
        def __init__(self, values):
            self._values = values
            self._counter = 0

        def __iter__(self):
            """Get an iterator"""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list"""
            if self._counter < len(self._values):
                i = self._counter
                self._counter += 1
                return self._values[i]
            else:
                raise StopIteration()

    def __init__(self, dataFormat, value=None, count=-1):
        super(SecsVarArray, self).__init__()

        self.item_decriptor = dataFormat
        self.count = count
        self.data = []
        if isinstance(dataFormat, list):
            self.name = SecsVarList.get_name_from_format(dataFormat)
        elif hasattr(dataFormat, "__name__"):
            self.name = dataFormat.__name__
        else:
            self.name = "UNKNOWN"

        if value is not None:
            self.set(value)

    @staticmethod
    def get_format(dataformat, showname=False):
        """Gets the format of the variable

        :returns: returns the string representation of the function
        :rtype: string
        """
        if showname:
            arrayName = "{}: "
            if isinstance(dataformat, list):
                arrayName = arrayName.format(SecsVarList.get_name_from_format(dataformat))
            else:
                arrayName = arrayName.format(dataformat.__name__)
        else:
            arrayName = ""

        if isinstance(dataformat, list):
            return "{}[\n{}\n    ...\n]".format(arrayName, indent_block(SecsVarList.get_format(dataformat), 4))
        else:
            return "{}[\n{}\n    ...\n]".format(arrayName, indent_block(dataformat.get_format(not showname), 4))

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.data) == 0:
            return "<{}>".format(self.textCode)

        data = ""

        for value in self.data:
            data += "{}\n".format(indent_block(value.__repr__()))

        return "<{} [{}]\n{}\n>".format(self.textCode, len(self.data), data)

    def __len__(self):
        """Get the lenth"""
        return len(self.data)

    def __getitem__(self, key):
        """Get an item using the indexer operator"""
        return self.data[key]

    def __iter__(self):
        """Get an iterator"""
        return SecsVarArray.SecsVarArrayIter(self.data)

    def __setitem__(self, key, value):
        """Set an item using the indexer operator"""
        if isinstance(value, type(self.data[key])) or isinstance(value, self.data[key].__class__.__bases__):
            self.data[key] = value
        elif isinstance(value, SecsVar):
            raise TypeError("Wrong type {} when expecting {}".format(value.__class__.__name__, self.data[key].__class__.__name__))
        else:
            self.data[key].set(value)

    def append(self, data):
        """Append data to the internal list

        :param value: new value
        :type value: various
        """
        new_object = SecsVar.generate(self.item_decriptor)
        new_object.set(data)
        self.data.append(new_object)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list
        """
        if not isinstance(value, list):
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if self.count >= 0:
            if not len(value) == self.count:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.count, len(value)))

        self.data = []

        for item in value:
            new_object = SecsVar.generate(self.item_decriptor)
            new_object.set(item)
            self.data.append(new_object)

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list
        """
        data = []
        for item in self.data:
            data.append(item.get())

        return data

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.data))

        for item in self.data:
            result += item.encode()

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

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
            new_object = SecsVar.generate(self.item_decriptor)
            text_pos = new_object.decode(data, text_pos)
            self.data.append(new_object)

        return text_pos


class SecsVarBinary(SecsVar):
    """Secs type for binary data

    :param value: initial value
    :type value: string/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o10
    textCode = "B"
    preferredTypes = [bytes, bytearray]

    def __init__(self, value=None, count=-1):
        super(SecsVarBinary, self).__init__()

        self.value = bytearray()
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.value) == 0:
            return "<{}>".format(self.textCode)

        data = " ".join("0x{:x}".format(c) for c in self.value)

        return "<{} {}>".format(self.textCode, data.strip())

    def __len__(self):
        """Get the lenth"""
        return len(self.value)

    def __getitem__(self, key):
        """Get an item using the indexer operator"""
        if key >= self.count:
            raise IndexError("Index {} out of bounds ({})".format(key, self.count))

        if key >= len(self.value):
            return 0

        return self.value[key]

    def __setitem__(self, key, item):
        """Set an item using the indexer operator"""
        if key >= self.count:
            raise IndexError("Index {} out of bounds ({})".format(key, self.count))

        if key >= len(self.value):
            while key >= len(self.value):
                self.value.append(0)

        self.value[key] = item

    def __eq__(self, other):
        """Check equality with other object"""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value
        elif isinstance(other, SecsVar):
            return other.value == self.value
        else:
            return other == self.value

    def __hash__(self):
        """Get data item for hashing"""
        return hash(bytes(self.value))

    def __check_single_item_support(self, value):
        if isinstance(value, bool):
            return True

        if isinstance(value, (int, long)):
            if 0 <= value <= 255:
                return True
            return False

        return False

    def supports_value(self, value):
        """Check if the current instance supports the provided value

        :param value: value to test
        :type value: any
        """
        if isinstance(value, list) or isinstance(value, tuple):
            if self.count > 0 and len(value) > self.count:
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True
        elif isinstance(value, bytearray):
            if self.count > 0 and len(value) > self.count:
                return False
            return True
        elif isinstance(value, bytes):
            if self.count > 0 and len(value) > self.count:
                return False
            return True

        elif isinstance(value, unicode):
            if self.count > 0 and len(value) > self.count:
                return False
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                return False

            return True
        else:
            return self.__check_single_item_support(value)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: string/integer
        """
        if value is None:
            return

        if isinstance(value, bytes):
            value = bytearray(value)
        elif isinstance(value, unicode):
            value = bytearray(value.encode('ascii'))
        elif isinstance(value, list) or isinstance(value, tuple):
            value = bytearray(value)
        elif isinstance(value, bytearray):
            pass
        elif isinstance(value, int) or isinstance(value, long):
            if 0 <= value <= 255:
                value = bytearray([value])
            else:
                raise ValueError("Value {} of type {} is out of range for {}".format(value, type(value).__name__, self.__class__.__name__))
        else:
            raise TypeError("Unsupported type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if 0 < self.count < len(value) :
            raise ValueError("Value longer than {} chars ({} chars)".format(self.count, len(value)))

        self.value = value

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if len(self.value) == 1:
            return self.value[0]

        return bytes(self.value)

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) if self.value is not None else 0)

        if self.value is not None:
            result += bytes(self.value)

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

        :param data: encoded data bytes
        :type data: string
        :param start: start position of value the data
        :type start: integer
        :returns: new start position
        :rtype: integer
        """
        (text_pos, _, length) = self.decode_item_header(data, start)

        # string
        result = None

        if length > 0:
            result = data[text_pos:text_pos + length]

        self.set(result)

        return text_pos + length


class SecsVarBoolean(SecsVar):
    """Secs type for boolean data

    :param value: initial value
    :type value: list/boolean
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o11
    textCode = "BOOLEAN"
    preferredTypes = [bool]

    _trueStrings = ["TRUE", "YES"]
    _falseStrings = ["FALSE", "NO"]

    def __init__(self, value=None, count=-1):
        super(SecsVarBoolean, self).__init__()

        self.value = []
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.value) == 0:
            return "<{}>".format(self.textCode)

        data = ""

        for boolean in self.value:
            data += "{} ".format(boolean)

        return "<{} {}>".format(self.textCode, data)

    def __len__(self):
        """Get the lenth"""
        return len(self.value)

    def __getitem__(self, key):
        """Get an item using the indexer operator"""
        return self.value[key]

    def __setitem__(self, key, item):
        """Set an item using the indexer operator"""
        self.value[key] = item

    def __eq__(self, other):
        """Check equality with other object"""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value
        elif isinstance(other, SecsVar):
            return other.value == self.value
        elif isinstance(other, list):
            return other == self.value
        else:
            return [other] == self.value

    def __hash__(self):
        """Get data item for hashing"""
        return hash(str(self.value))

    def __check_single_item_support(self, value):
        if isinstance(value, bool):
            return True

        if isinstance(value, (int, long)):
            if 0 <= value <= 1:
                return True
            return False

        if isinstance(value, str) or isinstance(value, unicode):
            if value.upper() in self._trueStrings or value.upper() in self._falseStrings:
                return True

            return False

        return False

    def supports_value(self, value):
        """Check if the current instance supports the provided value

        :param value: value to test
        :type value: any
        """
        if isinstance(value, list) or isinstance(value, tuple):
            if self.count > 0 and len(value) > self.count:
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True
        elif isinstance(value, bytearray):
            if self.count > 0 and len(value) > self.count:
                return False
            for char in value:
                if not 0 <= char <= 1:
                    return False
            return True
        else:
            return self.__check_single_item_support(value)

    def __convert_single_item(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, int) or isinstance(value, long):
            if not 0 <= value <= 1:
                raise ValueError("Value {} out of bounds".format(value))

            return bool(value)

        if isinstance(value, str) or isinstance(value, unicode):
            if value.upper() in self._trueStrings:
                return True
            elif value.upper() in self._falseStrings:
                return False
            else:
                raise ValueError("Value {} out of bounds".format(value))

        raise ValueError("Can't convert value {}".format(value))

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/boolean
        """
        if isinstance(value, list) or isinstance(value, tuple):
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
        """Return the internal value

        :returns: internal value
        :rtype: list/boolean
        """
        if len(self.value) == 1:
            return self.value[0]

        return self.value

    def encode(self):
        """Encode the value to secs data

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
        """Decode the secs byte data to the value

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


class SecsVarText(SecsVar):
    """Secs type base for any text data

    :param value: initial value
    :type value: string
    :param count: number of items this value
    :type count: integer
    """

    formatCode = -1
    textCode = u""
    controlChars = u"".join(chr(ch) for ch in range(256) if unicodedata.category(chr(ch))[0]=="C")
    coding = ""

    def __init__(self, value="", count=-1):
        super(SecsVarText, self).__init__()

        self.value = u""
        self.count = count

        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.value) == 0:
            return u"<{}>".format(self.textCode)

        data = u""
        last_char_printable = False

        for char in self.value:
            output = char

            if char not in self.controlChars:
                if last_char_printable:
                    data += output
                else:
                    data += ' "' + output
                last_char_printable = True
            else:
                if last_char_printable:
                    data += '" ' + hex(ord(output))
                else:
                    data += ' ' + hex(ord(output))
                last_char_printable = False

        if last_char_printable:
            data += '"'

        return u"<{}{}>".format(self.textCode, data)

    def __len__(self):
        """Get the lenth"""
        return len(self.value)

    def __eq__(self, other):
        """Check equality with other object"""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value
        elif isinstance(other, SecsVar):
            return other.value == self.value
        else:
            return other == self.value

    def __hash__(self):
        """Get data item for hashing"""
        return hash(self.value)

    def __check_single_item_support(self, value):
        if isinstance(value, bool):
            return True

        if isinstance(value, (int, long)):
            if 0 <= value <= 127:
                return True
            return False

        return False

    def __supports_value_listtypes(self, value):
        if self.count > 0 and len(value) > self.count:
            return False
        for item in value:
            if not self.__check_single_item_support(item):
                return False

        return True

    def supports_value(self, value):
        """Check if the current instance supports the provided value

        :param value: value to test
        :type value: any
        """
        if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, bytearray):
            return self.__supports_value_listtypes(value)
        elif isinstance(value, bytes):
            if self.count > 0 and len(value) > self.count:
                return False
            return True
        elif isinstance(value, (int, long, float, complex)):
            if self.count > 0 and len(str(value)) > self.count:
                return False
            return True
        elif isinstance(value, unicode):
            if self.count > 0 and len(value) > self.count:
                return False
            try:
                value.encode(self.coding)
            except UnicodeEncodeError:
                return False

            return True

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: string/integer
        """
        if value is None:
            raise ValueError("{} can't be None".format(self.__class__.__name__))

        if isinstance(value, bytes):
            value = value.decode(self.coding)
        elif isinstance(value, bytearray):
            value = bytes(value).decode(self.coding)
        elif isinstance(value, list) or isinstance(value, tuple):
            value = unicode(bytes(bytearray(value)).decode(self.coding))
        elif isinstance(value, int) or isinstance(value, long) or isinstance(value, float) or isinstance(value, complex):
            value = str(value)
        elif isinstance(value, unicode):
            value.encode(self.coding)  # try if it can be encoded as ascii (values 0-127)
        else:
            raise TypeError("Unsupported type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if 0 < self.count < len(value) :
            raise ValueError("Value longer than {} chars ({} chars)".format(self.count, len(value)))

        self.value = unicode(value)

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: string
        """
        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        result += self.value.encode(self.coding)

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

        :param data: encoded data bytes
        :type data: string
        :param start: start position of value the data
        :type start: integer
        :returns: new start position
        :rtype: integer
        """
        (text_pos, _, length) = self.decode_item_header(data, start)

        # string
        result = u""

        if length > 0:
            result = data[text_pos:text_pos + length].decode(self.coding)

        self.set(result)

        return text_pos + length


class SecsVarString(SecsVarText):
    """Secs type for string data

    :param value: initial value
    :type value: string
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o20
    textCode = u"A"
    preferredTypes = [bytes, unicode]
    controlChars = u"".join(chr(ch) for ch in range(256) if unicodedata.category(chr(ch))[0]=="C")
    coding = "ascii"


class SecsVarJIS8(SecsVarText):
    """Secs type for string data

    :param value: initial value
    :type value: string
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o21
    textCode = u"J"
    preferredTypes = [bytes, unicode]
    controlChars = u"".join(chr(ch) for ch in range(256) if unicodedata.category(chr(ch))[0]=="C")
    coding = "jis-8"


class SecsVarNumber(SecsVar):
    """Secs base type for numeric data

    :param value: initial value
    :type value: list/integer/float
    :param count: number of items this value
    :type count: integer
    """
    
    formatCode = 0
    textCode = ""
    _basetype = int
    _min = 0
    _max = 0
    _bytes = 0
    _structCode = ""

    def __init__(self, value=None, count=-1):
        super(SecsVarNumber, self).__init__()

        self.value = []
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        if len(self.value) == 0:
            return "<{}>".format(self.textCode)

        data = ""

        for item in self.value:
            data += "{} ".format(item)

        return "<{} {}>".format(self.textCode, data)

    def __len__(self):
        """Get the lenth"""
        return len(self.value)

    def __getitem__(self, key):
        """Get an item using the indexer operator"""
        return self.value[key]

    def __setitem__(self, key, item):
        """Set an item using the indexer operator"""
        self.value[key] = item

    def __eq__(self, other):
        """Check equality with other object"""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value
        elif isinstance(other, SecsVar):
            return other.value == self.value
        elif isinstance(other, list):
            return other == self.value
        else:
            return [other] == self.value

    def __hash__(self):
        """Get data item for hashing"""
        return hash(str(self.value))

    def __check_single_item_support(self, value):
        if isinstance(value, float) and self._basetype == int:
            return False

        if isinstance(value, bool):
            return True

        if isinstance(value, long) or isinstance(value, int) or isinstance(value, float):
            if value < self._min or value > self._max:
                return False
            return True

        if isinstance(value, bytes) or isinstance(value, unicode):
            try:
                val = self._basetype(value)
            except ValueError:
                return False
            if val < self._min or val > self._max:
                return False
            return True
        return False

    def supports_value(self, value):
        """Check if the current instance supports the provided value

        :param value: value to test
        :type value: any
        """
        if isinstance(value, list) or isinstance(value, tuple):
            if 0 <= self.count < len(value):
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False
            return True
        elif isinstance(value, bytearray):
            if 0 <= self.count < len(value):
                return False
            for item in value:
                if item < self._min or item > self._max:
                    return False
            return True
        else:
            return self.__check_single_item_support(value)


    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer/float
        """
        if isinstance(value, float) and self._basetype == int:
            raise ValueError("Invalid value {}".format(value))

        if isinstance(value, list) or isinstance(value, tuple):
            if 0 <= self.count < len(value):
                raise ValueError("Value longer than {} chars".format(self.count))

            new_list = []
            for item in value:
                item = self._basetype(item)
                if item < self._min or item > self._max:
                    raise ValueError("Invalid value {}".format(item))

                new_list.append(item)
            self.value = new_list
        elif isinstance(value, bytearray):
            if 0 <= self.count < len(value):
                raise ValueError("Value longer than {} chars".format(self.count))

            new_list = []
            for item in value:
                if item < self._min or item > self._max:
                    raise ValueError("Invalid value {}".format(item))
                new_list.append(item)
            self.value = new_list
        else:
            new_value = self._basetype(value)

            if new_value < self._min or new_value > self._max:
                raise ValueError("Invalid value {}".format(value))

            self.value = [new_value]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer/float
        """
        if len(self.value) == 1:
            return self.value[0]

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * self._bytes)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">{}".format(self._structCode), value)

        return result

    def decode(self, data, start=0):
        """Decode the secs byte data to the value

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
                    "No enough data found for {} with length {} at position {} ".format(
                        self.__class__.__name__,
                        length,
                        start))

            result.append(struct.unpack(">{}".format(self._structCode), result_text)[0])

            text_pos += self._bytes

        self.set(result)

        return text_pos


class SecsVarI8(SecsVarNumber):
    """Secs type for 8 byte signed data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o30
    textCode = "I8"
    _basetype = int
    _min = -9223372036854775808
    _max = 9223372036854775807
    _bytes = 8
    _structCode = "q"
    preferredTypes = [long, int]


class SecsVarI1(SecsVarNumber):
    """Secs type for 1 byte signed data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o31
    textCode = "I1"
    _basetype = int
    _min = -128
    _max = 127
    _bytes = 1
    _structCode = "b"
    preferredTypes = [int, long]


class SecsVarI2(SecsVarNumber):
    """Secs type for 2 byte signed data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o32
    textCode = "I2"
    _basetype = int
    _min = -32768
    _max = 32767
    _bytes = 2
    _structCode = "h"
    preferredTypes = [int, long]


class SecsVarI4(SecsVarNumber):
    """Secs type for 4 byte signed data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o34
    textCode = "I4"
    _basetype = int
    _min = -2147483648
    _max = 2147483647
    _bytes = 4
    _structCode = "l"
    preferredTypes = [int, long]


class SecsVarF8(SecsVarNumber):
    """Secs type for 8 byte float data

    :param value: initial value
    :type value: list/float
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o40
    textCode = "F8"
    _basetype = float
    _min = -1.79769e+308
    _max = 1.79769e+308
    _bytes = 8
    _structCode = "d"
    preferredTypes = [float]


class SecsVarF4(SecsVarNumber):
    """Secs type for 4 byte float data

    :param value: initial value
    :type value: list/float
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o44
    textCode = "F4"
    _basetype = float
    _min = -3.40282e+38
    _max = 3.40282e+38
    _bytes = 4
    _structCode = "f"
    preferredTypes = [float]


class SecsVarU8(SecsVarNumber):
    """Secs type for 8 byte unsigned data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o50
    textCode = "U8"
    _basetype = int
    _min = 0
    _max = 18446744073709551615
    _bytes = 8
    _structCode = "Q"
    preferredTypes = [long, int]


class SecsVarU1(SecsVarNumber):
    """Secs type for 1 byte unsigned data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o51
    textCode = "U1"
    _basetype = int
    _min = 0
    _max = 255
    _bytes = 1
    _structCode = "B"
    preferredTypes = [int, long]


class SecsVarU2(SecsVarNumber):
    """Secs type for 2 byte unsigned data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    formatCode = 0o52
    textCode = "U2"
    _basetype = int
    _min = 0
    _max = 65535
    _bytes = 2
    _structCode = "H"
    preferredTypes = [int, long]


class SecsVarU4(SecsVarNumber):
    """Secs type for 4 byte unsigned data

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """
    
    formatCode = 0o54
    textCode = "U4"
    _basetype = int
    _min = 0
    _max = 4294967295
    _bytes = 4
    _structCode = "L"
    preferredTypes = [int, long]

