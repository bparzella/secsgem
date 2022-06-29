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
from .. import variables
from .base import DataItemBase


class VLAACK(DataItemBase):
    """variable limit attribute acknowledge

       :Types: :class:`secsgem.secs.variables.Binary <secsgem.secs.variables.Binary>`
       :Length: 1

    **Values**
        +-------+-------------------+------------------------------------------------+
        | Value | Description       | Constant                                       |
        +=======+===================+================================================+
        | 0     | Ok                | :const:`secsgem.secs.data_items.VLAACK.Ok` |
        +-------+-------------------+------------------------------------------------+
        | 1     | limit attribute definition error   | :const:`secsgem.secs.data_items.VLAACK.ERROR`    |
        +-------+-------------------+------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F02 <secsgem.secs.functions.SecsS02F46>`

    """

    __type__ = secsgem.secs.variables.Binary
    __count__ = 1

    OK = 0
    LIMI_ATT_DEFITION_ERROR = 1
    CANNOT_PERFORM = 2
