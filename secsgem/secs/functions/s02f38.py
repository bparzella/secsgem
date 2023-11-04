#####################################################################
# s02f38.py
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
"""Class for stream 02 function 38."""

from secsgem.secs.data_items import ERACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F38(SecsStreamFunction):
    """en-/disable event report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F38
        ERACK: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F38(secsgem.secs.data_items.ERACK.CEID_UNKNOWN)
        S2F38
          <B 0x1> .

    Data Items:
        - :class:`ERACK <secsgem.secs.data_items.ERACK>`

    """

    _stream = 2
    _function = 38

    _data_format = ERACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
