#####################################################################
# trid.py
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
"""TRID data item."""
from .. import variables
from .base import DataItemBase


class TRID(DataItemBase):
    """Trace Request identifier

    :Types:
       - :class:`secsgem.secs.variables.String <secsgem.secs.variables.U4>`

    **Used In Function**
        - :class:`SecsS02F23 <secsgem.secs.functions.SecsS02F23>`
        - :class:`SecsS06F01 <secsgem.secs.functions.SecsS06F01>`
    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [variables.String, 
                        variables.U1, 
                        variables.U2, 
                        variables.U4, 
                        variables.U8, 
                        variables.I1, 
                        variables.I2, 
                        variables.I4, 
                        variables.I8]
