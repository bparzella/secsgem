#####################################################################
# s02f46.py
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
"""Class for stream 02 function 46."""

from secsgem.secs.data_items import LIMITACK, LIMITID, LVACK, VID, VLAACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F46(SecsStreamFunction):
    """Define variable limit attributes - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F46
        {
            VLAACK: B[1]
            DATA: [
                {
                    VID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    LVACK: B[1]
                    DATA: {
                        LIMITID: B[1]
                        LIMITACK: B[1]
                    }
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F46({
        ...     "VLAACK": secsgem.secs.data_items.VLAACK.LIMIT_DEF_ERROR,
        ...     "DATA": [{
        ...         "VID": 2,
        ...         "LVACK": secsgem.secs.data_items.LVACK.VARIABLE_UNKNOWN,
        ...         "DATA": {
        ...             "LIMITID": 3,
        ...             "LIMITACK": secsgem.secs.data_items.LIMITACK.ASCII_ILLEGAL
        ...         }
        ...     }]})
        S2F46
          <L [2]
            <B 0x1>
            <L [1]
              <L [3]
                <U1 2 >
                <B 0x1>
                <L [2]
                  <B 0x3>
                  <B 0x6>
                >
              >
            >
          > .

    Data Items:
        - :class:`VLAACK <secsgem.secs.data_items.VLAACK>`
        - :class:`VID <secsgem.secs.data_items.VID>`
        - :class:`LVACK <secsgem.secs.data_items.LVACK>`
        - :class:`LIMITID <secsgem.secs.data_items.LIMITID>`
        - :class:`LIMITACK <secsgem.secs.data_items.LIMITACK>`

    """

    _stream = 2
    _function = 46

    _data_format = [
        VLAACK,
        [
            [
                VID,
                LVACK,
                [
                    LIMITID,
                    LIMITACK,
                ],
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
