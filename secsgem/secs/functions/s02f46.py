#####################################################################
# s02f46.py
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
"""Class for stream 02 function 46."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import VLAACK, VID, LVACK, LIMITID, LIMITACK


class SecsS02F46(SecsStreamFunction):
    """Variable Limits attributes acknowledge

    **Data Items**

    - :class:`VLAACK <secsgem.secs.data_items.VLAACK>`
    - :class:`VID <secsgem.secs.data_items.VID>`
    - :class:`LIMITID <secsgem.secs.data_items.LIMITID>`
    - :class:`LIMITACK <secsgem.secs.data_items.LIMITACK>`


    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 46

    _data_format = [
        VLAACK,
        [
            [
                VID,
                LVACK,
                    [
                        LIMITID,
                        LIMITACK
                    ]
                
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
