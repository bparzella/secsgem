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
"""SECS-I protocol implementation."""
from __future__ import annotations

import enum
import queue
import struct
import threading
import typing

import secsgem.common

from .header import SecsIHeader
from .message import SecsIBlock, SecsIMessage

if typing.TYPE_CHECKING:
    from ..secs.functions.base import SecsStreamFunction
    from .settings import SecsISettings


class MessageSendResult(enum.Enum):
    """Enum for send result including not send state."""

    NOT_SENT = 0
    SENT_OK = 1
    SENT_ERROR = 2


class MessageSendInfo:
    """Container for sending message and waiting for result."""

    def __init__(self, data: bytes):
        """Initialize package send info object.

        Args:
            data: data to send.

        """
        self._data = data

        self._result = MessageSendResult.NOT_SENT
        self._result_trigger = threading.Event()

    @property
    def data(self) -> bytes:
        """Get the data for sending."""
        return self._data

    def resolve(self, result: bool):
        """Resolve the send data with a result.

        Args:
            result: result to resolve with

        """
        self._result = MessageSendResult.SENT_OK if result else MessageSendResult.SENT_ERROR
        self._result_trigger.set()

    def wait(self) -> bool:
        """Wait for the message is sent and a result is available."""
        self._result_trigger.wait()

        return self._result == MessageSendResult.SENT_OK


class SecsIBlockContainer:
    """Container for message blocks."""

    def __init__(self) -> None:
        """Initialize container."""
        self._messages: typing.Dict[int, SecsIMessage] = {}

    def add_block(self, block: SecsIBlock) -> typing.Optional[SecsIMessage]:
        """Add a block, and get completed message if available.

        Args:
            block: block to add

        Returns:
            completed message or None if paket not complete

        """
        if block.header.system not in self._messages:
            self._messages[block.header.system] = SecsIMessage.from_block(block)
        else:
            self._messages[block.header.system].blocks.append(block)

        message = self._messages[block.header.system]

        if not message.complete:
            return None

        del self._messages[block.header.system]
        return message


class SecsIProtocol(secsgem.common.Protocol):
    """Implementation for SECS-I protocol."""

    ENQ = 0b00000101
    EOT = 0b00000100
    ACK = 0b00000110
    NAK = 0b00010101

    block_size = 244

    def __init__(self, settings: SecsISettings):
        """
        Instantiate SECS I protocol class.

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

        self._receive_buffer = secsgem.common.ByteQueue()
        self._send_queue: queue.Queue[MessageSendInfo] = queue.Queue()
        self._block_container = SecsIBlockContainer()

        self._thread = secsgem.common.ProtocolDispatcher(
            self._process_data,
            self._dispatch_message,
            self._settings
        )

        self._system_queues: typing.Dict[int, queue.Queue[SecsIMessage]] = {}

    def send_message(self, message: secsgem.common.Message) -> bool:
        """
        Send a message to the remote host.

        Args:
            message: message to be transmitted

        """
        # encode the message
        data = message.data

        # split data into blocks
        blocks = [data[i: i + self.block_size] for i in range(0, len(data), self.block_size)]

        for index, block in enumerate(blocks):
            header_data = {
                "block": index + 1,
                "last_block": (index + 1) == len(blocks)
            }
            header = message.header.updated_with(**header_data)

            block_data = header.encode() + block

            block_length_data = bytes([len(block_data)])
            checksum_data = struct.pack(">H", self._calculate_checksum(block_data))

            message_data = block_length_data + block_data + checksum_data

            message_info = MessageSendInfo(message_data)
            self._send_queue.put(message_info)
            self._thread.trigger_receiver()

            if not message_info.wait():
                return False

        return True

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[secsgem.common.Message]:
        """Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            Message that was received

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_message = SecsIMessage(
            SecsIHeader(
                system_id,
                self._settings.session_id,
                function.stream,
                function.function,
                require_response=True,
                from_equipment=(self._settings.device_type == secsgem.common.DeviceType.EQUIPMENT)
            ),
            function.encode()
        )

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        if not self.send_message(out_message):
            self._logger.error("Sending message failed")
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.timeouts.t3)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_response(self, function: SecsStreamFunction, system: int) -> bool:
        """
        Send response function for system.

        :param function: function to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :param system: system to reply to
        :type system: integer
        """
        out_message = SecsIMessage(
            SecsIHeader(system, self._settings.session_id, function.stream, function.function),
            function.encode())

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            True if successful

        """
        out_message = SecsIMessage(
            SecsIHeader(
                self.get_next_system_counter(),
                self._settings.session_id,
                function.stream,
                function.function,
                require_response=True,
                from_equipment=(self._settings.device_type == secsgem.common.DeviceType.EQUIPMENT)
            ),
            function.encode()
        )

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def serialize_data(self) -> typing.Dict[str, typing.Any]:
        """
        Return data for serialization.

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {'port': self._settings.port, 'baud_rate': self._settings.speed}

    @property
    def timeouts(self) -> secsgem.common.Timeouts:
        """Property for timeout."""
        return self._settings.timeouts

    def _on_connected(self, _: typing.Dict[str, typing.Any]):
        """Handle connection was established event."""
        self._thread.start()
        self.events.fire("connected", {'connection': self})
        self.events.fire('communicating', {'connection': self})

    def _on_disconnected(self, _: typing.Dict[str, typing.Any]):
        """Handle connection was _ event."""
        # clear receive buffer
        self.events.fire("disconnected", {'connection': self})

        self._thread.stop()

        self._receive_buffer.clear()

    def _on_connection_data_received(self, data: typing.Dict[str, typing.Any]):
        """Data received by connection.

        Args:
            data: received data

        """
        self._receive_buffer.append(data["data"])
        self._thread.trigger_receiver()

    def _on_disconnecting(self, _: typing.Dict[str, typing.Any]):
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

            message_info = self._send_queue.get()

            self._connection.send_data(message_info.data)

            data_resonse = self._receive_buffer.wait_for_byte()

            message_info.resolve(data_resonse == self.ACK)

    def _process_received_data(self):
        if len(self._receive_buffer) < 1:
            return

        while len(self._receive_buffer) > 0:
            receive_byte = self._receive_buffer.pop_byte()

            if receive_byte != self.ENQ:
                raise Exception(f"Expected ENQ, received '{receive_byte}'")

            self._connection.send_data(bytes([self.EOT]))

            length = self._receive_buffer.wait_for_byte()

            data = self._receive_buffer.wait_for(length)

            checksum = self._receive_buffer.wait_for(2)

            received_checksum = struct.unpack(">H", checksum)[0]

            if received_checksum != self._calculate_checksum(data):
                self._connection.send_data(bytes([self.NAK]))
                return

            response = SecsIBlock.decode(data)

            # redirect message to hsms handler
            self._thread.queue_message(self, response)

            self._connection.send_data(bytes([self.ACK]))

    def _process_data(self):
        """Parse the receive buffer and dispatch callbacks."""
        self._process_send_queue()
        self._process_received_data()

    def _calculate_checksum(self, data: bytes) -> int:
        """Calculate checksum of data message.

        Args:
            data: message data

        Returns:
            checksum

        """
        calculated_checksum = 0

        for data_byte in data:
            calculated_checksum += data_byte

        return calculated_checksum

    def _on_connection_message_received(self, source: object, message: SecsIMessage):
        """Message received by connection.

        Args:
            source: source of event
            message: received data message

        """
        decoded_message = self._settings.streams_functions.decode(message)
        self._communication_logger.info("< %s\n%s", message, decoded_message, extra=self._get_log_extra())

        # someone is waiting for this message
        if message.header.system in self._system_queues:
            self._system_queues[message.header.system].put_nowait(message)
        else:
            self.events.fire("message_received", {'connection': source, 'message': message})

    def _dispatch_message(self, source: object, message: SecsIBlock):
        result = self._block_container.add_block(message)
        if result is None:
            return

        try:
            self._on_connection_message_received(source, result)
        except Exception:  # pylint: disable=broad-except
            self._logger.exception('ignoring exception for on_connection_message_received handler')

    def _get_log_extra(self):
        return {"port": self._settings.port,
                "speed": self._settings.speed,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name}

    # TODO: different way of waiting for response? BlockInfo?
    def _get_queue_for_system(self, system_id):
        """
        Create a new queue to receive responses for a certain system.

        :param system_id: system id to watch
        :type system_id: int
        :returns: queue to receive responses with
        :rtype: queue.Queue
        """
        self._system_queues[system_id] = queue.Queue()
        return self._system_queues[system_id]

    def _remove_queue(self, system_id):
        """
        Remove queue for system id from list.

        :param system_id: system id to remove
        :type system_id: int
        """
        del self._system_queues[system_id]
