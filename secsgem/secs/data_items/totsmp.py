#####################################################################
# totsmp.py
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
"""TOTSMP data item."""
from .. import variables
from .base import DataItemBase


class TOTSMP(DataItemBase):
    """Total Samples to be made

    :Types:
       - :class:`secsgem.secs.variables.String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS02F23 <secsgem.secs.functions.SecsS02F23>`
    """

    __type__ = secsgem.secs.variables.Dynamic    
    __allowedtypes__ = [secsgem.secs.variables.U1, secsgem.secs.variables.U2, secsgem.secs.variables.U4, secsgem.secs.variables.U8, secsgem.secs.variables.F4, secsgem.secs.variables.F8,secsgem.secs.variables.String]

