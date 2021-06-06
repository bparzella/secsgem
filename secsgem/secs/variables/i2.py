#####################################################################
# i2.py
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
"""SECS 2 byte signed integer variable type."""

from .base_number import BaseNumber


class I2(BaseNumber):
    """
    Secs type for 2 byte signed data.

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    format_code = 0o32
    text_code = "I2"
    _base_type = int
    _min = -32768
    _max = 32767
    _bytes = 2
    _struct_code = "h"
    preferred_types = [int]