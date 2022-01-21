#####################################################################
# ceed.py
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
"""CEED data item."""
from .. import variables
from .base import DataItemBase


class CEED(DataItemBase):
    """
    Collection event or trace enable/disable code.

       :Types: :class:`Boolean <secsgem.secs.variables.Boolean>`
       :Length: 1

    **Values**
        +-------+---------+
        | Value | State   |
        +=======+=========+
        | True  | Enable  |
        +-------+---------+
        | False | Disable |
        +-------+---------+

    **Used In Function**
        - :class:`SecsS02F37 <secsgem.secs.functions.SecsS02F37>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`

    """

    __type__ = variables.Boolean
    __count__ = 1

    ENABLE = True
    DISABLE = False
