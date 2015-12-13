#####################################################################
# equipmenthandler.py
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
"""Handler for GEM equipment."""

from secsgem.gem.handler import GemHandler


class GemEquipmentHandler(GemHandler):
    """Baseclass for creating equipment models. Inherit from this class and override required functions.

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

        self.isHost = False

        self.register_callback(2, 33, self.s02f33_handler)
        self.register_callback(2, 37, self.s02f37_handler)

    def s02f33_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 33, Define Report

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        handler.send_response(self.stream_function(2, 34)(0), packet.header.system)

    def s02f37_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 37, En-/Disable Event Report

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        handler.send_response(self.stream_function(2, 38)(0), packet.header.system)
