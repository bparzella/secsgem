#####################################################################
# s02f45.py
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
"""Class for stream 02 function 45."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import DATAID, VID, LIMITID, UPPERDB, LOWERDB


class SecsS02F45(SecsStreamFunction):
    """Variable limits attributes

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`VID <secsgem.secs.dataitems.VID>`
    - :class:`LIMITID <secsgem.secs.dataitems.LIMITID>`

   

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 45

    _data_format = [
        DATAID,
        [
            [
                VID,
                    [
                        [
                            LIMITID,
                                [
                                    UPPERDB,
                                    LOWERDB   
                                ]
                            
                        ]
                    ]
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
