#####################################################################
# s09f07.py
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
"""Class for stream 09 function 07."""

from .base import SecsStreamFunction
from ..data_items import MHEAD


class SecsS09F07(SecsStreamFunction):
    """
    illegal data.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F07
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F07("HEADERDATA")
        S9F7
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 7

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
