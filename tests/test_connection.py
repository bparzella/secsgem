#####################################################################
# test_connection.py
#
# (c) Copyright 2013-2023, Benjamin Parzella. All rights reserved.
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
from __future__ import annotations

import datetime
import logging
import typing

import secsgem.common
import secsgem.common.settings
import secsgem.hsms
from secsgem.hsms.protocol import HsmsProtocol


class HsmsTestConnection(secsgem.common.Connection):
    """
    Connection class for single connection from hsmsMultiPassiveServer.

    Handles connections incoming connection from hsmsMultiPassiveServer

    :param address: IP address of target host
    :type address: string
    :param port: TCP port of target host
    :type port: integer
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param delegate: target for messages
    :type delegate: inherited from :class:`secsgem.hsms.HsmsHandler`

    Example:

        # TODO: create example

    """

    def __init__(self, settings: HsmsTestServerSettings):
        super().__init__(settings)

        self._enabled = False
        self._fail_send = False

        self._packets = []

    def simulate_connect(self):
        # send connection enabled event
        if self._delegate and hasattr(self._delegate, 'on_connection_established') and callable(getattr(self._delegate, 'on_connection_established')):
            self._delegate.on_connection_established(self)

        self._connected = True

    def simulate_disconnect(self):
        self.disconnect()

    def simulate_packet(self, message):
        if self._delegate and hasattr(self._delegate, 'on_connection_message_received') and callable(getattr(self._delegate, 'on_connection_message_received')):
            self._delegate.on_connection_message_received(self, message)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def get_next_system_counter(self):
        self._system_counter += 1
        return self._system_counter

    def send_packet(self, packet):
        if self._fail_send:
            return False

        self._logger.info("> %s", packet)
        self._packets.append(packet)

        return True

    def disconnect(self):
        if self._connected:
            # notify listeners of disconnection
            if self._delegate and hasattr(self._delegate, 'on_connection_before_closed') and callable(getattr(self._delegate, 'on_connection_before_closed')):
                self._delegate.on_connection_before_closed(self)

            # notify listeners of disconnection
            if self._delegate and hasattr(self._delegate, 'on_connection_closed') and callable(getattr(self._delegate, 'on_connection_closed')):
                self._delegate.on_connection_closed(self)

        self._connected = False


class HsmsTestServerSettings(secsgem.common.Settings):
    """Test class settings."""

    @classmethod
    def _attributes(cls) -> typing.List[secsgem.common.settings.Setting]:
        """Get the available settings for the class."""
        return super()._attributes() + [
            secsgem.common.settings.Setting("server", None, "Server for connection"),
            secsgem.common.settings.Setting("connect_mode", secsgem.hsms.HsmsConnectMode.ACTIVE, "Hsms connect mode"),
            secsgem.common.settings.Setting("address", "127.0.0.1", "Remote (active) or local (passive) IP address"),
            secsgem.common.settings.Setting("port", 5000, "TCP port of remote host"),
            secsgem.common.settings.Setting("session_id", 0, "session / device ID to use for connection")
        ]

    def create_protocol(self) -> HsmsProtocol:
        """Protocol class for this configuration."""
        return HsmsProtocol(self)

    def create_connection(self) -> HsmsTestConnection:
        """Connection class for this configuration."""
        return self.server.create_connection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return "HSMS-TestServerSettings"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_Test_{functionality}"

    @property
    def is_active(self) -> bool:
        return self.connect_mode == secsgem.hsms.HsmsConnectMode.ACTIVE


class HsmsTestServer:
    """Server class for testing."""

    def __init__(self, connect_mode: secsgem.hsms.HsmsConnectMode = secsgem.hsms.HsmsConnectMode.PASSIVE):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.connection = None
        self.connect_mode = connect_mode

    def create_connection(self, settings: HsmsTestServerSettings):
        connection = HsmsTestConnection(settings)
        connection.handler = self

        self.connection = connection

        return connection

    @property
    def settings(self) -> HsmsTestServerSettings:
        return HsmsTestServerSettings(server=self, connect_mode=self.connect_mode)

    def start(self):
        self.logger.debug("server started")

    def stop(self, terminate_connections=True):
        if terminate_connections:
            if self.connection:
                self.connection.disconnect()

        self.logger.debug("server stopped")

    def simulate_connect(self):
        self.connection.simulate_connect()

    def simulate_disconnect(self):
        self.connection.simulate_disconnect()

    def fail_next_send(self):
        self.connection._fail_send = True

    def expect_packet(self, system_id=None, s_type=None, stream=None, function=None, timeout=5):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            for packet in self.connection._packets:
                match = False
                if system_id is not None and packet.header.system == system_id:
                    match = True

                if s_type is not None and packet.header.s_type.value == s_type:
                    match = True

                if stream is not None and packet.header.stream == stream:
                    match = True

                if function is not None and packet.header.function == function:
                    match = True

                if match:
                    self.connection._packets.remove(packet)
                    return packet

                if datetime.datetime.now() > end_time:
                    return None

    def simulate_packet(self, packet):
        return self.connection.simulate_packet(packet)

    def get_next_system_counter(self):
        return self.connection.get_next_system_counter()

    def generate_stream_function_packet(self, system_id, packet, session_id=0):
        return secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsStreamFunctionHeader(system_id, packet.stream, packet.function, True, session_id), packet.encode())
