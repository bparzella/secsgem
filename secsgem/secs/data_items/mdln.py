#####################################################################
# mdln.py
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
"""MDLN data item."""

from secsgem.secs import variables

from .base import DataItemBase


class MDLN(DataItemBase):
    """Equipment model type.

    :Type: :class:`String <secsgem.secs.variables.String>`
    :Length: 20

    **Used In Function**
        - :class:`SecsS01F02 <secsgem.secs.functions.SecsS01F02>`
        - :class:`SecsS01F13 <secsgem.secs.functions.SecsS01F13>`
        - :class:`SecsS01F14 <secsgem.secs.functions.SecsS01F14>`

    """

    __type__ = variables.String
    __count__ = 20
