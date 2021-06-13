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

from .header import HsmsHeader


class HsmsStreamFunctionHeader(HsmsHeader):
    """
    Header for SECS message.

    Header for message with SType 0.
    """

    def __init__(self, system, stream, function, require_response, session_id):
        """
        Initialize a stream function secs header.

        :param system: message ID
        :type system: integer
        :param stream: messages stream
        :type stream: integer
        :param function: messages function
        :type function: integer
        :param require_response: is response expected from remote
        :type require_response: boolean
        :param session_id: device / session ID
        :type session_id: integer

        **Example**::

            >>> import secsgem.hsms
            >>>
            >>> secsgem.hsms.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
            HsmsStreamFunctionHeader({sessionID:0x0064, stream:01, function:01, pType:0x00, sType:0x00, \
system:0x00000016, requireResponse:True})
        """
        HsmsHeader.__init__(self, system, session_id)
        self.sessionID = session_id
        self.requireResponse = require_response
        self.stream = stream
        self.function = function
        self.pType = 0x00
        self.sType = 0x00
        self.system = system