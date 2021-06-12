#####################################################################
# s12f06.py
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
"""Class for stream 12 function 06."""

from .base import SecsStreamFunction
from ..data_items import GRNT1


class SecsS12F06(SecsStreamFunction):
    """
    map transmit - grant.

    **Data Items**

    - :class:`GRNT1 <secsgem.secs.data_items.GRNT1>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F06
        GRNT1: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F06(secsgem.secs.data_items.GRNT1.MATERIALID_UNKNOWN)
        S12F6
          <B 0x5> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 6

    _data_format = GRNT1

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
