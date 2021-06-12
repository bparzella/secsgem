#####################################################################
# s07f05.py
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
"""Class for stream 07 function 05."""

from .base import SecsStreamFunction
from ..data_items import PPID


class SecsS07F05(SecsStreamFunction):
    """
    process program - request.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F05
        PPID: A/B[120]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F05("program")
        S7F5 W
          <A "program"> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 7
    _function = 5

    _data_format = PPID

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
