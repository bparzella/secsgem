#####################################################################
# testconnection.py
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


class HsmsTestConnection(object):
    """Connection class for single connection from hsmsMultiPassiveServer

    Handles connections incoming connection from hsmsMultiPassiveServer

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: inherited from :class:`secsgem.HsmsHandler.HsmsHandler`

    **Example**::

        # TODO: create example

    """

    T3 = 10
    T6 = 5
    T7 = 10

    def __init__(self, address, port=5000, session_id=0, delegate=None):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # initially not enabled
        self.address = address
        self.port = port
        self.sessionID = session_id
        self.delegate = delegate

        self.enabled = False

        self.disconnecting = False

        self.systemCounter = 0

        self.connected = False

        self.packets = []

    def simulate_connect(self):
        # send connection enabled event
        if self.delegate and hasattr(self.delegate, 'on_connection_established') and callable(getattr(self.delegate, 'on_connection_established')):
            self.delegate.on_connection_established(self)

        self.connected = True

    def simulate_disconnect(self):
        self.disconnect()

    def simulate_packet(self, packet):
        if self.delegate and hasattr(self.delegate, 'on_connection_packet_received') and callable(getattr(self.delegate, 'on_connection_packet_received')):
            self.delegate.on_connection_packet_received(self, packet)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_next_system_counter(self):
        self.systemCounter += 1
        return self.systemCounter

    def send_packet(self, packet):
        self.logger.info("> %s", packet)
        self.packets.append(packet)

    def disconnect(self):
        if self.connected:
            # notify listeners of disconnection
            if self.delegate and hasattr(self.delegate, 'on_connection_before_closed') and callable(getattr(self.delegate, 'on_connection_before_closed')):
                self.delegate.on_connection_before_closed(self)

            # notify listeners of disconnection
            if self.delegate and hasattr(self.delegate, 'on_connection_closed') and callable(getattr(self.delegate, 'on_connection_closed')):
                self.delegate.on_connection_closed(self)

        self.connected = False


class HsmsTestServer(object):
    """Server class for testing"""

    def __init__(self):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.connection = None

    def create_connection(self, address, port=5000, session_id=0, delegate=None):
        connection = HsmsTestConnection(address, port, session_id, delegate)
        connection.handler = self

        self.connection = connection

        return connection

    def start(self):
        self.logger.debug("server started")

    def stop(self, terminate_connections=True):
        if terminate_connections:
            self.connection.disconnect()

        self.logger.debug("server stopped")

    def simulate_connect(self):
        threading.Thread(target=self.connection.simulate_connect).start()
        while not self.connection.connected:
            time.sleep(0.1)

    def simulate_disconnect(self):
        self.connection.simulate_disconnect()

    def expect_packet(self, system_id=None, s_type=None, stream=None, function=None, timeout=5):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            for packet in self.connection.packets:
                match = False
                if system_id is not None and packet.header.system == system_id:
                    match = True

                if s_type is not None and packet.header.sType == s_type:
                    match = True

                if stream is not None and packet.header.stream == stream:
                    match = True

                if function is not None and packet.header.function == function:
                    match = True

                if match:
                    self.connection.packets.remove(packet)
                    return packet

                if datetime.datetime.now() > end_time:
                    return None

    def simulate_packet(self, packet):
        return self.connection.simulate_packet(packet)

    def get_next_system_counter(self):
        return self.connection.get_next_system_counter()
