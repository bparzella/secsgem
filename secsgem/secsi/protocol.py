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
import logging
import queue
import struct
import threading
import typing

import secsgem.common

from .header import SecsIHeader
from .packet import SecsIPacket

if typing.TYPE_CHECKING:
    from ..secs.functions.base import SecsStreamFunction
    from .settings import SecsISettings


class PacketSendResult(enum.Enum):
    """Enum for send result including not send state."""

    NOT_SENT = 0
    SENT_OK = 1
    SENT_ERROR = 2


class PacketSendInfo:
    """Container for sending packet and waiting for result."""

    def __init__(self, data: bytes):
        """Initialize package send info object.

        Args:
            data: data to send.

        """
        self._data = data

        self._result = PacketSendResult.NOT_SENT
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
        self._result = PacketSendResult.SENT_OK if result else PacketSendResult.SENT_ERROR
        self._result_trigger.set()

    def wait(self) -> bool:
        """Wait for the packet is sent and a result is available."""
        self._result_trigger.wait()

        return self._result == PacketSendResult.SENT_OK


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

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._communication_logger = logging.getLogger("communication")

        self.__connection: typing.Optional[secsgem.common.Connection] = None
        self._receive_buffer = secsgem.common.ByteQueue()
        self._send_queue: queue.Queue[PacketSendInfo] = queue.Queue()

        self._thread = secsgem.common.ProtocolDispatcher(
            self._process_data,
            self._dispatch_packet,
            self._settings
        )

        self._system_queues: typing.Dict[int, queue.Queue[SecsIPacket]] = {}

    @property
    def _connection(self) -> secsgem.common.Connection:
        if self.__connection is None:
            self.__connection = self._settings.create_connection()
            self.__connection.on_connected.register(self._on_connected)
            self.__connection.on_data.register(self._on_connection_data_received)
            self.__connection.on_disconnected.register(self._on_disconnected)

        return self.__connection

    def enable(self):
        """Enable the connection."""
        self._connection.enable()

    def disable(self):
        """Disable the connection."""
        self._connection.enable()

    def send_packet(self, packet: secsgem.common.Packet) -> bool:
        """
        Send a packet to the remote host.

        Args:
            packet: packet to be transmitted

        """
        # encode the packet
        data = packet.data

        # split data into blocks
        blocks = [data[i: i + self.block_size] for i in range(0, len(data), self.block_size)]

        for index, block in enumerate(blocks):
            header_data = {
                "block": index + 1,
                "last_block": (index + 1) == len(blocks)
            }
            header = packet.header.updated_with(**header_data)

            block_data = header.encode() + block

            block_length_data = bytes([len(block_data)])
            checksum_data = struct.pack(">H", self._calculate_checksum(block_data))

            packet_data = block_length_data + block_data + checksum_data

            packet_info = PacketSendInfo(packet_data)
            self._send_queue.put(packet_info)
            self._thread.trigger_receiver()

            if not packet_info.wait():
                return False

        return True

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[secsgem.common.Packet]:
        """Send the packet and wait for the response.

        Args:
            packet: packet to be sent

        Returns:
            Packet that was received

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_packet = SecsIPacket(
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

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        if not self.send_packet(out_packet):
            self._logger.error("Sending packet failed")
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
        out_packet = SecsIPacket(
            SecsIHeader(system, self._settings.session_id, function.stream, function.function),
            function.encode())

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        return self.send_packet(out_packet)

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the packet and wait for the response.

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        """
        out_packet = SecsIPacket(
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

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        return self.send_packet(out_packet)

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

            packet_info = self._send_queue.get()

            self._connection.send_data(packet_info.data)

            data_resonse = self._receive_buffer.wait_for_byte()

            packet_info.resolve(data_resonse == self.ACK)

    # TODO: join multi-block message before dispatching
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
                return False

            response = SecsIPacket.decode(data)

            # redirect packet to hsms handler
            self._thread.queue_packet(self, response)

            self._connection.send_data(bytes([self.ACK]))

    def _process_data(self):
        """Parse the receive buffer and dispatch callbacks."""
        self._process_send_queue()
        self._process_received_data()

    def _calculate_checksum(self, data: bytes) -> int:
        """Calculate checksum of data packet.

        Args:
            data: packet data

        Returns:
            checksum

        """
        calculated_checksum = 0

        for data_byte in data:
            calculated_checksum += data_byte

        return calculated_checksum

    def _on_connection_packet_received(self, source: object, packet: SecsIPacket):
        """Packet received by connection.

        Args:
            packet: received data packet

        """
        message = self._settings.streams_functions.decode(packet)
        self._communication_logger.info("< %s\n%s", packet, message, extra=self._get_log_extra())

        # someone is waiting for this message
        if packet.header.system in self._system_queues:
            self._system_queues[packet.header.system].put_nowait(packet)
        else:
            self.events.fire("packet_received", {'connection': source, 'packet': packet})

    def _dispatch_packet(self, source: object, packet: SecsIPacket):
        try:
            self._on_connection_packet_received(source, packet)
        except Exception:  # pylint: disable=broad-except
            self._logger.exception('ignoring exception for on_connection_packet_received handler')

    def _get_log_extra(self):
        return {"port": self._settings.port,
                "speed": self._settings.speed,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name}

    # TODO: different way of waiting for response? PacketInfo?
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
