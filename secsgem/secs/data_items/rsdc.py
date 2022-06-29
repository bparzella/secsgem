#####################################################################
# rsdc.py
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
"""RSDC data item."""
from .. import variables
from .base import DataItemBase


class RSDC(DataItemBase):
    """ Spool request code

       :Types: :class:`secsgem.secs.variables.Binary <secsgem.secs.variables.Binary>`
       :Length: 1

    **Values**
        +-------+-------------------+
        | Value | Description       | 
        +=======+===================+
        | 0     | OK                | 
        +-------+-------------------+
        | 1     | Retryable Busy    | 
        +-------+-------------------+
        | 2     | No Spool Data     | 
        +-------+-------------------+

    **Used In Function**
        - :class:`SecsS06F23 <secsgem.secs.functions.SecsS06F23>`

    """

    __type__ = secsgem.secs.variables.U1
    __count__ = 1

    TRANSMIT = 0
    PURGE = 1
