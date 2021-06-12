#####################################################################
# s05f11.py
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
"""Class for stream 05 function 11."""

from .base import SecsStreamFunction
from ..data_items import TIMESTAMP, EXID, EXTYPE, EXMESSAGE


class SecsS05F11(SecsStreamFunction):
    """
    exception clear - notify.

    **Data Items**

    - :class:`TIMESTAMP <secsgem.secs.data_items.TIMESTAMP>`
    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`EXTYPE <secsgem.secs.data_items.EXTYPE>`
    - :class:`EXMESSAGE <secsgem.secs.data_items.EXMESSAGE>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F11
        {
            TIMESTAMP: A[32]
            EXID: A[20]
            EXTYPE: A
            EXMESSAGE: A
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F11({"TIMESTAMP": "161006221500", "EXID": "EX123", "EXTYPE": "ALARM", \
"EXMESSAGE": "Exception"})
        S5F11
          <L [4]
            <A "161006221500">
            <A "EX123">
            <A "ALARM">
            <A "Exception">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 11

    _data_format = [
        TIMESTAMP,
        EXID,
        EXTYPE,
        EXMESSAGE,
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False
