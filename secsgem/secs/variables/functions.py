#####################################################################
# functions.py
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
"""SECS variable helper functions."""

import inspect

from . import base
from . import list_type  # pylint: disable=cyclic-import
from . import array  # pylint: disable=cyclic-import


def generate(data_format):
    """
    Generate actual variable from data format.

    :param data_format: data format to create variable for
    :type data_format: list/Base based class
    :returns: created variable
    :rtype: Base based class
    """
    if data_format is None:
        return None

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return array.Array(data_format[0])
        return list_type.List(data_format)
    if inspect.isclass(data_format):
        if issubclass(data_format, base.Base):
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
            return array.Array.get_format(data_format[0])
        return list_type.List.get_format(data_format)

    if inspect.isclass(data_format):
        if issubclass(data_format, base.Base):
            return data_format.get_format()
        raise TypeError("Can't generate data_format for class {}".format(data_format.__name__))

    raise TypeError("Can't handle item of class {}".format(data_format.__class__.__name__))
