#####################################################################
# s02f49.py
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
"""Class for stream 02 function 49."""

from secsgem.secs.data_items import CEPVAL, CPNAME, DATAID, OBJSPEC, RCMD
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F49(SecsStreamFunction):
    """Enhanced remote command.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F49
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            OBJSPEC: A
            RCMD: U1/I1/A
            PARAMS: [
                {
                    CPNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                    CEPVAL: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F49({
        ...     "DATAID": 1,
        ...     "OBJSPEC": 'test',
        ...     "RCMD": "COMMAND1",
        ...     "PARAMS": [{
        ...         "CPNAME": "CPARAM",
        ...         "CEPVAL": "VALUE"
        ...     }]})
        S2F49
          <L [4]
            <U1 1 >
            <A "test">
            <A "COMMAND1">
            <L [1]
              <L [2]
                <A "CPARAM">
                <A "VALUE">
              >
            >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`OBJSPEC <secsgem.secs.data_items.OBJSPEC>`
        - :class:`RCMD <secsgem.secs.data_items.RCMD>`
        - :class:`CPNAME <secsgem.secs.data_items.CPNAME>`
        - :class:`CEPVAL <secsgem.secs.data_items.CEPVAL>`

    """

    _stream = 2
    _function = 49

    _data_format = [
        DATAID,
        OBJSPEC,
        RCMD,
        [
            [
                "PARAMS",
                CPNAME,
                CEPVAL,
            ],
        ],
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
