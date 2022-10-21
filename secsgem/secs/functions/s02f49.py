#####################################################################
# s02f49.py
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
"""Class for stream 02 function 49."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import DATAID, OBJSPEC, RCMD, CPNAME, CEPVAL


class SecsS02F49(SecsStreamFunction):
    """
    host command - send.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`OBJSPEC <secsgem.secs.data_items.OBJSPEC>`
    - :class:`RCMD <secsgem.secs.data_items.RCMD>`
    - :class:`CPNAME <secsgem.secs.data_items.CPNAME>`
    - :class:`CEPVAL <secsgem.secs.data_items.CEPVAL>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F49
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            OBJSPEC: A
            RCMD: U1/I1/A
            PARAMS: [
                {
                    CPNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                    CEPVAL: LIST/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/A/B
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F49({"DATAID": 1, "OBJSPEC": "test", "RCMD": "COMMAND", "PARAMS": [{"CPNAME": "PARAM1", "CEPVAL": "VAL1"}, \
{"CPNAME": "PARAM2", "CEPVAL": "VAL2"}]})
        S2F49 W
          <L [2]
            <I 1>
            <A "test">
            <A "COMMAND">
            <L [2]
              <L [2]
                <A "PARAM1">
                <A "VAL1">
              >
              <L [2]
                <A "PARAM2">
                <A "VAL2">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 49

    _data_format = [
        DATAID,
        OBJSPEC,
        RCMD,
        [
            [
                "PARAMS",   # name of the list
                CPNAME,
                CEPVAL
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
