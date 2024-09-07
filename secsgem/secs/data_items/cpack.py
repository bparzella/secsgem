#####################################################################
# cpack.py
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
"""CPACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class CPACK(DataItemBase):
    """Command parameter acknowledge code.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------+-------------------------------------------------------------+
        | Value | Description            | Constant                                                    |
        +=======+========================+=============================================================+
        | 1     | Parameter name unknown | :const:`secsgem.secs.data_items.CPACK.PARAMETER_UNKNOWN`    |
        +-------+------------------------+-------------------------------------------------------------+
        | 2     | CPVAL value illegal    | :const:`secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_VALUE`  |
        +-------+------------------------+-------------------------------------------------------------+
        | 3     | CPVAL format illegal   | :const:`secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_FORMAT` |
        +-------+------------------------+-------------------------------------------------------------+
        | 4-63  | Reserved               |                                                             |
        +-------+------------------------+-------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
        - :class:`SecsS02F50 <secsgem.secs.functions.SecsS02F50>`

    """

    __type__ = variables.Binary
    __count__ = 1

    PARAMETER_UNKNOWN = 1
    CPVAL_ILLEGAL_VALUE = 2
    CPVAL_ILLEGAL_FORMAT = 3
