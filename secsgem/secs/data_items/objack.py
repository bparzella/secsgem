#####################################################################
# objack.py
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
"""OBJACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class OBJACK(DataItemBase):
    """Object acknowledgement code.

    :Type: :class:`U1 <secsgem.secs.variables.U1>`
    :Length: 1

    **Values**
        +-------+-------------+----------------------------------------------------+
        | Value | Description | Constant                                           |
        +=======+=============+====================================================+
        | 0     | Successful  | :const:`secsgem.secs.data_items.OBJACK.SUCCESSFUL` |
        +-------+-------------+----------------------------------------------------+
        | 1     | Error       | :const:`secsgem.secs.data_items.OBJACK.ERROR`      |
        +-------+-------------+----------------------------------------------------+
        | 2-63  | Reserved    |                                                    |
        +-------+-------------+----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`

    """

    __type__ = variables.U1
    __count__ = 1

    SUCCESSFUL = 0
    ERROR = 1
