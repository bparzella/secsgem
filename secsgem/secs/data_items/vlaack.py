#####################################################################
# vlaack.py
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
"""VLAACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class VLAACK(DataItemBase):
    """Variable limit attribute acknowledgement code.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+--------------------------------------------+---------------------------------------------------------+
        | Value | Description                                | Constant                                                |
        +=======+============================================+=========================================================+
        | 0     | Acknowledgement, command will be performed | :const:`secsgem.secs.data_items.VLAACK.ACK`             |
        +-------+--------------------------------------------+---------------------------------------------------------+
        | 1     | Limit attribute definition error           | :const:`secsgem.secs.data_items.VLAACK.LIMIT_DEF_ERROR` |
        +-------+--------------------------------------------+---------------------------------------------------------+
        | 2     | Cannot perform now                         | :const:`secsgem.secs.data_items.VLAACK.NOT_NOW`         |
        +-------+--------------------------------------------+---------------------------------------------------------+
        | 3-63  | Reserved, equipment specific error         |                                                         |
        +-------+--------------------------------------------+---------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F46 <secsgem.secs.functions.SecsS02F46>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    LIMIT_DEF_ERROR = 1
    NOT_NOW = 2
