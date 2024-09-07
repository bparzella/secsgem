#####################################################################
# rspack.py
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
"""RSPACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class RSPACK(DataItemBase):
    """Reset spooling acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+--------------------------------------+--------------------------------------------------+
        | Value | Description                          | Constant                                         |
        +=======+======================================+==================================================+
        | 0     | Acknowledge, spooling setup accepted | :const:`secsgem.secs.data_items.RSPACK.ACK`      |
        +-------+--------------------------------------+--------------------------------------------------+
        | 1     | Spooling setup rejected              | :const:`secsgem.secs.data_items.RSPACK.REJECTED` |
        +-------+--------------------------------------+--------------------------------------------------+
        | 2-63  | Reserved                             |                                                  |
        +-------+--------------------------------------+--------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F44 <secsgem.secs.functions.SecsS02F44>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    REJECTED = 1
