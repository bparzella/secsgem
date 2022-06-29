#####################################################################
# s02f44.py
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
"""Class for stream 02 function 44."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import RSPACK, STRID, STRACK, FCNID


class SecsS02F44(SecsStreamFunction):
    """Configure Spooling Acknowledge

    **Data Items**

    - :class:`RSPACK <secsgem.secs.dataitems.RSPACK>`
    - :class:`STRID <secsgem.secs.dataitems.STRID>`
    - :class:`STRACK <secsgem.secs.dataitems.STRACK>`
    - :class:`FCNID <secsgem.secs.dataitems.FCNID>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS02F44
        {
            RSPACK: B[1]
            STREAMS: [
                {
                    STRID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    STRACK: B[1]
                    FUNCTIONS: [
                        FN
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F42({ \
            "RSPACK": secsgem.RSPACK.OK, \
            "STREAMS": [ \
                {"STRID": 1, \
                "STRACK": secsgem.STRACK.ILLEGAL_VALUE, \
                "FUNCTION" : [13]}, \
                {"STRID": 2, \
                 "STRACK": secsgem.STRACK.ILLEGAL_FORMAT, \
                  }"FUNCTION" : [13]]})
        S2F44
        ......
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 44

    _data_format = [
        RSPACK,
        [
            [
                STRID,   
                STRACK,
                [
                FCNID
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
