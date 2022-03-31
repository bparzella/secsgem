#####################################################################
# s06f23.py
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
"""Class for stream 06 function 23."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import RSDC


class SecsS06F23(SecsStreamFunction):
    """
    Request spooled data

    **Data Items**

    - :class:`RSDC <secsgem.secs.dataitems.RSDC>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS06F23
            RSDC: U1

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F22("RSDC")
        S6F23 W
          <U1 RSDC> .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 23

    _dataFormat = RSDC

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False
