#####################################################################
# s06f16.py
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
"""Class for stream 06 function 16."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import DATAID
from secsgem.secs.data_items import CEID
from secsgem.secs.data_items import RPTID
from secsgem.secs.data_items import V


class SecsS06F16(SecsStreamFunction):
    """
    event report data.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`
    - :class:`RPTID <secsgem.secs.data_items.RPTID>`
    - :class:`V <secsgem.secs.data_items.V>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F16
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

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F16({
        ...     "DATAID": 1,
        ...     "CEID": 1337,
        ...     "RPT": [{
        ...         "RPTID": 1000,
        ...         "V": ["VAR", secsgem.secs.variables.U4(100)]}]})
        S6F16
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

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 6
    _function = 16

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "RPT",
                RPTID,
                [V]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
