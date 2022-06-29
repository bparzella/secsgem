#####################################################################
# rsda.py
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
"""RSDA data item."""
from .. import variables
from .base import DataItemBase


class RSDA(DataItemBase):
    """ Spool request reply 

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
        - :class:`SecsS06F24 <secsgem.secs.functions.SecsS05F02>`

    """

    __type__ = secsgem.secs.variables.Binary
    __count__ = 1

    OK = 0
    RETRYABLE_BUSY = 1
    NO_SPOOL_DATA = 2
