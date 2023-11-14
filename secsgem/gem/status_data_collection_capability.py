#####################################################################
# status_data_collection_capability.py
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
"""Status Data Collection capability."""
from __future__ import annotations

import secsgem.secs

from .capability import Capability
from .handler import GemHandler
from .status_variable import StatusVariable, StatusVariableId


class StatusDataCollectionCapability(GemHandler, Capability):
    """Status Data Collection capability on GEM equipment."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize capability."""
        super().__init__(*args, **kwargs)

        self.__status_variables: dict[int | str, StatusVariable] = {
            StatusVariableId.CLOCK.value: StatusVariable(
                StatusVariableId.CLOCK,
                "Clock",
                "",
                secsgem.secs.variables.String),
            StatusVariableId.CONTROL_STATE.value: StatusVariable(
                StatusVariableId.CONTROL_STATE,
                "ControlState",
                "",
                secsgem.secs.variables.Binary),
            StatusVariableId.EVENTS_ENABLED.value: StatusVariable(
                StatusVariableId.EVENTS_ENABLED,
                "EventsEnabled",
                "",
                secsgem.secs.variables.Array),
            StatusVariableId.ALARMS_ENABLED.value: StatusVariable(
                StatusVariableId.ALARMS_ENABLED,
                "AlarmsEnabled",
                "",
                secsgem.secs.variables.Array),
            StatusVariableId.ALARMS_SET.value: StatusVariable(
                StatusVariableId.ALARMS_SET,
                "AlarmsSet",
                "",
                secsgem.secs.variables.Array),
        }

    @property
    def _status_variables(self) -> dict[int | str, StatusVariable]:
        return self.__status_variables

    @property
    def status_variables(self) -> dict[int | str, StatusVariable]:
        """Get list of the status variables.

        Returns:
            Status variable list

        """
        return self._status_variables

    def on_sv_value_request(self,
                            svid: secsgem.secs.variables.Base,
                            status_variable: StatusVariable) -> secsgem.secs.variables.Base:
        """Get the status variable value depending on its configuation.

        Override in inherited class to provide custom status variable request handling.

        Args:
            svid: Id of the status variable encoded in the corresponding type
            status_variable: The status variable requested

        Returns:
            The value encoded in the corresponding type

        """
        del svid  # unused variable

        return status_variable.value_type(status_variable.value)

    def _get_sv_value(self, status_variable: StatusVariable) -> secsgem.secs.variables.Base:
        """Get the status variable value depending on its configuation.

        Args:
            status_variable: The status variable requested

        Returns:
            The value encoded in the corresponding type

        """
        if status_variable.svid == StatusVariableId.CLOCK.value:
            result = status_variable.value_type(self._get_clock())
        elif status_variable.svid == StatusVariableId.CONTROL_STATE.value:
            result = status_variable.value_type(self._get_control_state_id())
        elif status_variable.svid == StatusVariableId.EVENTS_ENABLED.value:
            events = self._get_events_enabled()
            result = status_variable.value_type(secsgem.secs.data_items.SV, events)
        elif status_variable.svid == StatusVariableId.ALARMS_ENABLED.value:
            alarms = self._get_alarms_enabled()
            result = status_variable.value_type(secsgem.secs.data_items.SV, alarms)
        elif status_variable.svid == StatusVariableId.ALARMS_SET.value:
            alarms = self._get_alarms_set()
            result = status_variable.value_type(secsgem.secs.data_items.SV, alarms)
        else:
            if status_variable.use_callback:
                result = self.on_sv_value_request(status_variable.id_type(status_variable.svid), status_variable)
            else:
                result = status_variable.value_type(status_variable.value)

        return result

    def _on_s01f03(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 3, Equipment status request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        responses = []

        if len(function) == 0:
            responses = [self._get_sv_value(status_variable) for status_variable in self._status_variables.values()]
        else:
            for status_variable_id in function:
                if status_variable_id not in self._status_variables:
                    responses.append(secsgem.secs.variables.Array(secsgem.secs.data_items.SV, []))
                else:
                    status_variable = self._status_variables[status_variable_id]
                    responses.append(self._get_sv_value(status_variable))

        return self.stream_function(1, 4)(responses)

    def _on_s01f11(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 1, Function 11, SV namelist request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        responses = []

        if len(function) == 0:
            responses = [{
                "SVID": status_variable.svid,
                "SVNAME": status_variable.name,
                "UNITS": status_variable.unit,
            } for status_variable in self._status_variables.values()]
        else:
            for status_variable_id in function:
                if status_variable_id not in self._status_variables:
                    responses.append({"SVID": status_variable_id, "SVNAME": "", "UNITS": ""})
                else:
                    status_variable = self._status_variables[status_variable_id]
                    responses.append({"SVID": status_variable.svid,
                                      "SVNAME": status_variable.name,
                                      "UNITS": status_variable.unit})

        return self.stream_function(1, 12)(responses)
