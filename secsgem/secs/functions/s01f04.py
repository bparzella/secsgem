#####################################################################
# s01f04.py
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
"""Class for stream 01 function 04."""

from secsgem.secs.data_items import SV
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS01F04(SecsStreamFunction):
    """selected equipment status - data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F04
        [
            SV: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F04([secsgem.secs.variables.U1(1), "text", secsgem.secs.variables.U4(1337)])
        S1F4
          <L [3]
            <U1 1 >
            <A "text">
            <U4 1337 >
          > .

    Data Items:
        - :class:`SV <secsgem.secs.data_items.SV>`

    """

    _stream = 1
    _function = 4

    _data_format = [SV]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
