#####################################################################
# s12f17.py
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
"""Class for stream 12 function 17."""

from .base import SecsStreamFunction
from ..data_items import MID, IDTYP, SDBIN


class SecsS12F17(SecsStreamFunction):
    """
    map data type 3 - request.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`SDBIN <secsgem.secs.data_items.SDBIN>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F17
        {
            MID: A/B[80]
            IDTYP: B[1]
            SDBIN: B[1]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F17({"MID": "materialID", \
                                               "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                                               "SDBIN": secsgem.secs.data_items.SDBIN.DONT_SEND})
        S12F17 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <B 0x1>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 17

    _data_format = [
        MID,
        IDTYP,
        SDBIN
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
