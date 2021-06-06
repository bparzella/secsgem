#####################################################################
# secs_var_dynamic.py
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
"""SECS dynamic variable type."""

from .secs_var import SecsVar
from .secs_var_list import SecsVarArray
from .secs_var_binary import SecsVarBinary
from .secs_var_boolean import SecsVarBoolean
from .secs_var_string import SecsVarString
from .secs_var_u1 import SecsVarU1
from .secs_var_u2 import SecsVarU2
from .secs_var_u4 import SecsVarU4
from .secs_var_u8 import SecsVarU8
from .secs_var_i1 import SecsVarI1
from .secs_var_i2 import SecsVarI2
from .secs_var_i4 import SecsVarI4
from .secs_var_i8 import SecsVarI8
from .secs_var_f4 import SecsVarF4
from .secs_var_f8 import SecsVarF8


class SecsVarDynamic(SecsVar):
    """Variable with interchangable type."""

    def __init__(self, types, value=None, count=-1):
        """
        Initialize a dynamic secs variable.

        :param types: list of supported types, default first. empty means all types are support, SecsVarString default
        :type types: list of :class:`secsgem.secs.variables.SecsVar` classes
        :param value: initial value
        :type value: various
        :param count: max number of items in type
        :type count: integer
        """
        super(SecsVarDynamic, self).__init__()

        self.value = None

        self.types = types
        self.count = count
        if value is not None:
            self.set(value)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return self.value.__repr__()

    def __len__(self):
        """Get the length."""
        return self.value.__len__()

    def __getitem__(self, key):
        """Get an item using the indexer operator."""
        return self.value.__getitem__(key)

    def __setitem__(self, key, item):
        """Set an item using the indexer operator."""
        self.value.__setitem__(key, item)

    def __eq__(self, other):
        """Check equality with other object."""
        if isinstance(other, SecsVarDynamic):
            return other.value.value == self.value.value
        if isinstance(other, SecsVar):
            return other.value == self.value.value
        if isinstance(other, list):
            return other == self.value.value
        if isinstance(other, (bytes, str)) and isinstance(self.value.value, (bytes, str)):
            return str(other) == str(self.value.value)

        return [other] == self.value.value

    def __hash__(self):
        """Get data item for hashing."""
        if isinstance(self.value.value, list):
            return hash(self.value.value[0])
        return hash(self.value.value)

    def __type_supported(self, typ):
        if not self.types:
            return True

        if typ in self.types:
            return True

        return False

    def set(self, value):
        """
        Set the internal value to the provided value.

        In doubt provide the variable wrapped in the matching :class:`secsgem.secs.variables.SecsVar` class,
        to avoid confusion.

        **Example**::

            >>> import secsgem
            >>>
            >>> var = secsgem.SecsVarDynamic([secsgem.secs.variables.SecsVarString,
            ...                               secsgem.secs.variables.SecsVarU1])
            >>> var.set(secsgem.secs.variables.SecsVarU1(10))
            >>> var
            <U1 10 >

        If no type is provided the default type is used which might not be the expected type.

        :param value: new value
        :type value: various
        """
        if isinstance(value, SecsVar):
            if isinstance(value, SecsVarDynamic):
                if not isinstance(value.value, tuple(self.types)) and self.types:
                    raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}"
                                     .format(value.value.__class__.__name__, self.types))

                self.value = value.value
            else:
                if not isinstance(value, tuple(self.types)) and self.types:
                    raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}"
                                     .format(value.__class__.__name__, self.types))

                self.value = value
        else:
            matched_type = self._match_type(value)

            if matched_type is None:
                raise ValueError('Value "{}" of type {} not valid for SecsDynamic with {}'
                                 .format(value, value.__class__.__name__, self.types))

            self.value = matched_type(count=self.count)
            self.value.set(value)

    def get(self):
        """
        Return the internal value.

        :returns: internal value
        :rtype: various
        """
        if self.value is not None:
            return self.value.get()

        return None

    def encode(self):
        """
        Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        return self.value.encode()

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
        (_, format_code, _) = self.decode_item_header(data, start)

        if format_code == SecsVarArray.format_code and self.__type_supported(SecsVarArray):
            self.value = SecsVarArray(ANYVALUE)
        elif format_code == SecsVarBinary.format_code and self.__type_supported(SecsVarBinary):
            self.value = SecsVarBinary(count=self.count)
        elif format_code == SecsVarBoolean.format_code and self.__type_supported(SecsVarBoolean):
            self.value = SecsVarBoolean(count=self.count)
        elif format_code == SecsVarString.format_code and self.__type_supported(SecsVarString):
            self.value = SecsVarString(count=self.count)
        elif format_code == SecsVarI8.format_code and self.__type_supported(SecsVarI8):
            self.value = SecsVarI8(count=self.count)
        elif format_code == SecsVarI1.format_code and self.__type_supported(SecsVarI1):
            self.value = SecsVarI1(count=self.count)
        elif format_code == SecsVarI2.format_code and self.__type_supported(SecsVarI2):
            self.value = SecsVarI2(count=self.count)
        elif format_code == SecsVarI4.format_code and self.__type_supported(SecsVarI4):
            self.value = SecsVarI4(count=self.count)
        elif format_code == SecsVarF8.format_code and self.__type_supported(SecsVarF8):
            self.value = SecsVarF8(count=self.count)
        elif format_code == SecsVarF4.format_code and self.__type_supported(SecsVarF4):
            self.value = SecsVarF4(count=self.count)
        elif format_code == SecsVarU8.format_code and self.__type_supported(SecsVarU8):
            self.value = SecsVarU8(count=self.count)
        elif format_code == SecsVarU1.format_code and self.__type_supported(SecsVarU1):
            self.value = SecsVarU1(count=self.count)
        elif format_code == SecsVarU2.format_code and self.__type_supported(SecsVarU2):
            self.value = SecsVarU2(count=self.count)
        elif format_code == SecsVarU4.format_code and self.__type_supported(SecsVarU4):
            self.value = SecsVarU4(count=self.count)
        else:
            raise ValueError(
                "Unsupported format {} for this instance of SecsVarDynamic, allowed {}".format(
                    format_code,
                    self.types))

        return self.value.decode(data, start)

    def _match_type(self, value):
        var_types = self.types
        # if no types are set use internal order
        if not self.types:
            var_types = [SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4,
                         SecsVarI8, SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]

        # first try to find the preferred type for the kind of value
        for var_type in var_types:
            if isinstance(value, tuple(var_type.preferred_types)):
                if var_type(count=self.count).supports_value(value):
                    return var_type

        # when no preferred type was found, then try to match any available type
        for var_type in var_types:
            if var_type(count=self.count).supports_value(value):
                return var_type

        return None

    @property
    def is_dynamic(self) -> bool:
        """Check if this instance is SecsVarDynamic or derived."""
        return True


class ANYVALUE(SecsVarDynamic):
    """
    Dummy data item for generation of unknown types.

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
        """
        Initialize an ANYVALUE variable.

        :param value: value of the variable
        """
        self.name = self.__class__.__name__

        super(ANYVALUE, self).__init__([SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8,
                                        SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarF4, SecsVarF8,
                                        SecsVarString, SecsVarBinary], value=value)
