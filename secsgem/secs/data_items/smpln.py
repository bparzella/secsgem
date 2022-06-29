#####################################################################
# smpln.py
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
"""SMPLN data item."""
from .. import variables
from .base import DataItemBase


class SMPLN(DataItemBase):
    """SECS message header

       :Types: :class:`secsgem.secs.variables.Binary <secsgem.secs.variables.Binary>`
       :Length: 10

    **Used In Function**
        - :class:`SecsS09F09 <secsgem.secs.functions.SecsS09F09>`

    """

    __type__ = secsgem.secs.variables.U4 # Centrotherm Firing Furnace

    # __type__ = secsgem.secs.variables.Dynamic
    # __allowedtypes__ = [secsgem.secs.variables.U1, secsgem.secs.variables.U2, secsgem.secs.variables.U4, secsgem.secs.variables.U8, secsgem.secs.variables.I1, secsgem.secs.variables.I2, secsgem.secs.variables.I4, secsgem.secs.variables.I8]
