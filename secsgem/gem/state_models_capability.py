#####################################################################
# state_models_capability.py
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
"""State Models capability."""
from __future__ import annotations

import typing

import secsgem.common

from .capability import Capability
from .collection_event import CollectionEventId
from .communication_state_machine import CommunicationState
from .control_state_machine import ControlState, ControlStateMachine
from .handler import GemHandler

if typing.TYPE_CHECKING:
    import secsgem.secs


class StateModelsCapability(GemHandler, Capability):
    """State Models capability."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize capability."""
        super().__init__(*args, **kwargs)

        self._control_state = ControlStateMachine(self._initial_control_state, self._initial_online_control_state)

        # 3, send S01E01
        self._control_state.attempt_online.events.enter.register(self._on_control_state_attempt_online)

        # 7, send collection event
        self._control_state.transition("initial_online_local").events.called.register(
            self._on_control_state_initial_online_local,
        )

        # 8, send collection event
        self._control_state.transition("switch_online_local").events.called.register(
            self._on_control_state_initial_online_local,
        )

        # 8, send collection event
        self._control_state.transition("initial_online_remote").events.called.register(
            self._on_control_state_initial_online_remote,
        )

        # 9, send collection event
        self._control_state.transition("switch_online_remote").events.called.register(
            self._on_control_state_initial_online_remote,
        )

        self._control_state.start()

    @property
    def control_state(self) -> ControlStateMachine:
        """Get control state."""
        return self._control_state

    def _on_control_state_attempt_online(self, _):
        if self._communication_state.current != CommunicationState.COMMUNICATING:
            self._control_state.attempt_online_fail_host_offline()
            return

        response = self.are_you_there()

        if response is None:
            self._control_state.attempt_online_fail_host_offline()
            return

        if response.header.stream != 1 or response.header.function != 2:
            self._control_state.attempt_online_fail_host_offline()
            return

        self._control_state.attempt_online_success()

    def _on_control_state_initial_online_local(self, _):
        self.trigger_collection_events([CollectionEventId.CONTROL_STATE_LOCAL.value])

    def _on_control_state_initial_online_remote(self, _):
        self.trigger_collection_events([CollectionEventId.CONTROL_STATE_REMOTE.value])

    def control_switch_online(self):
        """Operator switches to online control state."""
        self._control_state.switch_online()

    def control_switch_offline(self):
        """Operator switches to offline control state."""
        self._control_state.switch_offline()
        self.trigger_collection_events([CollectionEventId.EQUIPMENT_OFFLINE.value])

    def control_switch_online_local(self):
        """Operator switches to the local online control state."""
        self._control_state.switch_online_local()

    def control_switch_online_remote(self):
        """Operator switches to the local online control state."""
        self._control_state.switch_online_remote()

    def _on_s01f15(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 15, Request offline.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        oflack = 0

        if self._control_state.current in [ControlState.ONLINE, ControlState.ONLINE_LOCAL, ControlState.ONLINE_REMOTE]:
            self._control_state.remote_offline()
            self.trigger_collection_events([CollectionEventId.EQUIPMENT_OFFLINE.value])

        return self.stream_function(1, 16)(oflack)

    def _on_s01f17(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 17, Request online.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        onlack = 1

        if self._control_state.current == ControlState.HOST_OFFLINE:
            self._control_state.remote_online()
            onlack = 0
        elif self._control_state.current in [ControlState.ONLINE,
                                             ControlState.ONLINE_LOCAL,
                                             ControlState.ONLINE_REMOTE]:
            onlack = 2

        return self.stream_function(1, 18)(onlack)

    def _get_control_state_id(self) -> int:
        """Get id of the control state for the current control state.

        :returns: control state
        :rtype: integer
        """
        if self._control_state.current == ControlState.EQUIPMENT_OFFLINE:
            return 1
        if self._control_state.current == ControlState.ATTEMPT_ONLINE:
            return 2
        if self._control_state.current == ControlState.HOST_OFFLINE:
            return 3
        if self._control_state.current == ControlState.ONLINE_LOCAL:
            return 4
        if self._control_state.current == ControlState.ONLINE_REMOTE:
            return 5

        return -1
