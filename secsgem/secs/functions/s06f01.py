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

from secsgem.secs.data_items import SMPLN, STIME, SV, TRID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F01(SecsStreamFunction):
    """Trace data send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F01
        {
            TRID: I1/I2/I4/I8/U1/U2/U4/U8/A
            SMPLN: I1/I2/I4/I8/U1/U2/U4/U8
            STIME: A[32]
            SV: [
                DATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F01({
        ...     "TRID": 1,
        ...     "SMPLN": 3,
        ...     "STIME": "TIME",
        ...     "SV": [1, 4]})
        S6F1
          <L [4]
            <I1 1 >
            <I1 3 >
            <A "TIME">
            <L [2]
              <U1 1 >
              <U1 4 >
            >
          > .

    Data Items:
        - :class:`TRID <secsgem.secs.data_items.TRID>`
        - :class:`SMPLN <secsgem.secs.data_items.SMPLN>`
        - :class:`STIME <secsgem.secs.data_items.STIME>`
        - :class:`SV <secsgem.secs.data_items.SV>`

    """

    _stream = 6
    _function = 1

    _data_format = [
        TRID,
        SMPLN,
        STIME,
        [SV],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = True
