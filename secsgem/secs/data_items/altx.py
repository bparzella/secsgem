#####################################################################
# altx.py
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
"""ALTX data item."""

from secsgem.secs import variables

from .base import DataItemBase


class ALTX(DataItemBase):
    """Alarm text.

    :Type: :class:`String <secsgem.secs.variables.String>`
    :Length: 120

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`
        - :class:`SecsS05F08 <secsgem.secs.functions.SecsS05F08>`

    """

    __type__ = variables.String
    __count__ = 120
