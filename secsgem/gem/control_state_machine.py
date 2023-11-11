#####################################################################
# control_state_machine.py
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
"""State machine for control state."""
from __future__ import annotations

import enum

import secsgem.common


class ControlState(enum.Enum):
    """States for control state machine."""

    INIT = 0
    CONTROL = 1
    OFFLINE = 2
    EQUIPMENT_OFFLINE = 3
    ATTEMPT_ONLINE = 4
    HOST_OFFLINE = 5
    ONLINE = 6
    ONLINE_LOCAL = 7
    ONLINE_REMOTE = 8


class ControlStateMachine(secsgem.common.StateMachine):  # pylint: disable=too-many-instance-attributes
    """Control state machine."""

    def __init__(
        self,
        initial_control_state: str = "ATTEMPT_ONLINE",
        initial_online_control_state: str = "REMOTE",
    ) -> None:
        """Initialize state machine."""
        super().__init__()

        self._initial_control_states = ["EQUIPMENT_OFFLINE", "ATTEMPT_ONLINE", "HOST_OFFLINE", "ONLINE"]
        self._initial_control_state = initial_control_state

        self._online_control_states = ["LOCAL", "REMOTE"]
        self._online_control_state = initial_online_control_state

        self.init = secsgem.common.State(
            ControlState.INIT,
            "INIT",
            initial=True)
        self.control = secsgem.common.State(
            ControlState.CONTROL,
            "CONTROL")
        self.offline = secsgem.common.State(
            ControlState.OFFLINE,
            "OFFLINE")
        self.equipment_offline = secsgem.common.State(
            ControlState.EQUIPMENT_OFFLINE,
            "EQUIPMENT_OFFLINE")
        self.attempt_online = secsgem.common.State(
            ControlState.ATTEMPT_ONLINE,
            "ATTEMPT_ONLINE")
        self.host_offline = secsgem.common.State(
            ControlState.HOST_OFFLINE,
            "HOST_OFFLINE")
        self.online = secsgem.common.State(
            ControlState.ONLINE,
            "ONLINE")
        self.online_local = secsgem.common.State(
            ControlState.ONLINE_LOCAL,
            "ONLINE_LOCAL")
        self.online_remote = secsgem.common.State(
            ControlState.ONLINE_REMOTE,
            "ONLINE_REMOTE")

        # transition 1
        self._current_state: secsgem.common.State = self.init

        self._transitions: list[secsgem.common.Transition] = [
                secsgem.common.Transition(
                    "start",
                    self.init,
                    self.control),  # 1
                secsgem.common.Transition(
                    "initial_offline",
                    self.control,
                    self.offline),  # 1
                secsgem.common.Transition(
                    "initial_equipment_offline",
                    self.offline,
                    self.equipment_offline),  # 2
                secsgem.common.Transition(
                    "initial_attempt_online",
                    self.offline,
                    self.attempt_online),  # 2
                secsgem.common.Transition(
                    "initial_host_offline",
                    self.offline,
                    self.host_offline),  # 2
                secsgem.common.Transition(
                    "switch_online",
                    self.equipment_offline,
                    self.attempt_online),  # 3
                secsgem.common.Transition(
                    "attempt_online_fail_equipment_offline",
                    self.attempt_online,
                    self.equipment_offline),  # 4
                secsgem.common.Transition(
                    "attempt_online_fail_host_offline",
                    self.attempt_online,
                    self.host_offline),  # 4
                secsgem.common.Transition(
                    "attempt_online_success",
                    self.attempt_online,
                    self.online),  # 5
                secsgem.common.Transition(
                    "switch_offline",
                    [self.online, self.online_local, self.online_remote],
                    self.equipment_offline),  # 6, 12
                secsgem.common.Transition(
                    "initial_online",
                    self.control,
                    self.online),  # 1
                secsgem.common.Transition(
                    "initial_online_local",
                    self.online,
                    self.online_local),  # 7
                secsgem.common.Transition(
                    "initial_online_remote",
                    self.online,
                    self.online_remote),  # 7
                secsgem.common.Transition(
                    "switch_online_local",
                    self.online_remote,
                    self.online_local),  # 8
                secsgem.common.Transition(
                    "switch_online_remote",
                    self.online_local,
                    self.online_remote),  # 9
                secsgem.common.Transition(
                    "remote_offline",
                    [self.online, self.online_local, self.online_remote],
                    self.host_offline),  # 10
                secsgem.common.Transition(
                    "remote_online",
                    self.host_offline,
                    self.online),  # 11
        ]

        # 1, forward online/offline depending on configuration
        self.control.events.enter.register(self._on_control_state_control)

        # 2, forward to configured offline state
        self.offline.events.enter.register(self._on_control_state_offline)

        # 7, forward to configured online state
        self.online.events.enter.register(self._on_control_state_online)

    def _on_control_state_control(self, _):
        if self._initial_control_state == "ONLINE":
            self._perform_transition("initial_online")
        else:
            self._perform_transition("initial_offline")

    def _on_control_state_offline(self, _):
        if self._initial_control_state == "EQUIPMENT_OFFLINE":
            self._perform_transition("initial_equipment_offline")
        elif self._initial_control_state == "ATTEMPT_ONLINE":
            self._perform_transition("initial_attempt_online")
        elif self._initial_control_state == "HOST_OFFLINE":
            self._perform_transition("initial_host_offline")

    def _on_control_state_online(self, _):
        if self._online_control_state == "REMOTE":
            self._perform_transition("initial_online_remote")
        else:
            self._perform_transition("initial_online_local")

    def start(self) -> None:
        """Perform start transition."""
        self._perform_transition("start")

    def attempt_online_fail_host_offline(self) -> None:
        """Perform attempt_online_fail_host_offline transition."""
        self._perform_transition("attempt_online_fail_host_offline")

    def attempt_online_success(self) -> None:
        """Perform attempt_online_success transition."""
        self._perform_transition("attempt_online_success")

    def switch_online(self) -> None:
        """Perform switch_online transition."""
        self._perform_transition("switch_online")

    def switch_offline(self) -> None:
        """Perform switch_offline transition."""
        self._perform_transition("switch_offline")

    def switch_online_local(self) -> None:
        """Perform switch_online_local transition."""
        self._perform_transition("switch_online_local")
        self._online_control_state = "LOCAL"

    def switch_online_remote(self) -> None:
        """Perform switch_online_remote transition."""
        self._perform_transition("switch_online_remote")
        self._online_control_state = "REMOTE"

    def remote_offline(self) -> None:
        """Perform remote_offline transition."""
        self._perform_transition("remote_offline")

    def remote_online(self) -> None:
        """Perform remote_online transition."""
        self._perform_transition("remote_online")
