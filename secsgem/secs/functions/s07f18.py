#####################################################################
# s07f18.py
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
"""Class for stream 07 function 18."""

from secsgem.secs.data_items import ACKC7
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS07F18(SecsStreamFunction):
    """delete process program - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F18
        ACKC7: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F18(secsgem.secs.data_items.ACKC7.MODE_UNSUPPORTED)
        S7F18
          <B 0x5> .

    Data Items:
        - :class:`ACKC7 <secsgem.secs.data_items.ACKC7>`

    """

    _stream = 7
    _function = 18

    _data_format = ACKC7

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
