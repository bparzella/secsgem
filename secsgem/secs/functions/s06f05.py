#####################################################################
# s06f05.py
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
"""Class for stream 06 function 05."""

from secsgem.secs.data_items import DATAID, DATALENGTH
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F05(SecsStreamFunction):
    """multi block data inquiry.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F05
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATALENGTH: U1/U2/U4/U8/I1/I2/I4/I8
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F05({"DATAID": 1, "DATALENGTH": 1337})
        S6F5 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`DATALENGTH <secsgem.secs.data_items.DATALENGTH>`

    """

    _stream = 6
    _function = 5

    _data_format = [
        DATAID,
        DATALENGTH,
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
