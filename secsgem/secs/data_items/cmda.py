#####################################################################
# cmda.py
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
"""CMDA data item."""

from secsgem.secs import variables

from .base import DataItemBase


class CMDA(DataItemBase):
    """Command acknowledged code.

    :Types:
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`I1 <secsgem.secs.variables.I1>`

    **Values**
        +-------+------------------------------------+-------------------------------------------------------+
        | Value | Description                        | Constant                                              |
        +=======+====================================+=======================================================+
        | 0     | Completed or done                  | :const:`secsgem.secs.data_items.CMDA.DONE`            |
        +-------+------------------------------------+-------------------------------------------------------+
        | 1     | Command does not exist             | :const:`secsgem.secs.data_items.CMDA.COMMAND_UNKNOWN` |
        +-------+------------------------------------+-------------------------------------------------------+
        | 2     | Cannot perform now                 | :const:`secsgem.secs.data_items.CMDA.NOT_NOW`         |
        +-------+------------------------------------+-------------------------------------------------------+
        | 3-63  | Reserved, equipment specific error |                                                       |
        +-------+------------------------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F22 <secsgem.secs.functions.SecsS02F22>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.I1,
    ]

    DONE = 0
    COMMAND_UNKNOWN = 1
    NOT_NOW = 2
