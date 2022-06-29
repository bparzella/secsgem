#####################################################################
# s02f48.py
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
"""Class for stream 02 function 48."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import VID, UNITS, LIMITMIN, LIMITMAX, LIMITID, \
        UPPERDB, LOWERDB


class SecsS02F48(SecsStreamFunction):
    """Variable Limit Attribute Send

    **Data Items**

    - :class:`VID <secsgem.secs.data_items.VID>`
    - :class:`UNITS <secsgem.secs.data_items.UNITS>`
    - :class:`LIMITMIN <secsgem.secs.data_items.LIMITMIN>`
    - :class:`LIMITMIN <secsgem.secs.data_items.LIMITMAX>`
    - :class:`LIMITMIN <secsgem.secs.data_items.LIMITID>`
    - :class:`LIMITMIN <secsgem.secs.data_items.UPPERDB>`
    - :class:`LIMITMIN <secsgem.secs.data_items.LOWERDB>`


    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 48

    _data_format = [
        [
            VID,
            [
                UNITS,
                LIMITMIN,
                LIMITMAX,
                [
                    [
                        LIMITID,
                        UPPERDB,
                        LOWERDB
                    ]
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
