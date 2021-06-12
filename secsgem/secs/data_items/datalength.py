#####################################################################
# datalength.py
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
"""DATALENGTH data item."""
from .. import variables
from .base import DataItemBase


class DATALENGTH(DataItemBase):
    """
    Length of data to be sent.

    :Types:
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS02F39 <secsgem.secs.functions.SecsS02F39>`
        - :class:`SecsS03F15 <secsgem.secs.functions.SecsS03F15>`
        - :class:`SecsS03F29 <secsgem.secs.functions.SecsS03F29>`
        - :class:`SecsS03F31 <secsgem.secs.functions.SecsS03F31>`
        - :class:`SecsS04F25 <secsgem.secs.functions.SecsS04F25>`
        - :class:`SecsS06F05 <secsgem.secs.functions.SecsS06F05>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS14F23 <secsgem.secs.functions.SecsS14F23>`
        - :class:`SecsS16F01 <secsgem.secs.functions.SecsS16F01>`
        - :class:`SecsS16F11 <secsgem.secs.functions.SecsS16F11>`
        - :class:`SecsS18F05 <secsgem.secs.functions.SecsS18F05>`
        - :class:`SecsS18F07 <secsgem.secs.functions.SecsS18F07>`
        - :class:`SecsS19F19 <secsgem.secs.functions.SecsS19F19>`

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
        variables.I8
    ]
