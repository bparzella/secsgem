#####################################################################
# s06f12.py
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
"""Class for stream 06 function 12."""

from secsgem.secs.data_items import ACKC6
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F12(SecsStreamFunction):
    """event report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F12
        ACKC6: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F12(secsgem.secs.data_items.ACKC6.ACCEPTED)
        S6F12
          <B 0x0> .

    Data Items:
        - :class:`ACKC6 <secsgem.secs.data_items.ACKC6>`

    """

    _stream = 6
    _function = 12

    _data_format = ACKC6

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
