#####################################################################
# tiaack.py
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
"""TIAACK data item."""
from .. import variables
from .base import DataItemBase


class TIAACK(DataItemBase):
    """Trace acknowledge

       :Types: :class:`secsgem.secs.variables.Binary <secsgem.secs.variables.Binary>`
       :Length: 1

    **Values**
        +-------+-------------------+--------------------------------------------------+
        | Value | Description       | Constant                                         |
        +=======+=========================+==================================================+
        | 0     | ok                      |  |
        +-------+-------------------------+--------------------------------------------------+
        | 1     | too many SVDs           | :const:`secsgem.secs.dataitems.COMMACK.DENIED`   |
        +-------+-------------------------+--------------------------------------------------+
        | 2     | no more trace allowed   |                                       |
        +-------+-------------------------+--------------------------------------------------+
         | 3     | invalid period         |                                       |
        +-------+-------------------------+--------------------------------------------------+
         | 4     | unknown SVID           |                                       |
        +-------+-------------------------+--------------------------------------------------+
         | 5     | bad REPGSZ             |                                       |
        +-------+-------------------------+--------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F24 <secsgem.secs.functions.SecsS02F24>`
    """

    __type__ = secsgem.secs.variables.Binary
    __count__ = 1

    ACCEPTED = 0
    DENIED = 1
