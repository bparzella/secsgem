#####################################################################
# idtyp.py
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
"""IDTYP data item."""

from secsgem.secs import variables

from .base import DataItemBase


class IDTYP(DataItemBase):
    """ID type.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------------+-------------------------------------------------------+
        | Value | Description       | Constant                                              |
        +=======+===================+=======================================================+
        | 0     | Wafer ID          | :const:`secsgem.secs.data_items.IDTYP.WAFER`          |
        +-------+-------------------+-------------------------------------------------------+
        | 1     | Wafer cassette ID | :const:`secsgem.secs.data_items.IDTYP.WAFER_CASSETTE` |
        +-------+-------------------+-------------------------------------------------------+
        | 2     | Film frame ID     | :const:`secsgem.secs.data_items.IDTYP.FILM_FRAME`     |
        +-------+-------------------+-------------------------------------------------------+
        | 3-63  | Reserved, error   |                                                       |
        +-------+-------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F05>`
        - :class:`SecsS12F07 <secsgem.secs.functions.SecsS12F07>`
        - :class:`SecsS12F09 <secsgem.secs.functions.SecsS12F09>`
        - :class:`SecsS12F11 <secsgem.secs.functions.SecsS12F11>`
        - :class:`SecsS12F13 <secsgem.secs.functions.SecsS12F13>`
        - :class:`SecsS12F14 <secsgem.secs.functions.SecsS12F14>`
        - :class:`SecsS12F15 <secsgem.secs.functions.SecsS12F15>`
        - :class:`SecsS12F16 <secsgem.secs.functions.SecsS12F16>`
        - :class:`SecsS12F17 <secsgem.secs.functions.SecsS12F17>`
        - :class:`SecsS12F18 <secsgem.secs.functions.SecsS12F18>`

    """

    __type__ = variables.Binary
    __count__ = 1

    WAFER = 0
    WAFER_CASSETTE = 1
    FILM_FRAME = 2
