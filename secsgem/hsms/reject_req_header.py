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

from .header import HsmsHeader, HsmsSType


class HsmsRejectReqHeader(HsmsHeader):
    """Header for Reject Request.

    Header for message with SType 7.
    """

    def __init__(self, system: int, s_type: HsmsSType, reason: int):
        """Initialize a hsms reject request.

        :param system: message ID
        :type system: integer
        :param s_type: s_type of rejected message
        :type s_type: integer
        :param reason: reason for rejection
        :type reason: integer

        Example:
            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsRejectReqHeader(17, secsgem.hsms.HsmsSType.DESELECT_REQ, 4)
            HsmsRejectReqHeader({session_id:0xffff, stream:03, function:04, p_type:0x00, s_type:0x07, \
system:0x00000011, require_response:False})
        """
        super().__init__(system, 0xFFFF, s_type.value, reason, False, 0x00, HsmsSType.REJECT_REQ)
