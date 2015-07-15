#####################################################################
# hsmsTestConnection.py
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
"""Contains class for connection test."""

import logging

import datetime
import time

import threading


class hsmsTestConnection(object):
    """Connection class for single connection from hsmsMultiPassiveServer

    Handles connections incoming connection from hsmsMultiPassiveServer

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param delegate: target for messages
    :type delegate: object

    **Example**::

        # TODO: create example

    """

    T3 = 10
    T6 = 5

    def __init__(self, address, port=5000, sessionID=0, delegate=None):
        # initially not enabled
        self.delegate = delegate

        self.enabled = False

        self.disconnecting = False

        self.systemCounter = 0

        self.connected = False

        self.packets = []

    def simulate_connect(self):
        # send connection enabled event
        self.connected = True

        if self.delegate and hasattr(self.delegate, '_onConnectionEstablished') and callable(getattr(self.delegate, '_onConnectionEstablished')):
            self.delegate._onConnectionEstablished()


    def simulate_disconnect(self):
        self.disconnect()

    def simulate_packet(self, packet):
        if self.delegate and hasattr(self.delegate, '_onConnectionPacketReceived') and callable(getattr(self.delegate, '_onConnectionPacketReceived')):
            self.delegate._onConnectionPacketReceived(packet)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def getNextSystemCounter(self):
        self.systemCounter += 1
        return self.systemCounter

    def sendPacket(self, packet):
        logging.info("> %s", packet)
        self.packets.append(packet)

    def disconnect(self):
        if self.connected:
            # notify listeners of disconnection
            if self.delegate and hasattr(self.delegate, '_onBeforeConnectionClosed') and callable(getattr(self.delegate, '_onBeforeConnectionClosed')):
                self.delegate._onBeforeConnectionClosed()

            # notify listeners of disconnection
            if self.delegate and hasattr(self.delegate, '_onConnectionClosed') and callable(getattr(self.delegate, '_onConnectionClosed')):
                self.delegate._onConnectionClosed()

        self.connected = False


class hsmsTestServer(object):
    """Server class for testing"""

    def __init__(self):
        self.connection = None

    def createConnection(self, address, port=5000, sessionID=0, delegate=None):
        connection = hsmsTestConnection(address, port, sessionID, delegate)
        connection.handler = self

        self.connection = connection

        return connection

    def start(self):
        logging.debug("hsmsTestServer.start: server started")

    def stop(self, terminateConnections=True):
        if terminateConnections:
            self.connection.disconnect()

        logging.debug("hsmsTestServer.stop: server stopped")

    def simulate_connect(self):
        threading.Thread(target=self.connection.simulate_connect).start()
        while not self.connection.connected:
            time.sleep(0.1)

    def simulate_disconnect(self):
       self.connection.simulate_disconnect()

    def expect_packet(self, system_id=None, s_type=None, stream=None, function=None, timeout=5):
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            for packet in self.connection.packets:
                match = False
                if system_id is not None and packet.header.system == system_id:
                    match = True

                if s_type is not None and packet.header.sType == s_type:
                    match = True

                if match:
                    self.connection.packets.remove(packet)
                    return packet

                if datetime.datetime.now() > endTime:
                    return None

    def simulate_packet(self, packet):
        return self.connection.simulate_packet(packet)

    def getNextSystemCounter(self):
        return self.connection.getNextSystemCounter()
