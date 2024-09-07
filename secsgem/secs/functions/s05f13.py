#####################################################################
# s05f13.py
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
"""Class for stream 05 function 13."""

from secsgem.secs.data_items import EXID, EXRECVRA
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F13(SecsStreamFunction):
    """exception recover - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F13
        {
            EXID: A[20]
            EXRECVRA: A[40]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F13({"EXID": "EX123", "EXRECVRA": "EXRECVRA2"})
        S5F13 W
          <L [2]
            <A "EX123">
            <A "EXRECVRA2">
          > .

    Data Items:
        - :class:`EXID <secsgem.secs.data_items.EXID>`
        - :class:`EXRECVRA <secsgem.secs.data_items.EXRECVRA>`

    """

    _stream = 5
    _function = 13

    _data_format = [
        EXID,
        EXRECVRA,
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
