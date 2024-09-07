#####################################################################
# base.py
#
# (c) Copyright 2015-2021, Benjamin Parzella. All rights reserved.
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
"""Base class for for SECS stream and functions."""
from __future__ import annotations

import typing

import secsgem.common
from secsgem.secs.data_items import DataItemBase
from secsgem.secs.variables import functions

DataItemRecursive = typing.Union[typing.Type[DataItemBase], typing.Iterable["DataItemRecursive"]]


class StructureDisplayingMeta(type):
    """Meta class overriding the default __repr__ of a class."""

    def __repr__(cls):
        """Generate textual representation for an object of this class."""
        return cls.get_format()


class _ClassProperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class SecsStreamFunction(metaclass=StructureDisplayingMeta):  # pylint: disable=too-many-instance-attributes
    """Secs stream and function base class.

    This class is inherited to create a stream/function class.
    To create a function specific content the class variables :attr:`_stream`, :attr:`_function`
    and :attr:`_data_format` must be overridden.
    """

    _stream = 0
    _function = 0

    _data_format: DataItemRecursive | None = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False

    def __init__(self, value=None):
        """Initialize a stream function object.

        Example:
            class SecsS02F30(SecsStreamFunction):
                _stream = 2
                _function = 30

                _to_host = True
                _to_equipment = False

                _has_reply = False
                _is_reply_required = False

                _is_multi_block = True

                _data_format = [
                    [
                        ECID,
                        ECNAME,
                        ECMIN,
                        ECMAX,
                        ECDEF,
                        UNITS
                    ]
                ]

        :param value: set the value of stream/function parameters
        :type value: various
        """
        self.data = functions.generate(self._data_format)

        self.data_format = self._data_format
        self.to_host = self._to_host
        self.to_equipment = self._to_equipment

        self.has_reply = self._has_reply
        self.is_reply_required = self._is_reply_required

        self.is_multi_block = self._is_multi_block

        if value is not None and self.data is not None:
            self.data.set(value)

        self._object_intitialized = True

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        function = f"S{self.stream}F{self.function}"
        if self.data is None:
            return f"{function}{' W' if self._is_reply_required else ''} ."
        data = f"{self.data}"

        return f"{function}{' W' if self._is_reply_required else ''}\n{secsgem.common.indent_block(data)} ."

    def __getitem__(self, key):
        """Get an item using the indexer operator."""
        return self.data[key]

    def __setitem__(self, key, item):
        """Set an item using the indexer operator."""
        self.data[key] = item

    def __len__(self):
        """Get the length."""
        return len(self.data)

    def __getattr__(self, item):
        """Get an item as object member."""
        return self.data.__getattr__(item)

    def __setattr__(self, item, value):
        """Set an item as object member."""
        if "_object_intitialized" not in self.__dict__:
            dict.__setattr__(self, item, value)
            return

        if item in self.data.data:
            self.data.__setattr__(item, value)
            return

    def append(self, data):
        """Append data to list, if stream/function parameter is a list.

        :param data: list item to add
        :type data: various
        """
        if hasattr(self.data, "append") and callable(self.data.append):
            self.data.append(data)
        else:
            raise AttributeError(
                f"class {self.__class__.__name__} has no attribute 'append'")

    def encode(self):
        """Generate the encoded hsms data of the stream/function parameter.

        :returns: encoded data
        :rtype: string
        """
        if self.data is None:
            return b""

        return self.data.encode()

    def decode(self, data):
        """Update stream/function parameter data from the passed data.

        :param data: encoded data
        :type data: string
        """
        if self.data is not None:
            self.data.decode(data)

    def set(self, value):
        """Update the value of the stream/function parameter.

        :param value: new value for the parameter
        :type value: various
        """
        self.data.set(value)

    def get(self):
        """Get the current value of the stream/function parameter.

        :returns: current parameter value
        :rtype: various
        """
        if self.data is None:
            return None

        return self.data.get()

    @classmethod
    def get_format(cls):
        """Get the format of the function.

        :returns: returns the string representation of the function
        :rtype: string
        """
        if cls._data_format is not None:
            return functions.get_format(cls._data_format)

        return "Header only"

    @_ClassProperty
    def stream(self) -> int:
        """Get the stream number of this function."""
        return self._stream

    @_ClassProperty
    def function(self) -> int:
        """Get the function number of this function."""
        return self._function
