#####################################################################
# timestamp.py
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
"""TIMESTAMP data item."""
from .. import variables
from .base import DataItemBase


class TIMESTAMP(DataItemBase):
    """
    Timestamp.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem.secs.functions.SecsS05F11>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS15F41 <secsgem.secs.functions.SecsS15F41>`
        - :class:`SecsS15F44 <secsgem.secs.functions.SecsS15F44>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F07 <secsgem.secs.functions.SecsS16F07>`
        - :class:`SecsS16F09 <secsgem.secs.functions.SecsS16F09>`
    """

    __type__ = variables.String
    __count__ = 32
