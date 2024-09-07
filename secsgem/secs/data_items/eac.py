#####################################################################
# eac.py
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
"""EAC data item."""

from secsgem.secs import variables

from .base import DataItemBase


class EAC(DataItemBase):
    """Equipment acknowledge code.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+---------------------------------+-------------------------------------------------------+
        | Value | Description                     | Constant                                              |
        +=======+=================================+=======================================================+
        | 0     | Acknowledge                     | :const:`secsgem.secs.data_items.EAC.ACK`              |
        +-------+---------------------------------+-------------------------------------------------------+
        | 1     | Denied, not all constants exist | :const:`secsgem.secs.data_items.EAC.INVALID_CONSTANT` |
        +-------+---------------------------------+-------------------------------------------------------+
        | 2     | Denied, busy                    | :const:`secsgem.secs.data_items.EAC.BUSY`             |
        +-------+---------------------------------+-------------------------------------------------------+
        | 3     | Denied, constant out of range   | :const:`secsgem.secs.data_items.EAC.OUT_OF_RANGE`     |
        +-------+---------------------------------+-------------------------------------------------------+
        | 4-63  | Reserved, equipment specific    |                                                       |
        +-------+---------------------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F16 <secsgem.secs.functions.SecsS02F16>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    INVALID_CONSTANT = 1
    BUSY = 2
    OUT_OF_RANGE = 3
