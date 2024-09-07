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

from secsgem.secs import variables

from .base import DataItemBase


class TIAACK(DataItemBase):
    """Equipment acknowledgement code.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------+--------------------------------------------------------+
        | Value | Description            | Constant                                               |
        +=======+========================+========================================================+
        | 0     | Everything correct     | :const:`secsgem.secs.data_items.TIAACK.OK`             |
        +-------+------------------------+--------------------------------------------------------+
        | 1     | Too many SVIDs         | :const:`secsgem.secs.data_items.TIAACK.SVID_EXCEEDED`  |
        +-------+------------------------+--------------------------------------------------------+
        | 2     | No more traces allowed | :const:`secsgem.secs.data_items.TIAACK.TRACES_DENIED`  |
        +-------+------------------------+--------------------------------------------------------+
        | 3     | Invalid period         | :const:`secsgem.secs.data_items.TIAACK.INVALID_PERIOD` |
        +-------+------------------------+--------------------------------------------------------+
        | 4     | Unknown SVID           | :const:`secsgem.secs.data_items.TIAACK.SVID_UNKNOWN`   |
        +-------+------------------------+--------------------------------------------------------+
        | 5     | Invalid REPGSZ         | :const:`secsgem.secs.data_items.TIAACK.REPGSZ_INVALID` |
        +-------+------------------------+--------------------------------------------------------+
        | 6-63  | Reserved               |                                                        |
        +-------+------------------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F24 <secsgem.secs.functions.SecsS02F24>`

    """

    __type__ = variables.Binary
    __count__ = 1

    OK = 0
    SVID_EXCEEDED = 1
    TRACES_DENIED = 2
    INVALID_PERIOD = 3
    SVID_UNKNOWN = 4
    REPGSZ_INVALID = 5
