#####################################################################
# s05f03.py
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
"""Class for stream 05 function 03."""

from secsgem.secs.data_items import ALED, ALID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS05F03(SecsStreamFunction):
    """en-/disable alarm - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F03
        {
            ALED: B[1]
            ALID: U1/U2/U4/U8/I1/I2/I4/I8
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F03({"ALED": secsgem.secs.data_items.ALED.ENABLE, "ALID": 100})
        S5F3
          <L [2]
            <B 0x80>
            <U1 100 >
          > .

    Data Items:
        - :class:`ALED <secsgem.secs.data_items.ALED>`
        - :class:`ALID <secsgem.secs.data_items.ALID>`

    """

    _stream = 5
    _function = 3

    _data_format = [
        ALED,
        ALID,
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False
