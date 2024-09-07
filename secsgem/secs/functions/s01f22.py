#####################################################################
# s01f22.py
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
"""Class for stream 01 function 22."""

from secsgem.secs.data_items import DVVALNAME, UNITS, VID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS01F22(SecsStreamFunction):
    """Data variable namelist.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F22
        [
            {
                VID: U1/U2/U4/U8/I1/I2/I4/I8/A
                DVVALNAME: A
                UNITS: A
            }
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F22([{"VID": 1, "DVVALNAME": "EC1", "UNITS": "mm"}])
        S1F22
          <L [1]
            <L [3]
              <U1 1 >
              <A "EC1">
              <A "mm">
            >
          > .

    Data Items:
        - :class:`VID <secsgem.secs.data_items.VID>`
        - :class:`DVVALNAME <secsgem.secs.data_items.DVVALNAME>`
        - :class:`UNITS <secsgem.secs.data_items.UNITS>`

    """

    _stream = 1
    _function = 22

    _data_format = [
        [
            VID,
            DVVALNAME,
            UNITS,
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
