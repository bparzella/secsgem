#####################################################################
# s02f14.py
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
"""Class for stream 02 function 14."""

from secsgem.secs.data_items import ECV
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F14(SecsStreamFunction):
    """equipment constant - data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F14
        [
            ECV: L/BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F14([secsgem.secs.variables.U1(1), "text"])
        S2F14
          <L [2]
            <U1 1 >
            <A "text">
          > .

    Data Items:
        - :class:`ECV <secsgem.secs.data_items.ECV>`

    """

    _stream = 2
    _function = 14

    _data_format = [ECV]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
