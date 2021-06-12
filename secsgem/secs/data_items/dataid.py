#####################################################################
# dataid.py
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
"""DATAID data item."""
from .. import variables
from .base import DataItemBase


class DATAID(DataItemBase):
    """
    Data ID.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS02F33 <secsgem.secs.functions.SecsS02F33>`
        - :class:`SecsS02F35 <secsgem.secs.functions.SecsS02F35>`
        - :class:`SecsS02F39 <secsgem.secs.functions.SecsS02F39>`
        - :class:`SecsS02F45 <secsgem.secs.functions.SecsS02F45>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS03F15 <secsgem.secs.functions.SecsS03F15>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS04F19 <secsgem.secs.functions.SecsS04F19>`
        - :class:`SecsS04F25 <secsgem.secs.functions.SecsS04F25>`
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F05 <secsgem.secs.functions.SecsS06F05>`
        - :class:`SecsS06F07 <secsgem.secs.functions.SecsS06F07>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`
        - :class:`SecsS06F09 <secsgem.secs.functions.SecsS06F09>`
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS06F27 <secsgem.secs.functions.SecsS06F27>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS13F13 <secsgem.secs.functions.SecsS13F13>`
        - :class:`SecsS13F15 <secsgem.secs.functions.SecsS13F15>`
        - :class:`SecsS14F19 <secsgem.secs.functions.SecsS14F19>`
        - :class:`SecsS14F21 <secsgem.secs.functions.SecsS14F21>`
        - :class:`SecsS14F23 <secsgem.secs.functions.SecsS14F23>`
        - :class:`SecsS15F27 <secsgem.secs.functions.SecsS15F27>`
        - :class:`SecsS15F29 <secsgem.secs.functions.SecsS15F29>`
        - :class:`SecsS15F33 <secsgem.secs.functions.SecsS15F33>`
        - :class:`SecsS15F35 <secsgem.secs.functions.SecsS15F35>`
        - :class:`SecsS15F37 <secsgem.secs.functions.SecsS15F37>`
        - :class:`SecsS15F39 <secsgem.secs.functions.SecsS15F39>`
        - :class:`SecsS15F41 <secsgem.secs.functions.SecsS15F41>`
        - :class:`SecsS15F43 <secsgem.secs.functions.SecsS15F43>`
        - :class:`SecsS15F45 <secsgem.secs.functions.SecsS15F45>`
        - :class:`SecsS15F47 <secsgem.secs.functions.SecsS15F47>`
        - :class:`SecsS15F49 <secsgem.secs.functions.SecsS15F49>`
        - :class:`SecsS16F01 <secsgem.secs.functions.SecsS16F01>`
        - :class:`SecsS16F03 <secsgem.secs.functions.SecsS16F03>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F11 <secsgem.secs.functions.SecsS16F11>`
        - :class:`SecsS16F13 <secsgem.secs.functions.SecsS16F13>`
        - :class:`SecsS17F01 <secsgem.secs.functions.SecsS17F01>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`
        - :class:`SecsS17F09 <secsgem.secs.functions.SecsS17F09>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8,
        variables.String
    ]
