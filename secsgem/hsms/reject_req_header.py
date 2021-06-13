#####################################################################
# reject_req_header.py
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
"""Header for the hsms reject request."""

from .header import HsmsHeader


class HsmsRejectReqHeader(HsmsHeader):
    """
    Header for Reject Request.

    Header for message with SType 7.
    """

    def __init__(self, system, s_type, reason):
        """
        Initialize a hsms reject request.

        :param system: message ID
        :type system: integer
        :param s_type: sType of rejected message
        :type s_type: integer
        :param reason: reason for rejection
        :type reason: integer

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsRejectReqHeader(17, 3, 4)
            HsmsRejectReqHeader({sessionID:0xffff, stream:03, function:04, pType:0x00, sType:0x07, system:0x00000011, \
requireResponse:False})
        """
        HsmsHeader.__init__(self, system, 0xFFFF)
        self.requireResponse = False
        self.stream = s_type
        self.function = reason
        self.pType = 0x00
        self.sType = 0x07