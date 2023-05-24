#####################################################################
# equipmenthandler.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
# pylint: disable=too-many-lines
"""Handler for GEM equipment."""
from datetime import datetime
import typing

from dateutil.tz import tzlocal

import secsgem.common
import secsgem.secs.variables
import secsgem.secs.data_items

from .status_variable import StatusVariable
from .alarm import Alarm
from .collection_event import CollectionEvent
from .collection_event_link import CollectionEventLink
from .collection_event_report import CollectionEventReport
from .data_value import DataValue
from .equipment_constant import EquipmentConstant
from .remote_command import RemoteCommand
from .handler import GemHandler


ECID_ESTABLISH_COMMUNICATIONS_TIMEOUT = 1
ECID_TIME_FORMAT = 2

SVID_CLOCK = 1001
SVID_CONTROL_STATE = 1002
SVID_EVENTS_ENABLED = 1003
SVID_ALARMS_ENABLED = 1004
SVID_ALARMS_SET = 1005

CEID_EQUIPMENT_OFFLINE = 1
CEID_CONTROL_STATE_LOCAL = 2
CEID_CONTROL_STATE_REMOTE = 3

CEID_CMD_START_DONE = 20
CEID_CMD_STOP_DONE = 21

RCMD_START = "START"
RCMD_STOP = "STOP"


class GemEquipmentHandler(GemHandler):  # pylint: disable=too-many-instance-attributes
    """Baseclass for creating equipment models. Inherit from this class and override required functions."""

    def __init__(self,
                 settings: secsgem.common.Settings,
                 initial_control_state: str = "ATTEMPT_ONLINE",
                 initial_online_control_state: str = "REMOTE"):
        """
        Initialize a gem equipment handler.

        :param connection: Base connection
        :type address: string
        :param initial_control_state: initial state for the control state model, one of ["EQUIPMENT_OFFLINE",
        "ATTEMPT_ONLINE", "HOST_OFFLINE", "ONLINE"]
        :type initial_control_state: string
        """
        super().__init__(settings)

        self._is_host = False

        self._initial_control_states = ["EQUIPMENT_OFFLINE", "ATTEMPT_ONLINE", "HOST_OFFLINE", "ONLINE"]
        self._initial_control_state = initial_control_state

        self._online_control_states = ["LOCAL", "REMOTE"]
        self._online_control_state = initial_online_control_state

        self._time_format = 1

        self._data_values: typing.Dict[typing.Union[int, str], DataValue] = {
        }

        self._status_variables: typing.Dict[typing.Union[int, str], StatusVariable] = {
            SVID_CLOCK: StatusVariable(SVID_CLOCK, "Clock", "", secsgem.secs.variables.String),
            SVID_CONTROL_STATE: StatusVariable(SVID_CONTROL_STATE, "ControlState", "", secsgem.secs.variables.Binary),
            SVID_EVENTS_ENABLED: StatusVariable(SVID_EVENTS_ENABLED, "EventsEnabled", "", secsgem.secs.variables.Array),
            SVID_ALARMS_ENABLED: StatusVariable(SVID_ALARMS_ENABLED, "AlarmsEnabled", "", secsgem.secs.variables.Array),
            SVID_ALARMS_SET: StatusVariable(SVID_ALARMS_SET, "AlarmsSet", "", secsgem.secs.variables.Array),
        }

        self._collection_events: typing.Dict[typing.Union[int, str], CollectionEvent] = {
            CEID_EQUIPMENT_OFFLINE: CollectionEvent(CEID_EQUIPMENT_OFFLINE, "EquipmentOffline", []),
            CEID_CONTROL_STATE_LOCAL: CollectionEvent(CEID_CONTROL_STATE_LOCAL, "ControlStateLocal", []),
            CEID_CONTROL_STATE_REMOTE: CollectionEvent(CEID_CONTROL_STATE_REMOTE, "ControlStateRemote", []),
            CEID_CMD_START_DONE: CollectionEvent(CEID_CMD_START_DONE, "CmdStartDone", []),
            CEID_CMD_STOP_DONE: CollectionEvent(CEID_CMD_STOP_DONE, "CmdStopDone", []),
        }

        self._equipment_constants: typing.Dict[typing.Union[int, str], EquipmentConstant] = {
            ECID_ESTABLISH_COMMUNICATIONS_TIMEOUT: EquipmentConstant(ECID_ESTABLISH_COMMUNICATIONS_TIMEOUT,
                                                                     "EstablishCommunicationsTimeout", 10, 120, 10,
                                                                     "sec", secsgem.secs.variables.I2),
            ECID_TIME_FORMAT: EquipmentConstant(ECID_TIME_FORMAT, "TimeFormat", 0, 2, 1, "", secsgem.secs.variables.I4),
        }

        self._alarms: typing.Dict[typing.Union[int, str], Alarm] = {
        }

        self._remote_commands: typing.Dict[typing.Union[int, str], RemoteCommand] = {
            RCMD_START: RemoteCommand(RCMD_START, "Start", [], CEID_CMD_START_DONE),
            RCMD_STOP: RemoteCommand(RCMD_STOP, "Stop", [], CEID_CMD_STOP_DONE),
        }

        self._registered_reports: typing.Dict[typing.Union[int, str], CollectionEventReport] = {}
        self._registered_collection_events: typing.Dict[typing.Union[int, str], CollectionEventLink] = {}

        self._control_state = secsgem.common.Fysom({
            'initial': "INIT",
            'events': [
                {'name': 'start', 'src': 'INIT', 'dst': 'CONTROL'},  # 1
                {'name': 'initial_offline', 'src': 'CONTROL', 'dst': 'OFFLINE'},  # 1
                {'name': 'initial_equipment_offline', 'src': 'OFFLINE', 'dst': 'EQUIPMENT_OFFLINE'},  # 2
                {'name': 'initial_attempt_online', 'src': 'OFFLINE', 'dst': 'ATTEMPT_ONLINE'},  # 2
                {'name': 'initial_host_offline', 'src': 'OFFLINE', 'dst': 'HOST_OFFLINE'},  # 2
                {'name': 'switch_online', 'src': 'EQUIPMENT_OFFLINE', 'dst': 'ATTEMPT_ONLINE'},  # 3
                {'name': 'attempt_online_fail_equipment_offline', 'src': 'ATTEMPT_ONLINE',
                 'dst': 'EQUIPMENT_OFFLINE'},  # 4
                {'name': 'attempt_online_fail_host_offline', 'src': 'ATTEMPT_ONLINE', 'dst': 'HOST_OFFLINE'},  # 4
                {'name': 'attempt_online_success', 'src': 'ATTEMPT_ONLINE', 'dst': 'ONLINE'},  # 5
                {'name': 'switch_offline', 'src': ["ONLINE", "ONLINE_LOCAL", "ONLINE_REMOTE"],
                 'dst': 'EQUIPMENT_OFFLINE'},  # 6, 12
                {'name': 'initial_online', 'src': 'CONTROL', 'dst': 'ONLINE'},  # 1
                {'name': 'initial_online_local', 'src': 'ONLINE', 'dst': 'ONLINE_LOCAL'},  # 7
                {'name': 'initial_online_remote', 'src': 'ONLINE', 'dst': 'ONLINE_REMOTE'},  # 7
                {'name': 'switch_online_local', 'src': 'ONLINE_REMOTE', 'dst': 'ONLINE_LOCAL'},  # 8
                {'name': 'switch_online_remote', 'src': 'ONLINE_LOCAL', 'dst': 'ONLINE_REMOTE'},  # 9
                {'name': 'remote_offline', 'src': ["ONLINE", "ONLINE_LOCAL", "ONLINE_REMOTE"],
                 'dst': 'HOST_OFFLINE'},  # 10
                {'name': 'remote_online', 'src': 'HOST_OFFLINE', 'dst': 'ONLINE'},  # 11
            ],
            'callbacks': {
                'onCONTROL': self._on_control_state_control,  # 1, forward online/offline depending on configuration
                'onOFFLINE': self._on_control_state_offline,  # 2, forward to configured offline state
                'onATTEMPT_ONLINE': self._on_control_state_attempt_online,  # 3, send S01E01
                'onONLINE': self._on_control_state_online,  # 7, forward to configured online state
                'oninitial_online_local': self._on_control_state_initial_online_local,  # 7, send collection event
                'onswitch_online_local': self._on_control_state_initial_online_local,  # 8, send collection event
                'oninitial_online_remote': self._on_control_state_initial_online_remote,  # 8, send collection event
                'onswitch_online_remote': self._on_control_state_initial_online_remote,  # 9, send collection event
            },
            'autoforward': [
                # {'src': 'OFFLINE', 'dst': 'EQUIPMENT_OFFLINE'},  # 2
                # {'src': 'EQUIPMENT_INITIATED_CONNECT', 'dst': 'WAIT_CRA'},  # 5
                # {'src': 'HOST_INITIATED_CONNECT', 'dst': 'WAIT_CR_FROM_HOST'},  # 10
            ]
        })

        self._control_state.start()  # type: ignore

    @property
    def control_state(self) -> secsgem.common.Fysom:
        """Get control state."""
        return self._control_state

    # control state model

    def _on_control_state_control(self, _):
        if self._initial_control_state == "ONLINE":
            self._control_state.initial_online()
        else:
            self._control_state.initial_offline()

    def _on_control_state_offline(self, _):
        if self._initial_control_state == "EQUIPMENT_OFFLINE":
            self._control_state.initial_equipment_offline()
        elif self._initial_control_state == "ATTEMPT_ONLINE":
            self._control_state.initial_attempt_online()
        elif self._initial_control_state == "HOST_OFFLINE":
            self._control_state.initial_host_offline()

    def _on_control_state_attempt_online(self, _):
        if not self._communication_state.isstate("COMMUNICATING"):
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

    def _on_control_state_online(self, _):
        if self._online_control_state == "REMOTE":
            self._control_state.initial_online_remote()
        else:
            self._control_state.initial_online_local()

    def _on_control_state_initial_online_local(self, _):
        self.trigger_collection_events([CEID_CONTROL_STATE_LOCAL])

    def _on_control_state_initial_online_remote(self, _):
        self.trigger_collection_events([CEID_CONTROL_STATE_REMOTE])

    def control_switch_online(self):
        """Operator switches to online control state."""
        self._control_state.switch_online()

    def control_switch_offline(self):
        """Operator switches to offline control state."""
        self._control_state.switch_offline()
        self.trigger_collection_events([CEID_EQUIPMENT_OFFLINE])

    def control_switch_online_local(self):
        """Operator switches to the local online control state."""
        self._control_state.switch_online_local()
        self._online_control_state = "LOCAL"

    def control_switch_online_remote(self):
        """Operator switches to the local online control state."""
        self._control_state.switch_online_remote()
        self._online_control_state = "REMOTE"

    def _on_s01f15(self, 
                   handler: secsgem.secs.SecsHandler, 
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 15, Request offline.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler, packet  # unused parameters

        oflack = 0

        if self._control_state.current in ["ONLINE", "ONLINE_LOCAL", "ONLINE_REMOTE"]:
            self._control_state.remote_offline()  # type: ignore
            self.trigger_collection_events([CEID_EQUIPMENT_OFFLINE])

        return self.stream_function(1, 16)(oflack)

    def _on_s01f17(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 17, Request online.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler, packet  # unused parameters

        onlack = 1

        if self._control_state.isstate("HOST_OFFLINE"):
            self._control_state.remote_online()  # type: ignore
            onlack = 0
        elif self._control_state.current in ["ONLINE", "ONLINE_LOCAL", "ONLINE_REMOTE"]:
            onlack = 2

        return self.stream_function(1, 18)(onlack)

    # data values

    @property
    def data_values(self) -> typing.Dict[typing.Union[int, str], DataValue]:
        """
        Get list of the data values.

        :returns: Data value list
        :rtype: list of :class:`secsgem.gem.DataValue`
        """
        return self._data_values

    def on_dv_value_request(self, 
                            data_value_id: secsgem.secs.variables.Base, 
                            data_value: DataValue) -> secsgem.secs.variables.Base:
        """
        Get the data value depending on its configuation.

        Override in inherited class to provide custom data value request handling.

        :param dvid: Id of the data value encoded in the corresponding type
        :type dvid: :class:`secsgem.secs.variables.Base`
        :param dv: The data value requested
        :type dv: :class:`secsgem.gem.DataValue`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        del data_value_id  # unused variable

        return data_value.value_type(data_value.value)

    def _get_dv_value(self, data_value: DataValue) -> secsgem.secs.variables.Base:
        """
        Get the data value depending on its configuation.

        :param dv: The data value requested
        :type dv: :class:`secsgem.gem.DataValue`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        if data_value.use_callback:
            return self.on_dv_value_request(data_value.id_type(data_value.dvid), data_value)

        return data_value.value_type(data_value.value)

    # status variables

    @property
    def status_variables(self) -> typing.Dict[typing.Union[int, str], StatusVariable]:
        """
        Get list of the status variables.

        :returns: Status variable list
        :rtype: list of :class:`secsgem.gem.StatusVariables`
        """
        return self._status_variables

    def on_sv_value_request(self,
                            svid: secsgem.secs.variables.Base,
                            status_variable: StatusVariable) -> secsgem.secs.variables.Base:
        """
        Get the status variable value depending on its configuation.

        Override in inherited class to provide custom status variable request handling.

        :param svid: Id of the status variable encoded in the corresponding type
        :type svid: :class:`secsgem.secs.variables.Base`
        :param sv: The status variable requested
        :type sv: :class:`secsgem.gem.StatusVariable`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        del svid  # unused variable

        return status_variable.value_type(status_variable.value)

    def _get_sv_value(self, status_variable: StatusVariable) -> secsgem.secs.variables.Base:
        """
        Get the status variable value depending on its configuation.

        :param sv: The status variable requested
        :type sv: :class:`secsgem.gem.StatusVariable`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        if status_variable.svid == SVID_CLOCK:
            result = status_variable.value_type(self._get_clock())
        elif status_variable.svid == SVID_CONTROL_STATE:
            result = status_variable.value_type(self._get_control_state_id())
        elif status_variable.svid == SVID_EVENTS_ENABLED:
            events = self._get_events_enabled()
            result = status_variable.value_type(secsgem.secs.data_items.SV, events)
        elif status_variable.svid == SVID_ALARMS_ENABLED:
            alarms = self._get_alarms_enabled()
            result = status_variable.value_type(secsgem.secs.data_items.SV, alarms)
        elif status_variable.svid == SVID_ALARMS_SET:
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
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 3, Equipment status request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for status_variable_id, status_variable in self._status_variables.items():
                responses.append(self._get_sv_value(status_variable))
        else:
            for status_variable_id in message:
                if status_variable_id not in self._status_variables:
                    responses.append(secsgem.secs.variables.Array(secsgem.secs.data_items.SV, []))
                else:
                    status_variable = self._status_variables[status_variable_id]
                    responses.append(self._get_sv_value(status_variable))

        return self.stream_function(1, 4)(responses)

    def _on_s01f11(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 11, SV namelist request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for status_variable_id, status_variable in self._status_variables.items():
                responses.append({"SVID": status_variable.svid,
                                  "SVNAME": status_variable.name,
                                  "UNITS": status_variable.unit})
        else:
            for status_variable_id in message:
                if status_variable_id not in self._status_variables:
                    responses.append({"SVID": status_variable_id, "SVNAME": "", "UNITS": ""})
                else:
                    status_variable = self._status_variables[status_variable_id]
                    responses.append({"SVID": status_variable.svid,
                                      "SVNAME": status_variable.name,
                                      "UNITS": status_variable.unit})

        return self.stream_function(1, 12)(responses)

    # collection events

    @property
    def collection_events(self) -> typing.Dict[typing.Union[int, str], CollectionEvent]:
        """
        Get list of the collection events.

        :returns: Collection event list
        :rtype: list of :class:`secsgem.gem.CollectionEvent`
        """
        return self._collection_events

    @property
    def registered_reports(self) -> typing.Dict[typing.Union[int, str], CollectionEventReport]:
        """
        Get list of the subscribed reports.

        :returns: Collection event report list
        :rtype: dictionary of subscribed reports
        """
        return self._registered_reports

    @property
    def registered_collection_events(self) -> typing.Dict[typing.Union[int, str], CollectionEventLink]:
        """
        Get list of the subscribed collection events.

        :returns: Collection event list
        :rtype: dictionary of :class:`secsgem.gem.CollectionEventLink`

        """
        return self._registered_collection_events

    def trigger_collection_events(self, ceids: typing.List[typing.Union[int, str]]):
        """
        Triggers the supplied collection events.

        :param ceids: List of collection events
        :type ceids: list of various
        """
        if not isinstance(ceids, list):
            ceids = [ceids]

        for ceid in ceids:
            if ceid in self._registered_collection_events:
                if self._registered_collection_events[ceid].enabled:
                    reports = self._build_collection_event(ceid)

                    self.send_and_waitfor_response(self.stream_function(6, 11)(
                        {"DATAID": 1, "CEID": ceid, "RPT": reports}))

    def _on_s02f33(self,  # noqa: MC0001
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 33, Define Report.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        # 0  = Accept
        # 1  = Denied. Insufficient space.
        # 2  = Denied. Invalid format.
        # 3  = Denied. At least one RPTID already defined.
        # 4  = Denied. At least VID does not exist.
        # >4 = Other errors
        drack = 0

        # pre check message for errors
        for report in message.DATA:
            if report.RPTID in self._registered_reports and len(report.VID) > 0:
                drack = 3
            else:
                for vid in report.VID:
                    if (vid not in self._data_values) and (vid not in self._status_variables):
                        drack = 4

        result = self.stream_function(2, 34)(drack)

        if drack != 0:
            return result

        # no data -> remove all reports and links
        if not message.DATA:
            self._registered_collection_events.clear()
            self._registered_reports.clear()

            return result

        for report in message.DATA:
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

    def _on_s02f35(self,  # noqa: MC0001
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 35, Link event report.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        # 0  = Accepted
        # 1  = Denied. Insufficient space
        # 2  = Denied. Invalid format
        # 3  = Denied. At least one CEID link already defined
        # 4  = Denied. At least one CEID does not exist
        # 5  = Denied. At least one RPTID does not exist
        # >5 = Other errors
        lrack = 0

        # pre check message for errors
        for event in message.DATA:
            if event.CEID.get() not in self._collection_events:
                lrack = 4
            for rptid in event.RPTID:
                if event.CEID.get() in self._registered_collection_events:
                    collection_event = self._registered_collection_events[event.CEID.get()]
                    if rptid.get() in collection_event.reports:
                        lrack = 3
                if rptid.get() not in self._registered_reports:
                    lrack = 5

        # pre check okay
        if lrack == 0:
            for event in message.DATA:
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
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Callback handler for Stream 2, Function 37, En-/Disable Event Report.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        # 0  = Accepted
        # 1  = Denied. At least one CEID does not exist
        erack = 0

        if not self._set_ce_state(message.CEED.get(), message.CEID.get()):
            erack = 1

        return self.stream_function(2, 38)(erack)

    def _on_s06f15(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Callback handler for Stream 6, Function 15, event report request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        ceid = message.get()

        reports = []

        if ceid in self._registered_collection_events:
            if self._registered_collection_events[ceid].enabled:
                reports = self._build_collection_event(ceid)

        return self.stream_function(6, 16)({"DATAID": 1, "CEID": ceid, "RPT": reports})

    def _set_ce_state(self, ceed: bool, ceids: typing.List[typing.Union[int, str]]) -> bool:
        """
        En-/Disable event reports for the supplied ceids (or all, if ceid is an empty list).

        :param ceed: Enable (True) or disable (False) event reports
        :type ceed: bool
        :param ceids: List of collection events
        :type ceids: list of integer
        :returns: True if all ceids were ok, False if illegal ceid was supplied
        :rtype: bool
        """
        result = True
        if not ceids:
            for ceid, collection_event in self._registered_collection_events.items():
                collection_event.enabled = ceed
        else:
            for ceid in ceids:
                if ceid in self._registered_collection_events:
                    self._registered_collection_events[ceid].enabled = ceed
                else:
                    result = False

        return result

    def _build_collection_event(self, ceid: typing.Union[int, str]):
        """
        Build reports for a collection event.

        :param ceid: collection event to build
        :type ceid: integer
        :returns: collection event data
        :rtype: array
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

    # equipment constants

    @property
    def equipment_constants(self) -> typing.Dict[typing.Union[int, str], EquipmentConstant]:
        """
        The list of the equipments contstants.

        :returns: Equipment constant list
        :rtype: list of :class:`secsgem.gem.EquipmentConstant`
        """
        return self._equipment_constants

    def on_ec_value_request(self,
                            equipment_constant_id: secsgem.secs.variables.Base,
                            equipment_constant: EquipmentConstant) -> secsgem.secs.variables.Base:
        """
        Get the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant request handling.

        :param ecid: Id of the equipment constant encoded in the corresponding type
        :type ecid: :class:`secsgem.secs.variables.Base`
        :param ec: The equipment constant requested
        :type ec: :class:`secsgem.gem.EquipmentConstant`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        del equipment_constant_id  # unused variable

        return equipment_constant.value_type(equipment_constant.value)

    def on_ec_value_update(self,
                           equipment_constant_id: secsgem.secs.variables.Base,
                           equipment_constant: EquipmentConstant, 
                           value: typing.Union[int, float]):
        """
        Set the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant update handling.

        :param ecid: Id of the equipment constant encoded in the corresponding type
        :type ecid: :class:`secsgem.secs.variables.Base`
        :param ec: The equipment constant to be updated
        :type ec: :class:`secsgem.gem.EquipmentConstant`
        :param value: The value encoded in the corresponding type
        :type value: :class:`secsgem.secs.variables.Base`
        """
        del equipment_constant_id  # unused variable

        equipment_constant.value = value

    def _get_ec_value(self, equipment_constant: EquipmentConstant) -> secsgem.secs.variables.Base:
        """
        Get the equipment constant value depending on its configuation.

        :param ec: The equipment requested
        :type ec: :class:`secsgem.gem.EquipmentConstant`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.Base`
        """
        if equipment_constant.ecid == ECID_ESTABLISH_COMMUNICATIONS_TIMEOUT:
            return equipment_constant.value_type(self._establish_communication_timeout)
        if equipment_constant.ecid == ECID_TIME_FORMAT:
            return equipment_constant.value_type(self._time_format)

        if equipment_constant.use_callback:
            return self.on_ec_value_request(equipment_constant.id_type(equipment_constant.ecid), equipment_constant)
        return equipment_constant.value_type(equipment_constant.value)

    def _set_ec_value(self, equipment_constant: EquipmentConstant, value: typing.Union[int, float]):
        """
        Get the equipment constant value depending on its configuation.

        :param ec: The equipment requested
        :type ec: :class:`secsgem.gem.EquipmentConstant`
        :param value: The value encoded in the corresponding type
        :type value: :class:`secsgem.secs.variables.Base`
        """
        if equipment_constant.ecid == ECID_ESTABLISH_COMMUNICATIONS_TIMEOUT:
            self._establish_communication_timeout = int(value)
        if equipment_constant.ecid == ECID_TIME_FORMAT:
            self._time_format = int(value)

        if equipment_constant.use_callback:
            self.on_ec_value_update(equipment_constant.id_type(equipment_constant.ecid), equipment_constant, value)
        else:
            equipment_constant.value = value

    def _on_s02f13(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 13, Equipment constant request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for equipment_constant_id, equipment_constant in self._equipment_constants.items():
                responses.append(self._get_ec_value(equipment_constant))
        else:
            for equipment_constant_id in message:
                if equipment_constant_id not in self._equipment_constants:
                    responses.append(secsgem.secs.variables.Array(secsgem.secs.data_items.ECV, []))
                else:
                    equipment_constant = self._equipment_constants[equipment_constant_id]
                    responses.append(self._get_ec_value(equipment_constant))

        return self.stream_function(2, 14)(responses)

    def _on_s02f15(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 15, Equipment constant send.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        eac = 0

        for equipment_constant in message:
            if equipment_constant.ECID not in self._equipment_constants:
                eac = 1
            else:
                constant = self.equipment_constants[equipment_constant.ECID.get()]

                if constant.min_value is not None:
                    if equipment_constant.ECV.get() < constant.min_value:
                        eac = 3

                if constant.max_value is not None:
                    if equipment_constant.ECV.get() > constant.max_value:
                        eac = 3

        if eac == 0:
            for equipment_constant in message:
                self._set_ec_value(self._equipment_constants[equipment_constant.ECID], equipment_constant.ECV.get())

        return self.stream_function(2, 16)(eac)

    def _on_s02f29(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 29, EC namelist request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for ecid, eq_constant in self._equipment_constants.items():
                responses.append({"ECID": eq_constant.ecid, "ECNAME": eq_constant.name,
                                  "ECMIN": eq_constant.min_value if eq_constant.min_value is not None else "",
                                  "ECMAX": eq_constant.max_value if eq_constant.max_value is not None else "",
                                  "ECDEF": eq_constant.default_value, "UNITS": eq_constant.unit})
        else:
            for ecid in message:
                if ecid not in self._equipment_constants:
                    responses.append({"ECID": ecid, "ECNAME": "", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""})
                else:
                    eq_constant = self._equipment_constants[ecid]
                    responses.append({"ECID": eq_constant.ecid, "ECNAME": eq_constant.name,
                                      "ECMIN": eq_constant.min_value if eq_constant.min_value is not None else "",
                                      "ECMAX": eq_constant.max_value if eq_constant.max_value is not None else "",
                                      "ECDEF": eq_constant.default_value, "UNITS": eq_constant.unit})

        return self.stream_function(2, 30)(responses)

    # alarms

    @property
    def alarms(self) -> typing.Dict[typing.Union[int, str], Alarm]:
        """
        Get the list of the alarms.

        :returns: Alarms list
        :rtype: list of :class:`secsgem.gem.Alarm`
        """
        return self._alarms

    def set_alarm(self, alid: typing.Union[int, str]):
        """
        Set the list of the alarms.

        :param alid: Alarm id
        :type alid: str/int
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
                    "ALTX": self.alarms[alid].text
                }))

        self.alarms[alid].set = True

        self.trigger_collection_events([self.alarms[alid].ce_on])

    def clear_alarm(self, alid: typing.Union[int, str]):
        """
        Clear the list of the alarms.

        :param alid: Alarm id
        :type alid: str/int
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
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 5, Function 3, Alarm en-/disabled.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        # 0  = Accepted
        # 1  = Error
        result = secsgem.secs.data_items.ACKC5.ACCEPTED

        alid = message.ALID.get()
        if alid not in self._alarms:
            result = secsgem.secs.data_items.ACKC5.ERROR
        else:
            self.alarms[alid].enabled = message.ALED.get() == secsgem.secs.data_items.ALED.ENABLE

        return self.stream_function(5, 4)(result)

    def _on_s05f05(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 5, Function 5, Alarm list.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        result = []

        alids = message.get()

        if len(alids) == 0:
            alids = list(self.alarms.keys())

        for alid in alids:
            result.append({"ALCD": self.alarms[alid].code |
                           (secsgem.secs.data_items.ALCD.ALARM_SET if self.alarms[alid].set else 0),
                           "ALID": alid,
                           "ALTX": self.alarms[alid].text})

        return self.stream_function(5, 6)(result)

    def _on_s05f07(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 5, Function 7, Enabled alarm list.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler, packet  # unused parameters

        result = []

        for alid in list(self.alarms.keys()):
            if self.alarms[alid].enabled:
                result.append({"ALCD": self.alarms[alid].code |
                               (secsgem.secs.data_items.ALCD.ALARM_SET if self.alarms[alid].set else 0),
                               "ALID": alid, "ALTX": self.alarms[alid].text})

        return self.stream_function(5, 8)(result)

    # remote commands

    @property
    def remote_commands(self) -> typing.Dict[typing.Union[int, str], RemoteCommand]:
        """
        Get list of the remote commands.

        :returns: Remote command list
        :rtype: list of :class:`secsgem.gem.RemoteCommand`
        """
        return self._remote_commands

    def _on_s02f41(self,
                   handler: secsgem.secs.SecsHandler,
                   packet: secsgem.common.Packet) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 2, Function 41, host command send.

        The remote command handing differs from usual stream function handling, because we send the ack with later
        completion first.
        Then we run the actual remote command callback and signal success with the matching collection event.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.secs.SecsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.common.Packet`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        rcmd_name = message.RCMD.get()
        rcmd_callback_name = "rcmd_" + rcmd_name

        if rcmd_name not in self._remote_commands:
            self._logger.info("remote command %s not registered", rcmd_name)
            return self.stream_function(2, 42)({"HCACK": secsgem.secs.data_items.HCACK.INVALID_COMMAND, "PARAMS": []})

        if rcmd_callback_name not in self._callback_handler:
            self._logger.warning("callback for remote command %s not available", rcmd_name)
            return self.stream_function(2, 42)({"HCACK": secsgem.secs.data_items.HCACK.INVALID_COMMAND, "PARAMS": []})

        for param in message.PARAMS:
            if param.CPNAME.get() not in self._remote_commands[rcmd_name].params:
                self._logger.warning("parameter %s for remote command %s not available", param.CPNAME.get(), rcmd_name)
                return self.stream_function(2, 42)({"HCACK": secsgem.secs.data_items.HCACK.PARAMETER_INVALID,
                                                    "PARAMS": []})

        self.send_response(self.stream_function(2, 42)({"HCACK": secsgem.secs.data_items.HCACK.ACK_FINISH_LATER,
                                                        "PARAMS": []}),
                           packet.header.system)

        callback = getattr(self._callback_handler, rcmd_callback_name)

        kwargs = {}
        for param in message.PARAMS.get():
            kwargs[param['CPNAME']] = param['CPVAL']

        callback(**kwargs)

        self.trigger_collection_events([self._remote_commands[rcmd_name].ce_finished])

        return None

    def _on_rcmd_START(self):  # noqa: N802
        self._logger.warning("remote command START not implemented, this is required for GEM compliance")

    def _on_rcmd_STOP(self):  # noqa: N802
        self._logger.warning("remote command STOP not implemented, this is required for GEM compliance")

    # helpers

    def _get_clock(self) -> str:
        """
        Get the clock depending on configured time format.

        :returns: time code
        :rtype: string
        """
        now = datetime.now(tzlocal())
        if self._time_format == 0:
            return now.strftime("%y%m%d%H%M%S")

        if self._time_format == 2:
            return now.isoformat()

        return now.strftime("%Y%m%d%H%M%S") + now.strftime("%f")[0:2]

    def _get_control_state_id(self) -> int:
        """
        Get id of the control state for the current control state.

        :returns: control state
        :rtype: integer
        """
        if self._control_state.isstate("EQUIPMENT_OFFLINE"):
            return 1
        if self._control_state.isstate("ATTEMPT_ONLINE"):
            return 2
        if self._control_state.isstate("HOST_OFFLINE"):
            return 3
        if self._control_state.isstate("ONLINE_LOCAL"):
            return 4
        if self._control_state.isstate("ONLINE_REMOTE"):
            return 5

        return -1

    def _get_events_enabled(self) -> typing.List[typing.Union[int, str]]:
        """
        List of the enabled collection events.

        :returns: collection event
        :rtype: list of various
        """
        enabled_ceid = []

        for ceid, collection_event in self._registered_collection_events.items():
            if collection_event.enabled:
                enabled_ceid.append(ceid)

        return enabled_ceid

    def _get_alarms_enabled(self) -> typing.List[typing.Union[int, str]]:
        """
        List of the enabled alarms.

        :returns: alarms
        :rtype: list of various
        """
        enabled_alarms = []

        for alid, alarm in self._alarms.items():
            if alarm.enabled:
                enabled_alarms.append(alid)

        return enabled_alarms

    def _get_alarms_set(self) -> typing.List[typing.Union[int, str]]:
        """
        List of the set alarms.

        :returns: alarms
        :rtype: list of various
        """
        set_alarms = []

        for alid, alarm in self._alarms.items():
            if alarm.set:
                set_alarms.append(alid)

        return set_alarms

    def on_connection_closed(self, connection):
        """Handle connection was closed event."""
        # call parent handlers
        super().on_connection_closed(connection)

        # update control state
        if self._control_state.current in ["ONLINE", "ONLINE_LOCAL", "ONLINE_REMOTE"]:
            self._control_state.switch_offline()

        if self._control_state.current in ["EQUIPMENT_OFFLINE"]:
            self._control_state.switch_online()
