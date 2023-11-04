#####################################################################
# s05f04.py
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
"""Class for stream 05 function 04."""

from secsgem.secs.data_items import ACKC5
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F04(SecsStreamFunction):
    """en-/disable alarm - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F04
        ACKC5: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F04(secsgem.secs.data_items.ACKC5.ACCEPTED)
        S5F4
          <B 0x0> .

    Data Items:
        - :class:`ACKC5 <secsgem.secs.data_items.ACKC5>`

    """

    _stream = 5
    _function = 4

    _data_format = ACKC5

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
