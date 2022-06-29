#####################################################################
# stime.py
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
"""STIME data item."""
from .. import variables
from .base import DataItemBase


class STIME(DataItemBase):
    """ECV Time Format

    :Types:
       - :class:`secsgem.secs.variables.I8 <secsgem.secs.variables.I8>`
       - :class:`secsgem.secs.variables.I1 <secsgem.secs.variables.I1>`
       - :class:`secsgem.secs.variables.I2 <secsgem.secs.variables.I2>`
       - :class:`secsgem.secs.variables.I4 <secsgem.secs.variables.I4>`

    **Used In Function**
        - :class:`SecsS06F01 <secsgem.secs.functions.SecsS06F01>`
    """

    __type__ = variables.String
