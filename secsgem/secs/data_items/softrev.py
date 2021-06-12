#####################################################################
# softrev.py
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
"""SOFTREV data item."""
from .. import variables
from .base import DataItemBase


class SOFTREV(DataItemBase):
    """
    Software revision.

    :Types:
       - :class:`String <secsgem.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS01F02 <secsgem.secs.functions.SecsS01F02>`
        - :class:`SecsS01F13 <secsgem.secs.functions.SecsS01F13>`
        - :class:`SecsS01F14 <secsgem.secs.functions.SecsS01F14>`
        - :class:`SecsS07F22 <secsgem.secs.functions.SecsS07F22>`
        - :class:`SecsS07F23 <secsgem.secs.functions.SecsS07F23>`
        - :class:`SecsS07F26 <secsgem.secs.functions.SecsS07F26>`
        - :class:`SecsS07F31 <secsgem.secs.functions.SecsS07F31>`
        - :class:`SecsS07F39 <secsgem.secs.functions.SecsS07F39>`
        - :class:`SecsS07F43 <secsgem.secs.functions.SecsS07F43>`

    """

    __type__ = variables.String
    __count__ = 20
