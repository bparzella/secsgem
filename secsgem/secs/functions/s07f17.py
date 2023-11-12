#####################################################################
# s07f17.py
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
"""Class for stream 07 function 17."""

from secsgem.secs.data_items import PPID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS07F17(SecsStreamFunction):
    """delete process program - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F17
        [
            PPID: A/B[120]
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F17(["program1", "program2"])
        S7F17 W
          <L [2]
            <A "program1">
            <A "program2">
          > .

    Data Items:
        - :class:`PPID <secsgem.secs.data_items.PPID>`

    """

    _stream = 7
    _function = 17

    _data_format = [PPID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
