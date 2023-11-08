#####################################################################
# communication_state_machine.py
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
"""State machine for communication state."""
from __future__ import annotations

import enum
import threading

import secsgem.common


class CommunicationState(enum.Enum):
    """States for connection state machine."""

    DISABLED = 0
    ENABLED = 1
    NOT_COMMUNICATING = 2
    HOST_INITIATED_CONNECT = 3
    WAIT_CR_FROM_HOST = 4
    EQUIPMENT_INITIATED_CONNECT = 5
    WAIT_DELAY = 6
    WAIT_CRA = 7
    COMMUNICATING = 8

class CommunicationStateMachine(secsgem.common.StateMachine):  # pylint: disable=too-many-instance-attributes
    """Communication state machine.

    Not going to HOST_INITIATED_CONNECT because two states at a time are not supported.
    There is a transistion to get out of EQUIPMENT_INITIATED_CONNECT when the HOST_INITIATED_CONNECT happens.
    """

    def __init__(self, settings: secsgem.common.Settings) -> None:
        """Initialize state machine.

        Args:
            settings: communication settings

        """
        super().__init__()

        self._settings = settings

        self.disabled = secsgem.common.State(
            CommunicationState.DISABLED,
            "DISABLED",
            initial=True)
        self.enabled = secsgem.common.State(
            CommunicationState.ENABLED,
            "ENABLED")
        self.not_communicating = secsgem.common.State(
            CommunicationState.NOT_COMMUNICATING,
            "NOT_COMMUNICATING",
            parent=self.enabled)
        self.host_initiated_connect = secsgem.common.State(
            CommunicationState.HOST_INITIATED_CONNECT,
            "HOST_INITIATED_CONNECT",
            parent=self.enabled)
        self.wait_cr_from_host = secsgem.common.State(
            CommunicationState.WAIT_CR_FROM_HOST,
            "WAIT_CR_FROM_HOST",
            parent=self.enabled)
        self.equipment_initiated_connect = secsgem.common.State(
            CommunicationState.EQUIPMENT_INITIATED_CONNECT,
            "EQUIPMENT_INITIATED_CONNECT",
            parent=self.enabled)
        self.wait_delay = secsgem.common.State(
            CommunicationState.WAIT_DELAY,
            "WAIT_DELAY",
            parent=self.enabled)
        self.wait_cra = secsgem.common.State(
            CommunicationState.WAIT_CRA,
            "WAIT_CRA",
            parent=self.enabled)
        self.communicating = secsgem.common.State(
            CommunicationState.COMMUNICATING,
            "COMMUNICATING",
            parent=self.enabled)

        # transition 1
        self._current_state: secsgem.common.State = self.disabled

        self._transitions: list[secsgem.common.Transition] = [
            secsgem.common.Transition("enable", self.disabled, self.not_communicating),  # 2 and 4
            secsgem.common.Transition("disable",
                [
                    self.enabled,
                    self.not_communicating,
                    self.communicating,
                    self.equipment_initiated_connect,
                    self.wait_delay,
                    self.wait_cra,
                    self.host_initiated_connect,
                    self.wait_cr_from_host,
                ],
                self.disabled),  # 3
            secsgem.common.Transition("select", self.not_communicating, self.wait_cra),  # 5
            secsgem.common.Transition("communicationreqfail", self.wait_cra, self.wait_delay),  # 6
            secsgem.common.Transition("delayexpired", self.wait_delay, self.wait_cra),  # 7
            secsgem.common.Transition("messagereceived", self.wait_delay, self.wait_cra),  # 8
            secsgem.common.Transition("s1f14received", self.wait_cra, self.communicating),  # 9
            secsgem.common.Transition("communicationfail", self.communicating, self.not_communicating),  # 14
            secsgem.common.Transition("s1f13received",
                [
                    self.wait_cr_from_host,
                    self.wait_delay,
                    self.wait_cra,
                ],
                self.communicating),  # 14
        ]

        self._wait_cra_timer: threading.Thread | None = None
        self._comm_delay_timer: threading.Thread | None = None

        self.wait_cra.events.enter.register(self._on_state_wait_cra)
        self.wait_delay.events.enter.register(self._on_state_wait_delay)
        self.wait_cra.events.leave.register(self._on_state_leave_wait_cra)
        self.wait_delay.events.leave.register(self._on_state_leave_wait_delay)

    def _on_state_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA.

        Args:
            data: event attributes

        """
        self._wait_cra_timer = threading.Timer(self._settings.timeouts.t3, self._on_wait_cra_timeout)
        self._wait_cra_timer.start()

    def _on_state_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY.

        Args:
            data: event attributes

        """
        self._comm_delay_timer = threading.Timer(self._settings.establish_communication_timeout,
                                                 self._on_wait_comm_delay_timeout)
        self._comm_delay_timer.start()

    def _on_state_leave_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA.

        Args:
            data: event attributes

        """
        if self._wait_cra_timer is not None:
            self._wait_cra_timer.cancel()

    def _on_state_leave_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY.

        Args:
            data: event attributes

        """
        if self._comm_delay_timer is not None:
            self._comm_delay_timer.cancel()

    def _on_wait_cra_timeout(self):
        """Linktest time timed out, so send linktest request."""
        self._perform_transition("communicationreqfail")

    def _on_wait_comm_delay_timeout(self):
        """Linktest time timed out, so send linktest request."""
        self._perform_transition("delayexpired")

    def enable(self) -> None:
        """Perform enable transition."""
        self._perform_transition("enable")

    def disable(self) -> None:
        """Perform disable transition."""
        self._perform_transition("disable")

    def select(self) -> None:
        """Perform select transition."""
        self._perform_transition("select")

    def messagereceived(self) -> None:
        """Perform messagereceived transition."""
        self._perform_transition("messagereceived")

    def s1f14received(self) -> None:
        """Perform s1f14received transition."""
        self._perform_transition("s1f14received")

    def communicationfail(self) -> None:
        """Perform communicationfail transition."""
        self._perform_transition("communicationfail")

    def s1f13received(self) -> None:
        """Perform s1f13received transition."""
        self._perform_transition("s1f13received")
