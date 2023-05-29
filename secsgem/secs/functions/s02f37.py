#####################################################################
# s02f37.py
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
"""Class for stream 02 function 37."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import CEED
from secsgem.secs.data_items import CEID


class SecsS02F37(SecsStreamFunction):
    """
    en-/disable event report.

    **Data Items**

    - :class:`CEED <secsgem.secs.data_items.CEED>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F37
        {
            CEED: BOOLEAN[1]
            CEID: [
                DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                ...
            ]
        }

    Example:

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F37({"CEED": True, "CEID": [1337]})
        S2F37 W
          <L [2]
            <BOOLEAN True >
            <L [1]
              <U2 1337 >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 2
    _function = 37

    _data_format = [
        CEED,
        [CEID]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
