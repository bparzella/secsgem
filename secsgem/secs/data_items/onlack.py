#####################################################################
# onlack.py
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
"""ONLACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ONLACK(DataItemBase):
    """Acknowledge code for ONLINE request.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+--------------------+-----------------------------------------------------+
        | Value | Description        | Constant                                            |
        +=======+====================+=====================================================+
        | 0     | ONLINE Accepted    | :const:`secsgem.secs.data_items.ONLACK.ACCEPTED`    |
        +-------+--------------------+-----------------------------------------------------+
        | 1     | ONLINE Not allowed | :const:`secsgem.secs.data_items.ONLACK.NOT_ALLOWED` |
        +-------+--------------------+-----------------------------------------------------+
        | 2     | Already ONLINE     | :const:`secsgem.secs.data_items.ONLACK.ALREADY_ON`  |
        +-------+--------------------+-----------------------------------------------------+
        | 3-63  | Reserved           |                                                     |
        +-------+--------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F18 <secsgem.secs.functions.SecsS01F18>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACCEPTED = 0
    NOT_ALLOWED = 1
    ALREADY_ON = 2
