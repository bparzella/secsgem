#####################################################################
# limitack.py
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
"""LIMITACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class LIMITACK(DataItemBase):
    """Acknowledgement code for variable limit.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------------------+-----------------------------------------------------------------+
        | Value | Description                        | Constant                                                        |
        +=======+====================================+=================================================================+
        | 0     | OK                                 | :const:`secsgem.secs.data_items.LIMITACK.OK`                    |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 1     | LIMITID does not exist             | :const:`secsgem.secs.data_items.LIMITACK.LIMITID_UNKNOWN`       |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 2     | UPPERDB > LIMITMAX                 | :const:`secsgem.secs.data_items.LIMITACK.UPPERDB_MORE_LIMITMAX` |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 3     | LOWERDB < LIMITMIN                 | :const:`secsgem.secs.data_items.LIMITACK.LOWERDB_LESS_LIMITMIN` |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 4     | UPPERDB < LOWERDB                  | :const:`secsgem.secs.data_items.LIMITACK.UPPERDB_LESS_LOWERDB`  |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 5     | Illegal format UPPER-/LOWERDB      | :const:`secsgem.secs.data_items.LIMITACK.ILLEGAL_FORMAT`        |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 6     | Illegal ASCII value                | :const:`secsgem.secs.data_items.LIMITACK.ASCII_ILLEGAL`         |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 7     | Duplicate limit definition         | :const:`secsgem.secs.data_items.LIMITACK.DUPLICATE`             |
        +-------+------------------------------------+-----------------------------------------------------------------+
        | 8-63  | Reserved, equipment specific error |                                                                 |
        +-------+------------------------------------+-----------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F46 <secsgem.secs.functions.SecsS02F46>`

    """

    __type__ = variables.Binary
    __count__ = 1

    OK = 0
    LIMITID_UNKNOWN = 1
    UPPERDB_MORE_LIMITMAX = 2
    LOWERDB_LESS_LIMITMIN = 3
    UPPERDB_LESS_LOWERDB = 4
    ILLEGAL_FORMAT = 5
    ASCII_ILLEGAL = 6
    DUPLICATE = 7
