#####################################################################
# s02f36.py
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
"""Class for stream 02 function 36."""

from secsgem.secs.data_items import LRACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F36(SecsStreamFunction):
    """link event report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F36
        LRACK: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F36(secsgem.secs.data_items.LRACK.CEID_UNKNOWN)
        S2F36
          <B 0x4> .

    Data Items:
        - :class:`LRACK <secsgem.secs.data_items.LRACK>`

    """

    _stream = 2
    _function = 36

    _data_format = LRACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
