#####################################################################
# s06f08.py
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
"""Class for stream 06 function 08."""

from secsgem.secs.data_items import CEID, DATAID, DSID, DVNAME, DVVAL
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F08(SecsStreamFunction):
    """data transfer data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F08
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DS: [
                {
                    DSID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    DV: [
                        {
                            DVNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                            DVVAL: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        }
                        ...
                    ]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F08({
        ...     "DATAID": 1,
        ...     "CEID": 1337,
        ...     "DS": [{
        ...         "DSID": 1000,
        ...         "DV": [
        ...             {"DVNAME": "VAR1", "DVVAL": "VAR"},
        ...             {"DVNAME": "VAR2", "DVVAL": secsgem.secs.variables.U4(100)}]}]})
        S6F8
          <L [3]
            <U1 1 >
            <U2 1337 >
            <L [1]
              <L [2]
                <U2 1000 >
                <L [2]
                  <L [2]
                    <A "VAR1">
                    <A "VAR">
                  >
                  <L [2]
                    <A "VAR2">
                    <U4 100 >
                  >
                >
              >
            >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`CEID <secsgem.secs.data_items.CEID>`
        - :class:`DSID <secsgem.secs.data_items.DSID>`
        - :class:`DVNAME <secsgem.secs.data_items.DVNAME>`
        - :class:`DVVAL <secsgem.secs.data_items.DVVAL>`

    """

    _stream = 6
    _function = 8

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "DS",
                DSID,
                [
                    [
                        "DV",
                        DVNAME,
                        DVVAL,
                    ],
                ],
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
