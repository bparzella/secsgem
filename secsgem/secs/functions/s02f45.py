#####################################################################
# s02f45.py
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
"""Class for stream 02 function 45."""

from secsgem.secs.data_items import DATAID, LIMITID, LOWERDB, UPPERDB, VID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F45(SecsStreamFunction):
    """Define variable limit attributes.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F45
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATA: [
                {
                    VID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    DATA: [
                        {
                            LIMITID: B[1]
                            DATA: {
                                UPPERDB: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                                LOWERDB: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                            }
                        }
                        ...
                    ]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F45({
        ...     "DATAID": 1,
        ...     "DATA": [{
        ...         "VID": 2,
        ...         "DATA": [{
        ...             "LIMITID": 3,
        ...             "DATA": [30, 20]
        ...         }]
        ...     }]})
        S2F45 W
          <L [2]
            <U1 1 >
            <L [1]
              <L [2]
                <U1 2 >
                <L [1]
                  <L [2]
                    <B 0x3>
                    <L [2]
                      <U1 30 >
                      <U1 20 >
                    >
                  >
                >
              >
            >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`VID <secsgem.secs.data_items.VID>`
        - :class:`LIMITID <secsgem.secs.data_items.LIMITID>`
        - :class:`UPPERDB <secsgem.secs.data_items.UPPERDB>`
        - :class:`LOWERDB <secsgem.secs.data_items.LOWERDB>`

    """

    _stream = 2
    _function = 45

    _data_format = [
        DATAID,
        [
            [
                VID,
                [
                    [
                        LIMITID,
                        [
                            UPPERDB,
                            LOWERDB,
                        ],
                    ],
                ],
            ],
        ],
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
