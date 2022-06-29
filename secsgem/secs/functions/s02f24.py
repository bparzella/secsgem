#####################################################################
# s02f24.py
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
"""Class for stream 02 function 24."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import TIAACK


class SecsS02F24(SecsStreamFunction):
    """trace - acknowledge
    **Data Items**

    - :class:`TIAACK <secsgem.secs.dataitems.TIAACK>`

    **Example**::

        >>> import secsgem
        >>> secsgem.secs.functions.SecsS02F24(...)

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 2
    _function = 24

    _data_format = TIAACK    

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
