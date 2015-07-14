#####################################################################
# hsmsConnectionManager.py
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

from hsmsHandler import hsmsHandler
from hsmsConnections import hsmsMultiPassiveServer
from common import EventProducer, EventHandler


class hsmsConnectionManager(EventProducer):
    """High level class that handles multiple active and passive connections and the model for them.

    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, eventHandler=None):
        EventProducer.__init__(self, eventHandler)

        self.handlers = {}

        self.servers = {}

        self.stopping = False

    def hasConnectionTo(self, index):
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

    def getConnectionID(self, address, port):
        """Generates connection ids used for internal indexing.

        :param address: The IP address for the affected remote.
        :type address: string
        :param port: The TCP port for the affected remote.
        :type port: integer
        :param sessionID: Session / device ID for the affected remote
        :type sessionID: integer
        """
        return "%s" % (address)

    def _updateRequiredServers(self, additionalPort=-1):
        """Starts server if any active handler is found

        .. warning:: Do not call this directly, for internal use only.
        """
        requiredPorts = []

        if additionalPort > 0:
            requiredPorts.append(additionalPort)

        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            if not handler.active:
                if not handler.port in requiredPorts:
                    requiredPorts.append(handler.port)

        for serverPort in self.servers.keys():
            if not serverPort in requiredPorts:
                logging.debug("hsmsConnectionManager._updateRequiredServers: stopping server on port {0}".format(serverPort))
                self.servers[serverPort].stop()
                del self.servers[serverPort]

        for requiredPort in requiredPorts:
            if requiredPort not in self.servers:
                logging.debug("hsmsConnectionManager._updateRequiredServers: starting server on port {0}".format(requiredPort))
                self.servers[requiredPort] = hsmsMultiPassiveServer(requiredPort)
                self.servers[requiredPort].start()

    def _onEvent(self, eventName, data):
        """Callback function for disconnection event

        :param eventName: Name of the event
        :type eventName: string
        :param data: Data supplied with event
        :type data: dict

        .. warning:: Do not call this directly, for internal use only.
        """
        connection = data['connection']

        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort)

        if connectionID in self.handlers.keys():
            data['handler'] = self.handlers[connectionID]

        self.fireEvent(eventName, data)

    def addPeer(self, name, address, port, active, sessionID, connectionHandler=hsmsHandler):
        """Add a new connection

        :param name: Name of the peers configuration
        :type name: string
        :param address: IP address of peer
        :type address: string
        :param port: TCP port of peer
        :type port: integer
        :param active: Is the connection active (*True*) or passive (*False*)
        :type active: boolean
        :param sessionID: session / device ID of peer
        :type sessionID: integer
        :param connectionHandler: Model handling this connection
        :type connectionHandler: inherited from :class:`secsgem.hsmsHandler.hsmsHandler`
        """
        logging.debug("hsmsConnectionManager.addPeer: new remote %s at %s:%d", name, address, port)

        connectionID = self.getConnectionID(address, port)

        self._updateRequiredServers(port)

        if active:
            handler = connectionHandler(address, port, active, sessionID, name, self.parentEventHandler)
        else:
            handler = connectionHandler(address, port, active, sessionID, name, self.parentEventHandler, self.servers[port])

        handler.enable()

        self.handlers[connectionID] = handler

        return handler

    def removePeer(self, name, address, port, sessionID):
        """Remove a previously added connection

        :param name: Name of the peers configuration
        :type name: string
        :param address: IP address of peer
        :type address: string
        :param port: TCP port of peer
        :type port: integer
        :param sessionID: session / device ID of peer
        :type sessionID: integer
        """
        logging.debug("hsmsConnectionManager.removePeer: disconnecting from %s at %s:%d", name, address, port)

        connectionID = self.getConnectionID(address, port)

        if connectionID in self.handlers.keys():
            handler = self.handlers[connectionID]

            handler.disconnect()
            handler.disable()

            del self.handlers[connectionID]

            self._updateRequiredServers()

    def stop(self):
        """Stop all servers and terminate the connections"""
        self.stopping = True

        for handlerID in self.handlers.keys():
            handler = self.handlers[handlerID]
            handler.connection.disconnect(separate=True)

        self.handlers.clear()

        self._updateRequiredServers()
