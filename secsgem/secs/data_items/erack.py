#####################################################################
# erack.py
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
"""ERACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ERACK(DataItemBase):
    """Enable/disable event report acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+----------------------------+-----------------------------------------------------+
        | Value | Description                | Constant                                            |
        +=======+============================+=====================================================+
        | 0     | Accepted                   | :const:`secsgem.secs.data_items.ERACK.ACCEPTED`     |
        +-------+----------------------------+-----------------------------------------------------+
        | 1     | Denied, CEID doesn't exist | :const:`secsgem.secs.data_items.ERACK.CEID_UNKNOWN` |
        +-------+----------------------------+-----------------------------------------------------+
        | 2-63  | Reserved                   |                                                     |
        +-------+----------------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F38 <secsgem.secs.functions.SecsS02F38>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACCEPTED = 0
    CEID_UNKNOWN = 1
