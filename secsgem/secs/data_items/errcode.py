#####################################################################
# errocde.py
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
"""ERRCODE data item."""
from .. import variables
from .base import DataItemBase


class ERRCODE(DataItemBase):
    """
    Reference point.

    :Types:
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`

    **Used In Function**
        - :class:`SecsS01F03 <secsgem.secs.functions.SecsS01F03>`
        - :class:`SecsS01F20 <secsgem.secs.functions.SecsS01F20>`
        - :class:`SecsS03F16 <secsgem.secs.functions.SecsS03F16>`
        - :class:`SecsS03F30 <secsgem.secs.functions.SecsS03F30>`
        - :class:`SecsS03F32 <secsgem.secs.functions.SecsS03F32>`
        - :class:`SecsS04F20 <secsgem.secs.functions.SecsS04F20>`
        - :class:`SecsS04F22 <secsgem.secs.functions.SecsS04F22>`
        - :class:`SecsS04F23 <secsgem.secs.functions.SecsS04F23>`
        - :class:`SecsS04F33 <secsgem.secs.functions.SecsS04F33>`
        - :class:`SecsS04F35 <secsgem.secs.functions.SecsS04F35>`
        - :class:`SecsS05F14 <secsgem.secs.functions.SecsS05F14>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS05F18 <secsgem.secs.functions.SecsS05F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F28 <secsgem.secs.functions.SecsS14F28>`
        - :class:`SecsS15F18 <secsgem.secs.functions.SecsS15F18>`
        - :class:`SecsS15F20 <secsgem.secs.functions.SecsS15F20>`
        - :class:`SecsS15F22 <secsgem.secs.functions.SecsS15F22>`
        - :class:`SecsS15F24 <secsgem.secs.functions.SecsS15F24>`
        - :class:`SecsS15F26 <secsgem.secs.functions.SecsS15F26>`
        - :class:`SecsS15F28 <secsgem.secs.functions.SecsS15F28>`
        - :class:`SecsS15F30 <secsgem.secs.functions.SecsS15F30>`
        - :class:`SecsS15F32 <secsgem.secs.functions.SecsS15F32>`
        - :class:`SecsS15F34 <secsgem.secs.functions.SecsS15F34>`
        - :class:`SecsS15F36 <secsgem.secs.functions.SecsS15F36>`
        - :class:`SecsS15F38 <secsgem.secs.functions.SecsS15F38>`
        - :class:`SecsS15F40 <secsgem.secs.functions.SecsS15F40>`
        - :class:`SecsS15F42 <secsgem.secs.functions.SecsS15F42>`
        - :class:`SecsS15F44 <secsgem.secs.functions.SecsS15F44>`
        - :class:`SecsS15F48 <secsgem.secs.functions.SecsS15F48>`
        - :class:`SecsS15F53 <secsgem.secs.functions.SecsS15F53>`
        - :class:`SecsS16F12 <secsgem.secs.functions.SecsS16F12>`
        - :class:`SecsS16F14 <secsgem.secs.functions.SecsS16F14>`
        - :class:`SecsS16F16 <secsgem.secs.functions.SecsS16F16>`
        - :class:`SecsS16F18 <secsgem.secs.functions.SecsS16F18>`
        - :class:`SecsS16F24 <secsgem.secs.functions.SecsS16F24>`
        - :class:`SecsS16F26 <secsgem.secs.functions.SecsS16F26>`
        - :class:`SecsS16F28 <secsgem.secs.functions.SecsS16F28>`
        - :class:`SecsS17F02 <secsgem.secs.functions.SecsS17F02>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F06 <secsgem.secs.functions.SecsS17F06>`
        - :class:`SecsS17F08 <secsgem.secs.functions.SecsS17F08>`
        - :class:`SecsS17F10 <secsgem.secs.functions.SecsS17F10>`
        - :class:`SecsS17F12 <secsgem.secs.functions.SecsS17F12>`
        - :class:`SecsS17F14 <secsgem.secs.functions.SecsS17F14>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8
    ]
