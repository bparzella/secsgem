#####################################################################
# mapft.py
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
"""MAPFT data item."""

from secsgem.secs import variables

from .base import DataItemBase


class MAPFT(DataItemBase):
    """Map data format.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------------+---------------------------------------------------+
        | Value | Description       | Constant                                          |
        +=======+===================+===================================================+
        | 0     | Row format        | :const:`secsgem.secs.data_items.MAPFT.ROW`        |
        +-------+-------------------+---------------------------------------------------+
        | 1     | Array format      | :const:`secsgem.secs.data_items.MAPFT.ARRAY`      |
        +-------+-------------------+---------------------------------------------------+
        | 2     | Coordinate format | :const:`secsgem.secs.data_items.MAPFT.COORDINATE` |
        +-------+-------------------+---------------------------------------------------+
        | 3-63  | Error             |                                                   |
        +-------+-------------------+---------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F05>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ROW = 0
    ARRAY = 1
    COORDINATE = 2
