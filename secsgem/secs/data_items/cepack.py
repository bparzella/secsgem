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
from .. import variables
from .base import DataItemBase


class CEPACK(DataItemBase):
    """
    Command parameter acknowledge code.

       :Types: :class:`Binary <secsgem.secs.variables.Binary>`
       :Length: 1

    **Values**
        +-------+------------------------+--------------------------------------------------------------+
        | Value | Description            | Constant                                                     |
        +=======+========================+==============================================================+
        | 0     | No error               | :const:`secsgem.secs.data_items.CEPACK.NO_ERROR`             |
        +-------+------------------------+--------------------------------------------------------------+
        | 1     | Parameter name unknown | :const:`secsgem.secs.data_items.CEPACK.PARAMETER_UNKNOWN`    |
        +-------+------------------------+--------------------------------------------------------------+
        | 2     | CEPVAL value illegal   | :const:`secsgem.secs.data_items.CEPACK.CEPVAL_ILLEGAL_VALUE` |
        +-------+------------------------+--------------------------------------------------------------+
        | 3     | CEPVAL format illegal  | :const:`secsgem.secs.data_items.CEPACK.CEPVAL_ILLEGAL_FORMAT`|
        +-------+------------------------+--------------------------------------------------------------+
        | 4     | CPNAME format illegal  | :const:`secsgem.secs.data_items.CEPACK.CPNAME_NOT_VALID`     |
        +-------+------------------------+--------------------------------------------------------------+
        | 5-63  | Reserved               |                                                              |
        +-------+------------------------+--------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F50 <secsgem.secs.functions.SecsS02F50>`
    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.Array,
        variables.U1
    ]
    __count__ = 1

    NO_ERROR = 0
    PARAMETER_UNKNOWN = 1
    CEPVAL_ILLEGAL_VALUE = 2
    CEPVAL_ILLEGAL_FORMAT = 3
    CPNAME_NOT_VALID = 4
