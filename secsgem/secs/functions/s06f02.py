#####################################################################
# s06f02.py
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
"""Class for stream 06 function 02."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import ACKC6


class SecsS06F02(SecsStreamFunction):
    """trace report - acknowledge
    **Data Items**

    - :class:`ACKC6 <secsgem.secs.dataitems.ACKC6>`

    **Structure E->H**::

        {
            COMMACK: B[1]
            DATA: {
                MDLN: A[20]
                SOFTREV: A[20]
            }
        }

    **Structure H->E**::

        {
            COMMACK: B[1]
            DATA: []
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F02(...)
        S6F02
        ...

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 6
    _function = 2

    _data_format = ACKC6

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
