#####################################################################
# s02f26.py
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
"""Class for stream 02 function 26."""

from secsgem.secs.data_items import ABS
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F26(SecsStreamFunction):
    """Loopback diagnostic data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F26
        ABS: B

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F26("Text")
        S2F26
          <B 0x54 0x65 0x78 0x74> .

    Data Items:
        - :class:`ABS <secsgem.secs.data_items.ABS>`

    """

    _stream = 2
    _function = 26

    _data_format = ABS

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
