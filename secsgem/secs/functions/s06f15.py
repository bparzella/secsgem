#####################################################################
# s06f15.py
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
"""Class for stream 06 function 15."""

from secsgem.secs.data_items import CEID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F15(SecsStreamFunction):
    """event report request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F15
        CEID: U1/U2/U4/U8/I1/I2/I4/I8/A

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F15(1337)
        S6F15 W
          <U2 1337 > .

    Data Items:
        - :class:`CEID <secsgem.secs.data_items.CEID>`

    """

    _stream = 6
    _function = 15

    _data_format = CEID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
