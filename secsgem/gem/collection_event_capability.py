#####################################################################
# collection_event_capability.py
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
"""Event Notification (collection events) capability."""
from __future__ import annotations

import threading

import secsgem.common
import secsgem.secs

from .capability import Capability
from .collection_event import CollectionEvent, CollectionEventId
from .collection_event_link import CollectionEventLink
from .collection_event_report import CollectionEventReport
from .handler import GemHandler


class CollectionEventCapability(GemHandler, Capability):
    """Event Notification (collection events) capability on GEM equipment."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize capability."""
        super().__init__(*args, **kwargs)

        self._collection_events: dict[int | str | CollectionEventId, CollectionEvent] = {
            CollectionEventId.EQUIPMENT_OFFLINE.value: CollectionEvent(
                CollectionEventId.EQUIPMENT_OFFLINE,
                "EquipmentOffline",
                []),
            CollectionEventId.CONTROL_STATE_LOCAL.value: CollectionEvent(
                CollectionEventId.CONTROL_STATE_LOCAL,
                "ControlStateLocal",
                []),
            CollectionEventId.CONTROL_STATE_REMOTE.value: CollectionEvent(
                CollectionEventId.CONTROL_STATE_REMOTE,
                "ControlStateRemote",
                []),
            CollectionEventId.CMD_START_DONE.value: CollectionEvent(
                CollectionEventId.CMD_START_DONE,
                "CmdStartDone",
                []),
            CollectionEventId.CMD_STOP_DONE.value: CollectionEvent(
                CollectionEventId.CMD_STOP_DONE,
                "CmdStopDone",
                []),
        }

        self._registered_reports: dict[int | str, CollectionEventReport] = {}
        self._registered_collection_events: dict[int | str, CollectionEventLink] = {}

    @property
    def collection_events(self) -> dict[int | str | CollectionEventId, CollectionEvent]:
        """Get list of the collection events.

        Returns:
            Collection event list

        """
        return self._collection_events

    @property
    def registered_reports(self) -> dict[int | str, CollectionEventReport]:
        """Get list of the subscribed reports.

        Returns:
            Collection event report list

        """
        return self._registered_reports

    @property
    def registered_collection_events(self) -> dict[int | str, CollectionEventLink]:
        """Get list of the subscribed collection events.

        Returns:
            Collection event list

        """
        return self._registered_collection_events

    def _get_events_enabled(self) -> list[int | str]:
        """List of the enabled collection events.

        :returns: collection event
        :rtype: list of various
        """
        enabled_ceid = []

        for ceid, collection_event in self._registered_collection_events.items():
            if collection_event.enabled:
                enabled_ceid.append(ceid)

        return enabled_ceid

    def trigger_collection_events(self, ceids: list[int | str | CollectionEventId]):
        """Triggers the supplied collection events.

        Args:
            ceids: List of collection events

        """
        def _ce_sender():
            nonlocal ceids
            if not isinstance(ceids, list):
                ceids = [ceids]

            for ceid in ceids:
                if isinstance(ceid, CollectionEventId):
                    ceid = ceid.value

                if ceid in self._registered_collection_events and self._registered_collection_events[ceid].enabled:
                    reports = self._build_collection_event(ceid)

                    self.send_and_waitfor_response(self.stream_function(6, 11)(
                        {"DATAID": 1, "CEID": ceid, "RPT": reports}))

        threading.Thread(target=_ce_sender, daemon=True).start()

    def _on_s02f33(self,  # noqa: C901, pylint: disable=too-many-branches
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 2, Function 33, Define Report.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        drack = secsgem.secs.data_items.DRACK.ACK

        # pre check message for errors
        for report in function.DATA:
            if report.RPTID in self._registered_reports and len(report.VID) > 0:
                drack = secsgem.secs.data_items.DRACK.RPTID_REDEFINED
            else:
                for vid in report.VID:
                    if (vid not in self._data_values) and (vid not in self._status_variables):
                        drack = secsgem.secs.data_items.DRACK.VID_UNKNOWN

        result = self.stream_function(2, 34)(drack)

        if drack != 0:
            return result

        # no data -> remove all reports and links
        if not function.DATA:
            self._registered_collection_events.clear()
            self._registered_reports.clear()

            return result

        for report in function.DATA:
            # no vids -> remove this reports and links
            if not report.VID:
                # remove report from linked collection events
                for collection_event in list(self._registered_collection_events):
                    if report.RPTID in self._registered_collection_events[collection_event].reports:
                        self._registered_collection_events[collection_event].reports.remove(report.RPTID)
                        # remove collection event link if no collection events present
                        if not self._registered_collection_events[collection_event].reports:
                            del self._registered_collection_events[collection_event]
                # remove report
                if report.RPTID in self._registered_reports:
                    del self._registered_reports[report.RPTID]
            else:
                # add report
                self._registered_reports[report.RPTID] = CollectionEventReport(report.RPTID, report.VID)

        return result

    def _on_s02f35(self,  # noqa: C901, pylint: disable=too-many-branches
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 2, Function 35, Link event report.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        lrack = secsgem.secs.data_items.LRACK.ACK

        # pre check message for errors
        for event in function.DATA:
            if event.CEID.get() not in self._collection_events:
                lrack = secsgem.secs.data_items.LRACK.CEID_UNKNOWN
            for rptid in event.RPTID:
                if event.CEID.get() in self._registered_collection_events:
                    collection_event = self._registered_collection_events[event.CEID.get()]
                    if rptid.get() in collection_event.reports:
                        lrack = secsgem.secs.data_items.LRACK.CEID_LINKED
                if rptid.get() not in self._registered_reports:
                    lrack = secsgem.secs.data_items.LRACK.RPTID_UNKNOWN

        # pre check okay
        if lrack == 0:
            for event in function.DATA:
                # no report ids, remove all links for collection event
                if not event.RPTID:
                    if event.CEID.get() in self._registered_collection_events:
                        del self._registered_collection_events[event.CEID.get()]
                else:
                    if event.CEID.get() in self._registered_collection_events:
                        collection_event = self._registered_collection_events[event.CEID.get()]
                        for rptid in event.RPTID.get():
                            collection_event.reports.append(rptid)
                    else:
                        self._registered_collection_events[event.CEID.get()] = \
                            CollectionEventLink(self._collection_events[event.CEID.get()], event.RPTID.get())

        return self.stream_function(2, 36)(lrack)

    def _on_s02f37(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Callback handler for Stream 2, Function 37, En-/Disable Event Report.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        erack = secsgem.secs.data_items.ERACK.ACCEPTED

        if not self._set_ce_state(function.CEED.get(), function.CEID.get()):
            erack = secsgem.secs.data_items.ERACK.CEID_UNKNOWN

        return self.stream_function(2, 38)(erack)

    def _on_s06f15(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Callback handler for Stream 6, Function 15, event report request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        ceid = function.get()

        reports = []

        if ceid in self._registered_collection_events and self._registered_collection_events[ceid].enabled:
            reports = self._build_collection_event(ceid)

        return self.stream_function(6, 16)({"DATAID": 1, "CEID": ceid, "RPT": reports})

    def _set_ce_state(self, ceed: bool, ceids: list[int | str]) -> bool:
        """En-/Disable event reports for the supplied ceids (or all, if ceid is an empty list).

        Args:
            ceed: Enable (True) or disable (False) event reports
            ceids: List of collection events

        Returns:
            True if all ceids were ok, False if illegal ceid was supplied

        """
        result = True
        if not ceids:
            for collection_event in self._registered_collection_events.values():
                collection_event.enabled = ceed
        else:
            for ceid in ceids:
                if ceid in self._registered_collection_events:
                    self._registered_collection_events[ceid].enabled = ceed
                else:
                    result = False

        return result

    def _build_collection_event(self, ceid: int | str):
        """Build reports for a collection event.

        Args:
            ceid: collection event to build

        Returns:
            collection event data

        """
        reports = []

        for rptid in self._registered_collection_events[ceid].reports:
            report = self._registered_reports[rptid]
            variables = []
            for var in report.vars:
                if var in self._status_variables:
                    value = self._get_sv_value(self._status_variables[var])
                    variables.append(value)
                elif var in self._data_values:
                    value = self._get_dv_value(self._data_values[var])
                    variables.append(value)

            reports.append({"RPTID": rptid, "V": variables})

        return reports

    def get_ceid_name(self, ceid: int | str) -> str:
        """Get the name of a collection event.

        Args:
            ceid: ID of collection event

        Returns:
            Name of the event or empty string if not found

        """
        if ceid in self._collection_events:
            return self._collection_events[ceid].name

        return ""
