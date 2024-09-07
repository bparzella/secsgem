#####################################################################
# s05f18.py
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
"""Class for stream 05 function 18."""

from secsgem.secs.data_items import ACKA, ERRCODE, ERRTEXT, EXID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F18(SecsStreamFunction):
    """exception recover abort - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F18
        {
            EXID: A[20]
            DATA: {
                ACKA: BOOLEAN[1]
                DATA: {
                    ERRCODE: I1/I2/I4/I8
                    ERRTEXT: A[120]
                }
            }
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F18({
        ...     "EXID": "EX123",
        ...     "DATA": {
        ...         "ACKA": False,
        ...         "DATA": {
        ...             "ERRCODE": 10,
        ...             "ERRTEXT": "Error"}}})
        S5F18
          <L [2]
            <A "EX123">
            <L [2]
              <BOOLEAN False >
              <L [2]
                <I1 10 >
                <A "Error">
              >
            >
          > .

    Data Items:
        - :class:`EXID <secsgem.secs.data_items.EXID>`
        - :class:`ACKA <secsgem.secs.data_items.ACKA>`
        - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
        - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    """

    _stream = 5
    _function = 18

    _data_format = [
        EXID,
        [
            ACKA,
            [
                ERRCODE,
                ERRTEXT,
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
