#####################################################################
# protocol.py
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
"""protocol base class."""
from __future__ import annotations

import abc
import logging
import queue
import random
import typing

from .block_send_info import BlockSendInfo
from .byte_queue import ByteQueue
from .events import EventProducer
from .protocol_dispatcher import ProtocolDispatcher

if typing.TYPE_CHECKING:
    from secsgem.secs.functions.base import SecsStreamFunction

    from .connection import Connection
    from .message import Block, Message
    from .settings import Settings

MessageT = typing.TypeVar("MessageT", bound="Message")
BlockT = typing.TypeVar("BlockT", bound="Block")


class Protocol(abc.ABC, typing.Generic[MessageT, BlockT]):  # pylint: disable=too-many-instance-attributes
    """Abstract base class for a protocol."""

    message_type: type[MessageT]

    def __init__(self, settings: Settings) -> None:
        """Initialize protocol base object."""
        super().__init__()

        self._settings = settings

        self._event_producer = EventProducer()
        self._event_producer.targets += self

        self._system_counter = random.randint(0, (2 ** 32) - 1)  # noqa: S311

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._communication_logger = logging.getLogger("communication")

        self.__connection: Connection | None = None

        self._response_queues: dict[int, queue.Queue[MessageT]] = {}

        self._receive_buffer = ByteQueue()
        self._send_queue: queue.Queue[BlockSendInfo] = queue.Queue()
        self._incomplete_messages: dict[int, MessageT] = {}

        self._thread = ProtocolDispatcher(
            self._process_data,
            self._dispatch_block,
            self._settings,
        )

    @property
    def _connection(self) -> Connection:
        if self.__connection is None:
            self.__connection = self._settings.create_connection()
            self.__connection.on_connected.register(self._on_connected)
            self.__connection.on_data.register(self._on_connection_data_received)
            self.__connection.on_disconnecting.register(self._on_disconnecting)
            self.__connection.on_disconnected.register(self._on_disconnected)

        return self.__connection

    @abc.abstractmethod
    def _on_connected(self, _: dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_connected missing implementation")

    @abc.abstractmethod
    def _on_disconnecting(self, _: dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_disconnecting missing implementation")

    @abc.abstractmethod
    def _on_disconnected(self, _: dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_disconnected missing implementation")

    def _on_connection_data_received(self, data: dict[str, typing.Any]):
        """Data received by connection.

        Args:
            data: received data

        """
        self._receive_buffer.append(data["data"])
        self._thread.trigger_receiver()

    def _process_data(self):
        """Parse the receive buffer and dispatch callbacks."""
        self._process_send_queue()
        self._process_received_data()

    @abc.abstractmethod
    def _process_send_queue(self):
        """Process the send to communication queue."""
        raise NotImplementedError("Protocol._process_send_queue missing implementation")

    @abc.abstractmethod
    def _process_received_data(self):
        """Process the receive from communication queue."""
        raise NotImplementedError("Protocol._process_received_data missing implementation")

    def _dispatch_block(self, source: object, block: BlockT):
        result = self._add_message_block(block)
        if result is None:
            return

        try:
            self._on_connection_message_received(source, result)
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_connection_message_received handler")

    @property
    def events(self):
        """Property for event handling."""
        return self._event_producer

    def get_next_system_counter(self):
        """Return the next System.

        Returns:
            System for the next command

        """
        self._system_counter += 1

        if self._system_counter > ((2 ** 32) - 1):
            self._system_counter = 0

        return self._system_counter

    def enable(self):
        """Enable the connection."""
        self._connection.enable()

    def disable(self):
        """Disable the connection."""
        self._connection.disable()

    @abc.abstractmethod
    def serialize_data(self) -> dict[str, typing.Any]:
        """Get protocol serialized data for debugging."""
        raise NotImplementedError("Protocol.serialize_data missing implementation")

    @abc.abstractmethod
    def _on_connection_message_received(self, source: object, message: MessageT):
        """Message received by connection.

        Args:
            source: source of event
            message: received data message

        """
        raise NotImplementedError("Protocol._on_connection_message_received missing implementation")

    def _get_queue_for_system(self, system_id: int) -> queue.Queue:
        """Create a new queue to receive responses for a certain system.

        Args:
            system_id: system id to watch

        Returns:
            queue to receive responses with

        """
        self._response_queues[system_id] = queue.Queue()
        return self._response_queues[system_id]

    def _remove_queue(self, system_id: int):
        """Remove queue for system id from list.

        Args:
            system_id: system id to remove

        """
        del self._response_queues[system_id]

    def _add_message_block(self, block: BlockT) -> MessageT | None:
        """Add a block, and get completed message if available.

        Args:
            block: block to add

        Returns:
            completed message or None if paket not complete

        """
        if block.header.system not in self._incomplete_messages:
            self._incomplete_messages[block.header.system] = self.message_type.from_block(block)
        else:
            self._incomplete_messages[block.header.system].blocks.append(block)

        message = self._incomplete_messages[block.header.system]

        if not message.complete:
            return None

        del self._incomplete_messages[block.header.system]
        return message

    @abc.abstractmethod
    def _create_message_for_function(
            self,
            function: SecsStreamFunction,
            system_id: int,
    ) -> Message:
        """Create a protocol specific message for a function.

        Args:
            function: function to create message for
            system_id: system

        Returns:
            created message

        """
        raise NotImplementedError("Protocol._create_message_for_function missing implementation")

    def send_message(self, message: Message) -> bool:
        """Send a message to the remote host.

        Args:
            message: message to be transmitted

        Returns:
            True if sending was successful

        """
        for block in message.blocks:
            block_send_info = BlockSendInfo(block.encode())
            self._send_queue.put(block_send_info)
            self._thread.trigger_receiver()

            if not block_send_info.wait():
                return False

        return True

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> Message | None:
        """Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            Message that was received

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_message = self._create_message_for_function(function, system_id)

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        if not self.send_message(out_message):
            self._logger.error("Sending message failed")
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self._settings.timeouts.t3)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_response(self, function: SecsStreamFunction, system: int) -> bool:
        """Send response function for system.

        Args:
            function: function to be sent
            system: system to reply to

        Returns:
            True if sending was successful

        """
        out_message = self._create_message_for_function(function, system)

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            True if successful

        """
        out_message = self._create_message_for_function(function, self.get_next_system_counter())

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__} {self.serialize_data()}"

    @abc.abstractmethod
    def _get_log_extra(self) -> dict[str, typing.Any]:
        """Get extra fields for logging."""
        raise NotImplementedError("Protocol._get_log_extra missing implementation")
