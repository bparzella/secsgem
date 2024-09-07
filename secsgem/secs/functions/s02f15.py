#####################################################################
# s02f15.py
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
"""Class for stream 02 function 15."""

from secsgem.secs.data_items import ECID, ECV
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F15(SecsStreamFunction):
    """new equipment constant - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F15
        [
            {
                ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
                ECV: L/BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
            }
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F15([
        ...     {"ECID": 1, "ECV": secsgem.secs.variables.U4(10)},
        ...     {"ECID": "1337", "ECV": "text"}])
        S2F15 W
          <L [2]
            <L [2]
              <U1 1 >
              <U4 10 >
            >
            <L [2]
              <A "1337">
              <A "text">
            >
          > .

    Data Items:
        - :class:`ECID <secsgem.secs.data_items.ECID>`
        - :class:`ECV <secsgem.secs.data_items.ECV>`

    """

    _stream = 2
    _function = 15

    _data_format = [
        [
            ECID,
            ECV,
        ],
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
