#####################################################################
# string.py
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
"""SECS string text variable type."""

import unicodedata

from .base_text import BaseText


class String(BaseText):
    """
    Secs type for string data.

    :param value: initial value
    :type value: string
    :param count: number of items this value
    :type count: integer
    """

    format_code = 0o20
    text_code = u"A"
    preferred_types = [bytes, str]
    control_chars = u"".join(chr(ch) for ch in range(256) if unicodedata.category(chr(ch))[0] == "C" or ch > 127)
    coding = "latin-1"