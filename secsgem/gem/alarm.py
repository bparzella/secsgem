#####################################################################
# alarm.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
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
"""Wrapper for GEM alarm."""
from __future__ import annotations

import typing

import secsgem.secs


class Alarm:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Alarm definition."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        alid: str | int,
        name: str,
        text: str,
        code: int,
        ce_on: str | int,
        ce_off: str | int,
        **kwargs
    ):
        """Initialize an alarm.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Args:
            alid: ID of the alarm
            name: long name of the alarm
            text: alarm text
            code: alarm code
            ce_on: collection event for alarm set
            ce_off: collection event for alarm cleared
            **kwargs: additional attributes for object

        """
        self.alid = alid
        self.name = name
        self.text = text
        self.code = code
        self.ce_on = ce_on
        self.ce_off = ce_off
        self.enabled = False
        self.set = False

        self.id_type: type[secsgem.secs.variables.Base]

        if isinstance(self.alid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)


class AlarmMixin(secsgem.secs.SecsHandler):
    """Mixin for GEM alarms on equipment."""

    if typing.TYPE_CHECKING:
        def trigger_collection_events(self, ceids: list[int | str]):
            """Triggers the supplied collection events.

            Args:
                ceids: List of collection events

            """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize mixin."""
        super().__init__(*args, **kwargs)

        self._alarms: dict[int | str, Alarm] = {
        }

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
