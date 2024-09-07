#####################################################################
# lrack.py
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
"""LRACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class LRACK(DataItemBase):
    """Link report acknowledge code.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-----------------------------+-----------------------------------------------------------+
        | Value | Description                 | Constant                                                  |
        +=======+=============================+===========================================================+
        | 0     | Acknowledge                 | :const:`secsgem.secs.data_items.LRACK.ACK`                |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 1     | Denied, insufficient space  | :const:`secsgem.secs.data_items.LRACK.INSUFFICIENT_SPACE` |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 2     | Denied, invalid format      | :const:`secsgem.secs.data_items.LRACK.INVALID_FORMAT`     |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 3     | Denied, CEID already linked | :const:`secsgem.secs.data_items.LRACK.CEID_LINKED`        |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 4     | Denied, CEID doesn't exist  | :const:`secsgem.secs.data_items.LRACK.CEID_UNKNOWN`       |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 5     | Denied, RPTID doesn't exist | :const:`secsgem.secs.data_items.LRACK.RPTID_UNKNOWN`      |
        +-------+-----------------------------+-----------------------------------------------------------+
        | 6-63  | Reserved, other errors      |                                                           |
        +-------+-----------------------------+-----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F36 <secsgem.secs.functions.SecsS02F36>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    INSUFFICIENT_SPACE = 1
    INVALID_FORMAT = 2
    CEID_LINKED = 3
    CEID_UNKNOWN = 4
    RPTID_UNKNOWN = 5
