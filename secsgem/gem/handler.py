#####################################################################
# handler.py
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
"""Handler for GEM commands."""
from __future__ import annotations

import logging
import threading
import typing

import secsgem.common
import secsgem.secs

from .communication_state_machine import CommunicationState, CommunicationStateMachine


class GemHandler(secsgem.secs.SecsHandler):  # pylint: disable=too-many-instance-attributes
    """Baseclass for creating Host/Equipment models. This layer contains GEM functionality."""

    def __init__(self, settings: secsgem.common.Settings):
        """Initialize a gem handler.

        Inherit from this class and override required functions.

        Args:
            settings: communication settings

        """
        super().__init__(settings)
        self._protocol.events.communicating += self._on_communicating

        self._mdln = "secsgem"  #: model number returned by S01E13/14
        self._softrev = "0.2.0"  #: software version returned by S01E13/14

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._is_host = True

        self._communication_state = CommunicationStateMachine(self.settings)
        self._communication_state.wait_cra.events.enter.register(self._on_state_wait_cra)
        self._communication_state.communicating.events.enter.register(self._on_state_communicating)

        self._report_id_counter = 1000

        self._wait_event_list: list[threading.Event] = []

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__} {self.serialize_data()}"

    @property
    def communication_state(self) -> CommunicationStateMachine:
        """Get the communication state model."""
        return self._communication_state

    def serialize_data(self) -> dict[str, typing.Any]:
        """Get serialized data.

        Returns:
            data to serialize for this object

        """
        data = self.protocol.serialize_data()
        data.update({"communicationState": self._communication_state.current,
                     "commDelayTimeout": self.settings.establish_communication_timeout,
                     "reportIDCounter": self._report_id_counter})
        return data

    def enable(self) -> None:
        """Enable the connection."""
        self._communication_state.enable()
        self.protocol.enable()

        self._logger.info("Connection enabled")

    def disable(self) -> None:
        """Disable the connection."""
        self.protocol.disable()
        self._communication_state.disable()

        self._logger.info("Connection disabled")

    def _on_message_received(self, data: dict[str, typing.Any]):
        """Message received from protocol layer.

        Args:
            data: received event data

        """
        message = data["message"]
        if self._communication_state.current == CommunicationState.WAIT_CRA:
            if message.header.stream == 1 and message.header.function == 13:
                if self._is_host:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                                                    "MDLN": []}),
                                       message.header.system)
                else:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                                                    "MDLN": [self._mdln, self._softrev]}),
                                       message.header.system)

                self._communication_state.s1f13received()
            elif message.header.stream == 1 and message.header.function == 14:
                self._communication_state.s1f14received()
        elif self._communication_state.current == CommunicationState.WAIT_DELAY:
            pass
        elif self._communication_state.current == CommunicationState.COMMUNICATING:
            self._handle_stream_function(message)

    def _on_communicating(self, _):
        """Selected received from hsms layer."""
        self._communication_state.select()

    def _on_state_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA.

        Args:
            data: event attributes

        """
        if self._is_host:
            self.send_stream_function(self.stream_function(1, 13)())
        else:
            self.send_stream_function(self.stream_function(1, 13)([self._mdln, self._softrev]))

    def _on_state_communicating(self, _):
        """Connection state model changed to state COMMUNICATING.

        Args:
            data: event attributes

        """
        self.events.fire("handler_communicating", {"handler": self})

        for event in self._wait_event_list:
            event.set()

    def on_connection_closed(self, _):
        """Handle connection was closed event."""
        self._logger.info("Connection was closed")

        if self._communication_state.current == CommunicationState.COMMUNICATING:
            # update communication state
            self._communication_state.communicationfail()

    def on_commack_requested(self) -> int:
        """Get the acknowledgement code for the connection request.

        override to accept or deny connection request

        Returns:
            0 when connection is accepted, 1 when connection is denied

        """
        return 0

    def send_process_program(self,
                             ppid: int | str,
                             ppbody: str):
        """Send a process program.

        Args:
            ppid: Transferred process programs ID
            ppbody: Content of process program

        """
        # send remote command
        self._logger.info("Send process program %s", ppid)

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(7, 3)(
            {"PPID": ppid, "PPBODY": ppbody}))).get()

    def request_process_program(self,
                                ppid: int | str) -> tuple[int | str, str]:
        """Request a process program.

        ppid: Transferred process programs ID

        """
        self._logger.info("Request process program %s", ppid)

        # send remote command
        s7f6 = self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(7, 5)(ppid)))
        return s7f6.PPID.get(), s7f6.PPBODY.get()

    def waitfor_communicating(self, timeout: float | None = None) -> bool:
        """Wait until connection gets into communicating state. Returns immediately if state is communicating.

        Args:
            timeout: seconds to wait before aborting

        Returns:
            True if state is communicating, False if timed out

        """
        event = threading.Event()
        self._wait_event_list.append(event)

        if self._communication_state.current == CommunicationState.COMMUNICATING:
            self._wait_event_list.remove(event)
            return True

        result = event.wait(timeout)

        self._wait_event_list.remove(event)

        return result

    def _on_s01f01(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 1, Are You There.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        if self._is_host:
            return self.stream_function(1, 2)()

        return self.stream_function(1, 2)([self._mdln, self._softrev])

    def _on_s01f13(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 13, Establish Communication Request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        if self._is_host:
            return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": []})

        return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                            "MDLN": [self._mdln, self._softrev]})
