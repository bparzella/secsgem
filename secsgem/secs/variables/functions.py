#####################################################################
# functions.py
#
# (c) Copyright 2021-2023, Benjamin Parzella. All rights reserved.
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

from .base import Base


def generate(data_format):
    """Generate actual variable from data format.

    :param data_format: data format to create variable for
    :type data_format: list/Base based class
    :returns: created variable
    :rtype: Base based class
    """
    from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import
    from .list_type import List  # pylint: disable=import-outside-toplevel,cyclic-import

    if data_format is None:
        return None

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return Array(data_format[0])
        return List(data_format)
    if inspect.isclass(data_format):
        if issubclass(data_format, Base):
            return data_format()
        raise TypeError(f"Can't generate item of class {data_format.__name__}")
    raise TypeError(f"Can't handle item of class {data_format.__class__.__name__}")


def get_format(data_format, showname=False):
    """Get the format of the function.

    :returns: returns the string representation of the function
    :rtype: string
    """
    del showname  # unused variable

    from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import
    from .list_type import List  # pylint: disable=import-outside-toplevel,cyclic-import

    if data_format is None:
        return None

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return Array.get_format(data_format[0])
        return List.get_format(data_format)

    if inspect.isclass(data_format):
        if issubclass(data_format, Base):
            return data_format.get_format()
        raise TypeError(f"Can't generate data_format for class {data_format.__name__}")

    raise TypeError(f"Can't handle item of class {data_format.__class__.__name__}")
