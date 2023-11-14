#####################################################################
# alarm_capability.py
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
"""Alarm Management capability."""
from __future__ import annotations

import typing

import secsgem.secs

from .capability import Capability
from .handler import GemHandler

if typing.TYPE_CHECKING:
    from .alarm import Alarm


class AlarmCapability(GemHandler, Capability):
    """Alarm Management capability for GEM."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize capability."""
        super().__init__(*args, **kwargs)

        self.__alarms: dict[int | str, Alarm] = {
        }

    @property
    def _alarms(self) -> dict[int | str, Alarm]:
        return self.__alarms

    @property
    def alarms(self) -> dict[int | str, Alarm]:
        """Get the list of the alarms.

        Returns:
            Alarms list

        """
        return self._alarms

    def set_alarm(self, alid: int | str):
        """Set the list of the alarms.

        Args:
            alid: Alarm id

        """
        if alid not in self.alarms:
            raise ValueError(f"Unknown alarm id {alid}")

        if self.alarms[alid].set:
            return

        if self.alarms[alid].enabled:
            self.send_and_waitfor_response(self.stream_function(5, 1)(
                {
                    "ALCD": self.alarms[alid].code | secsgem.secs.data_items.ALCD.ALARM_SET,
                    "ALID": alid,
                    "ALTX": self.alarms[alid].text,
                }))

        self.alarms[alid].set = True

        self.trigger_collection_events([self.alarms[alid].ce_on])

    def clear_alarm(self, alid: int | str):
        """Clear the list of the alarms.

        Args:
            alid: Alarm id

        """
        if alid not in self.alarms:
            raise ValueError(f"Unknown alarm id {alid}")

        if not self.alarms[alid].set:
            return

        if self.alarms[alid].enabled:
            self.send_and_waitfor_response(self.stream_function(5, 1)({"ALCD": self.alarms[alid].code,
                                                                       "ALID": alid, "ALTX": self.alarms[alid].text}))

        self.alarms[alid].set = False

        self.trigger_collection_events([self.alarms[alid].ce_off])

    def _on_s05f03(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 5, Function 3, Alarm en-/disabled.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        result = secsgem.secs.data_items.ACKC5.ACCEPTED

        alid = function.ALID.get()
        if alid not in self._alarms:
            result = secsgem.secs.data_items.ACKC5.ERROR
        else:
            self.alarms[alid].enabled = function.ALED.get() == secsgem.secs.data_items.ALED.ENABLE

        return self.stream_function(5, 4)(result)

    def _on_s05f05(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 5, Function 5, Alarm list.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        alids = function.get()

        if len(alids) == 0:
            alids = list(self.alarms.keys())

        result = [{
            "ALCD": self.alarms[alid].code | (secsgem.secs.data_items.ALCD.ALARM_SET if self.alarms[alid].set else 0),
            "ALID": alid,
            "ALTX": self.alarms[alid].text,
        } for alid in alids]

        return self.stream_function(5, 6)(result)

    def _on_s05f07(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 5, Function 7, Enabled alarm list.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        result = [{
            "ALCD": self.alarms[alid].code | (secsgem.secs.data_items.ALCD.ALARM_SET if self.alarms[alid].set else 0),
            "ALID": alid,
            "ALTX": self.alarms[alid].text,
        } for alid in list(self.alarms.keys()) if self.alarms[alid].enabled]

        return self.stream_function(5, 8)(result)

    def _get_alarms_enabled(self) -> list[int | str]:
        """List of the enabled alarms.

        :returns: alarms
        :rtype: list of various
        """
        enabled_alarms = []

        for alid, alarm in self._alarms.items():
            if alarm.enabled:
                enabled_alarms.append(alid)

        return enabled_alarms

    def _get_alarms_set(self) -> list[int | str]:
        """List of the set alarms.

        :returns: alarms
        :rtype: list of various
        """
        set_alarms = []

        for alid, alarm in self._alarms.items():
            if alarm.set:
                set_alarms.append(alid)

        return set_alarms
