#####################################################################
# ffrot.py
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
"""FFROT data item."""

from secsgem.secs import variables

from .base import DataItemBase


class FFROT(DataItemBase):
    """Film frame rotation.

    In degrees from the bottom CW. (Bottom equals zero degrees.) Zero length indicates not used.

    :Type: :class:`U2 <secsgem.secs.variables.U2>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`

    """

    __type__ = variables.U2
