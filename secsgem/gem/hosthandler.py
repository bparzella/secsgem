#####################################################################
# hosthandler.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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
"""Handler for GEM host."""

from secsgem.gem.handler import GemHandler


class GemHostHandler(GemHandler):
    """Baseclass for creating host models. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        GemHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

        self.isHost = True
