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

import logging
import queue
import struct
import typing

import secsgem.common

from .header import SecsIHeader
from .packet import SecsIPacket
from .protocol_state_machine import ProtocolStateMachine

if typing.TYPE_CHECKING:
    from ..secs.functions.base import SecsStreamFunction
    from .settings import SecsISettings

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

        self._connected = False

        self._receive_buffer = secsgem.common.ByteQueue()

        self._system_queues: typing.Dict[int, queue.Queue[SecsIPacket]] = {}

        self.__connection: typing.Optional[secsgem.common.Connection] = None
        self._state_machine = ProtocolStateMachine()

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
                "block": index,
                "last_block": index == len(blocks)
            }
            header = packet.header.updated_with(**header_data)

            block_data = header.encode() + block

            block_length_data = bytes([len(block_data)])
            checksum_data = struct.pack(">H", self._calculate_checksum(block_data))

            packet_data = block_length_data + block_data + checksum_data

            self._request_send()

            self._connection.send_data(packet_data)

            if not self._get_send_result():
                return False

        return True

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[secsgem.common.Packet]:
        """
        Send the packet and wait for the response.

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.HsmsPacket`
        """

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
        self.events.fire("connected", {'connection': self})
        self.events.fire('communicating', {'connection': self})

    def _on_disconnected(self, _: typing.Dict[str, typing.Any]):
        """Handle connection was _ event."""
        # clear receive buffer
        self._receive_buffer.clear()

        self.events.fire("disconnected", {'connection': self})

    def _on_connection_data_received(self, data: typing.Dict[str, typing.Any]):
        """Data received by connection.

        Args:
            data: received data

        """
        self._receive_buffer.append(data["data"])

        # handle data in input buffer
        while self._process_receive_buffer():
            pass

    def _process_receive_buffer(self):
        """Parse the receive buffer and dispatch callbacks."""
        if self._state_machine.state == "IDLE":
            if len(self._receive_buffer) < 1:
                return False

            if self._receive_buffer.peek_byte() != self.ENQ:
                raise Exception("Expected ENQ in IDLE state")

            self._receive_buffer.pop()

            self._state_machine.ENQReceived()

            self._connection.send_data(bytes([self.EOT]))

            self._state_machine.Receive()
        elif self._state_machine.state == "RECEIVE":
            if len(self._receive_buffer) < self._receive_buffer.peek_byte() + 3:
                return False

            length = self._receive_buffer.pop_byte()
            data = self._receive_buffer.pop(length)
            checksum = self._receive_buffer.pop(2)

            received_checksum = struct.unpack(">H", checksum)[0]

            if received_checksum != self._calculate_checksum(data):
                self._state_machine.ReceiveComplete()
                self._connection.send_data(bytes([self.NAK]))
                return False

            response = SecsIPacket.decode(data)

            # redirect packet to hsms handler
            try:
                self._on_connection_packet_received(self, response)
            except Exception:  # pylint: disable=broad-except
                self._logger.exception('ignoring exception for on_connection_packet_received handler')

            self._state_machine.ReceiveComplete()

            self._connection.send_data(bytes([self.ACK]))

        elif self._state_machine.state == "SEND":
            raise Exception("TBD_SEND")
        else:
            raise Exception("ELSE")

        # return True if more data is available
        if len(self._receive_buffer) > 0:
            return True

        return False

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

    def _on_connection_packet_received(self, _, packet: SecsIPacket):
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
            self.events.fire("packet_received", {'connection': self, 'packet': packet})

    def _get_log_extra(self):
        return {"port": self._settings.port,
                "speed": self._settings.speed,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name}
