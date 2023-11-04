#####################################################################
# s02f13.py
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
"""Class for stream 02 function 13."""

from secsgem.secs.data_items import ECID
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F13(SecsStreamFunction):
    """equipment constant - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F13
        [
            ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F13([1, 1337])
        S2F13 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    Data Items:
        - :class:`ECID <secsgem.secs.data_items.ECID>`

    An empty list will return all available equipment constants.

    """

    _stream = 2
    _function = 13

    _data_format = [ECID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
