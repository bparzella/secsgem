#####################################################################
# aled.py
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
"""ALED data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ALED(DataItemBase):
    """Alarm en-/disable code byte.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +---------+-------------+-----------------------------------------------+
        | Value   | Description | Constant                                      |
        +=========+=============+===============================================+
        | 0       | Disable     | :const:`secsgem.secs.data_items.ALED.DISABLE` |
        +---------+-------------+-----------------------------------------------+
        | 1-127   | Not used    |                                               |
        +---------+-------------+-----------------------------------------------+
        | 128     | Enable      | :const:`secsgem.secs.data_items.ALED.ENABLE`  |
        +---------+-------------+-----------------------------------------------+
        | 129-255 | Not used    |                                               |
        +---------+-------------+-----------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F03 <secsgem.secs.functions.SecsS05F03>`

    """

    __type__ = variables.Binary
    __count__ = 1

    DISABLE = 0
    ENABLE = 128
