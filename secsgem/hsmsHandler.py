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

import threading

from hsmsConnections import *

class hsmsDefaultHandler:
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
    """
    def __init__(self, address, port, active, sessionID, name):
        self.address = address
        self.port = port
        self.active = active
        self.sessionID = sessionID
        self.name = name
        self.connection = None
        self.connected = False
        self.dead = False

        self.events = {}
        self.eventsLock = threading.Lock()
        self.eventNotify = {}

    def _setConnection(self, connection):
        """Set the connection of the for this models. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`.

        :param connection: The connection the model uses
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        self.connection = connection
        if connection:
            self.connected = True
        else:
            self.connected = False

    def _clearConnection(self):
        """Clear the connection associated with the model instance. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`."""
        self.postEvent("terminate")

        self.connection = None
        self.connected = False

    def _postInit(self):
        """Event called by :class:`secsgem.hsmsHandler.hsmsConnectionManager` after the connection is established (including Select, Linktest, ...)."""
        pass

    def postEvent(self, event, data={}):
        """Add event to notify event list and notify listeners

        :param event: name of event
        :type event: string
        :param data: parameters to event
        :type data: dict
        """
        #call event handler function if present
        eventFuncName = "event_" + event
        eventFunc = getattr(self, eventFuncName, None)
        if callable(eventFunc):
            eventFunc(event, data)

        self.eventsLock.acquire()

        data["event"] = event
        for queue in self.events:
            self.events[queue].append(data)

            self.eventNotify[queue].set()

        self.eventsLock.release()

    def waitForEvents(self, queue):
        """Wait for events in the event list and return

        :returns: currently available events
        :rtype: list
        """
        self.eventsLock.acquire()

        if not queue in self.events:
            self.events[queue] = []
            self.eventNotify[queue] = threading.Event()

        if not self.events[queue]:
            self.eventsLock.release()

            while not self.eventNotify[queue].wait(1):
                pass

            self.eventsLock.acquire()
            self.eventNotify[queue].clear()

        result = list(self.events[queue])
        self.events[queue] = []

        self.eventsLock.release()

        return result

    def stop(self):
        """Mark peer as dead"""
        self.dead = True

class hsmsConnectionManager:
    """High level class that handles multiple active and passive connections and the model for them.

    :param connectionCallback: method to call when the connection is established
    :type connectionCallback: def connectionCallback(peer)
    :param disconnectionCallback: method to call when the connection is terminated
    :type disconnectionCallback: def disconnectionCallback(peer)
    :param postInitCallback: method to call when the connection is initialized
    :type postInitCallback: def postInitCallback(peer)
    """
    def __init__(self, connectionCallback = None, disconnectionCallback = None, postInitCallback = None):
        self.peers = {}
        self.clients = {}

        self.stopping = False

        self.reconnectTimeout = 10.0

        self.connectionCallback = connectionCallback
        self.disconnectionCallback = disconnectionCallback
        self.postInitCallback = postInitCallback

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

    def getConnectionID(self, address, port, sessionID):
        """Generates connection ids used for internal indexing.

        :param address: The IP address for the affected remote.
        :type address: string
        :param port: The TCP port for the affected remote.
        :type port: integer
        :param sessionID: Session / device ID for the affected remote
        :type sessionID: integer
        """
        return "%s:%05d:%05d" % (address, port, sessionID)

    def _startActiveConnect(self, peer):
        """Starts thread to (re)connect active connection to remote host.

        :param peer: Model for the affected remote.
        :type peer: inherited from :class:`secsgem.hsmsHandler.hsmsDefaultHandler`

        .. warning:: Do not call this directly, for internal use only.
        """
        if not self.stopping:
            threading.Thread(target=self.__activeConnectThread, args=(peer,)).start()

    def __activeConnectThread(self, peer):
        """Thread function to (re)connect active connection to remote host.

        :param peer: Model for the affected remote.
        :type peer: inherited from :class:`secsgem.hsmsHandler.hsmsDefaultHandler`

        .. warning:: Do not call this directly, for internal use only.
        """
        connectionID = self.getConnectionID(peer.address, peer.port, peer.sessionID)

        self.clients[connectionID] = hsmsClient(peer.address, peer.port, sessionID = peer.sessionID, connectionCallback = self._connectionCallback, disconnectionCallback = self._disconnectionCallback)

        while self.clients[connectionID].connect() == None:
            for i in range(int(self.reconnectTimeout) * 5):
                time.sleep(0.2)

                #check if connect was aborted
                if self.clients[connectionID].aborted:
                    del self.clients[connectionID]
                    return

        del self.clients[connectionID]

        peer._postInit()

        if not self.postInitCallback == None:
            self.postInitCallback(peer)

    def _connectionCallback(self, connection):
        """Callback function for connection event

        :param connection: Connection that was connected
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`

        .. warning:: Do not call this directly, for internal use only.
        """
        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort, connection.sessionID)

        peer = self.peers[connectionID]

        peer._setConnection(connection)

        if not self.connectionCallback == None:
            self.connectionCallback(peer)

    def _disconnectionCallback(self, connection):
        """Callback function for disconnection event

        :param connection: Connection that was disconnected
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`

        .. warning:: Do not call this directly, for internal use only.
        """
        connectionID = self.getConnectionID(connection.remoteIP, connection.remotePort, connection.sessionID)

        peer = self.peers[connectionID]
        
        peer._clearConnection()

        if not self.disconnectionCallback == None:
            self.disconnectionCallback(peer)

        if not peer.dead:
            if peer.active:
                self._startActiveConnect(peer)

    def addPeer(self, name, address, port, active, sessionID, connectionHandler = hsmsDefaultHandler):
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
        logging.debug("hsmsConnectionManager.addPeer: connecting to %s at %s:%d", name, address, port)

        peer = connectionHandler(address, port, active, sessionID, name)

        connectionID = self.getConnectionID(address, port, sessionID)
        self.peers[connectionID] = peer

        if peer.active:
            self._startActiveConnect(peer)

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
        connectionID = self.getConnectionID(address, port, sessionID)

        if connectionID in self.clients:
            self.clients[connectionID].cancel()

        if connectionID in self.peers:
            peer = self.peers[connectionID]

            peer.stop()
            if peer.connection:
                peer.connection.disconnect()

            del self.peers[connectionID]


    def stop(self):
        """Stop all servers and terminate the connections"""
        self.stopping = True

        for clientID in self.clients.keys():
            client = self.clients[clientID]
            client.cancel()

        for peerID in self.peers.keys():
            peer = self.peers[peerID]
            if peer.connection:
                peer.connection.disconnect()
