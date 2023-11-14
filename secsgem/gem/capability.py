#####################################################################
# capability.py
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
"""Capability base class."""
from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import secsgem.secs

    from .alarm import Alarm
    from .collection_event import CollectionEventId
    from .data_value import DataValue
    from .status_variable import StatusVariable


class Capability(abc.ABC):  # pylint: disable=too-few-public-methods
    """Capability base class for GEM equipment."""

    @property
    @abc.abstractmethod
    def _initial_control_state(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _initial_online_control_state(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _alarms(self) -> dict[int | str, Alarm]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _status_variables(self) -> dict[int | str, StatusVariable]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _data_values(self) -> dict[int | str, DataValue]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _time_format(self) -> int:
        raise NotImplementedError

    @_time_format.setter
    @abc.abstractmethod
    def _time_format(self, value: int):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_sv_value(self, status_variable: StatusVariable) -> secsgem.secs.variables.Base:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_dv_value(self, data_value: DataValue) -> secsgem.secs.variables.Base:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_control_state_id(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_events_enabled(self) -> list[int | str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_alarms_enabled(self) -> list[int | str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_alarms_set(self) -> list[int | str]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_clock(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def trigger_collection_events(self, ceids: list[int | str | CollectionEventId]):
        """Triggers the supplied collection events.

        Args:
            ceids: List of collection events

        """
        raise NotImplementedError
