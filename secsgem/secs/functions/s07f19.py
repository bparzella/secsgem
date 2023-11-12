#####################################################################
# s07f19.py
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
"""Class for stream 07 function 19."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS07F19(SecsStreamFunction):
    """current equipment process program - request.

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F19
        Header only

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F19()
        S7F19 W .

    """

    _stream = 7
    _function = 19

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
