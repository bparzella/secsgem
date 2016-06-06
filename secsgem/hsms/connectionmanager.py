#####################################################################
# connectionmanager.py
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
"""Contains class for handling multiple connections."""

import logging

from ..common import EventProducer

from handler import HsmsHandler
from connections import HsmsMultiPassiveServer


class HsmsConnectionManager(EventProducer):
    """High level class that handles multiple active and passive connections and the model for them.

    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, event_handler=None):
        EventProducer.__init__(self, event_handler)

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.handlers = {}

        self.servers = {}

        self.stopping = False

    def has_connection_to(self, index):
        """Check if connection to certain peer exists.

        :param index: Name of the reqested handler.
        :type index: string
        :returns: Is peer available
        :rtype: boolean
        """
        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            if handler.name == index:
                return handler

        return None

    def __getitem__(self, index):
        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            if handler.name == index:
                return handler

        return None

    @staticmethod
    def get_connection_id(address):
        """Generates connection ids used for internal indexing.

        :param address: The IP address for the affected remote.
        :type address: string
        """
        return "%s" % address

    def _update_required_servers(self, additional_port=-1):
        """Starts server if any active handler is found

        .. warning:: Do not call this directly, for internal use only.
        """
        required_ports = []

        if additional_port > 0:
            required_ports.append(additional_port)

        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            if not handler.active:
                if handler.port not in required_ports:
                    required_ports.append(handler.port)

        for serverPort in self.servers.keys():
            if serverPort not in required_ports:
                self.logger.debug("stopping server on port {0}".format(serverPort))
                self.servers[serverPort].stop()
                del self.servers[serverPort]

        for requiredPort in required_ports:
            if requiredPort not in self.servers:
                self.logger.debug("starting server on port {0}".format(requiredPort))
                self.servers[requiredPort] = HsmsMultiPassiveServer(requiredPort)
                self.servers[requiredPort].start()

    def _on_event(self, event_name, data):
        """Callback function for disconnection event

        :param event_name: Name of the event
        :type event_name: string
        :param data: Data supplied with event
        :type data: dict

        .. warning:: Do not call this directly, for internal use only.
        """
        connection = data['connection']

        connection_id = self.get_connection_id(connection.remoteIP)

        if connection_id in self.handlers.keys():
            data['handler'] = self.handlers[connection_id]

        self.fire_event(event_name, data)

    def add_peer(self, name, address, port, active, session_id, connection_handler=HsmsHandler):
        """Add a new connection

        :param name: Name of the peers configuration
        :type name: string
        :param address: IP address of peer
        :type address: string
        :param port: TCP port of peer
        :type port: integer
        :param active: Is the connection active (*True*) or passive (*False*)
        :type active: boolean
        :param session_id: session / device ID of peer
        :type session_id: integer
        :param connection_handler: Model handling this connection
        :type connection_handler: inherited from :class:`secsgem.hsms.handler.HsmsHandler`
        """
        self.logger.debug("new remote %s at %s:%d", name, address, port)

        connection_id = self.get_connection_id(address)

        self._update_required_servers(port)

        if active:
            handler = connection_handler(address, port, active, session_id, name, self.parentEventHandler)
        else:
            handler = connection_handler(address, port, active, session_id, name, self.parentEventHandler, self.servers[port])

        handler.enable()

        self.handlers[connection_id] = handler

        return handler

    def remove_peer(self, name, address, port):
        """Remove a previously added connection

        :param name: Name of the peers configuration
        :type name: string
        :param address: IP address of peer
        :type address: string
        :param port: TCP port of peer
        :type port: integer
        """
        self.logger.debug("disconnecting from %s at %s:%d", name, address, port)

        connection_id = self.get_connection_id(address)

        if connection_id in self.handlers.keys():
            handler = self.handlers[connection_id]

            handler.connection.disconnect()
            handler.disable()

            del self.handlers[connection_id]

            self._update_required_servers()

    def stop(self):
        """Stop all servers and terminate the connections"""
        self.stopping = True

        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            handler.connection.disconnect()

        self.handlers.clear()

        self._update_required_servers()
