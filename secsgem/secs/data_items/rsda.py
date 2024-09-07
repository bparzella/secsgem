#####################################################################
# rsda.py
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
"""RSDA data item."""

from secsgem.secs import variables

from .base import DataItemBase


class RSDA(DataItemBase):
    """Request spooled data acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------------------------------+------------------------------------------------------+
        | Value | Description                         | Constant                                             |
        +=======+=====================================+======================================================+
        | 0     | OK                                  | :const:`secsgem.secs.data_items.RSDA.ACK`            |
        +-------+-------------------------------------+------------------------------------------------------+
        | 1     | Denied, busy try later              | :const:`secsgem.secs.data_items.RSDA.DENIED_BUSY`    |
        +-------+-------------------------------------+------------------------------------------------------+
        | 2     | Denied, spooled data does not exist | :const:`secsgem.secs.data_items.RSDA.DENIED_NO_DATA` |
        +-------+-------------------------------------+------------------------------------------------------+
        | 3-63  | Reserved                            |                                                      |
        +-------+-------------------------------------+------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F24 <secsgem.secs.functions.SecsS06F24>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    DENIED_BUSY = 1
    DENIED_NO_DATA = 2
