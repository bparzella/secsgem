#####################################################################
# base.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
# pylint: disable=non-parent-init-called
"""Data item base class."""
from __future__ import annotations

from secsgem.secs import variables


class DataItemMeta(type):
    """Meta class for data items."""

    def __new__(cls, name, bases, attrs):
        """Meta class creation."""
        if name != "DataItemBase":
            bases += (attrs["__type__"], )
        return type.__new__(cls, name, bases, attrs)


class DataItemBase(metaclass=DataItemMeta):
    """Base class for data items.

    It provides type and output handling.
    """

    __type__: type[variables.Base] | None = None
    __allowedtypes__: list[type[variables.Base]] | None = None
    __count__ = -1

    def __init__(self, value=None):
        """Initialize a data item.

        :param value: Value of the data item
        """
        self.name = self.__class__.__name__

        if self.__type__ is variables.Dynamic:
            self.__type__.__init__(self, self.__allowedtypes__, value, self.__count__)
        else:
            self.__type__.__init__(self, value, self.__count__)

    @property
    def typ(self) -> type[variables.Base] | None:
        """Get the configured type."""
        return self.__type__

    @classmethod
    def get_format(cls, showname=True) -> str:
        """Format the contents as a string.

        Args:
            showname: Display the real class name when True

        Returns:
            Formatted value string

        """
        clsname = format(cls.__name__) if showname else "DATA"

        if cls.__type__ is variables.Dynamic:
            if cls.__count__ > 0:
                return f"{clsname}: {'/'.join([x.text_code for x in cls.__allowedtypes__])}[{cls.__count__}]"

            return f"{clsname}: {'/'.join([x.text_code for x in cls.__allowedtypes__])}"

        if cls.__count__ > 0:
            return f"{clsname}: {cls.__type__.text_code}[{cls.__count__}]"

        return f"{clsname}: {cls.__type__.text_code}"
