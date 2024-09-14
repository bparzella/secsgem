#####################################################################
# protocol.py
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
"""Contains class to create model for hsms endpoints."""

from __future__ import annotations

import queue
import struct
import threading
import typing

import secsgem.common

from .connection_state_machine import ConnectionState, ConnectionStateMachine
from .deselect_req_header import HsmsDeselectReqHeader
from .deselect_rsp_header import HsmsDeselectRspHeader
from .header import HsmsSType
from .linktest_req_header import HsmsLinktestReqHeader
from .linktest_rsp_header import HsmsLinktestRspHeader
from .message import HsmsBlock, HsmsMessage
from .reject_req_header import HsmsRejectReqHeader
from .select_req_header import HsmsSelectReqHeader
from .select_rsp_header import HsmsSelectRspHeader
from .separate_req_header import HsmsSeparateReqHeader
from .stream_function_header import HsmsStreamFunctionHeader

if typing.TYPE_CHECKING:
    from secsgem.common.protocol import Protocol
    from secsgem.secs.functions.base import SecsStreamFunction

    from .settings import HsmsSettings


class HsmsProtocol(secsgem.common.Protocol[HsmsMessage, HsmsBlock]):  # pylint: disable=too-many-instance-attributes
    """Baseclass for creating Host/Equipment models.

    This layer contains the HSMS functionality.
    Inherit from this class and override required functions.
    """

    send_packet_size = 1024 * 1024
    """ Block size for outbound data ."""

    message_type = HsmsMessage

    def __init__(self, settings: HsmsSettings):
        """Initialize hsms handler.

        Args:
            settings: protocol and communication settings

        Example:
            import secsgem.hsms

            settings = secsgem.hsms.HsmsSettings(
                address="10.211.55.33",
                port=5000,
                active=secsgem.hsms.HsmsConnectMode.ACTIVE,
                name="test"
            )
            def onConnect(event, data):
                print ("Connected")

            client = secsgem.hsms.HsmsProtocol(settings)
            client.events.connected += onConnect

            client.enable()

            time.sleep(3)

            client.disable()

        """
        super().__init__(settings)
        self._settings: HsmsSettings = settings

        self._connected = False

        # repeating linktest variables
        self._linktest_timer = None
        self._linktest_timeout = 30

        # select request thread for active connections, to avoid blocking state changes
        self._select_req_thread: threading.Thread | None = None

        # hsms connection state fsm
        self._connection_state = ConnectionStateMachine()

        self._connection_state.connected.events.enter.register(self._on_state_connect)
        self._connection_state.connected.events.leave.register(self._on_state_disconnect)
        self._connection_state.connected_selected.events.enter.register(self._on_state_select)

    @property
    def connection_state(self) -> ConnectionStateMachine:
        """Property for connection state."""
        return self._connection_state

    def _send_select_req_thread(self):
        """Send select request thread function."""
        try:
            response = self.send_select_req()
            if response is None:
                self._logger.warning("select request failed")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self._logger.warning("exception in _send_select_req_thread", exc_info=exc)

    def _start_linktest_timer(self):
        """Start the linktest timer."""
        self._linktest_timer = threading.Timer(self._linktest_timeout, self._on_linktest_timer)
        self._linktest_timer.daemon = True  # kill thread automatically on main program termination
        self._linktest_timer.name = "secsgem_hsmsProtocol_linktestTimer"
        self._linktest_timer.start()

    def _on_state_connect(self, _: dict[str, typing.Any]):
        """Handle connection state model got event connect.

        Args:
            data: event attributes

        """
        # start linktest timer
        self._start_linktest_timer()

        # start select process if connection is active
        if self._settings.is_active:
            self._select_req_thread = threading.Thread(
                target=self._send_select_req_thread,
                name="secsgem_hsmsProtocol_sendSelectReqThread",
            )
            self._select_req_thread.daemon = True  # kill thread automatically on main program termination
            self._select_req_thread.start()

    def _on_state_disconnect(self, _: dict[str, typing.Any]):
        """Handle connection state model got event disconnect.

        Args:
            data: event attributes

        """
        # stop linktest timer
        if self._linktest_timer:
            self._linktest_timer.cancel()

        self._linktest_timer = None

    def _on_state_select(self, _: dict[str, typing.Any]):
        """Handle connection state model got event select.

        Args:
            data: event attributes

        """
        # send event
        self.events.fire("communicating", {"connection": self})

    def _on_linktest_timer(self):
        """Linktest time timed out, so send linktest request."""
        # send linktest request and wait for response
        self.send_linktest_req()

        # restart the timer
        self._start_linktest_timer()

    def _on_connected(self, _: dict[str, typing.Any]):
        """Handle connection was established event.

        The arguemnt is a dictionary with the following keys
        - source: connection object that triggered the event

        """
        self._connected = True

        self._thread.start()

        # update connection state
        self._connection_state.connect()

        self.events.fire("connected", {"connection": self})

    def _on_disconnecting(self, _: dict[str, typing.Any]):
        """Handle connection is about to be closed event.

        The arguemnt is a dictionary with the following keys
        - source: connection object that triggered the event

        """
        # send separate request
        self.send_separate_req()

    def _on_disconnected(self, _: dict[str, typing.Any]):
        """Handle connection was closed event.

        The arguemnt is a dictionary with the following keys
        - source: connection object that triggered the event

        """
        # update connection state
        self._connected = False
        self._connection_state.disconnect()

        self._thread.stop()
        self._receive_buffer.clear()

        self.events.fire("disconnected", {"connection": self})

    def __handle_hsms_requests_select_req(self, message: HsmsMessage):
        """Handle HSMS Select Request.

        Args:
            message: received message

        """
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_select_rsp(message.header.system)

            self._connection_state.select()

    def __handle_hsms_requests_select_rsp(self, message: HsmsMessage):
        """Handle HSMS Select Response.

        Args:
            message: received message

        """
        self._connection_state.select()

        if message.header.system in self._response_queues:
            self._response_queues[message.header.system].put_nowait(message)

    def __handle_hsms_requests_deselect_req(self, message: HsmsMessage):
        """Handle HSMS Deselect Request.

        Args:
            message: received message

        """
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_deselect_rsp(message.header.system)

            self._connection_state.deselect()

    def __handle_hsms_requests_deselect_rsp(self, message: HsmsMessage):
        """Handle HSMS Deselect Response.

        Args:
            message: received message

        """
        self._connection_state.deselect()

        if message.header.system in self._response_queues:
            self._response_queues[message.header.system].put_nowait(message)

    def __handle_hsms_requests_linktest_req(self, message: HsmsMessage):
        """Handle HSMS Linktest Request.

        Args:
            message: received message

        """
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_linktest_rsp(message.header.system)

    def __handle_hsms_requests(self, message: HsmsMessage):
        """Handle HSMS messages.

        Args:
            message: received message

        """
        self._communication_logger.info("< %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())

        if message.header.s_type == HsmsSType.SELECT_REQ:
            self.__handle_hsms_requests_select_req(message)
        elif message.header.s_type == HsmsSType.SELECT_RSP:
            self.__handle_hsms_requests_select_rsp(message)
        elif message.header.s_type == HsmsSType.DESELECT_REQ:
            self.__handle_hsms_requests_deselect_req(message)
        elif message.header.s_type == HsmsSType.DESELECT_RSP:
            self.__handle_hsms_requests_deselect_rsp(message)
        elif message.header.s_type == HsmsSType.LINKTEST_REQ:
            self.__handle_hsms_requests_linktest_req(message)
        else:
            if message.header.system in self._response_queues:
                self._response_queues[message.header.system].put_nowait(message)

    def _process_received_data(self):
        """Process the received data from communication queue."""
        if len(self._receive_buffer) < 4:
            return

        while len(self._receive_buffer) > 3:
            length_data = self._receive_buffer.wait_for(4, peek=True)
            length = struct.unpack(">L", length_data)[0] + 4

            data = self._receive_buffer.wait_for(length)

            # decode received message
            response = HsmsBlock.decode(data)

            self._thread.queue_block(self, response)

    def _on_connection_message_received(self, _: Protocol, message: HsmsMessage):
        """Message received by connection.

        Args:
            source: source of event
            message: received data message

        """
        if message.header.s_type.value > 0:
            self.__handle_hsms_requests(message)
        else:
            decoded_message = self._settings.streams_functions.decode(message)
            self._communication_logger.info("< %s\n%s", message, decoded_message, extra=self._get_log_extra())

            if self._connection_state.current != ConnectionState.CONNECTED_SELECTED:
                self._logger.warning("received message when not selected")

                out_message = HsmsMessage(HsmsRejectReqHeader(message.header.system, message.header.s_type, 4), b"")
                self._communication_logger.info(
                    "> %s\n  %s",
                    out_message,
                    out_message.header.s_type.text,
                    extra=self._get_log_extra(),
                )
                self.send_message(out_message)

                return

            # someone is waiting for this message
            if message.header.system in self._response_queues:
                # send message to request sender
                self._response_queues[message.header.system].put_nowait(message)
            # just log if nobody is interested
            else:
                self.events.fire("message_received", {"connection": self, "message": message})

    def serialize_data(self) -> dict[str, typing.Any]:
        """Return data for serialization.

        Returns:
            data to serialize for this object

        """
        return {
            "address": self._settings.address,
            "port": self._settings.port,
            "connect_mode": self._settings.connect_mode,
            "session_id": self._settings.session_id,
            "name": self._settings.name,
            "connected": self._connected,
        }

    def _process_send_queue(self):
        """Process the send to communication queue."""
        if self._send_queue.empty():
            return

        while not self._send_queue.empty():
            block_info = self._send_queue.get()

            packets = [
                block_info.data[i : i + self.send_packet_size]
                for i in range(0, len(block_info.data), self.send_packet_size)
            ]

            for packet in packets:
                if not self._connection.send_data(packet):
                    block_info.resolve(False)
                    return

            block_info.resolve(True)

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
        return HsmsMessage(
            HsmsStreamFunctionHeader(
                system_id,
                function.stream,
                function.function,
                function.is_reply_required,
                self._settings.session_id,
            ),
            function.encode(),
        )

    def send_select_req(self) -> HsmsMessage | None:
        """Send a Select Request to the remote host.

        Returns:
            received message or None

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsSelectReqHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self._settings.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_select_rsp(self, system_id: int) -> bool:
        """Send a Select Response to the remote host.

        Args:
            system_id: System of the request to reply for

        Returns:
            False if sending was not successful

        """
        message = HsmsMessage(HsmsSelectRspHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())
        return self.send_message(message)

    def send_linktest_req(self) -> HsmsMessage | None:
        """Send a Linktest Request to the remote host.

        Returns:
            received message or None

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsLinktestReqHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self._settings.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_linktest_rsp(self, system_id: int) -> bool:
        """Send a Linktest Response to the remote host.

        Args:
            system_id: System of the request to reply for

        Returns:
            False if sending was not successful

        """
        message = HsmsMessage(HsmsLinktestRspHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())
        return self.send_message(message)

    def send_deselect_req(self) -> HsmsMessage | None:
        """Send a Deselect Request to the remote host.

        Returns:
            received message or None

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsDeselectReqHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self._settings.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_deselect_rsp(self, system_id: int) -> bool:
        """Send a Deselect Response to the remote host.

        Args:
            system_id: System of the request to reply for

        Returns:
            False if sending was not successful

        """
        message = HsmsMessage(HsmsDeselectRspHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())
        return self.send_message(message)

    def send_reject_rsp(self, system_id: int, s_type: HsmsSType, reason: int) -> bool:
        """Send a Reject Response to the remote host.

        Args:
            system_id: System of the request to reply for
            s_type: Type of the request to reply for
            reason: Reason of the rejection

        Returns:
            False if sending was not successful

        """
        message = HsmsMessage(HsmsRejectReqHeader(system_id, s_type, reason), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())
        return self.send_message(message)

    def send_separate_req(self) -> int | None:
        """Send a Separate Request to the remote host.

        Returns:
            system id of the request or None if sending failed

        """
        system_id = self.get_next_system_counter()

        message = HsmsMessage(HsmsSeparateReqHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text, extra=self._get_log_extra())

        if not self.send_message(message):
            return None

        return system_id

    # helpers

    def _get_log_extra(self) -> dict[str, typing.Any]:
        """Get extra fields for logging."""
        return {
            "address": self._settings.address,
            "port": self._settings.port,
            "session_id": self._settings.session_id,
            "remoteName": self._settings.name,
        }
