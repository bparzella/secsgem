#####################################################################
# mdack.py
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
"""MDACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class MDACK(DataItemBase):
    """Map data acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------------+-----------------------------------------------------+
        | Value | Description       | Constant                                            |
        +=======+===================+=====================================================+
        | 0     | Map received      | :const:`secsgem.secs.data_items.MDACK.ACK`          |
        +-------+-------------------+-----------------------------------------------------+
        | 1     | Format error      | :const:`secsgem.secs.data_items.MDACK.FORMAT_ERROR` |
        +-------+-------------------+-----------------------------------------------------+
        | 2     | No ID match       | :const:`secsgem.secs.data_items.MDACK.UNKNOWN_ID`   |
        +-------+-------------------+-----------------------------------------------------+
        | 3     | Abort/discard map | :const:`secsgem.secs.data_items.MDACK.ABORT_MAP`    |
        +-------+-------------------+-----------------------------------------------------+
        | 4-63  | Reserved, error   |                                                     |
        +-------+-------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F08 <secsgem.secs.functions.SecsS12F08>`
        - :class:`SecsS12F10 <secsgem.secs.functions.SecsS12F10>`
        - :class:`SecsS12F12 <secsgem.secs.functions.SecsS12F12>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    FORMAT_ERROR = 1
    UNKNOWN_ID = 2
    ABORT_MAP = 3
