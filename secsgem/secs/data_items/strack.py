#####################################################################
# strack.py
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
"""STRACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class STRACK(DataItemBase):
    """Spool stream acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------------------+----------------------------------------------------------+
        | Value | Description                        | Constant                                                 |
        +=======+====================================+==========================================================+
        | 1     | Spooling not allowed for stream    | :const:`secsgem.secs.data_items.STRACK.NOT_ALLOWED`      |
        +-------+------------------------------------+----------------------------------------------------------+
        | 2     | Stream unknown                     | :const:`secsgem.secs.data_items.STRACK.STREAM_UNKNOWN`   |
        +-------+------------------------------------+----------------------------------------------------------+
        | 3     | Unknown function for stream        | :const:`secsgem.secs.data_items.STRACK.FUNCTION_UNKNOWN` |
        +-------+------------------------------------+----------------------------------------------------------+
        | 4     | Secondary function for this stream | :const:`secsgem.secs.data_items.STRACK.SECONDARY`        |
        +-------+------------------------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F44 <secsgem.secs.functions.SecsS02F44>`

    """

    __type__ = variables.Binary
    __count__ = 1

    NOT_ALLOWED = 1
    STREAM_UNKNOWN = 2
    FUNCTION_UNKNOWN = 3
    SECONDARY = 4
