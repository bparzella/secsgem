#####################################################################
# s01f15.py
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
"""Class for stream 01 function 15."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS01F15(SecsStreamFunction):
    """request offline.

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F15
        Header only

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F15()
        S1F15 W .

    """

    _stream = 1
    _function = 15

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
