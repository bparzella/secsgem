#####################################################################
# s06f01.py
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
"""Class for stream 06 function 01."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import TRID, SMPLN, STIME, SV


class SecsS06F01(SecsStreamFunction):
    """trace event report

    **Data Items**

    - :class:`TRID <secsgem.secs.data_items.TRID>`
    - :class:`SMPLN <secsgem.secs.data_items.SMPLN>`
    - :class:`STIME <secsgem.secs.data_items.STIME>`
    - :class:`SV <secsgem.secs.data_items.SV>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS06F01
        {
        TRID: U4
        SMPLN: U4
        STIME: A
        SV: [
            DATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            ...
            ]
        }
       

    **Example**::

        >>> import secsgem
        

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 1

    _data_format = [
        TRID,
        SMPLN,
        STIME,
        [
            SV
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
