#####################################################################
# deselect_rsp_header.py
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
"""Header for the hsms deselect response."""

from .header import HsmsHeader


class HsmsDeselectRspHeader(HsmsHeader):
    """
    Header for Deselect Response.

    Header for message with SType 4.
    """

    def __init__(self, system):
        """
        Initialize a hsms deslelct response.

        :param system: message ID
        :type system: integer

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsDeselectRspHeader(1)
            HsmsDeselectRspHeader({sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x04, \
system:0x00000001, requireResponse:False})
        """
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = 0x00
        self.function = 0x00
        self.pType = 0x00
        self.sType = 0x04