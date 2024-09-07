#####################################################################
# alcd.py
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
"""ALCD data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ALCD(DataItemBase):
    """Alarm code byte.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+---------------------------+-----------------------------------------------------------------+
        | Value | Description               | Constant                                                        |
        +=======+===========================+=================================================================+
        | 0     | Not used                  |                                                                 |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 1     | Personal safety           | :const:`secsgem.secs.data_items.ALCD.PERSONAL_SAFETY`           |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 2     | Equipment safety          | :const:`secsgem.secs.data_items.ALCD.EQUIPMENT_SAFETY`          |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 3     | Parameter control warning | :const:`secsgem.secs.data_items.ALCD.PARAMETER_CONTROL_WARNING` |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 4     | Parameter control error   | :const:`secsgem.secs.data_items.ALCD.PARAMETER_CONTROL_ERROR`   |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 5     | Irrecoverable error       | :const:`secsgem.secs.data_items.ALCD.IRRECOVERABLE_ERROR`       |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 6     | Equipment status warning  | :const:`secsgem.secs.data_items.ALCD.EQUIPMENT_STATUS_WARNING`  |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 7     | Attention flags           | :const:`secsgem.secs.data_items.ALCD.ATTENTION_FLAGS`           |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 8     | Data integrity            | :const:`secsgem.secs.data_items.ALCD.DATA_INTEGRITY`            |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 9-63  | Other catogeries          |                                                                 |
        +-------+---------------------------+-----------------------------------------------------------------+
        | 128   | Alarm set flag            | :const:`secsgem.secs.data_items.ALCD.ALARM_SET`                 |
        +-------+---------------------------+-----------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`
        - :class:`SecsS05F08 <secsgem.secs.functions.SecsS05F08>`

    """

    __type__ = variables.Binary
    __count__ = 1

    PERSONAL_SAFETY = 1
    EQUIPMENT_SAFETY = 2
    PARAMETER_CONTROL_WARNING = 3
    PARAMETER_CONTROL_ERROR = 4
    IRRECOVERABLE_ERROR = 5
    EQUIPMENT_STATUS_WARNING = 6
    ATTENTION_FLAGS = 7
    DATA_INTEGRITY = 8
    ALARM_SET = 128
