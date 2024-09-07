#####################################################################
# s12f15.py
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
"""Class for stream 12 function 15."""

from secsgem.secs.data_items import IDTYP, MID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F15(SecsStreamFunction):
    """map data type 2 - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F15
        {
            MID: A/B[80]
            IDTYP: B[1]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F15({"MID": "materialID", "IDTYP": secsgem.secs.data_items.IDTYP.WAFER})
        S12F15 W
          <L [2]
            <A "materialID">
            <B 0x0>
          > .

    Data Items:
        - :class:`MID <secsgem.secs.data_items.MID>`
        - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`

    """

    _stream = 12
    _function = 15

    _data_format = [
        MID,
        IDTYP,
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
