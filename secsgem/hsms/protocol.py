#####################################################################
# protocol.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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

from .message import HsmsMessage
from .header import HsmsSType
from .select_req_header import HsmsSelectReqHeader
from .select_rsp_header import HsmsSelectRspHeader
from .deselect_req_header import HsmsDeselectReqHeader
from .deselect_rsp_header import HsmsDeselectRspHeader
from .linktest_req_header import HsmsLinktestReqHeader
from .linktest_rsp_header import HsmsLinktestRspHeader
from .reject_req_header import HsmsRejectReqHeader
from .separate_req_header import HsmsSeparateReqHeader
from .stream_function_header import HsmsStreamFunctionHeader
from .connectionstatemachine import ConnectionStateMachine

from ..secs.functions.base import SecsStreamFunction


if typing.TYPE_CHECKING:
    from .settings import HsmsSettings


HSMS_STYPES = {
    1: "Select.req",
    2: "Select.rsp",
    3: "Deselect.req",
    4: "Deselect.rsp",
    5: "Linktest.req",
    6: "Linktest.rsp",
    7: "Reject.req",
    9: "Separate.req"
}
"""Names for hsms header SType."""


class HsmsProtocol(secsgem.common.Protocol):  # pylint: disable=too-many-instance-attributes
    """
    Baseclass for creating Host/Equipment models.

    This layer contains the HSMS functionality.
    Inherit from this class and override required functions.
    """

    send_block_size = 1024 * 1024
    """ Block size for outbound data ."""

    def __init__(self, settings: HsmsSettings):
        """
        Initialize hsms handler.

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

        self._connected = False

        # repeating linktest variables
        self._linktest_timer = None
        self._linktest_timeout = 30

        # select request thread for active connections, to avoid blocking state changes
        self._select_req_thread = None

        # response queues
        self._system_queues: typing.Dict[int, queue.Queue[HsmsMessage]] = {}

        # hsms connection state fsm
        self._connection_state = ConnectionStateMachine({"on_enter_CONNECTED": self._on_state_connect,
                                                         "on_exit_CONNECTED": self._on_state_disconnect,
                                                         "on_enter_CONNECTED_SELECTED": self._on_state_select})

        # buffer for received data
        self._receive_buffer = b""

    @property
    def connection_state(self) -> ConnectionStateMachine:
        """Property for connection state."""
        return self._connection_state

    def _send_select_req_thread(self):
        response = self.send_select_req()
        if response is None:
            self._logger.warning("select request failed")

    def _start_linktest_timer(self):
        self._linktest_timer = threading.Timer(self._linktest_timeout, self._on_linktest_timer)
        self._linktest_timer.daemon = True  # kill thread automatically on main program termination
        self._linktest_timer.name = "secsgem_hsmsProtocol_linktestTimer"
        self._linktest_timer.start()

    def _on_state_connect(self):
        """
        Handle connection state model got event connect.

        :param data: event attributes
        :type data: object
        """
        # start linktest timer
        self._start_linktest_timer()

        # start select process if connection is active
        if self._settings.is_active:
            self._select_req_thread = threading.Thread(
                target=self._send_select_req_thread,
                name="secsgem_hsmsProtocol_sendSelectReqThread")
            self._select_req_thread.daemon = True  # kill thread automatically on main program termination
            self._select_req_thread.start()

    def _on_state_disconnect(self):
        """
        Handle connection state model got event disconnect.

        :param data: event attributes
        :type data: object
        """
        # stop linktest timer
        if self._linktest_timer:
            self._linktest_timer.cancel()

        self._linktest_timer = None

    def _on_state_select(self):
        """
        Handle connection state model got event select.

        :param data: event attributes
        :type data: object
        """
        # send event
        self.events.fire('communicating', {'connection': self})

    def _on_linktest_timer(self):
        """Linktest time timed out, so send linktest request."""
        # send linktest request and wait for response
        self.send_linktest_req()

        # restart the timer
        self._start_linktest_timer()

    def _on_connected(self, _: typing.Dict[str, typing.Any]):
        """Handle connection was established event."""
        self._connected = True

        # update connection state
        self._connection_state.connect()

        self.events.fire("connected", {'connection': self})

    def _on_disconnecting(self, _: typing.Dict[str, typing.Any]):
        """Handle connection is about to be closed event."""
        # send separate request
        self.send_separate_req()

    def _on_disconnected(self, _: typing.Dict[str, typing.Any]):
        """Handle connection was _ event."""
        # update connection state
        self._connected = False
        self._connection_state.disconnect()

        # clear receive buffer
        self._receive_buffer = b""

        self.events.fire("disconnected", {'connection': self})

    def __handle_hsms_requests_select_req(self, message: HsmsMessage):
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_select_rsp(message.header.system)

            self._connection_state.select()

    def __handle_hsms_requests_select_rsp(self, message: HsmsMessage):
        self._connection_state.select()

        if message.header.system in self._system_queues:
            self._system_queues[message.header.system].put_nowait(message)

    def __handle_hsms_requests_deselect_req(self, message: HsmsMessage):
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_deselect_rsp(message.header.system)

            self._connection_state.deselect()

    def __handle_hsms_requests_deselect_rsp(self, message: HsmsMessage):
        self._connection_state.deselect()

        if message.header.system in self._system_queues:
            self._system_queues[message.header.system].put_nowait(message)

    def __handle_hsms_requests_linktest_req(self, message: HsmsMessage):
        if self._connection.disconnecting:
            self.send_reject_rsp(message.header.system, message.header.s_type, 4)
        else:
            self.send_linktest_rsp(message.header.system)

    def __handle_hsms_requests(self, message: HsmsMessage):
        self._communication_logger.info("< %s\n  %s", message, message.header.s_type.text,
                                        extra=self._get_log_extra())

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
            if message.header.system in self._system_queues:
                self._system_queues[message.header.system].put_nowait(message)

    def _on_connection_data_received(self, data: typing.Dict[str, typing.Any]):
        """Data received by connection.

        Args:
            data: received data

        """
        self._receive_buffer += data["data"]

        # handle data in input buffer
        while self._process_receive_buffer():
            pass

    def _process_receive_buffer(self):
        """
        Parse the receive buffer and dispatch callbacks.

        .. warning:: Do not call this directly, will be called from
        :func:`secsgem.hsmsConnections.hsmsConnection.__receiver_thread` method.
        """
        # check if enough data in input buffer
        if len(self._receive_buffer) < 4:
            return False

        # unpack length from input buffer
        length = struct.unpack(">L", self._receive_buffer[0:4])[0] + 4

        # check if enough data in input buffer
        if len(self._receive_buffer) < length:
            return False

        # extract and remove message from input buffer
        data = self._receive_buffer[0:length]
        self._receive_buffer = self._receive_buffer[length:]

        # decode received message
        response = HsmsMessage.decode(data)

        # redirect message to hsms handler
        try:
            self._on_connection_message_received(self, response)
        except Exception:  # pylint: disable=broad-except
            self._logger.exception('ignoring exception for on_connection_message_received handler')

        # return True if more data is available
        if len(self._receive_buffer) > 0:
            return True

        return False

    def _on_connection_message_received(self, _, message: HsmsMessage):
        """Message received by connection.

        Args:
            message: received data message

        """
        if message.header.s_type.value > 0:
            self.__handle_hsms_requests(message)
        else:
            decoded_message = self._settings.streams_functions.decode(message)
            self._communication_logger.info("< %s\n%s", message, decoded_message, extra=self._get_log_extra())

            if not self._connection_state.is_CONNECTED_SELECTED():
                self._logger.warning("received message when not selected")

                out_message = HsmsMessage(HsmsRejectReqHeader(message.header.system, message.header.s_type, 4), b"")
                self._communication_logger.info(
                    "> %s\n  %s", out_message, out_message.header.s_type.text,
                    extra=self._get_log_extra())
                self.send_message(out_message)

                return

            # someone is waiting for this message
            if message.header.system in self._system_queues:
                # send message to request sender
                self._system_queues[message.header.system].put_nowait(message)
            # just log if nobody is interested
            else:
                self.events.fire("message_received", {'connection': self, 'message': message})

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

    def __repr__(self):
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__} {str(self.serialize_data())}"

    def serialize_data(self) -> typing.Dict[str, typing.Any]:
        """
        Return data for serialization.

        :returns: data to serialize for this object
        :rtype: dict
        """
        return {
            'address': self._settings.address,
            'port': self._settings.port,
            'connect_mode': self._settings.connect_mode,
            'session_id': self._settings.session_id,
            'name': self._settings.name,
            'connected': self._connected
        }

    def send_message(self, message: secsgem.common.Message) -> bool:
        """
        Send a message to the remote host.

        Args:
            message: message to be transmitted

        """
        # encode the message
        data = message.encode()

        # split data into blocks
        blocks = [data[i: i + self.send_block_size] for i in range(0, len(data), self.send_block_size)]

        for block in blocks:
            if not self._connection.send_data(block):
                return False

        return True

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            True if successful

        """
        out_message = HsmsMessage(
            HsmsStreamFunctionHeader(self.get_next_system_counter(), function.stream, function.function,
                                     function.is_reply_required, self._settings.session_id),
            function.encode())

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[secsgem.common.Message]:
        """
        Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            Message that was received

        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_message = HsmsMessage(
            HsmsStreamFunctionHeader(
                system_id,
                function.stream,
                function.function,
                True,
                self._settings.session_id),
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
        out_message = HsmsMessage(HsmsStreamFunctionHeader(system, function.stream, function.function, False,
                                                           self._settings.session_id),
                                  function.encode())

        self._communication_logger.info("> %s\n%s", out_message, function, extra=self._get_log_extra())

        return self.send_message(out_message)

    def send_select_req(self):
        """
        Send a Select Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsSelectReqHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_select_rsp(self, system_id):
        """
        Send a Select Response to the remote host.

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        message = HsmsMessage(HsmsSelectRspHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())
        return self.send_message(message)

    def send_linktest_req(self):
        """
        Send a Linktest Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsLinktestReqHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_linktest_rsp(self, system_id):
        """
        Send a Linktest Response to the remote host.

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        message = HsmsMessage(HsmsLinktestRspHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())
        return self.send_message(message)

    def send_deselect_req(self):
        """
        Send a Deselect Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        message = HsmsMessage(HsmsDeselectReqHeader(system_id), b"")
        self._communication_logger.info("> %s\n  %s", message, message.header.s_type.text,
                                        extra=self._get_log_extra())

        if not self.send_message(message):
            self._remove_queue(system_id)
            return None

        try:
            response = response_queue.get(True, self.timeouts.t6)
        except queue.Empty:
            response = None

        self._remove_queue(system_id)

        return response

    def send_deselect_rsp(self, system_id):
        """
        Send a Deselect Response to the remote host.

        :param system_id: System of the request to reply for
        :type system_id: integer
        """
        message = HsmsMessage(HsmsDeselectRspHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())
        return self.send_message(message)

    def send_reject_rsp(self, system_id: int, s_type: HsmsSType, reason: int):
        """
        Send a Reject Response to the remote host.

        :param system_id: System of the request to reply for
        :type system_id: integer
        :param s_type: s_type of rejected message
        :type s_type: integer
        :param reason: reason for rejection
        :type reason: integer
        """
        message = HsmsMessage(HsmsRejectReqHeader(system_id, s_type, reason), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())
        return self.send_message(message)

    def send_separate_req(self):
        """Send a Separate Request to the remote host."""
        system_id = self.get_next_system_counter()

        message = HsmsMessage(HsmsSeparateReqHeader(system_id), b"")
        self._communication_logger.info(
            "> %s\n  %s", message, message.header.s_type.text,
            extra=self._get_log_extra())

        if not self.send_message(message):
            return None

        return system_id

    # helpers

    def _get_log_extra(self):
        return {"address": self._settings.address,
                "port": self._settings.port,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name}
