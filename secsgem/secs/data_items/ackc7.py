#####################################################################
# ackc7.py
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
"""ACKC7 data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ACKC7(DataItemBase):
    """Acknowledge code for stream 7.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------+---------------------------------------------------------+
        | Value | Description            | Constant                                                |
        +=======+========================+=========================================================+
        | 0     | Accepted               | :const:`secsgem.secs.data_items.ACKC7.ACCEPTED`         |
        +-------+------------------------+---------------------------------------------------------+
        | 1     | Permission not granted | :const:`secsgem.secs.data_items.ACKC7.NO_PERMISSION`    |
        +-------+------------------------+---------------------------------------------------------+
        | 2     | Length error           | :const:`secsgem.secs.data_items.ACKC7.LENGTH_ERROR`     |
        +-------+------------------------+---------------------------------------------------------+
        | 3     | Matrix overflow        | :const:`secsgem.secs.data_items.ACKC7.MATRIX_OVERFLOW`  |
        +-------+------------------------+---------------------------------------------------------+
        | 4     | PPID not found         | :const:`secsgem.secs.data_items.ACKC7.PPID_NOT_FOUND`   |
        +-------+------------------------+---------------------------------------------------------+
        | 5     | Mode unsupported       | :const:`secsgem.secs.data_items.ACKC7.MODE_UNSUPPORTED` |
        +-------+------------------------+---------------------------------------------------------+
        | 6     | Performed later        | :const:`secsgem.secs.data_items.ACKC7.PERFORMED_LATER`  |
        +-------+------------------------+---------------------------------------------------------+
        | 7-63  | Reserved               |                                                         |
        +-------+------------------------+---------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS07F04 <secsgem.secs.functions.SecsS07F04>`
        - :class:`SecsS07F18 <secsgem.secs.functions.SecsS07F18>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACCEPTED = 0
    NO_PERMISSION = 1
    LENGTH_ERROR = 2
    MATRIX_OVERFLOW = 3
    PPID_NOT_FOUND = 4
    MODE_UNSUPPORTED = 5
    PERFORMED_LATER = 6
