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
from .. import variables
from .base import DataItemBase


class CMDA(DataItemBase):
    """
    Acknowledge code.

       :Types: :class:`Binary <secsgem.secs.variables.I1>`
       :Types: :class:`Binary <secsgem.secs.variables.U1>`
       :Length: 1

    **Values**
        +-------+------------------------+---------------------------------------------------------+
        | Value | Description            | Constant                                                |
        +=======+========================+=========================================================+
        | 0     | Completed or done      | :const:`secsgem.secs.data_items.CMDA.COMPLETED_DONE`         |
        +-------+------------------------+---------------------------------------------------------+
        | 1     | Command does not exist | :const:`secsgem.secs.data_items.CMDA.CMD_DOES_NOT_EXIST`    |
        +-------+------------------------+---------------------------------------------------------+
        | 2     | Cannot perform now     | :const:`secsgem.secs.data_items.CMDA.CANNOT_PERFORM_NOW`     |
        +-------+------------------------+---------------------------------------------------------+
        | 3-63  | Reserved               |                                                         |
        +-------+------------------------+---------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F22 <secsgem.secs.functions.SecsS02F22>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.I1,
    ]

    COMPLETED_DONE = 0
    CMD_DOES_NOT_EXIST = 1
    CANNOT_PERFORM_NOW = 2
