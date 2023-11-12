#####################################################################
# s00f00.py
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
"""Class for stream 00 function 00."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS00F00(SecsStreamFunction):
    """Hsms communication.

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS00F00
        Header only

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS00F00()
        S0F0 .

    """

    _stream = 0
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
