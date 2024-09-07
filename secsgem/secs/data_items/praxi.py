#####################################################################
# praxi.py
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
"""PRAXI data item."""

from secsgem.secs import variables

from .base import DataItemBase


class PRAXI(DataItemBase):
    """Process axis.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+----------------------------+--------------------------------------------------------+
        | Value | Description                | Constant                                               |
        +=======+============================+========================================================+
        | 0     | Rows, top, increasing      | :const:`secsgem.secs.data_items.PRAXI.ROWS_TOP_INCR`   |
        +-------+----------------------------+--------------------------------------------------------+
        | 1     | Rows, top, decreasing      | :const:`secsgem.secs.data_items.PRAXI.ROWS_TOP_DECR`   |
        +-------+----------------------------+--------------------------------------------------------+
        | 2     | Rows, bottom, increasing   | :const:`secsgem.secs.data_items.PRAXI.ROWS_BOT_INCR`   |
        +-------+----------------------------+--------------------------------------------------------+
        | 3     | Rows, bottom, decreasing   | :const:`secsgem.secs.data_items.PRAXI.ROWS_BOT_DECR`   |
        +-------+----------------------------+--------------------------------------------------------+
        | 4     | Columns, left, increasing  | :const:`secsgem.secs.data_items.PRAXI.COLS_LEFT_INCR`  |
        +-------+----------------------------+--------------------------------------------------------+
        | 5     | Columns, left, decreasing  | :const:`secsgem.secs.data_items.PRAXI.COLS_LEFT_DECR`  |
        +-------+----------------------------+--------------------------------------------------------+
        | 6     | Columns, right, increasing | :const:`secsgem.secs.data_items.PRAXI.COLS_RIGHT_INCR` |
        +-------+----------------------------+--------------------------------------------------------+
        | 7     | Columns, right, decreasing | :const:`secsgem.secs.data_items.PRAXI.COLS_RIGHT_DECR` |
        +-------+----------------------------+--------------------------------------------------------+
        | 8-63  | Error                      |                                                        |
        +-------+----------------------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ROWS_TOP_INCR = 0
    ROWS_TOP_DECR = 1
    ROWS_BOT_INCR = 2
    ROWS_BOT_DECR = 3
    COLS_LEFT_INCR = 4
    COLS_LEFT_DECR = 5
    COLS_RIGHT_INCR = 6
    COLS_RIGHT_DECR = 7
