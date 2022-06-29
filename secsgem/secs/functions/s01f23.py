#####################################################################
# s01f23.py
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
"""Class for stream 01 function 23."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import CEID


class SecsS01F23(SecsStreamFunction):
    """collection event name list request

     **Data Items**
     - :class:`CEID <secsgem.secs.dataitems.CEID>`

     **Structure**::
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F23
        [
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

     **Example**::
         >>> import secsgem
        >>> secsgem.secs.functions.SecsS01F23([1,100])
        S1F23 W
          <L [2]
            <U1 1 >
            <U1 100 >
          > .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 1
    _function = 23
    _data_format = [CEID]
    _to_host = False
    _to_equipment = True
    _has_reply = True
    _is_reply_required = True
    _is_multi_block = False
