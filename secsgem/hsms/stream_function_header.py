#####################################################################
# stream_function_header.py
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
"""HSMS Header for streams/functions."""

from .header import HsmsHeader, HsmsSType


class HsmsStreamFunctionHeader(HsmsHeader):
    """Header for SECS message.

    Header for message with SType 0.
    """

    def __init__(  # pylint: disable=too-many-arguments
            self,
            system: int,
            stream: int,
            function: int,
            require_response: bool,
            session_id: int):
        """Initialize a stream function secs header.

        Args:
            system: message ID
            stream: messages stream
            function: messages function
            require_response: is response expected from remote
            session_id: device / session ID

        Example:
            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
            HsmsStreamFunctionHeader({session_id:0x0064, stream:01, function:01, p_type:0x00, s_type:0x00, \
system:0x00000016, require_response:True})
        """
        super().__init__(system, session_id, stream, function, require_response, 0x00, HsmsSType.DATA_MESSAGE)
