#####################################################################
# s07f01.py
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
"""Class for stream 07 function 01."""

from secsgem.secs.data_items import LENGTH, PPID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS07F01(SecsStreamFunction):
    """process program load - inquire.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F01
        {
            PPID: A/B[120]
            LENGTH: U1/U2/U4/U8/I1/I2/I4/I8
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F01({"PPID": "program", "LENGTH": 4})
        S7F1 W
          <L [2]
            <A "program">
            <U1 4 >
          > .

    Data Items:
        - :class:`PPID <secsgem.secs.data_items.PPID>`
        - :class:`LENGTH <secsgem.secs.data_items.LENGTH>`

    """

    _stream = 7
    _function = 1

    _data_format = [
        PPID,
        LENGTH,
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
