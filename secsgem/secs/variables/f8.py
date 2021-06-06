#####################################################################
# f8.py
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
"""SECS 8 byte float variable type."""

from .base_number import BaseNumber


class F8(BaseNumber):
    """
    Secs type for 8 byte float data.

    :param value: initial value
    :type value: list/float
    :param count: number of items this value
    :type count: integer
    """

    format_code = 0o40
    text_code = "F8"
    _base_type = float
    _min = -1.79769e+308
    _max = 1.79769e+308
    _bytes = 8
    _struct_code = "d"
    preferred_types = [float]