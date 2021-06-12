#####################################################################
# s02f16.py
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
"""Class for stream 02 function 16."""

from .base import SecsStreamFunction
from ..data_items import EAC


class SecsS02F16(SecsStreamFunction):
    """
    new equipment constant - acknowledge.

    **Data Items**

    - :class:`EAC <secsgem.secs.data_items.EAC>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F16
        EAC: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F16(secsgem.secs.data_items.EAC.BUSY)
        S2F16
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 2
    _function = 16

    _data_format = EAC

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
