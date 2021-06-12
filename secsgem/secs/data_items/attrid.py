#####################################################################
# attrid.py
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
"""ATTRID data item."""
from .. import variables
from .base import DataItemBase


class ATTRID(DataItemBase):
    """
    Object attribute identifier.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS01F19 <secsgem.secs.functions.SecsS01F19>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS03F18 <secsgem.secs.functions.SecsS03F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
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
        - :class:`SecsS18F01 <secsgem.secs.functions.SecsS18F01>`
        - :class:`SecsS18F03 <secsgem.secs.functions.SecsS18F03>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.String
    ]
