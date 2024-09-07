#####################################################################
# s02f50.py
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
"""Class for stream 02 function 50."""

from secsgem.secs.data_items import CPACK, CPNAME, HCACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F50(SecsStreamFunction):
    """Enhanced remote command - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F50
        {
            HCACK: B[1]
            PARAMS: [
                {
                    CPNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                    CPACK: B[1]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F50({
        ...     "HCACK": secsgem.secs.data_items.HCACK.INVALID_COMMAND,
        ...     "PARAMS": [
        ...         {"CPNAME": "PARAM1", "CPACK": secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_VALUE},
        ...         {"CPNAME": "PARAM2", "CPACK": secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_FORMAT}]})
        S2F50
          <L [2]
            <B 0x1>
            <L [2]
              <L [2]
                <A "PARAM1">
                <B 0x2>
              >
              <L [2]
                <A "PARAM2">
                <B 0x3>
              >
            >
          > .

    Data Items:
        - :class:`HCACK <secsgem.secs.data_items.HCACK>`
        - :class:`CPNAME <secsgem.secs.data_items.CPNAME>`
        - :class:`CPACK <secsgem.secs.data_items.CPACK>`

    """

    _stream = 2
    _function = 50

    _data_format = [
        HCACK,
        [
            [
                "PARAMS",
                CPNAME,
                CPACK,
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
