#####################################################################
# strack.py
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
"""STRACK data item."""
from .. import variables
from .base import DataItemBase


class STRACK(DataItemBase):
    """ spooling stream acknowledge 

       :Types: :class:`secsgem.secs.variables.Binary <secsgem.secs.variables.Binary>`
       :Length: 1

    **Values**
        +-------+---------+
        | Value |         |
        +=======+=========+
        | 1     | not allowed for stream |
        +-------+---------+
        | 2     | unknown stream  |
        +-------+---------+
        | 3     |unknown function |
        +-------+---------+
        | 4     | secondary function  |
        +-------+---------+

    **Used In Function**
        - :class:`SecsS02F44 <secsgem.secs.functions.SecsS02F44>`
    """

    __type__ = secsgem.secs.variables.Binary
    __count__ = 1
    STREAM_NOT_ALLOWED = 1
    UNKNOWN_STREAM = 2
    UNKNOWN_FUNCTION =3
    SECONDARY_FUNCTION = 4
