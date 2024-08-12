#####################################################################
# dynamic.py
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

from .array import Array
from .base import Base
from .binary import Binary
from .boolean import Boolean
from .f4 import F4
from .f8 import F8
from .i1 import I1
from .i2 import I2
from .i4 import I4
from .i8 import I8
from .string import String
from .u1 import U1
from .u2 import U2
from .u4 import U4
from .u8 import U8


class Dynamic(Base):
    """Variable with interchangable type."""

    def __init__(self, types, value=None, count=-1):
        """Initialize a dynamic secs variable.

        :param types: list of supported types, default first. empty means all types are support, String default
        :type types: list of :class:`secsgem.secs.variables.Base` classes
        :param value: initial value
        :type value: various
        :param count: max number of items in type
        :type count: integer
        """
        super().__init__()

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
        if isinstance(other, Dynamic):
            return other.value.value == self.value.value
        if isinstance(other, Base):
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

        return typ in self.types

    @property
    def preferred_type(self):
        """Get the preferred type."""
        types = []
        for typ in self.types:
            types += typ.preferred_types

        return types[0]

    def set(self, value):
        """Set the internal value to the provided value.

        In doubt provide the variable wrapped in the matching :class:`secsgem.secs.variables.Base` class,
        to avoid confusion.

        Example:
            >>> import secsgem.secs
            >>>
            >>> var = secsgem.secs.variables.Dynamic([secsgem.secs.variables.String,
            ...                                       secsgem.secs.variables.U1])
            >>> var.set(secsgem.secs.variables.U1(10))
            >>> var
            <U1 10 >

        If no type is provided the default type is used which might not be the expected type.

        :param value: new value
        :type value: various
        """
        if isinstance(value, Base):
            if isinstance(value, Dynamic):
                if not isinstance(value.value, tuple(self.types)) and self.types:
                    raise ValueError(
                        f"Unsupported type {value.value.__class__.__name__} "
                        f"for this instance of Dynamic, allowed {self.types}")

                self.value = value.value
            else:
                if not isinstance(value, tuple(self.types)) and self.types:
                    raise ValueError(
                        f"Unsupported type {value.__class__.__name__} "
                        f"for this instance of Dynamic, allowed {self.types}")

                self.value = value
        else:
            matched_type = self._match_type(value)

            if matched_type is None:
                raise ValueError(
                    f'Value "{value}" of type {value.__class__.__name__} not valid for SecsDynamic with {self.types}')

            self.value = matched_type(count=self.count)
            self.value.set(value)

    def get(self):
        """Return the internal value.

        :returns: internal value
        :rtype: various
        """
        if self.value is not None:
            return self.value.get()

        return None

    def encode(self):
        """Encode the value to secs data.

        :returns: encoded data bytes
        :rtype: string
        """
        return self.value.encode()

    def decode(self, data, start=0):
        """Decode the secs byte data to the value.

        :param data: encoded data bytes
        :type data: string
        :param start: start position of value the data
        :type start: integer
        :returns: new start position
        :rtype: integer
        """
        (_, format_code, _) = self.decode_item_header(data, start)

        format_codes = {
            Array.format_code: Array,
            Binary.format_code: Binary,
            Boolean.format_code: Boolean,
            String.format_code: String,
            I8.format_code: I8,
            I1.format_code: I1,
            I2.format_code: I2,
            I4.format_code: I4,
            F8.format_code: F8,
            F4.format_code: F4,
            U8.format_code: U8,
            U1.format_code: U1,
            U2.format_code: U2,
            U4.format_code: U4,
        }

        if format_code not in format_codes or not self.__type_supported(format_codes[format_code]):
            raise ValueError(
                f"Unsupported format {format_code} for this instance of Dynamic, allowed {self.types}")

        typ = format_codes[format_code]
        if typ == Array:
            self.value = Array(ANYVALUE)
        else:
            self.value = typ(count=self.count)

        return self.value.decode(data, start)

    def _match_type(self, value):
        var_types = self.types
        # if no types are set use internal order
        if not self.types:
            var_types = [Boolean, U1, U2, U4, U8, I1, I2, I4,
                         I8, F4, F8, String, Binary]

        # first try to find the preferred type for the kind of value
        for var_type in var_types:
            if isinstance(value, tuple(var_type.preferred_types)) and var_type(count=self.count).supports_value(value):
                return var_type

        # when no preferred type was found, then try to match any available type
        for var_type in var_types:
            if var_type(count=self.count).supports_value(value):
                return var_type

        return None

    @property
    def is_dynamic(self) -> bool:
        """Check if this instance is Dynamic or derived."""
        return True


class ANYVALUE(Dynamic):
    """Dummy data item for generation of unknown types.

    :Types:
       - :class:`Array <secsgem.secs.variables.Array>`
       - :class:`Binary <secsgem.secs.variables.Binary>`
       - :class:`Boolean <secsgem.secs.variables.Boolean>`
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`
       - :class:`F8 <secsgem.secs.variables.F8>`
       - :class:`F4 <secsgem.secs.variables.F4>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    """

    def __init__(self, value=None):
        """Initialize an ANYVALUE variable.

        :param value: value of the variable
        """
        self.name = self.__class__.__name__

        super().__init__([Array, Boolean, U1, U2, U4, U8, I1, I2, I4, I8, F4, F8, String, Binary], value=value)
