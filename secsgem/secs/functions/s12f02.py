#####################################################################
# s12f02.py
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
"""Class for stream 12 function 02."""

from secsgem.secs.data_items import SDACK
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F02(SecsStreamFunction):
    """map setup data - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F02
        SDACK: B[1]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F02(secsgem.secs.data_items.SDACK.ACK)
        S12F2
          <B 0x0> .

    Data Items:
        - :class:`SDACK <secsgem.secs.data_items.SDACK>`

    """

    _stream = 12
    _function = 2

    _data_format = SDACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
