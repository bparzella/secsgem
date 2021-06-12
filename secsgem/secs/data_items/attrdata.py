#####################################################################
# attrdata.py
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
"""ATTRDATA data item."""
from .. import variables
from .base import DataItemBase


class ATTRDATA(DataItemBase):
    """
    Object attribute value.

    :Types:
       - :class:`Array <secsgem.secs.variables.Array>`
       - :class:`Binary <secsgem.secs.variables.Binary>`
       - :class:`Boolean <secsgem.secs.variables.Boolean>`
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`
       - :class:`F8 <secsgem.secs.variables.F8>`
       - :class:`F4 <secsgem.secs.variables.F4>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS01F20 <secsgem.secs.functions.SecsS01F20>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS03F18 <secsgem.secs.functions.SecsS03F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F09 <secsgem.secs.functions.SecsS14F09>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F11 <secsgem.secs.functions.SecsS14F11>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F13 <secsgem.secs.functions.SecsS14F13>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F15 <secsgem.secs.functions.SecsS14F15>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F17 <secsgem.secs.functions.SecsS14F17>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS18F02 <secsgem.secs.functions.SecsS18F02>`
        - :class:`SecsS18F03 <secsgem.secs.functions.SecsS18F03>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.Array,
        variables.Boolean,
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8,
        variables.F4,
        variables.F8,
        variables.String,
        variables.Binary
    ]
