#####################################################################
# rcmd.py
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
"""RCMD data item."""

from secsgem.secs import variables

from .base import DataItemBase


class RCMD(DataItemBase):
    """Remote command.

    :Types:
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS02F21 <secsgem.secs.functions.SecsS02F21>`
        - :class:`SecsS02F41 <secsgem.secs.functions.SecsS02F41>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.I1,
        variables.String,
    ]
