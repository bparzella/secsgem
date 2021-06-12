#####################################################################
# objspec.py
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
"""OBJSPEC data item."""
from .. import variables
from .base import DataItemBase


class OBJSPEC(DataItemBase):
    """
    Specific object instance.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS13F13 <secsgem.secs.functions.SecsS13F13>`
        - :class:`SecsS13F15 <secsgem.secs.functions.SecsS13F15>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F05 <secsgem.secs.functions.SecsS14F05>`
        - :class:`SecsS14F07 <secsgem.secs.functions.SecsS14F07>`
        - :class:`SecsS14F09 <secsgem.secs.functions.SecsS14F09>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F11 <secsgem.secs.functions.SecsS14F11>`
        - :class:`SecsS14F13 <secsgem.secs.functions.SecsS14F13>`
        - :class:`SecsS14F15 <secsgem.secs.functions.SecsS14F15>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F17 <secsgem.secs.functions.SecsS14F17>`
        - :class:`SecsS14F19 <secsgem.secs.functions.SecsS14F19>`
        - :class:`SecsS14F25 <secsgem.secs.functions.SecsS14F25>`
        - :class:`SecsS14F27 <secsgem.secs.functions.SecsS14F27>`
        - :class:`SecsS15F43 <secsgem.secs.functions.SecsS15F43>`
        - :class:`SecsS15F47 <secsgem.secs.functions.SecsS15F47>`

    """

    __type__ = variables.String
