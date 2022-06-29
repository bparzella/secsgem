#####################################################################
# s02f21.py
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
"""Class for stream 02 function 21."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS02F21(SecsStreamFunction):
    """Remote Command Send

    **Data Items**

    - :class:`RCMD <secsgem.secs.data_items.RCMD>` Remote Command
    
    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F21
        TIME: A[32]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F21({"RCMD":"ABCD"})
        S2F23 W
          <L [1]
            <L [5]
              <A "1">
              <A "000100">
              <U4 10 >
              <U4 1 >
              <L [2]
                <U4 1002004 >
                <U4 400210 >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: ASCII string
    """

    _stream = 2
    _function = 21

    _data_format = RCMD
    

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
