#####################################################################
# s02f48.py
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
"""Class for stream 02 function 48."""

from secsgem.secs.data_items import LIMITID, LIMITMAX, LIMITMIN, LOWERDB, UNITS, UPPERDB, VID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F48(SecsStreamFunction):
    """Define variable limit attributes - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F48
        [
            {
                VID: U1/U2/U4/U8/I1/I2/I4/I8/A
                DATA: {
                    UNITS: A
                    LIMITMIN: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                    LIMITMAX: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                    DATA: [
                        {
                            LIMITID: B[1]
                            UPPERDB: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                            LOWERDB: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A[1]
                        }
                        ...
                    ]
                }
            }
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F48([{
        ...     "VID": 1,
        ...     "DATA": {
        ...         "UNITS": "meters",
        ...         "LIMITMIN": 10,
        ...         "LIMITMAX": 20,
        ...         "DATA": [{
        ...             "LIMITID": 3,
        ...             "UPPERDB": 50,
        ...             "LOWERDB": 5
        ...         }]
        ...     }}])
        S2F48
          <L [1]
            <L [2]
              <U1 1 >
              <L [4]
                <A "meters">
                <U1 10 >
                <U1 20 >
                <L [1]
                  <L [3]
                    <B 0x3>
                    <U1 50 >
                    <U1 5 >
                  >
                >
              >
            >
          > .

    Data Items:
        - :class:`VID <secsgem.secs.data_items.VID>`
        - :class:`UNITS <secsgem.secs.data_items.UNITS>`
        - :class:`LIMITMIN <secsgem.secs.data_items.LIMITMIN>`
        - :class:`LIMITMAX <secsgem.secs.data_items.LIMITMAX>`
        - :class:`LIMITID <secsgem.secs.data_items.LIMITID>`
        - :class:`UPPERDB <secsgem.secs.data_items.UPPERDB>`
        - :class:`LOWERDB <secsgem.secs.data_items.LOWERDB>`

    """

    _stream = 2
    _function = 48

    _data_format = [
        [
            VID,
            [
                UNITS,
                LIMITMIN,
                LIMITMAX,
                [
                    [
                        LIMITID,
                        UPPERDB,
                        LOWERDB,
                    ],
                ],
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
