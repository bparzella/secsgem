#####################################################################
# maper.py
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
"""MAPER data item."""

from secsgem.secs import variables

from .base import DataItemBase


class MAPER(DataItemBase):
    """Map error.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+---------------+-----------------------------------------------------+
        | Value | Description   | Constant                                            |
        +=======+===============+=====================================================+
        | 0     | ID not found  | :const:`secsgem.secs.data_items.MAPER.ID_UNKNOWN`   |
        +-------+---------------+-----------------------------------------------------+
        | 1     | Invalid data  | :const:`secsgem.secs.data_items.MAPER.INVALID_DATA` |
        +-------+---------------+-----------------------------------------------------+
        | 2     | Format error  | :const:`secsgem.secs.data_items.MAPER.FORMAT_ERROR` |
        +-------+---------------+-----------------------------------------------------+
        | 3-63  | Invalid error |                                                     |
        +-------+---------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F19 <secsgem.secs.functions.SecsS12F19>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ID_UNKNOWN = 0
    INVALID_DATA = 1
    FORMAT_ERROR = 2
