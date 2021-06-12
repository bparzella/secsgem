#####################################################################
# objtype.py
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
"""OBJTYPE data item."""
from .. import variables
from .base import DataItemBase


class OBJTYPE(DataItemBase):
    """
    Class of object identifier.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS01F19 <secsgem.secs.functions.SecsS01F19>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F07 <secsgem.secs.functions.SecsS14F07>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F25 <secsgem.secs.functions.SecsS14F25>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F27 <secsgem.secs.functions.SecsS14F27>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.String
    ]
