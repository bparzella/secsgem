#####################################################################
# connectionmanager.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
from __future__ import annotations

import logging

import secsgem.common

from .multi_passive_server import HsmsMultiPassiveServer
from .protocol import HsmsProtocol


class HsmsConnectionManager:
    """High level class that handles multiple active and passive connections and the model for them."""

    def __init__(self):
        """Initialize a hsms connection manager."""
        self._event_producer = secsgem.common.EventProducer()

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.handlers = {}

        self.servers = {}

        self.stopping = False

        self._test_server_object = None

    @property
    def events(self):
        """Property for event handling."""
        return self._event_producer

    def has_connection_to(self, index):
        """Check if connection to certain peer exists.

        :param index: Name of the reqested handler.
        :type index: string
        :returns: Is peer available
        :rtype: boolean
        """
        for handler in self.handlers.values():
            if handler.name == index:
                return handler

        return None

    def __getitem__(self, index):
        """Get a connection by using [] on the object."""
        return self.has_connection_to(index)

    @staticmethod
    def get_connection_id(address):
        """Generate connection ids used for internal indexing.

        :param address: The IP address for the affected remote.
        :type address: string
        """
        return f"{address}"

    def _update_required_servers(self, additional_port=-1):
        """Start server if any active handler is found.

        .. warning:: Do not call this directly, for internal use only.
        """
        if self._test_server_object:
            return

        required_ports = []

        if additional_port > 0:
            required_ports.append(additional_port)

        for handler in self.handlers.values():
            if not handler.active and handler.port not in required_ports:
                required_ports.append(handler.port)

        for server_port, server in self.servers.items():
            if server_port not in required_ports:
                self.logger.debug("stopping server on port %d", server_port)
                server.stop()
                del self.servers[server_port]

        for required_port in required_ports:
            if required_port not in self.servers:
                self.logger.debug("starting server on port %d", required_port)
                self.servers[required_port] = HsmsMultiPassiveServer(required_port)
                self.servers[required_port].start()

    def add_peer(  # pylint: disable=too-many-arguments
            self,
            name: str,
            address: str,
            port: int,
            active: bool,
            session_id: int,
            connection_handler: type[HsmsProtocol] = HsmsProtocol):
        """Add a new connection.

        Args:
            name: Name of the peers configuration
            address: IP address of peer
            port: TCP port of peer
            active: Is the connection active (*True*) or passive (*False*)
            session_id: session / device ID of peer
            connection_handler: Model handling this connection

        """
        self.logger.debug("new remote %s at %s:%d", name, address, port)

        connection_id = self.get_connection_id(address)

        self._update_required_servers(port)

        if self._test_server_object:
            if active:
                handler = connection_handler(address, port, active, session_id, name, self._test_server_object)
            else:
                handler = connection_handler(address, port, active, session_id, name, self._test_server_object)
        else:
            if active:
                handler = connection_handler(address, port, active, session_id, name)
            else:
                handler = connection_handler(address, port, active, session_id, name, self.servers[port])

        handler._event_producer += self._event_producer  # noqa: SLF001
        handler.enable()

        self.handlers[connection_id] = handler

        return handler

    def remove_peer(self, name, address, port):
        """Remove a previously added connection.

        :param name: Name of the peers configuration
        :type name: string
        :param address: IP address of peer
        :type address: string
        :param port: TCP port of peer
        :type port: integer
        """
        self.logger.debug("disconnecting from %s at %s:%d", name, address, port)

        connection_id = self.get_connection_id(address)

        if connection_id in self.handlers:
            handler = self.handlers[connection_id]

            handler.connection.disconnect()
            handler.disable()

            del self.handlers[connection_id]

            self._update_required_servers()

    def stop(self):
        """Stop all servers and terminate the connections."""
        self.stopping = True

        for handler in self.handlers.values():
            handler.connection.disconnect()

        self.handlers.clear()

        self._update_required_servers()
