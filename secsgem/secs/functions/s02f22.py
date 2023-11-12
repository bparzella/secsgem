#####################################################################
# s02f22.py
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
"""Class for stream 02 function 22."""

from secsgem.secs.data_items import CMDA
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F22(SecsStreamFunction):
    """Remote command - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F22
        CMDA: U1/I1

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F22(secsgem.secs.data_items.CMDA.DONE)
        S2F22
          <U1 0 > .

    Data Items:
        - :class:`CMDA <secsgem.secs.data_items.CMDA>`

    """

    _stream = 2
    _function = 22

    _data_format = CMDA

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
