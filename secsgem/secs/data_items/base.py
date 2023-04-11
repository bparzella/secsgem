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
import typing

from .. import variables


class DataItemMeta(type):
    """Meta class for data items."""

    def __new__(mcs, name, bases, attrs):
        if name != "DataItemBase":
            bases += (attrs["__type__"], )
        return type.__new__(mcs, name, bases, attrs)


class DataItemBase(metaclass=DataItemMeta):
    """
    Base class for data items.

    It provides type and output handling.
    """

    __type__: typing.Optional[typing.Type[variables.Base]] = None
    __allowedtypes__: typing.Optional[typing.List[typing.Type[variables.Base]]] = None
    __count__ = -1

    def __init__(self, value=None):
        """
        Initialize a data item.

        :param value: Value of the data item
        """
        self.name = self.__class__.__name__

        if self.__type__ is variables.Dynamic:
            self.__type__.__init__(self, self.__allowedtypes__, value, self.__count__)
        else:
            self.__type__.__init__(self, value, self.__count__)

    @classmethod
    def get_format(cls, showname=True):
        """
        Format the contents as a string.

        :param showname: Display the real class name when True
        :return: Formatted value string
        """
        if showname:
            clsname = format(cls.__name__)
        else:
            clsname = "DATA"

        if cls.__type__ is variables.Dynamic:
            if cls.__count__ > 0:
                return f"{clsname}: {'/'.join([x.text_code for x in cls.__allowedtypes__])}[{cls.__count__}]"

            return f"{clsname}: {'/'.join([x.text_code for x in cls.__allowedtypes__])}"

        if cls.__count__ > 0:
            return f"{clsname}: {cls.text_code}[{cls.__count__}]"

        return f"{clsname}: {cls.text_code}"
