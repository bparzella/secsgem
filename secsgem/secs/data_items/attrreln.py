#####################################################################
# attrreln.py
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
"""ATTRRELN data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ATTRRELN(DataItemBase):
    """Attribute relation to attribute of object.

    :Type: :class:`U1 <secsgem.secs.variables.U1>`

    **Values**
        +-------+-----------------------+------------------------------------------------------+
        | Value | Description           | Constant                                             |
        +=======+=======================+======================================================+
        | 0     | Equal to              | :const:`secsgem.secs.data_items.ATTRRELN.EQUAL`      |
        +-------+-----------------------+------------------------------------------------------+
        | 1     | Not equal to          | :const:`secsgem.secs.data_items.ATTRRELN.NOT_EQUAL`  |
        +-------+-----------------------+------------------------------------------------------+
        | 2     | Less than             | :const:`secsgem.secs.data_items.ATTRRELN.LESS`       |
        +-------+-----------------------+------------------------------------------------------+
        | 3     | Less than or equal to | :const:`secsgem.secs.data_items.ATTRRELN.LESS_EQUAL` |
        +-------+-----------------------+------------------------------------------------------+
        | 4     | More than             | :const:`secsgem.secs.data_items.ATTRRELN.MORE`       |
        +-------+-----------------------+------------------------------------------------------+
        | 5     | More than or equal to | :const:`secsgem.secs.data_items.ATTRRELN.MORE_EQUAL` |
        +-------+-----------------------+------------------------------------------------------+
        | 6     | Value present         | :const:`secsgem.secs.data_items.ATTRRELN.PRESENT`    |
        +-------+-----------------------+------------------------------------------------------+
        | 7     | Value absent          | :const:`secsgem.secs.data_items.ATTRRELN.ABSENT`     |
        +-------+-----------------------+------------------------------------------------------+
        | 8-63  | Error                 |                                                      |
        +-------+-----------------------+------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`

    """

    __type__ = variables.U1

    EQUAL = 0
    NOT_EQUAL = 1
    LESS = 2
    LESS_EQUAL = 3
    MORE = 4
    MORE_EQUAL = 5
    PRESENT = 6
    ABSENT = 7
