#####################################################################
# s01f14.py
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
"""Class for stream 01 function 14."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import COMMACK, MDLN


class SecsS01F14(SecsStreamFunction):
    """
    establish communication - acknowledge.

    .. caution::

        This Stream/function has different structures depending on the source.
        See structure definition below for details.
        Be sure to fill the array accordingly.

    **Data Items**

    - :class:`COMMACK <secsgem.secs.data_items.COMMACK>`

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

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F14({"COMMACK": secsgem.secs.data_items.COMMACK.ACCEPTED, \
                                               "MDLN": ["secsgem", "0.0.6"]})
        S1F14
          <L [2]
            <B 0x0>
            <L [2]
              <A "secsgem">
              <A "0.0.6">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 1
    _function = 14

    _data_format = [
        COMMACK,
        [MDLN]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
