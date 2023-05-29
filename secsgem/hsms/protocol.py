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

import logging
import queue
import random
import threading
import typing

import secsgem.common

from .connection import HSMS_STYPES
from .packet import HsmsPacket
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


class HsmsProtocol(secsgem.common.Protocol):  # pylint: disable=too-many-instance-attributes
    """
    Baseclass for creating Host/Equipment models.

    This layer contains the HSMS functionality.
    Inherit from this class and override required functions.
    """

    def __init__(self, settings: HsmsSettings):
        """
        Initialize hsms handler.

        Args:
            settings: protocol and communication settings

        **Example**::

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
            client.events.hsms_connected += onConnect

            client.enable()

            time.sleep(3)

            client.disable()

        """
        super().__init__(settings)
        self._settings = settings

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._communication_logger = logging.getLogger("hsms_communication")

        self._connected = False

        # system id counter
        self._system_counter = random.randint(0, (2 ** 32) - 1)

        # repeating linktest variables
        self._linktest_timer = None
        self._linktest_timeout = 30

        # select request thread for active connections, to avoid blocking state changes
        self._select_req_thread = None

        # response queues
        self._system_queues: typing.Dict[int, HsmsPacket] = {}

        # hsms connection state fsm
        self._connection_state = ConnectionStateMachine({"on_enter_CONNECTED": self._on_state_connect,
                                                         "on_exit_CONNECTED": self._on_state_disconnect,
                                                         "on_enter_CONNECTED_SELECTED": self._on_state_select})

        self.__connection: typing.Optional[secsgem.common.Connection] = None

    @property
    def _connection(self) -> secsgem.common.Connection:
        if self.__connection is None:
            self.__connection = self._settings.create_connection()

        return self.__connection

    @property
    def timeouts(self) -> secsgem.common.Timeouts:
        """Property for timeout."""
        return self._settings.timeouts

    @property
    def name(self) -> str:
        """Property for name."""
        return self._settings.name

    @property
    def connection(self) -> secsgem.common.Connection:
        """Property for connection."""
        return self._connection

    @property
    def connection_state(self) -> ConnectionStateMachine:
        """Property for connection state."""
        return self._connection_state

    def get_next_system_counter(self):
        """
        Return the next System.

        :returns: System for the next command
        :rtype: integer
        """
        self._system_counter += 1

        if self._system_counter > ((2 ** 32) - 1):
            self._system_counter = 0

        return self._system_counter

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
        self.events.fire('hsms_selected', {'connection': self})

    def _on_linktest_timer(self):
        """Linktest time timed out, so send linktest request."""
        # send linktest request and wait for response
        self.send_linktest_req()

        # restart the timer
        self._start_linktest_timer()

    def on_connection_established(self, _):
        """Handle connection was established event."""
        self._connected = True

        # update connection state
        self._connection_state.connect()

        self.events.fire("hsms_connected", {'connection': self})

    def on_connection_before_closed(self, _):
        """Handle connection is about to be closed event."""
        # send separate request
        self.send_separate_req()

    def on_connection_closed(self, _):
        """Handle connection was closed event."""
        # update connection state
        self._connected = False
        self._connection_state.disconnect()

        self.events.fire("hsms_disconnected", {'connection': self})

    def __handle_hsms_requests(self, packet: HsmsPacket):  # noqa: MC0001
        self._communication_logger.info("< %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
                                        extra=self._get_log_extra())

        # check if it is a select request
        if packet.header.s_type == 0x01:
            # if we are disconnecting send reject else send response
            if self._connection.disconnecting:
                self.send_reject_rsp(packet.header.system, packet.header.s_type, 4)
            else:
                self.send_select_rsp(packet.header.system)

                # update connection state
                self._connection_state.select()

        # check if it is a select response
        elif packet.header.s_type == 0x02:
            # update connection state
            self._connection_state.select()

            if packet.header.system in self._system_queues:
                # send packet to request sender
                self._system_queues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?

        # check if it is a deselect request
        elif packet.header.s_type == 0x03:
            # if we are disconnecting send reject else send response
            if self._connection.disconnecting:
                self.send_reject_rsp(packet.header.system, packet.header.s_type, 4)
            else:
                self.send_deselect_rsp(packet.header.system)
                # update connection state
                self._connection_state.deselect()

        # check if it is a deselect response
        elif packet.header.s_type == 0x04:
            # update connection state
            self._connection_state.deselect()

            if packet.header.system in self._system_queues:
                # send packet to request sender
                self._system_queues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?

        # check if it is a linktest request
        elif packet.header.s_type == 0x05:
            # if we are disconnecting send reject else send response
            if self._connection.disconnecting:
                self.send_reject_rsp(packet.header.system, packet.header.s_type, 4)
            else:
                self.send_linktest_rsp(packet.header.system)

        else:
            if packet.header.system in self._system_queues:
                # send packet to request sender
                self._system_queues[packet.header.system].put_nowait(packet)

            # what to do if no sender for request waiting?

    def on_connection_packet_received(self, _, packet):
        """
        Packet received by connection.

        :param packet: received data packet
        :type packet: :class:`secsgem.hsms.HsmsPacket`
        """
        if packet.header.s_type > 0:
            self.__handle_hsms_requests(packet)
        else:
            message = self._settings.streams_functions.decode(packet)
            self._communication_logger.info("< %s\n%s", packet, message, extra=self._get_log_extra())

            if not self._connection_state.is_CONNECTED_SELECTED():
                self._logger.warning("received message when not selected")

                out_packet = HsmsPacket(HsmsRejectReqHeader(packet.header.system, packet.header.s_type, 4))
                self._communication_logger.info(
                    "> %s\n  %s", out_packet, HSMS_STYPES[out_packet.header.s_type],
                    extra=self._get_log_extra())
                self._connection.send_packet(out_packet)

                return

            # someone is waiting for this message
            if packet.header.system in self._system_queues:
                # send packet to request sender
                self._system_queues[packet.header.system].put_nowait(packet)
            # just log if nobody is interested
            else:
                self.events.fire("hsms_packet_received", {'connection': self, 'packet': packet})

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
            'name': self.name,
            'connected': self._connected
        }

    def enable(self):
        """Enable the connection."""
        self._connection.enable()

    def disable(self):
        """Disable the connection."""
        self._connection.disable()

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the packet and wait for the response.

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        """
        out_packet = HsmsPacket(
            HsmsStreamFunctionHeader(self.get_next_system_counter(), function.stream, function.function,
                                     function.is_reply_required, self._settings.session_id),
            function.encode())

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        return self._connection.send_packet(out_packet)

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[secsgem.common.Packet]:
        """
        Send the packet and wait for the response.

        :param packet: packet to be sent
        :type packet: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.hsms.HsmsPacket`
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        out_packet = HsmsPacket(HsmsStreamFunctionHeader(system_id, function.stream, function.function, True,
                                                         self._settings.session_id),
                                function.encode())

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        if not self._connection.send_packet(out_packet):
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
        out_packet = HsmsPacket(HsmsStreamFunctionHeader(system, function.stream, function.function, False,
                                                         self._settings.session_id),
                                function.encode())

        self._communication_logger.info("> %s\n%s", out_packet, function, extra=self._get_log_extra())

        return self._connection.send_packet(out_packet)

    def send_select_req(self):
        """
        Send a Select Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsSelectReqHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())

        if not self._connection.send_packet(packet):
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
        packet = HsmsPacket(HsmsSelectRspHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())
        return self._connection.send_packet(packet)

    def send_linktest_req(self):
        """
        Send a Linktest Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsLinktestReqHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())

        if not self._connection.send_packet(packet):
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
        packet = HsmsPacket(HsmsLinktestRspHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())
        return self._connection.send_packet(packet)

    def send_deselect_req(self):
        """
        Send a Deselect Request to the remote host.

        :returns: System of the sent request
        :rtype: integer
        """
        system_id = self.get_next_system_counter()

        response_queue = self._get_queue_for_system(system_id)

        packet = HsmsPacket(HsmsDeselectReqHeader(system_id))
        self._communication_logger.info("> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
                                        extra=self._get_log_extra())

        if not self._connection.send_packet(packet):
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
        packet = HsmsPacket(HsmsDeselectRspHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())
        return self._connection.send_packet(packet)

    def send_reject_rsp(self, system_id, s_type, reason):
        """
        Send a Reject Response to the remote host.

        :param system_id: System of the request to reply for
        :type system_id: integer
        :param s_type: s_type of rejected message
        :type s_type: integer
        :param reason: reason for rejection
        :type reason: integer
        """
        packet = HsmsPacket(HsmsRejectReqHeader(system_id, s_type, reason))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())
        return self._connection.send_packet(packet)

    def send_separate_req(self):
        """Send a Separate Request to the remote host."""
        system_id = self.get_next_system_counter()

        packet = HsmsPacket(HsmsSeparateReqHeader(system_id))
        self._communication_logger.info(
            "> %s\n  %s", packet, HSMS_STYPES[packet.header.s_type],
            extra=self._get_log_extra())

        if not self._connection.send_packet(packet):
            return None

        return system_id

    # helpers

    def _get_log_extra(self):
        return {"address": self._settings.address,
                "port": self._settings.port,
                "session_id": self._settings.session_id,
                "remoteName": self._settings.name}
