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
from .. import variables
from .base import DataItemBase


class PPID(DataItemBase):
    """
    Process program ID.

    :Types:
       - :class:`Binary <secsgem.secs.variables.Binary>`
       - :class:`String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS02F27 <secsgem.secs.functions.SecsS02F27>`
        - :class:`SecsS07F01 <secsgem.secs.functions.SecsS07F01>`
        - :class:`SecsS07F03 <secsgem.secs.functions.SecsS07F03>`
        - :class:`SecsS07F05 <secsgem.secs.functions.SecsS07F05>`
        - :class:`SecsS07F06 <secsgem.secs.functions.SecsS07F06>`
        - :class:`SecsS07F08 <secsgem.secs.functions.SecsS07F08>`
        - :class:`SecsS07F10 <secsgem.secs.functions.SecsS07F10>`
        - :class:`SecsS07F11 <secsgem.secs.functions.SecsS07F11>`
        - :class:`SecsS07F13 <secsgem.secs.functions.SecsS07F13>`
        - :class:`SecsS07F17 <secsgem.secs.functions.SecsS07F17>`
        - :class:`SecsS07F20 <secsgem.secs.functions.SecsS07F20>`
        - :class:`SecsS07F23 <secsgem.secs.functions.SecsS07F23>`
        - :class:`SecsS07F25 <secsgem.secs.functions.SecsS07F25>`
        - :class:`SecsS07F26 <secsgem.secs.functions.SecsS07F26>`
        - :class:`SecsS07F27 <secsgem.secs.functions.SecsS07F27>`
        - :class:`SecsS07F31 <secsgem.secs.functions.SecsS07F31>`
        - :class:`SecsS07F33 <secsgem.secs.functions.SecsS07F33>`
        - :class:`SecsS07F34 <secsgem.secs.functions.SecsS07F34>`
        - :class:`SecsS07F36 <secsgem.secs.functions.SecsS07F36>`
        - :class:`SecsS07F53 <secsgem.secs.functions.SecsS07F53>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [variables.String, variables.Binary]
    __count__ = 120
