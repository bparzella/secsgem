#####################################################################
# s05f17.py
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
"""Class for stream 05 function 17."""

from secsgem.secs.data_items import EXID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F17(SecsStreamFunction):
    """exception recover abort - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F17
        EXID: A[20]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F17("EX123")
        S5F17 W
          <A "EX123"> .

    Data Items:
        - :class:`EXID <secsgem.secs.data_items.EXID>`

    """

    _stream = 5
    _function = 17

    _data_format = EXID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
