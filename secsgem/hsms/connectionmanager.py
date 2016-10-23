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

from __future__ import absolute_import

import logging

from ..common.events import EventProducer

from .handler import HsmsHandler
from .connections import HsmsMultiPassiveServer


class HsmsConnectionManager(object):
    """High level class that handles multiple active and passive connections and the model for them."""

    def __init__(self):
        self._eventProducer = EventProducer()

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.handlers = {}

        self.servers = {}

        self.stopping = False

        self._testServerObject = None 

    @property
    def events(self):
        """Property for event handling""" 
        return self._eventProducer

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
        """Get a connection by using [] on the object"""
        return self.has_connection_to(index)

    @staticmethod
    def get_connection_id(address):
        """Generates connection ids used for internal indexing.

        :param address: The IP address for the affected remote.
        :type address: string
        """
        return "%s" % address

    def _update_required_servers(self, additional_port=-1):  # pragma: no cover
        """Starts server if any active handler is found

        .. warning:: Do not call this directly, for internal use only.
        """
        if self._testServerObject:
            return

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
                self.logger.debug("stopping server on port %d", serverPort)
                self.servers[serverPort].stop()
                del self.servers[serverPort]

        for requiredPort in required_ports:
            if requiredPort not in self.servers:
                self.logger.debug("starting server on port %d", requiredPort)
                self.servers[requiredPort] = HsmsMultiPassiveServer(requiredPort)
                self.servers[requiredPort].start()

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

        if self._testServerObject:
            if active:
                handler = connection_handler(address, port, active, session_id, name, self._testServerObject)
            else:
                handler = connection_handler(address, port, active, session_id, name, self._testServerObject)
        else:  # pragma: no cover
            if active:
                handler = connection_handler(address, port, active, session_id, name)
            else:
                handler = connection_handler(address, port, active, session_id, name, self.servers[port])

        handler._eventProducer += self._eventProducer
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
