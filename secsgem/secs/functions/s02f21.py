#####################################################################
# s02f21.py
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
"""Class for stream 02 function 21."""

from secsgem.secs.data_items import RCMD
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F21(SecsStreamFunction):
    """Remote command send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F21
        RCMD: U1/I1/A

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F21("COMMMAND1")
        S2F21
          <A "COMMMAND1"> .

    Data Items:
        - :class:`RCMD <secsgem.secs.data_items.RCMD>`

    """

    _stream = 2
    _function = 21

    _data_format = RCMD

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False
