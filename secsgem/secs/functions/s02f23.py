#####################################################################
# s02f23.py
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
"""Class for stream 02 function 23."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import TRID
from secsgem.secs.data_items import DSPER
from secsgem.secs.data_items import TOTSMP
from secsgem.secs.data_items import REPGSZ
from secsgem.secs.data_items import SVID


class SecsS02F23(SecsStreamFunction):
    """
    Trace initialize.

    **Data Items**

    - :class:`TRID <secsgem.secs.data_items.TRID>`
    - :class:`DSPER <secsgem.secs.data_items.DSPER>`
    - :class:`TOTSMP <secsgem.secs.data_items.TOTSMP>`
    - :class:`REPGSZ <secsgem.secs.data_items.REPGSZ>`
    - :class:`SVID <secsgem.secs.data_items.SVID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F23
        {
            TRID: I1/I2/I4/I8/U1/U2/U4/U8/A
            DSPER: A
            TOTSMP: I1/I2/I4/I8/U1/U2/U4/U8/A
            REPGSZ: I1/I2/I4/I8/U1/U2/U4/U8/A
            SVID: [
                DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F23({
        ...     "TRID":1,
        ...     "DSPER":'000010',
        ...     "TOTSMP":secsgem.secs.variables.U4(10),
        ...     "REPGSZ":secsgem.secs.variables.U4(1),
        ...     "SVID":[1002004,400210]})
        S2F23 W
          <L [5]
            <I1 1 >
            <A "000010">
            <U4 10 >
            <U4 1 >
            <L [2]
              <U4 1002004 >
              <U4 400210 >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 2
    _function = 23

    _data_format = [
        TRID,
        DSPER,
        TOTSMP,
        REPGSZ,
        [SVID]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
