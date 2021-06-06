#####################################################################
# i8.py
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
"""SECS 8 byte signed integer variable type."""

from .base_number import BaseNumber


class I8(BaseNumber):
    """
    Secs type for 8 byte signed data.

    :param value: initial value
    :type value: list/integer
    :param count: number of items this value
    :type count: integer
    """

    format_code = 0o30
    text_code = "I8"
    _base_type = int
    _min = -9223372036854775808
    _max = 9223372036854775807
    _bytes = 8
    _struct_code = "q"
    preferred_types = [int]