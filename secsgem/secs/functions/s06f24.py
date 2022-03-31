#####################################################################
# s06f24.py
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
"""Class for stream 06 function 24."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import RSDA


class SecsS06F24(SecsStreamFunction):
    """
    Request spooled data acknowledge.

    **Data Items**

    - :class:`RSDA <secsgem.secs.dataitems.RSDA>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS06F24
            RSDA: B

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F22(RSDA)
        S6F24
          <B [1] 0x01> .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 24

    _dataFormat = RSDA

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False
