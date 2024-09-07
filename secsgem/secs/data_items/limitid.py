#####################################################################
# limitid.py
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
"""LIMITID data item."""

from secsgem.secs import variables

from .base import DataItemBase


class LIMITID(DataItemBase):
    """Limit ID.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 1

    **Used In Function**
        - :class:`SecsS02F45 <secsgem.secs.functions.SecsS02F45>`
        - :class:`SecsS02F46 <secsgem.secs.functions.SecsS02F46>`
        - :class:`SecsS02F48 <secsgem.secs.functions.SecsS02F48>`

    """

    __type__ = variables.Binary
    __count__ = 1
