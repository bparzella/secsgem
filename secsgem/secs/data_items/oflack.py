#####################################################################
# oflack.py
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
"""OFLACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class OFLACK(DataItemBase):
    """Acknowledge code for OFFLINE request.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+---------------------+---------------------------------------------+
        | Value | Description         | Constant                                    |
        +=======+=====================+=============================================+
        | 0     | OFFLINE Acknowledge | :const:`secsgem.secs.data_items.OFLACK.ACK` |
        +-------+---------------------+---------------------------------------------+
        | 1-63  | Reserved            |                                             |
        +-------+---------------------+---------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F16 <secsgem.secs.functions.SecsS01F16>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
