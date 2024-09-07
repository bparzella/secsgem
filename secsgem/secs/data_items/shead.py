#####################################################################
# shead.py
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
"""SHEAD data item."""

from secsgem.secs import variables

from .base import DataItemBase


class SHEAD(DataItemBase):
    """SECS message header.

    :Type: :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 10

    **Used In Function**
        - :class:`SecsS09F09 <secsgem.secs.functions.SecsS09F09>`

    """

    __type__ = variables.Binary
    __count__ = 10
