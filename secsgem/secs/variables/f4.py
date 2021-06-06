#####################################################################
# f4.py
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
"""SECS 4 byte float variable type."""

from .base_number import BaseNumber


class F4(BaseNumber):
    """
    Secs type for 4 byte float data.

    :param value: initial value
    :type value: list/float
    :param count: number of items this value
    :type count: integer
    """

    format_code = 0o44
    text_code = "F4"
    _base_type = float
    _min = -3.40282e+38
    _max = 3.40282e+38
    _bytes = 4
    _struct_code = "f"
    preferred_types = [float]