#####################################################################
# s10f03.py
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
"""Class for stream 10 function 03."""

from .base import SecsStreamFunction
from ..data_items import TID, TEXT


class SecsS10F03(SecsStreamFunction):
    """
    terminal single - display.

    **Data Items**

    - :class:`TID <secsgem.secs.data_items.TID>`
    - :class:`TEXT <secsgem.secs.data_items.TEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F03
        {
            TID: B[1]
            TEXT: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F03({"TID": 0, "TEXT": "hello!"})
        S10F3
          <L [2]
            <B 0x0>
            <A "hello!">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 10
    _function = 3

    _data_format = [
        TID,
        TEXT
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False
