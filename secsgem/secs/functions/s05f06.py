#####################################################################
# s05f06.py
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
"""Class for stream 05 function 06."""

from secsgem.secs.data_items import ALCD, ALID, ALTX
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F06(SecsStreamFunction):
    """list alarms - data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F06
        [
            {
                ALCD: B[1]
                ALID: U1/U2/U4/U8/I1/I2/I4/I8
                ALTX: A[120]
            }
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F06([
        ...     {"ALCD": secsgem.secs.data_items.ALCD.PERSONAL_SAFETY |
        ...              secsgem.secs.data_items.ALCD.ALARM_SET,
        ...      "ALID": 100,
        ...      "ALTX": "text"}])
        S5F6
          <L [1]
            <L [3]
              <B 0x81>
              <U1 100 >
              <A "text">
            >
          > .

    Data Items:
        - :class:`ALCD <secsgem.secs.data_items.ALCD>`
        - :class:`ALID <secsgem.secs.data_items.ALID>`
        - :class:`ALTX <secsgem.secs.data_items.ALTX>`

    """

    _stream = 5
    _function = 6

    _data_format = [
        [
            ALCD,
            ALID,
            ALTX,
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
