#####################################################################
# ackc6.py
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
"""ACKC6 data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ACKC6(DataItemBase):
    """Acknowledge code for stream 6.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------+-------------------------------------------------+
        | Value | Description | Constant                                        |
        +=======+=============+=================================================+
        | 0     | Accepted    | :const:`secsgem.secs.data_items.ACKC6.ACCEPTED` |
        +-------+-------------+-------------------------------------------------+
        | 1-63  | Error       | :const:`secsgem.secs.data_items.ACKC6.ERROR`    |
        +-------+-------------+-------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F02 <secsgem.secs.functions.SecsS06F02>`
        - :class:`SecsS06F12 <secsgem.secs.functions.SecsS06F12>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACCEPTED = 0
    ERROR = 1
