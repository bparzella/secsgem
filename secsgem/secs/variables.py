#####################################################################
# variables.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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

import struct

from collections import OrderedDict

DEBUG_DECODE = False
DEBUG_DECODE_DEPTH = 0


class SecsVar(object):
    """Base class for SECS variables. Due to the python types, wrapper classes for variables are required. If constructor is called with SecsVar or subclass only the value is copied."""
    formatCode = -1

    def __init__(self):
        self.__dict__["value"] = None

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: various
        """
        raise NotImplementedError("Function set not implemented on SecsVar")

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
            return chr(format_byte) + chr((length & 0xFF0000) >> 16) + chr((length & 0x00FF00) >> 8) + chr((length & 0x0000FF))
        elif length > 0xFF:
            length_bytes = 2
            format_byte = (self.formatCode << 2) | length_bytes
            return chr(format_byte) + chr((length & 0x00FF00) >> 8) + chr((length & 0x0000FF))
        else:
            length_bytes = 1
            format_byte = (self.formatCode << 2) | length_bytes
            return chr(format_byte) + chr((length & 0x0000FF))

    def decode_item_header(self, data, text_pos=0):
        """Encode item header depending on the number of length bytes required.

        :param data: encoded data
        :type data: string
        :param text_pos: start of item header in data
        :type text_pos: integer
        :returns: start position for next item, format code, length item of data
        :rtype: (integer, integer, integer)
        """
        if DEBUG_DECODE:
            print "{}--Decoded item header for {} starting at {}".format((" " * DEBUG_DECODE_DEPTH), self.__class__.__name__, text_pos)

        if data == "":
            raise ValueError("Decoding for {} without any text".format(self.__class__.__name__))

        # parse format byte
        format_byte = ord(data[text_pos])
        format_code = (format_byte & 0b11111100) >> 2
        length_bytes = (format_byte & 0b00000011)

        text_pos += 1

        # read 1-3 length bytes
        length = 0
        for i in range(length_bytes):
            length <<= 8
            length += ord(data[text_pos])

            text_pos += 1

        if 0 <= self.formatCode != format_code:
            raise ValueError("Decoding data for {} ({}) has invalid format {}".format(self.__class__.__name__, self.formatCode, format_code))

        if DEBUG_DECODE:
            print "{}Decoded item header with data @{} / format {} / length {}".format((" " * DEBUG_DECODE_DEPTH), text_pos, format_code, length)

        return text_pos, format_code, length


class SecsVarDynamic(SecsVar):
    """Variable with interchangable type.

    :param types: list of supported types, default first. empty list means all types are support, SecsVarString default
    :type types: list of :class:`secsgem.secs.variables.SecsVar` classes
    :param length: max number of items in type
    :type length: integer
    :param value: initial value
    :type value: various
    """

    def __init__(self, types, length=-1, value=None):
        super(SecsVarDynamic, self).__init__()

        if not types:
            self.value = SecsVarString(length)
        else:
            self.value = types[0](length)

        self.types = types
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return self.value.__repr__()

    def __len__(self):
        return self.value.__len__()

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __setitem__(self, key, item):
        self.value.__setitem__(key, item)

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
            >>> var.set(10)
            >>> var
            A '10'
            >>> var.set(secsgem.SecsVarU1(value=10))
            >>> var
            U1 10

        If no type is provided the default type is used which might not be the expected type.

        :param value: new value
        :type value: various
        """
        if isinstance(value, SecsVar):
            if not isinstance(value, tuple(self.types)):
                raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}".format(value.__class__.__name__, self.types))

            self.value = value
        else:
            self.value.set(value)

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: various
        """
        return self.value.get()

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        if format_code == SecsVarArray.formatCode and self.__type_supported(SecsVarArray):
            self.value = SecsVarArray(SecsVarDynamic([], self.length))
        elif format_code == SecsVarBinary.formatCode and self.__type_supported(SecsVarBinary):
            self.value = SecsVarBinary(self.length)
        elif format_code == SecsVarBoolean.formatCode and self.__type_supported(SecsVarBoolean):
            self.value = SecsVarBoolean(self.length)
        elif format_code == SecsVarString.formatCode and self.__type_supported(SecsVarString):
            self.value = SecsVarString(self.length)
        elif format_code == SecsVarI8.formatCode and self.__type_supported(SecsVarI8):
            self.value = SecsVarI8(self.length)
        elif format_code == SecsVarI1.formatCode and self.__type_supported(SecsVarI1):
            self.value = SecsVarI1(self.length)
        elif format_code == SecsVarI2.formatCode and self.__type_supported(SecsVarI2):
            self.value = SecsVarI2(self.length)
        elif format_code == SecsVarI4.formatCode and self.__type_supported(SecsVarI4):
            self.value = SecsVarI4(self.length)
        elif format_code == SecsVarF8.formatCode and self.__type_supported(SecsVarF8):
            self.value = SecsVarF8(self.length)
        elif format_code == SecsVarF4.formatCode and self.__type_supported(SecsVarF4):
            self.value = SecsVarF4(self.length)
        elif format_code == SecsVarU8.formatCode and self.__type_supported(SecsVarU8):
            self.value = SecsVarU8(self.length)
        elif format_code == SecsVarU1.formatCode and self.__type_supported(SecsVarU1):
            self.value = SecsVarU1(self.length)
        elif format_code == SecsVarU2.formatCode and self.__type_supported(SecsVarU2):
            self.value = SecsVarU2(self.length)
        elif format_code == SecsVarU4.formatCode and self.__type_supported(SecsVarU4):
            self.value = SecsVarU4(self.length)
        else:
            raise ValueError("Unsupported format {} for this instance of SecsVarDynamic, allowed {}".format(format_code, self.types))

        return self.value.decode(data, start)

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarDynamic`
        """
        return SecsVarDynamic(self.types, self.length, self.value.get())


class SecsVarList(SecsVar):
    """List variable type. List with items of different types

    :param data: internal data values
    :type data: OrderedDict
    :param field_count: number of fields in the list
    :type field_count: integer
    :param value: initial value
    :type value: dict/list
    """
    formatCode = 0

    def __init__(self, data, field_count=-1, value=None):
        super(SecsVarList, self).__init__()

        self.__dict__["data"] = data
        self.__dict__["fieldCount"] = field_count
        if self.fieldCount >= 0:
            if not len(data) == field_count:
                raise ValueError(
                    "Definition has invalid field count (expected: {}, actual: {})".format(self.fieldCount, len(data)))

        if value is not None:
            self.set(value)

    def __repr__(self):
        data = ""
        first = True

        for field_name in self.data:
            if not first:
                data += ", "
            data += "{}: {}".format(field_name, self.data[field_name].__repr__())
            first = False

        return "[{}]".format(data)

    def __len__(self):
        return len(self.data)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: dict/list
        """
        if isinstance(value, dict):
            for field_name in value:
                self.data[field_name].set(value[field_name])
        elif isinstance(value, list):
            if not len(value) == self.fieldCount:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.length, len(self.data)))
            counter = 0
            for field_name in self.data:
                self.data[field_name].set(value[counter])
                counter += 1
        else:
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list
        """
        data = []
        for field_name in self.data:
            data.append(self.data[field_name].get())

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        global DEBUG_DECODE_DEPTH

        # list
        for i in range(length):
            DEBUG_DECODE_DEPTH += 2
            field_name = self.data.keys()[i]
            text_pos = self.data[field_name].decode(data, text_pos)
            DEBUG_DECODE_DEPTH -= 2

        return text_pos

    def __getattr__(self, name):
        if name not in self.__dict__["data"]:
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        if isinstance(self.__dict__["data"][name], SecsVarArray) or isinstance(self.data[name], SecsVarList):
            return self.__dict__["data"][name]
        else:
            return self.__dict__["data"][name].get()

    def __setattr__(self, name, value):
        if name not in self.__dict__["data"]:
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        self.__dict__["data"][name].set(value)

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarList`
        """
        new_data = OrderedDict()
        for item in self.data:
            new_data[item] = self.data[item].clone()

        return SecsVarList(new_data, self.fieldCount)


class SecsVarArray(SecsVar):
    """List variable type. List with items of same type

    :param data: internal data definition/sample
    :type data: :class:`secsgem.secs.variables.SecsVar`
    :param field_count: number of fields in the list
    :type field_count: integer
    :param value: initial value
    :type value: list
    """
    formatCode = 0

    def __init__(self, data, field_count=-1, value=None):
        super(SecsVarArray, self).__init__()

        self.__dict__["itemDecriptor"] = data
        self.__dict__["fieldCount"] = field_count
        self.__dict__["data"] = []
        if value is not None:
            self.set(value)

    def __repr__(self):
        data = ""
        first = True

        for value in self.data:
            if not first:
                data += ", "
            data += "{}".format(value.__repr__())
            first = False

        return "[{}]".format(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if isinstance(self.data[key], SecsVarArray) or isinstance(self.data[key], SecsVarList):
            return self.data[key]
        else:
            return self.data[key].get()

    def __setitem__(self, key, item):
        self.data[key].set(item)

    def append(self, data):
        """Append data to the internal list

        :param value: new value
        :type value: various
        """
        new_object = self.__dict__["itemDecriptor"].clone()
        new_object.set(data)
        self.data.append(new_object)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list
        """
        if not isinstance(value, list):
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if self.__dict__["fieldCount"] >= 0:
            if not len(value) == self.__dict__["fieldCount"]:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.__dict__["fieldCount"], len(value)))

        self.__dict__["data"] = []

        for counter in range(len(value)):
            new_object = self.__dict__["itemDecriptor"].clone()
            new_object.set(value[counter])
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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        global DEBUG_DECODE_DEPTH

        # list
        self.__dict__["data"] = []

        for counter in range(length):
            DEBUG_DECODE_DEPTH += 2
            new_object = self.__dict__["itemDecriptor"].clone()
            text_pos = new_object.decode(data, text_pos)
            self.data.append(new_object)
            DEBUG_DECODE_DEPTH -= 2

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarArray`
        """
        item_decriptor = self.__dict__["itemDecriptor"].clone()
        new_data = []
        for item in self.data:
            new_data.append(item.get())

        return SecsVarArray(item_decriptor, self.__dict__["fieldCount"], new_data)


class SecsVarBinary(SecsVar):
    """Secs type for binary data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: string/integer
    """
    formatCode = 010

    def __init__(self, length=-1, value=None):
        super(SecsVarBinary, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.value) == 1:
            return "B {}".format(self.get())
        else:
            return "B <{} bytes>".format(len(self.value))

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return ord(self.value[key])

    def __setitem__(self, key, item):
        self.value[key] = chr(item)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: string/integer
        """
        if value is None:
            return

        if not isinstance(value, str):
            value = chr(value)

        if 0 <= self.length != len(value):
            raise ValueError("Value longer than {} chars".format(self.length))

        self.value = value

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return ord(self.value[0])
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        if self.value is None:
            length = 0
        else:
            length = len(self.value)

        result = self.encode_item_header(length)

        if self.value is not None:
            result += self.value

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        # string
        result = None

        if length > 0:
            result = data[text_pos:text_pos + length]

            if DEBUG_DECODE:
                print "{}Decoded {} bytes".format((" " * DEBUG_DECODE_DEPTH), len(result))

        self.set(result)

        return text_pos + length

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarBinary`
        """
        return SecsVarBinary(self.length, self.value)


class SecsVarBoolean(SecsVar):
    """Secs type for boolean data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/boolean
    """
    formatCode = 011

    def __init__(self, length=-1, value=None):
        super(SecsVarBoolean, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "TF {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/boolean
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [bool(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/boolean
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += chr(value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length):
            result_text = data[text_pos]
            result.append(bool(struct.unpack(">b", result_text)[0]))

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 1

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarBoolean`
        """
        return SecsVarBoolean(self.length, self.value)


class SecsVarString(SecsVar):
    """Secs type for string data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: string
    """
    formatCode = 020

    def __init__(self, length=-1, value=None):
        super(SecsVarString, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "A '{}'".format(self.value)

    def __len__(self):
        return len(self.value)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: string
        """
        if not isinstance(value, str):
            value = str(value)

        if 0 <= self.length < len(value):
            raise ValueError("Value longer than {} chars".format(self.length))

        self.value = value

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

        result += self.value

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        # string
        result = None

        if length > 0:
            result = data[text_pos:text_pos + length]

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result)

        self.set(result)

        return text_pos + length

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarString`
        """
        return SecsVarString(self.length, self.value)


class SecsVarI8(SecsVar):
    """Secs type for 8 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 030

    def __init__(self, length=-1, value=None):
        super(SecsVarI8, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "I8 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 8)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">q", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 8):
            result_text = data[text_pos:text_pos + 8]

            if len(result_text) != 8:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">q", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 8

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarI8`
        """
        return SecsVarI8(self.length, self.value)


class SecsVarI1(SecsVar):
    """Secs type for 1 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 031

    def __init__(self, length=-1, value=None):
        super(SecsVarI1, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "I1 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">b", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length):
            result_text = data[text_pos:text_pos]

            if len(result_text) != 1:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">b", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 1

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarI1`
        """
        return SecsVarI1(self.length, self.value)


class SecsVarI2(SecsVar):
    """Secs type for 2 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 032

    def __init__(self, length=-1, value=None):
        super(SecsVarI2, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "I2 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 2)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">h", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 2):
            result_text = data[text_pos:text_pos + 2]

            if len(result_text) != 2:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">h", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 2

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarI2`
        """
        return SecsVarI2(self.length, self.value)


class SecsVarI4(SecsVar):
    """Secs type for 4 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 034

    def __init__(self, length=-1, value=None):
        super(SecsVarI4, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "I4 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 4)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">l", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 4):
            result_text = data[text_pos:text_pos + 4]

            if len(result_text) != 4:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">l", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 4

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarI4`
        """
        return SecsVarI4(self.length, self.value)


class SecsVarF8(SecsVar):
    """Secs type for 8 byte float data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/float
    """
    formatCode = 040

    def __init__(self, length=-1, value=None):
        super(SecsVarF8, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "F8 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/float
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [float(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/float
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 8)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">d", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 8):
            result_text = data[text_pos:text_pos + 8]

            if len(result_text) != 8:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">d", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 8

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarF8`
        """
        return SecsVarF8(self.length, self.value)


class SecsVarF4(SecsVar):
    """Secs type for 4 byte float data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/float
    """
    formatCode = 044

    def __init__(self, length=-1, value=None):
        super(SecsVarF4, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "F4 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/float
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [float(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/float
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 4)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">f", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 4):
            result_text = data[text_pos:text_pos + 4]

            if len(result_text) != 4:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">f", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 4

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarF4`
        """
        return SecsVarF4(self.length, self.value)


class SecsVarU8(SecsVar):
    """Secs type for 8 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 050

    def __init__(self, length=-1, value=None):
        super(SecsVarU8, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "U8 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 8)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">Q", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 8):
            result_text = data[text_pos:text_pos + 8]

            if len(result_text) != 8:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">Q", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 8

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarU8`
        """
        return SecsVarU8(self.length, self.value)


class SecsVarU1(SecsVar):
    """Secs type for 1 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 051

    def __init__(self, length=-1, value=None):
        super(SecsVarU1, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "U1 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">B", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length):
            result_text = data[text_pos]

            if len(result_text) != 1:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">B", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 1

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarU1`
        """
        return SecsVarU1(self.length, self.value)


class SecsVarU2(SecsVar):
    """Secs type for 2 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 052

    def __init__(self, length=-1, value=None):
        super(SecsVarU2, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "U2 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 2)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">H", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 2):
            result_text = data[text_pos:text_pos + 2]

            if len(result_text) != 2:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">H", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 2

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarU2`
        """
        return SecsVarU2(self.length, self.value)


class SecsVarU4(SecsVar):
    """Secs type for 4 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 054

    def __init__(self, length=-1, value=None):
        super(SecsVarU4, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        return "U4 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/integer
        """
        if isinstance(value, list):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [int(value)]

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: list/integer
        """
        if self.value is None:
            return None

        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        """Encode the value to secs data

        :returns: encoded data bytes
        :rtype: string
        """
        result = self.encode_item_header(len(self.value) * 4)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">L", value)

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
        (text_pos, format_code, length) = self.decode_item_header(data, start)

        result = []

        for i in range(length / 4):
            result_text = data[text_pos:text_pos + 4]

            if len(result_text) != 4:
                raise ValueError("No enough data found for {} with length {} at position {} ".format(self.__class__.__name__, length, start))

            result.append(struct.unpack(">L", result_text)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            text_pos += 4

        self.set(result)

        return text_pos

    def clone(self):
        """Returns copy of the object

        :returns: copy
        :rtype: :class:`secsgem.secs.variables.SecsVarU4`
        """
        return SecsVarU4(self.length, self.value)
