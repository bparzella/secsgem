#####################################################################
# hsmsHandler.py
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
"""Contains classes to create models for hsms endpoints."""

import logging

import time
import threading

from hsmsConnections import *


class hsmsDefaultHandler(EventProducer):
    """Baseclass for creating Host/Equipment models. This layer contains the HSMS functionality. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, address, port, active, sessionID, name, eventHandler=None):
        EventProducer.__init__(self, eventHandler)

        self.address = address
        self.port = port
        self.active = active
        self.sessionID = sessionID
        self.name = name
        self.connection = None
        self.connected = False
        self.dead = False

    def _serializeData(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {'address': self.address, 'port': self.port, 'active': self.active, 'sessionID': self.sessionID, 'name': self.name, 'connected': self.connected, 'dead': self.dead}

    # connection handling
    def _setConnection(self, connection):
        """Set the connection of the for this models. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`.

        :param connection: The connection the model uses
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        self.connection = connection
        if connection:
            self.connected = True
            self.fireEvent("HandlerConnected", {'remoteIP': self.connection.remoteIP, 'remotePort': self.connection.remotePort, 'peer': self, 'connection': self.connection})
        else:
            self.connected = False

    def _clearConnection(self):
        """Clear the connection associated with the model instance. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`."""
        self.fireEvent("HandlerTerminated", {'peer': self, 'connection': self.connection})

        self.connection = None
        self.connected = False

    def _postInit(self):
        """Event called by :class:`secsgem.hsmsHandler.hsmsConnectionManager` after the connection is established (including Select, Linktest, ...)."""
        pass

    def stop(self):
        """Mark peer as dead"""
        self.dead = True


class hsmsConnectionManager(EventProducer):
    """High level class that handles multiple active and passive connections and the model for them.

    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, eventHandler=None):
        EventProducer.__init__(self, eventHandler)

        self.peers = {}
        self.clients = {}

        self.server = None

        self.stopping = False

        self.reconnectTimeout = 10.0

    def hasConnectionTo(self, index):
        """Check if connection to certain peer exists.

        :param index: Name of the reqested peer.
        :type index: string
        :returns: Is peer available
        :rtype: boolean
        """
        for peerID in self.peers:
            peer = self.peers[peerID]
            if peer.name == index:
                return peer

        return None

    def __getitem__(self, index):
        for peerID in self.peers:
            peer = self.peers[peerID]
            if peer.name == index:
                return peer

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

    def _startActiveConnect(self, peer):
        """Starts thread to (re)connect active connection to remote host.

        :param peer: Model for the affected remote.
        :type peer: inherited from :class:`secsgem.hsmsHandler.hsmsDefaultHandler`

        .. warning:: Do not call this directly, for internal use only.
        """
        if not self.stopping:
            threading.Thread(target=self.__activeConnectThread, args=(peer,), name="secsgem_hsmsConnectionManager_activeConnectThread_{}".format(peer.name)).start()

    def __activeConnectThread(self, peer):
        """Thread function to (re)connect active connection to remote host.

        :param peer: Model for the affected remote.
        :type peer: inherited from :class:`secsgem.hsmsHandler.hsmsDefaultHandler`

        .. warning:: Do not call this directly, for internal use only.
        """
        connectionID = self.getConnectionID(peer.address, peer.port)

        self.clients[connectionID] = hsmsClient(peer.address, peer.port, sessionID=peer.sessionID, eventHandler=EventHandler(self))

        while self.clients[connectionID].connect() == None:
            for i in range(int(self.reconnectTimeout) * 5):
                time.sleep(0.2)

                # check if connect was aborted
                if self.clients[connectionID].aborted:
                    del self.clients[connectionID]
                    return

        del self.clients[connectionID]

    def _startServerIfRequired(self):
        """Starts server if any active peer is found

        .. warning:: Do not call this directly, for internal use only.
        """
        if self.server:
            logging.debug("hsmsConnectionManager._startServerIfRequired: server already running")
            return

        found = False

        for connectionID in self.peers:
            peer = self.peers[connectionID]

            if not peer.active:
                logging.debug("hsmsConnectionManager._startServerIfRequired: passive connection found")
                found = True

        if found:
            logging.debug("hsmsConnectionManager._startServerIfRequired: starting server")
            self.server = hsmsMultiServer(eventHandler=EventHandler(self))
            self.server.start()

    def _stopServerIfRequired(self):
        """Stops server if no active peer is found

        .. warning:: Do not call this directly, for internal use only.
        """
        if not self.server:
            logging.debug("hsmsConnectionManager._stopServerIfRequired: server isn't running")
            return

        found = False

        for connectionID in self.peers:
            peer = self.peers[connectionID]

            if not peer.active:
                logging.debug("hsmsConnectionManager._stopServerIfRequired: passive connection found")
                found = True

        if not found:
            logging.debug("hsmsConnectionManager._stopServerIfRequired: stopping server")

            self.server.stop()
            del self.server
            self.server = None

    def _onEventRemoteConnected(self, data):
        """Callback function for connection event

        :param data: Data supplied with event
        :type data: dict

        .. warning:: Do not call this directly, for internal use only.
        """
        connection = data['connection']

        logging.debug("hsmsConnectionManager._onEventRemoteConnected: new connection from %s:%d", connection.remoteIP, connection.remotePort)

        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort)

        peer = self.peers[connectionID]

        connection.sessionID = peer.sessionID

        peer._setConnection(connection)

        data['peer'] = peer

        self.fireEvent("PeerConnected", data)

    def _onEventRemoteInitialized(self, data):
        """Callback function for post connection event (receiver running)

        :param data: Data supplied with event
        :type data: dict

        .. warning:: Do not call this directly, for internal use only.
        """
        connection = data['connection']

        logging.debug("hsmsConnectionManager._onEventRemoteInitialized: connection from %s:%d", connection.remoteIP, connection.remotePort)
        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort)

        peer = self.peers[connectionID]

        peer._postInit()

        data['peer'] = peer

        self.fireEvent("PeerInitialized", data)

    def _onEventRemoteDisconnected(self, data):
        """Callback function for disconnection event

        :param data: Data supplied with event
        :type data: dict

        .. warning:: Do not call this directly, for internal use only.
        """
        connection = data['connection']

        logging.debug("hsmsConnectionManager._onEventRemoteDisconnected: disconnected from %s:%d", connection.remoteIP, connection.remotePort)

        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort)

        peer = self.peers[connectionID]

        peer._clearConnection()

        data['peer'] = peer

        self.fireEvent("PeerDisconnected", data)

        if not peer.dead:
            if peer.active:
                self._startActiveConnect(peer)

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

        if connectionID in self.peers:
            data['peer'] = self.peers[connectionID]

        self.fireEvent(eventName, data)

    def addPeer(self, name, address, port, active, sessionID, connectionHandler=hsmsDefaultHandler):
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
        :type connectionHandler: inherited from :class:`secsgem.hsmsHandler.hsmsDefaultHandler`
        """
        logging.debug("hsmsConnectionManager.addPeer: new remote %s at %s:%d", name, address, port)

        peer = connectionHandler(address, port, active, sessionID, name, self.parentEventHandler)

        connectionID = self.getConnectionID(address, port)
        self.peers[connectionID] = peer

        if peer.active:
            self._startActiveConnect(peer)
        else:
            self._startServerIfRequired()

        return peer

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

        if connectionID in self.clients:
            self.clients[connectionID].cancel()

        if connectionID in self.peers:
            peer = self.peers[connectionID]

            peer.stop()
            if peer.connection:
                peer.connection.disconnect()

            del self.peers[connectionID]

            self._stopServerIfRequired()

    def stop(self):
        """Stop all servers and terminate the connections"""
        self.stopping = True

        if self.server:
            self.server.stop()
            del self.server
            self.server = None

        for clientID in self.clients.keys():
            client = self.clients[clientID]
            client.cancel()

        for peerID in self.peers.keys():
            peer = self.peers[peerID]
            if peer.connection:
                peer.connection.disconnect(separate=True)
