#####################################################################
# ppid.py
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
"""PPID data item."""

from secsgem.secs import variables

from .base import DataItemBase


class PPID(DataItemBase):
    """Process program ID.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`Binary <secsgem.secs.variables.Binary>`
    :Length: 120

    **Used In Function**
        - :class:`SecsS07F01 <secsgem.secs.functions.SecsS07F01>`
        - :class:`SecsS07F03 <secsgem.secs.functions.SecsS07F03>`
        - :class:`SecsS07F05 <secsgem.secs.functions.SecsS07F05>`
        - :class:`SecsS07F06 <secsgem.secs.functions.SecsS07F06>`
        - :class:`SecsS07F17 <secsgem.secs.functions.SecsS07F17>`
        - :class:`SecsS07F20 <secsgem.secs.functions.SecsS07F20>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.String,
        variables.Binary,
    ]
    __count__ = 120
