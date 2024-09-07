#####################################################################
# cepack.py
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
"""CEPACK data item."""

from secsgem.secs import variables

from .base import DataItemBase


class CEPACK(DataItemBase):
    """Command enhanced parameter acknowledge.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`

    **Values**
        +-------+----------------------------+---------------------------------------------------------------+
        | Value | Description                | Constant                                                      |
        +=======+============================+===============================================================+
        | 0     | No error                   | :const:`secsgem.secs.data_items.CEPACK.NO_ERROR`              |
        +-------+----------------------------+---------------------------------------------------------------+
        | 1     | CPNAME name does not exist | :const:`secsgem.secs.data_items.CEPACK.CPNAME_UNKNOWN`        |
        +-------+----------------------------+---------------------------------------------------------------+
        | 2     | Illegal value for CEPVAL   | :const:`secsgem.secs.data_items.CEPACK.CEPVAL_ILLEGAL_VALUE`  |
        +-------+----------------------------+---------------------------------------------------------------+
        | 3     | Illegal format for CEPVAL  | :const:`secsgem.secs.data_items.CEPACK.CEPVAL_ILLEGAL_FORMAT` |
        +-------+----------------------------+---------------------------------------------------------------+
        | 4     | CPNAME not valid as used   | :const:`secsgem.secs.data_items.CEPACK.CPNAME_INVALID`        |
        +-------+----------------------------+---------------------------------------------------------------+
        | 5-63  | Reserved                   |                                                               |
        +-------+----------------------------+---------------------------------------------------------------+

    """

    __type__ = variables.Binary

    NO_ERROR = 0
    CPNAME_UNKNOWN = 1
    CEPVAL_ILLEGAL_VALUE = 2
    CEPVAL_ILLEGAL_FORMAT = 3
    CPNAME_INVALID = 4
