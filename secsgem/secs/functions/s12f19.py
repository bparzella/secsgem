#####################################################################
# s12f19.py
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
"""Class for stream 12 function 19."""

from secsgem.secs.data_items import DATLC, MAPER
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F19(SecsStreamFunction):
    """map error report - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F19
        {
            MAPER: B[1]
            DATLC: U1
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F19({"MAPER": secsgem.secs.data_items.MAPER.INVALID_DATA, "DATLC": 0})
        S12F19
          <L [2]
            <B 0x1>
            <U1 0 >
          > .

    Data Items:
        - :class:`MAPER <secsgem.secs.data_items.MAPER>`
        - :class:`DATLC <secsgem.secs.data_items.DATLC>`

    """

    _stream = 12
    _function = 19

    _data_format = [
        MAPER,
        DATLC,
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
