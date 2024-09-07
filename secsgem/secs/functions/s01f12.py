#####################################################################
# s01f12.py
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
"""Class for stream 01 function 12."""

from secsgem.secs.data_items import SVID, SVNAME, UNITS
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS01F12(SecsStreamFunction):
    """status variable namelist - reply.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F12
        [
            {
                SVID: U1/U2/U4/U8/I1/I2/I4/I8/A
                SVNAME: A
                UNITS: A
            }
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"},
        ...     {"SVID": 1337, "SVNAME": "SV2", "UNITS": ""}])
        S1F12
          <L [2]
            <L [3]
              <U1 1 >
              <A "SV1">
              <A "mm">
            >
            <L [3]
              <U2 1337 >
              <A "SV2">
              <A>
            >
          > .

    Data Items:
        - :class:`SVID <secsgem.secs.data_items.SVID>`
        - :class:`SVNAME <secsgem.secs.data_items.SVNAME>`
        - :class:`UNITS <secsgem.secs.data_items.UNITS>`

    """

    _stream = 1
    _function = 12

    _data_format = [
        [
            SVID,
            SVNAME,
            UNITS,
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
