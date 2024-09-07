#####################################################################
# s12f11.py
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
"""Class for stream 12 function 11."""

from secsgem.secs.data_items import BINLT, IDTYP, MID, XYPOS
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F11(SecsStreamFunction):
    """map data type 3 - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F11
        {
            MID: A/B[80]
            IDTYP: B[1]
            DATA: [
                {
                    XYPOS: I1/I2/I4/I8[2]
                    BINLT: U1/A
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F11({
        ...     "MID": "materialID",
        ...     "IDTYP": secsgem.secs.data_items.IDTYP.WAFER,
        ...     "DATA": [
        ...         {"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]},
        ...         {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F11 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I1 1 2 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I1 3 4 >
                <U1 5 6 7 8 >
              >
            >
          > .

    Data Items:
        - :class:`MID <secsgem.secs.data_items.MID>`
        - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
        - :class:`XYPOS <secsgem.secs.data_items.XYPOS>`
        - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    """

    _stream = 12
    _function = 11

    _data_format = [
        MID,
        IDTYP,
        [
            [
                XYPOS,
                BINLT,
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
