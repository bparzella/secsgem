#####################################################################
# s02f34.py
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
"""Class for stream 02 function 34."""

from secsgem.secs.data_items import DRACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F34(SecsStreamFunction):
    """define report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F34
        DRACK: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F34(secsgem.secs.data_items.DRACK.INVALID_FORMAT)
        S2F34
          <B 0x2> .

    Data Items:
        - :class:`DRACK <secsgem.secs.data_items.DRACK>`

    """

    _stream = 2
    _function = 34

    _data_format = DRACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
