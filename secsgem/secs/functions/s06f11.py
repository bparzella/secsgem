#####################################################################
# s06f11.py
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
"""Class for stream 06 function 11."""

from secsgem.secs.data_items import CEID, DATAID, RPTID, V
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F11(SecsStreamFunction):
    """event report.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F11
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            RPT: [
                {
                    RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    V: [
                        DATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        ...
                    ]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F11({
        ...     "DATAID": 1,
        ...     "CEID": 1337,
        ...     "RPT": [{
        ...         "RPTID": 1000,
        ...         "V": ["VAR", secsgem.secs.variables.U4(100)]}]})
        S6F11 W
          <L [3]
            <U1 1 >
            <U2 1337 >
            <L [1]
              <L [2]
                <U2 1000 >
                <L [2]
                  <A "VAR">
                  <U4 100 >
                >
              >
            >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`CEID <secsgem.secs.data_items.CEID>`
        - :class:`RPTID <secsgem.secs.data_items.RPTID>`
        - :class:`V <secsgem.secs.data_items.V>`

    """

    _stream = 6
    _function = 11

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "RPT",
                RPTID,
                [V],
            ],
        ],
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
