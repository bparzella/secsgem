#####################################################################
# equipmenthandler.py
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
"""Handler for GEM equipment."""
from __future__ import annotations

import typing

import secsgem.common
import secsgem.secs.data_items

from .alarm_capability import AlarmCapability
from .clock_capability import ClockCapability
from .collection_event_capability import CollectionEventCapability
from .control_state_machine import ControlState
from .data_value_capability import DataValueCapability
from .equipment_constants_capability import EquipmentConstantsCapability
from .handler import GemHandler
from .remote_control_capability import RemoteControlCapability
from .state_models_capability import StateModelsCapability
from .status_data_collection_capability import StatusDataCollectionCapability

if typing.TYPE_CHECKING:
    import secsgem.secs.variables


class GemEquipmentHandler(  # pylint: disable=too-many-ancestors
    AlarmCapability,
    ClockCapability,
    DataValueCapability,
    EquipmentConstantsCapability,
    RemoteControlCapability,
    StateModelsCapability,
    CollectionEventCapability,
    StatusDataCollectionCapability,
    GemHandler):
    """Baseclass for creating equipment models. Inherit from this class and override required functions."""

    def __init__(self,
                 settings: secsgem.common.Settings,
                 initial_control_state: str = "ATTEMPT_ONLINE",
                 initial_online_control_state: str = "REMOTE"):
        """Initialize a gem equipment handler.

        Args:
            settings: communication layer settings
            initial_control_state: initial state for the control state model, one of ["EQUIPMENT_OFFLINE",
            "ATTEMPT_ONLINE", "HOST_OFFLINE", "ONLINE"]
            initial_online_control_state: initial state for online control state model

        """
        self.__initial_control_state = initial_control_state
        self.__initial_online_control_state = initial_online_control_state

        super().__init__(settings)

        self._is_host = False

    @property
    def _initial_control_state(self) -> str:
        return self.__initial_control_state

    @property
    def _initial_online_control_state(self) -> str:
        return self.__initial_online_control_state

    def on_connection_closed(self, connection):
        """Handle connection was closed event."""
        # call parent handlers
        super().on_connection_closed(connection)

        # update control state
        if self._control_state.current in [ControlState.ONLINE, ControlState.ONLINE_LOCAL, ControlState.ONLINE_REMOTE]:
            self._control_state.switch_offline()

        if self._control_state.current == ControlState.EQUIPMENT_OFFLINE:
            self._control_state.switch_online()
