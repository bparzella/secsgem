#####################################################################
# s05f09.py
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
"""Class for stream 05 function 09."""

from secsgem.secs.data_items import EXID, EXMESSAGE, EXRECVRA, EXTYPE, TIMESTAMP
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F09(SecsStreamFunction):
    """exception post - notify.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F09
        {
            TIMESTAMP: A[32]
            EXID: A[20]
            EXTYPE: A
            EXMESSAGE: A
            EXRECVRA: [
                DATA: A[40]
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F09({
        ...     "TIMESTAMP": "161006221500",
        ...     "EXID": "EX123",
        ...     "EXTYPE": "ALARM",
        ...     "EXMESSAGE": "Exception",
        ...     "EXRECVRA": ["EXRECVRA1", "EXRECVRA2"] })
        S5F9
          <L [5]
            <A "161006221500">
            <A "EX123">
            <A "ALARM">
            <A "Exception">
            <L [2]
              <A "EXRECVRA1">
              <A "EXRECVRA2">
            >
          > .

    Data Items:
        - :class:`TIMESTAMP <secsgem.secs.data_items.TIMESTAMP>`
        - :class:`EXID <secsgem.secs.data_items.EXID>`
        - :class:`EXTYPE <secsgem.secs.data_items.EXTYPE>`
        - :class:`EXMESSAGE <secsgem.secs.data_items.EXMESSAGE>`
        - :class:`EXRECVRA <secsgem.secs.data_items.EXRECVRA>`

    """

    _stream = 5
    _function = 9

    _data_format = [
        TIMESTAMP,
        EXID,
        EXTYPE,
        EXMESSAGE,
        [EXRECVRA],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False
