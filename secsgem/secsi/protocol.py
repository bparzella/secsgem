#####################################################################
# protocol.py
#
# (c) Copyright 2023-2024, Benjamin Parzella. All rights reserved.
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
"""SECS-I protocol implementation."""

from __future__ import annotations

import typing

import secsgem.common

from .header import SecsIHeader
from .message import SecsIBlock, SecsIMessage

if typing.TYPE_CHECKING:
    from secsgem.secs.functions.base import SecsStreamFunction
    from secsgem.secsitcp.settings import SecsITcpSettings

    from .settings import SecsISettings


class SecsIProtocol(secsgem.common.Protocol[SecsIMessage, SecsIBlock]):
    """Implementation for SECS-I protocol."""

    ENQ = 0b00000101
    EOT = 0b00000100
    ACK = 0b00000110
    NAK = 0b00010101

    block_size = SecsIMessage.block_size

    message_type = SecsIMessage

    def __init__(self, settings: SecsISettings | SecsITcpSettings):
        """Instantiate SECS I protocol class.

        Args:
            settings: protocol and communication settings

        Example:
            import secsgem.secsi

            settings = secsgem.secsi.SecsISettings(
                port="COM1",
            )

            def onConnect(event, data):
                print ("Connected")

            client = secsgem.secsi.SecsIProtocol(settings)
            client.events.connected += onConnect

            client.enable()

            time.sleep(3)

            client.disable()

        """
        super().__init__(settings)
        self._settings: SecsISettings | SecsITcpSettings = settings

    def _create_message_for_function(
        self,
        function: SecsStreamFunction,
        system_id: int,
    ) -> secsgem.common.Message:
        """Create a protocol specific message for a function.

        Args:
            function: function to create message for
            system_id: system

        Returns:
            created message

        """
        return SecsIMessage(
            SecsIHeader(
                system_id,
                self._settings.session_id,
                function.stream,
                function.function,
                require_response=function.is_reply_required,
                from_equipment=(self._settings.device_type == secsgem.common.DeviceType.EQUIPMENT),
            ),
            function.encode(),
        )

    def serialize_data(self) -> dict[str, typing.Any]:
        """Return data for serialization.

        :returns: data to serialize for this object
        :rtype: dict
        """
        from .settings import SecsISettings  # pylint: disable=import-outside-toplevel

        if not isinstance(self._settings, SecsISettings):
            return {
                "address": self._settings.address,
                "port": self._settings.port,
                "connect_mode": self._settings.connect_mode,
                "session_id": self._settings.session_id,
                "name": self._settings.name,
            }

        return {
            "port": self._settings.port,
            "baud_rate": self._settings.speed,
            "session_id": self._settings.session_id,
            "name": self._settings.name,
        }

    def _on_connected(self, _: dict[str, typing.Any]):
        """Handle connection was established event."""
        self._thread.start()
        self.events.fire("connected", {"connection": self})
        self.events.fire("communicating", {"connection": self})

    def _on_disconnected(self, _: dict[str, typing.Any]):
        """Handle connection was _ event."""
        # clear receive buffer
        self.events.fire("disconnected", {"connection": self})

        self._thread.stop()

        self._receive_buffer.clear()

    def _on_disconnecting(self, _: dict[str, typing.Any]):
        pass

    def _process_send_queue(self):
        if self._send_queue.empty():
            return

        while not self._send_queue.empty():
            self._connection.send_data(bytes([self.ENQ]))

            enq_resonse = self._receive_buffer.wait_for_byte(peek=True)

            if enq_resonse == self.ENQ and self._settings.device_type == secsgem.common.DeviceType.HOST:
                self._process_received_data()
                continue

            enq_resonse = self._receive_buffer.pop_byte()

            block_info = self._send_queue.get()

            self._connection.send_data(block_info.data)

            data_response = self._receive_buffer.wait_for_byte()

            block_info.resolve(data_response == self.ACK)

    def _process_received_data(self):
        if len(self._receive_buffer) < 1:
            return

        while len(self._receive_buffer) > 0:
            receive_byte = self._receive_buffer.pop_byte()

            if receive_byte != self.ENQ:
                self._logger.info("Expected ENQ, received '%s'. Ignoring", receive_byte)

            self._connection.send_data(bytes([self.EOT]))

            length = self._receive_buffer.wait_for_byte(peek=True)

            data = self._receive_buffer.wait_for(length + 3)

            response = SecsIBlock.decode(data)

            if response is None:
                self._connection.send_data(bytes([self.NAK]))
                return

            # redirect message to hsms handler
            self._thread.queue_block(self, response)

            self._connection.send_data(bytes([self.ACK]))

    def _on_connection_message_received(self, source: object, message: SecsIMessage):
        """Message received from connection.

        Args:
            source: source of event
            message: received data message

        """
        decoded_message = self._settings.streams_functions.decode(message)
        self._communication_logger.info("< %s\n%s", message, decoded_message, extra=self._get_log_extra())

        # someone is waiting for this message
        if message.header.system in self._response_queues:
            self._response_queues[message.header.system].put_nowait(message)
        else:
            self.events.fire("message_received", {"connection": source, "message": message})

    def _get_log_extra(self) -> dict[str, typing.Any]:
        """Get extra fields for logging."""
        from .settings import SecsISettings  # pylint: disable=import-outside-toplevel

        if not isinstance(self._settings, SecsISettings):
            return {
                "address": self._settings.address,
                "port": self._settings.port,
                "connect_mode": self._settings.connect_mode,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name,
            }

        return {
            "port": self._settings.port,
            "speed": self._settings.speed,
            "session_id": self._settings.session_id,
            "remoteName": self._settings.name,
        }
