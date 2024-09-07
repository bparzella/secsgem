#####################################################################
# grant6.py
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
"""GRANT6 data item."""

from secsgem.secs import variables

from .base import DataItemBase


class GRANT6(DataItemBase):
    """Permission to send.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+----------------+--------------------------------------------------------+
        | Value | Description    | Constant                                               |
        +=======+================+========================================================+
        | 0     | Granted        | :const:`secsgem.secs.data_items.GRANT6.GRANTED`        |
        +-------+----------------+--------------------------------------------------------+
        | 1     | Busy           | :const:`secsgem.secs.data_items.GRANT6.BUSY`           |
        +-------+----------------+--------------------------------------------------------+
        | 2     | Not interested | :const:`secsgem.secs.data_items.GRANT6.NOT_INTERESTED` |
        +-------+----------------+--------------------------------------------------------+
        | 3-63  | Other error    |                                                        |
        +-------+----------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F06 <secsgem.secs.functions.SecsS06F06>`

    """

    __type__ = variables.Binary
    __count__ = 1

    GRANTED = 0
    BUSY = 1
    NOT_INTERESTED = 2
