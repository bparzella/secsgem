#####################################################################
# deselect_req_header.py
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
"""Header for the hsms deselect request."""

from .header import HsmsHeader, HsmsSType


class HsmsDeselectReqHeader(HsmsHeader):
    """Header for Deselect Request.

    Header for message with SType 3.
    """

    def __init__(self, system: int):
        """Initialize a hsms deselect request.

        Args:
            system: message ID

        Example:
            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsDeselectReqHeader(1)
            HsmsDeselectReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x03, \
system:0x00000001, require_response:False})

        """
        super().__init__(system, 0xFFFF, 0, 0, False, 0x00, HsmsSType.DESELECT_REQ)
