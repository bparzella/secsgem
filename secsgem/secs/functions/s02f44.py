#####################################################################
# s02f44.py
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
"""Class for stream 02 function 44."""

from secsgem.secs.data_items import FCNID, RSPACK, STRACK, STRID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F44(SecsStreamFunction):
    """reset spooling - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F44
        {
            RSPACK: B[1]
            DATA: [
                {
                    STRID: U1[1]
                    STRACK: B[1]
                    FCNID: [
                        DATA: U1[1]
                        ...
                    ]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F44({
        ...     "RSPACK": secsgem.secs.data_items.RSPACK.REJECTED,
        ...     "DATA": [
        ...         {"STRID": 1, "STRACK": secsgem.secs.data_items.STRACK.NOT_ALLOWED, "FCNID": [10]},
        ...         {"STRID": 2, "STRACK": secsgem.secs.data_items.STRACK.FUNCTION_UNKNOWN, "FCNID": [20]}]})
        S2F44
          <L [2]
            <B 0x1>
            <L [2]
              <L [3]
                <U1 1 >
                <B 0x1>
                <L [1]
                  <U1 10 >
                >
              >
              <L [3]
                <U1 2 >
                <B 0x3>
                <L [1]
                  <U1 20 >
                >
              >
            >
          > .

    Data Items:
        - :class:`RSPACK <secsgem.secs.data_items.RSPACK>`
        - :class:`STRID <secsgem.secs.data_items.STRID>`
        - :class:`STRACK <secsgem.secs.data_items.STRACK>`
        - :class:`FCNID <secsgem.secs.data_items.FCNID>`

    """

    _stream = 2
    _function = 44

    _data_format = [
        RSPACK,
        [
            [
                STRID,
                STRACK,
                [FCNID],
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
