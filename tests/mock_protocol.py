#####################################################################
# mock_protocol.py
#
# (c) Copyright 2023, Benjamin Parzella. All rights reserved.
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
"""Mock class for protocol."""
from __future__ import annotations

import datetime
import typing

import secsgem.common
import secsgem.secs

if typing.TYPE_CHECKING:
    from .mock_settings import MockSettings


class MockHeader(secsgem.common.Header):
    """Mock header."""
    def encode(self) -> bytes:
        """Encode header to message.

        Returns:
            encoded header

        """
        return b""

    @classmethod
    def decode(cls, data: bytes) -> MockHeader:
        """Decode byte array header to Header object.

        Args:
            data: byte-encode header data

        Returns:
            Header object

        """
        raise NotImplementedError("Header.decode missing implementation")

    @property
    def _as_dictionary(self) -> dict[str, typing.Any]:
        """Get the data as dictionary.

        Returns:
            Header data as dictionary.

        """
        return {
            "system": self._system,
            "session_id": self._session_id,
            "stream": self._stream,
            "function": self._function,
        }

class MockBlock(secsgem.common.Block[MockHeader]):
    """Mock block class."""


class MockMessage(secsgem.common.Message[MockBlock]):
    """Mock message class."""

    block_type = MockBlock

    def __init__(self, header: MockHeader, data: secsgem.secs.SecsStreamFunction):
        """Initialize a Message object.

        Args:
            header: header used for this message
            data: data part used for streams and functions (SType 0)

        """
        #self._blocks: list[MockBlock] = self._split_blocks(data, header)
        self._header = header
        self._function = data

    @property
    def header(self) -> MockHeader:
        """Get the header."""
        return self._header

    @property
    def data(self) -> secsgem.secs.SecsStreamFunction:
        """Get the header."""
        return self._function

    @property
    def complete(self) -> bool:
        """Check if the message is complete."""
        return True


class MockProtocol(secsgem.common.Protocol[secsgem.common.Message, secsgem.common.Block]):
    """Mock protocol class."""

    def __init__(self, settings: MockSettings) -> None:
        """Instantiate mock protocol class."""
        super().__init__(settings)

        self.received_messages: list[secsgem.common.Message] = []

    def _on_connected(self, _: dict[str, typing.Any]):
        raise NotImplementedError("MockProtocol._on_connected missing implementation")

    def _on_disconnecting(self, _: dict[str, typing.Any]):
        raise NotImplementedError("MockProtocol._on_disconnecting missing implementation")

    def _on_disconnected(self, _: dict[str, typing.Any]):
        raise NotImplementedError("MockProtocol._on_disconnected missing implementation")

    def _process_send_queue(self):
        """Process the send to communication queue."""
        raise NotImplementedError("MockProtocol._process_send_queue missing implementation")

    def _process_received_data(self):
        """Process the receive from communication queue."""
        raise NotImplementedError("MockProtocol._process_received_data missing implementation")

    def serialize_data(self) -> dict[str, typing.Any]:
        """Get protocol serialized data for debugging."""
        return {
            "mock": True
        }

    def _on_connection_message_received(self, source: object, message: secsgem.common.Message):
        """Message received by connection.

        Args:
            source: source of event
            message: received data message

        """
        raise NotImplementedError("MockProtocol._on_connection_message_received missing implementation")

    def _create_message_for_function(
            self,
            function: secsgem.secs.SecsStreamFunction,
            system_id: int,
    ) -> secsgem.common.Message:
        """Create a protocol specific message for a function.

        Args:
            function: function to create message for
            system_id: system

        Returns:
            created message

        """
        return MockMessage(MockHeader(system_id, 0, function.stream, function.function, function.is_reply_required), function)

    create_message_for_function = _create_message_for_function

    def _get_log_extra(self) -> dict[str, typing.Any]:
        """Get extra fields for logging."""
        return {
            "mock": True
        }

    def enable(self):
        """Enable the connection."""

    def disable(self):
        """Disable the connection."""

    def simulate_connect(self):
        """Simulate connection established."""
        self.events.fire("connected", {"connection": self})
        self.events.fire("communicating", {"connection": self})

    def send_message(self, message: secsgem.common.Message) -> bool:
        """Send a message to the remote host.

        Args:
            message: message to be transmitted

        Returns:
            True if sending was successful

        """
        self.received_messages.append(message)

        return True

    def expect_message(self, system_id=None, s_type=None, stream=None, function=None, timeout=5):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            for message in self.received_messages:
                match = False
                if system_id is not None and message.header.system == system_id:
                    match = True

                if s_type is not None and message.header.s_type.value == s_type:
                    match = True

                if stream is not None and message.header.stream == stream:
                    match = True

                if function is not None and message.header.function == function:
                    match = True

                if match:
                    self.received_messages.remove(message)
                    return message

                if datetime.datetime.now() > end_time:
                    return None

    def simulate_message(self, message: MockMessage):
        if message.header.system in self._response_queues:
            self._response_queues[message.header.system].put_nowait(message)
        else:
            self.events.fire("message_received", {"connection": None, "message": message})