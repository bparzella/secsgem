#####################################################################
# rptid.py
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
"""RPTID data item."""
from .. import variables
from .base import DataItemBase


class RPTID(DataItemBase):
    """
    Report ID.

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
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS06F19 <secsgem.secs.functions.SecsS06F19>`
        - :class:`SecsS06F21 <secsgem.secs.functions.SecsS06F21>`
        - :class:`SecsS06F27 <secsgem.secs.functions.SecsS06F27>`
        - :class:`SecsS06F30 <secsgem.secs.functions.SecsS06F30>`
        - :class:`SecsS17F01 <secsgem.secs.functions.SecsS17F01>`
        - :class:`SecsS17F02 <secsgem.secs.functions.SecsS17F02>`
        - :class:`SecsS17F03 <secsgem.secs.functions.SecsS17F03>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`
        - :class:`SecsS17F09 <secsgem.secs.functions.SecsS17F09>`
        - :class:`SecsS17F11 <secsgem.secs.functions.SecsS17F11>`
        - :class:`SecsS17F12 <secsgem.secs.functions.SecsS17F12>`

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
