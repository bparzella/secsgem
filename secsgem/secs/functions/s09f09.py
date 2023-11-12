#####################################################################
# s09f09.py
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
"""Class for stream 09 function 09."""

from secsgem.secs.data_items import SHEAD
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS09F09(SecsStreamFunction):
    """transaction timer timeout.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F09
        SHEAD: B[10]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F09("HEADERDATA")
        S9F9
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    Data Items:
        - :class:`SHEAD <secsgem.secs.data_items.SHEAD>`

    """

    _stream = 9
    _function = 9

    _data_format = SHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
