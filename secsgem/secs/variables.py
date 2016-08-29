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
import inspect

from collections import OrderedDict

from ..common import indent_block

class SecsVar(object):
    """Base class for SECS variables. Due to the python types, wrapper classes for variables are required. If constructor is called with SecsVar or subclass only the value is copied."""
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

        return None

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
        if data == "":
            raise ValueError("Decoding for {} without any text".format(self.__class__.__name__))

        # parse format byte
        format_byte = ord(data[text_pos])
        format_code = (format_byte & 0b11111100) >> 2
        length_bytes = (format_byte & 0b00000011)

        text_pos += 1

        # read 1-3 length bytes
        length = 0
        for _ in range(length_bytes):
            length <<= 8
            length += ord(data[text_pos])

            text_pos += 1

        if 0 <= self.formatCode != format_code:
            raise ValueError("Decoding data for {} ({}) has invalid format {}".format(self.__class__.__name__, self.formatCode, format_code))

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

        self.value = None

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
            >>> var.set(secsgem.SecsVarU1(value=10))
            >>> var
            <U1 10 >

        If no type is provided the default type is used which might not be the expected type.

        :param value: new value
        :type value: various
        """
        if isinstance(value, SecsVar):
            if not isinstance(value, tuple(self.types)) and self.types:
                raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}".format(value.__class__.__name__, self.types))

            self.value = value
        else:
            matched_type = self._match_type(value)

            if matched_type is None:
                raise ValueError('Value "{}" of type {} not valid for SecsDynamic with {}'.format(value, value.__class__.__name__, self.types))

            self.value = matched_type(length=self.length)
            self.value.set(value)

    def get(self):
        """Return the internal value

        :returns: internal value
        :rtype: various
        """
        if self.value:
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
            self.value = SecsVarArray(SecsVarDynamic([], length=self.length))
        elif format_code == SecsVarBinary.formatCode and self.__type_supported(SecsVarBinary):
            self.value = SecsVarBinary(length=self.length)
        elif format_code == SecsVarBoolean.formatCode and self.__type_supported(SecsVarBoolean):
            self.value = SecsVarBoolean(length=self.length)
        elif format_code == SecsVarString.formatCode and self.__type_supported(SecsVarString):
            self.value = SecsVarString(length=self.length)
        elif format_code == SecsVarI8.formatCode and self.__type_supported(SecsVarI8):
            self.value = SecsVarI8(length=self.length)
        elif format_code == SecsVarI1.formatCode and self.__type_supported(SecsVarI1):
            self.value = SecsVarI1(length=self.length)
        elif format_code == SecsVarI2.formatCode and self.__type_supported(SecsVarI2):
            self.value = SecsVarI2(length=self.length)
        elif format_code == SecsVarI4.formatCode and self.__type_supported(SecsVarI4):
            self.value = SecsVarI4(length=self.length)
        elif format_code == SecsVarF8.formatCode and self.__type_supported(SecsVarF8):
            self.value = SecsVarF8(length=self.length)
        elif format_code == SecsVarF4.formatCode and self.__type_supported(SecsVarF4):
            self.value = SecsVarF4(length=self.length)
        elif format_code == SecsVarU8.formatCode and self.__type_supported(SecsVarU8):
            self.value = SecsVarU8(length=self.length)
        elif format_code == SecsVarU1.formatCode and self.__type_supported(SecsVarU1):
            self.value = SecsVarU1(length=self.length)
        elif format_code == SecsVarU2.formatCode and self.__type_supported(SecsVarU2):
            self.value = SecsVarU2(length=self.length)
        elif format_code == SecsVarU4.formatCode and self.__type_supported(SecsVarU4):
            self.value = SecsVarU4(length=self.length)
        else:
            raise ValueError(
                "Unsupported format {} for this instance of SecsVarDynamic, allowed {}".format(
                    format_code,
                    self.types))

        return self.value.decode(data, start)

    def _match_type(self, value):
        # first try to find the preferred type for the kind of value
        for var_type in self.types:
            if isinstance(value, tuple(var_type.preferredTypes)):
                if var_type(length=self.length).supports_value(value):
                    return var_type

        # when no preferred type was found, then try to match any available type
        for var_type in self.types:
            if var_type(length=self.length).supports_value(value):
                return var_type

        return None


class SecsVarList(SecsVar):
    """List variable type. List with items of different types

    :param dataformat: internal data values
    :type dataformat: OrderedDict
    :param length: number of fields in the list
    :type length: integer
    :param value: initial value
    :type value: dict/list
    """
    formatCode = 0
    preferredTypes = [dict]

    def __init__(self, dataformat, length=-1, value=None):
        super(SecsVarList, self).__init__()

        self.name = "DATA"

        self.data = self._generate(dataformat)
        self.length = length
        if self.length >= 0:
            if not len(self.data) == length:
                raise ValueError(
                    "Definition has invalid field count (expected: {}, actual: {})".format(self.length, len(self.data)))

        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.data) == 0:
            return "<L>"

        data = ""

        for field_name in self.data:
            data += "{}\n".format(indent_block(self.data[field_name].__repr__()))

        return "<L [{}]\n{}\n>".format(len(self.data), data)

    def __len__(self):
        return len(self.data)

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
            if not len(value) == self.length:
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
        (text_pos, _, length) = self.decode_item_header(data, start)

        # list
        for i in range(length):
            field_name = self.data.keys()[i]
            text_pos = self.data[field_name].decode(data, text_pos)

        return text_pos


class SecsVarArray(SecsVar):
    """List variable type. List with items of same type

    :param dataFormat: internal data definition/sample
    :type dataFormat: :class:`secsgem.secs.variables.SecsVar`
    :param length: number of fields in the list
    :type length: integer
    :param value: initial value
    :type value: list
    """
    formatCode = 0
    preferredTypes = [list]

    def __init__(self, dataFormat, length=-1, value=None):
        super(SecsVarArray, self).__init__()

        self.item_decriptor = dataFormat
        self.length = length
        self.data = []
        if isinstance(dataFormat, list):
            self.name = SecsVarList.get_name_from_format(dataFormat)
        else:
            self.name = dataFormat.__name__

        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.data) == 0:
            return "<L>"

        data = ""

        for value in self.data:
            data += "{}\n".format(indent_block(value.__repr__()))

        return "<L [{}]\n{}\n>".format(len(self.data), data)

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

        if self.length >= 0:
            if not len(value) == self.length:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.length, len(value)))

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

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: string/integer
    """
    formatCode = 010
    preferredTypes = [str, bytearray]

    def __init__(self, length=-1, value=None):
        super(SecsVarBinary, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.value) == 0:
            return "<B>"

        data = ""

        for char in self.value:
            data += "{} ".format(hex(ord(char)))

        return "<B {}>".format(data.strip())

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return ord(self.value[key])

    def __setitem__(self, key, item):
        self.value[key] = chr(item)

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
            if self.length > 0 and len(value) > self.length:
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True
        elif isinstance(value, bytearray):
            if self.length > 0 and len(value) > self.length:
                return False
            return True
        elif isinstance(value, str):
            if self.length > 0 and len(value) > self.length:
                return False
            return True

        elif isinstance(value, unicode):
            if self.length > 0 and len(value) > self.length:
                return False
            try:
                value.decode('ascii')
            except Exception:
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

        if not isinstance(value, str) and not isinstance(value, unicode) and not isinstance(value, list) and not isinstance(value, tuple) and not isinstance(value, bytearray):
            value = chr(value)

        #if self.length >= 0 and (0 <= len(value) <= self.length):
        #if 0 <= self.length != len(value):
        if self.length > 0 and len(value) > self.length:
            raise ValueError("Value longer than {} chars ({} chars)".format(self.length, len(value)))

        if isinstance(value, list) or isinstance(value, tuple):
            self.value = ''.join(chr(e) for e in value)
        elif isinstance(value, unicode):
            self.value = value.encode('ascii')
        else:
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
        result = self.encode_item_header(len(self.value) if self.value is not None else 0)

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
        (text_pos, _, length) = self.decode_item_header(data, start)

        # string
        result = None

        if length > 0:
            result = data[text_pos:text_pos + length]

        self.set(result)

        return text_pos + length


class SecsVarBoolean(SecsVar):
    """Secs type for boolean data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/boolean
    """
    formatCode = 011
    preferredTypes = [bool]

    _trueStrings = ["TRUE", "YES"]
    _falseStrings = ["FALSE", "NO"]

    def __init__(self, length=-1, value=None):
        super(SecsVarBoolean, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.value) == 0:
            return "<BOOLEAN>"

        data = ""

        for boolean in self.value:
            data += "{} ".format(boolean)

        return "<BOOLEAN {}>".format(data)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

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
            if self.length > 0 and len(value) > self.length:
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True
        elif isinstance(value, bytearray):
            if self.length > 0 and len(value) > self.length:
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

            self.value = value
            return

        raise ValueError("Can't convert value {}".format(value))

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: list/boolean
        """

        if isinstance(value, list) or isinstance(value, tuple):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            new_value = []
            for item in value:
                new_value.append(self.__convert_single_item(item))

            self.value = new_value
        elif isinstance(value, bytearray):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

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
        (text_pos, _, length) = self.decode_item_header(data, start)

        result = []

        for _ in range(length):
            result_text = data[text_pos]
            result.append(bool(struct.unpack(">b", result_text)[0]))

            text_pos += 1

        self.set(result)

        return text_pos


class SecsVarString(SecsVar):
    """Secs type for string data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: string
    """
    formatCode = 020
    preferredTypes = [str]

    def __init__(self, length=-1, value=""):
        super(SecsVarString, self).__init__()

        if value is None:
            value = ""

        self.value = ""
        self.length = length
        self.set(value)

    def __repr__(self):
        if len(self.value) == 0:
            return "<A>"

        printables = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        data = ""
        last_char_printable = False

        for char in self.value:
            if char in printables:
                if last_char_printable:
                    data += char
                else:
                    data += ' "' + char
                last_char_printable = True
            else:
                if last_char_printable:
                    data += '" ' + hex(ord(char))
                else:
                    data += ' ' + hex(ord(char))
                last_char_printable = False

        if last_char_printable:
            data += '"'

        return "<A{}>".format(data)

    def __len__(self):
        return len(self.value)

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
            if self.length > 0 and len(value) > self.length:
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False

            return True
        elif isinstance(value, bytearray):
            if self.length > 0 and len(value) > self.length:
                return False
            return True
        elif isinstance(value, str):
            if self.length > 0 and len(value) > self.length:
                return False
            return True
        elif isinstance(value, (int, long, float, complex)):
            if self.length > 0 and len(str(value)) > self.length:
                return False
            return True
        elif isinstance(value, unicode):
            if self.length > 0 and len(value) > self.length:
                return False
            try:
                value.decode('ascii')
            except Exception:
                return False

            return True
        else:
            return self.__check_single_item_support(value)

    def set(self, value):
        """Set the internal value to the provided value

        :param value: new value
        :type value: string
        """
        if value is None:
            raise ValueError("{} can't be None".format(self.__class__.__name__))

        if not isinstance(value, str) and \
          not isinstance(value, unicode) and \
          not isinstance(value, list) and \
          not isinstance(value, tuple) and \
          not isinstance(value, bytearray):
            value = str(value)

        if self.length > 0 and len(value) > self.length:
            raise ValueError("Value longer than {} chars ({} chars)".format(self.length, len(value)))

        if isinstance(value, list) or isinstance(value, tuple):
            self.value = ''.join(chr(e) for e in value)
        elif isinstance(value, unicode):
            self.value = value.encode('ascii')
        else:
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
        (text_pos, _, length) = self.decode_item_header(data, start)

        # string
        result = ""

        if length > 0:
            result = data[text_pos:text_pos + length]

        self.set(result)

        return text_pos + length


class SecsVarNumber(SecsVar):
    """Secs base type for numeric data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer/float
    """
    formatCode = 0
    _basetype = int
    _min = 0
    _max = 0
    _sml = ""
    _bytes = 0
    _structCode = ""

    def __init__(self, length=-1, value=None):
        super(SecsVarNumber, self).__init__()

        self.value = None
        self.length = length
        if value is not None:
            self.set(value)

    def __repr__(self):
        if len(self.value) == 0:
            return "<{}>".format(self._sml)

        data = ""

        for item in self.value:
            data += "{} ".format(item)

        return "<{} {}>".format(self._sml, data)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def __check_single_item_support(self, value):
        if isinstance(value, float) and self._basetype == int:
            return False

        if isinstance(value, bool):
            return True

        if isinstance(value, long) or isinstance(value, int) or isinstance(value, float):
            if value < self._min or value > self._max:
                return False
            return True

        if isinstance(value, str) or isinstance(value, unicode):
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
            if 0 <= self.length < len(value):
                return False
            for item in value:
                if not self.__check_single_item_support(item):
                    return False
            return True
        elif isinstance(value, bytearray):
            if 0 <= self.length < len(value):
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
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

            new_list = []
            for item in value:
                item = self._basetype(item)
                if item < self._min or item > self._max:
                    raise ValueError("Invalid value {}".format(item))

                new_list.append(item)
            self.value = new_list
        elif isinstance(value, bytearray):
            if 0 <= self.length < len(value):
                raise ValueError("Value longer than {} chars".format(self.length))

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

        for _ in range(length / self._bytes):
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

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 030
    _basetype = int
    _min = -9223372036854775808
    _max = 9223372036854775807
    _sml = "I8"
    _bytes = 8
    _structCode = "q"
    preferredTypes = [long, int]


class SecsVarI1(SecsVarNumber):
    """Secs type for 1 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 031
    _basetype = int
    _min = -128
    _max = 127
    _sml = "I1"
    _bytes = 1
    _structCode = "b"
    preferredTypes = [int, long]


class SecsVarI2(SecsVarNumber):
    """Secs type for 2 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 032
    _basetype = int
    _min = -32768
    _max = 32767
    _sml = "I2"
    _bytes = 2
    _structCode = "h"
    preferredTypes = [int, long]


class SecsVarI4(SecsVarNumber):
    """Secs type for 4 byte signed data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 034
    _basetype = int
    _min = -2147483648
    _max = 2147483647
    _sml = "I4"
    _bytes = 4
    _structCode = "l"
    preferredTypes = [int, long]


class SecsVarF8(SecsVarNumber):
    """Secs type for 8 byte float data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/float
    """
    formatCode = 040
    _basetype = float
    _min = -1.79769e+308
    _max = 1.79769e+308
    _sml = "F8"
    _bytes = 8
    _structCode = "d"
    preferredTypes = [float]


class SecsVarF4(SecsVarNumber):
    """Secs type for 4 byte float data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/float
    """
    formatCode = 044
    _basetype = float
    _min = -3.40282e+38
    _max = 3.40282e+38
    _sml = "F4"
    _bytes = 4
    _structCode = "f"
    preferredTypes = [float]


class SecsVarU8(SecsVarNumber):
    """Secs type for 8 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 050
    _basetype = int
    _min = 0
    _max = 18446744073709551615
    _sml = "U8"
    _bytes = 8
    _structCode = "Q"
    preferredTypes = [long, int]


class SecsVarU1(SecsVarNumber):
    """Secs type for 1 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 051
    _basetype = int
    _min = 0
    _max = 255
    _sml = "U1"
    _bytes = 1
    _structCode = "B"
    preferredTypes = [int, long]


class SecsVarU2(SecsVarNumber):
    """Secs type for 2 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 052
    _basetype = int
    _min = 0
    _max = 65535
    _sml = "U2"
    _bytes = 2
    _structCode = "H"
    preferredTypes = [int, long]


class SecsVarU4(SecsVarNumber):
    """Secs type for 4 byte unsigned data

    :param length: number of items this value
    :type length: integer
    :param value: initial value
    :type value: list/integer
    """
    formatCode = 054
    _basetype = int
    _min = 0
    _max = 4294967295
    _sml = "U4"
    _bytes = 4
    _structCode = "L"
    preferredTypes = [int, long]

SECSVARSAVAILABLE = [
    SecsVarList,
    SecsVarArray,
    SecsVarBinary,
    SecsVarBoolean,
    SecsVarI8,
    SecsVarI1,
    SecsVarI2,
    SecsVarI4,
    SecsVarF8,
    SecsVarF4,
    SecsVarU8,
    SecsVarU1,
    SecsVarU2,
    SecsVarU4
]
