#####################################################################
# s02f35.py
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
"""Class for stream 02 function 35."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F35(SecsStreamFunction):
    """Link Event Report (LER).

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F35
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATA: [
                {
                    CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    RPTID: [
                        DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                        ...
                    ]
                }
                ...
            ]
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F35({"DATAID": 1, "DATA": [{"CEID": 1337, "RPTID": [1000, 1001]}]})
        S2F35 W
          <L [2]
            <U1 1 >
            <L [1]
              <L [2]
                <U2 1337 >
                <L [2]
                  <U2 1000 >
                  <U2 1001 >
                >
              >
            >
          > .

    Data Items:
        - :class:`DATAID <secsgem.secs.data_items.DATAID>`
        - :class:`CEID <secsgem.secs.data_items.CEID>`
        - :class:`RPTID <secsgem.secs.data_items.RPTID>`

    """

    _stream = 2
    _function = 35

    _data_format = """
    < L
      < DATAID >
      < L
        < L
          < CEID >
          <L
            < RPTID >
          >
        >
      >
    >
    """

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True
