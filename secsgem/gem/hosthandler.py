#####################################################################
# hosthandler.py
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
"""Handler for GEM host."""
import collections
import typing

import secsgem.hsms
import secsgem.secs

from .handler import GemHandler


class GemHostHandler(GemHandler):
    """Baseclass for creating host models. Inherit from this class and override required functions."""

    def __init__(self, connection: secsgem.hsms.HsmsHandler):
        """
        Initialize a gem host handler.

        :param connection: Connection
        """
        GemHandler.__init__(self, connection)

        self.isHost = True

        self.reportSubscriptions: typing.Dict[typing.Union[int, str], typing.List[typing.Union[int, str]]] = {}

    def clear_collection_events(self) -> None:
        """Clear all collection events."""
        self.logger.info("Clearing collection events")

        # clear subscribed reports
        self.reportSubscriptions = {}

        # disable all ceids
        self.disable_ceids()

        # delete all reports
        self.disable_ceid_reports()

    def subscribe_collection_event(self,
                                   ceid: typing.Union[int, str],
                                   dvs: typing.List[typing.Union[int, str]],
                                   report_id: typing.Optional[typing.Union[int, str]] = None):
        """
        Subscribe to a collection event.

        :param ceid: ID of the collection event
        :type ceid: integer
        :param dvs: DV IDs to add for collection event
        :type dvs: list of integers
        :param report_id: optional - ID for report, autonumbering if None
        :type report_id: integer
        """
        self.logger.info("Subscribing to collection event %s", ceid)

        if report_id is None:
            report_id = self.reportIDCounter
            self.reportIDCounter += 1

        # note subscribed reports
        self.reportSubscriptions[report_id] = dvs

        # create report
        self.send_and_waitfor_response(self.stream_function(2, 33)(
            {"DATAID": 0, "DATA": [{"RPTID": report_id, "VID": dvs}]}))

        # link event report to collection event
        self.send_and_waitfor_response(self.stream_function(2, 35)(
            {"DATAID": 0, "DATA": [{"CEID": ceid, "RPTID": [report_id]}]}))

        # enable collection event
        self.send_and_waitfor_response(self.stream_function(2, 37)({"CEED": True, "CEID": [ceid]}))

    def send_remote_command(self,
                            rcmd: typing.Union[int, str],
                            params: typing.List[str]):
        """
        Send a remote command.

        :param rcmd: Name of command
        :type rcmd: string
        :param params: DV IDs to add for collection event
        :type params: list of strings
        """
        self.logger.info("Send RCMD %s", rcmd)

        s2f41 = self.stream_function(2, 41)()
        s2f41.RCMD = rcmd
        if isinstance(params, list):
            for param in params:
                s2f41.PARAMS.append({"CPNAME": param[0], "CPVAL": param[1]})
        elif isinstance(params, collections.OrderedDict):
            for param in params:
                s2f41.PARAMS.append({"CPNAME": param, "CPVAL": params[param]})

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(s2f41))

    def delete_process_programs(self,
                                ppids: typing.List[typing.Union[int, str]]):
        """
        Delete a list of process program.

        :param ppids: Process programs to delete
        :type ppids: list of strings
        """
        self.logger.info("Delete process programs %s", ppids)

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 17)(ppids))).get()

    def get_process_program_list(self) -> secsgem.secs.SecsStreamFunction:
        """Get process program list."""
        self.logger.info("Get process program list")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 19)())).get()

    def go_online(self) -> typing.Optional[str]:
        """Set control state to online."""
        self.logger.info("Go online")

        # send remote command
        resp = self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 17)()))
        if resp is None:
            return None

        return resp.get()

    def go_offline(self) -> typing.Optional[str]:
        """Set control state to offline."""
        self.logger.info("Go offline")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 15)())).get()

    def enable_alarm(self, alid: typing.Union[int, str]):
        """
        Enable alarm.

        :param alid: alarm id to enable
        :type alid: :class:`secsgem.secs.dataitems.ALID`
        """
        self.logger.info("Enable alarm %d", alid)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 3)(
            {"ALED": secsgem.secs.data_items.ALED.ENABLE, "ALID": alid}))).get()

    def disable_alarm(self, alid: typing.Union[int, str]):
        """
        Disable alarm.

        :param alid: alarm id to disable
        :type alid: :class:`secsgem.secs.dataitems.ALID`
        """
        self.logger.info("Disable alarm %d", alid)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 3)(
            {"ALED": secsgem.secs.data_items.ALED.DISABLE, "ALID": alid}))).get()

    def list_alarms(self, 
                    alids: typing.Optional[typing.List[typing.Union[int, str]]] = None):
        """
        List alarms.

        :param alids: alarms to list details for
        :type alids: array of int/str
        """
        if alids is None:
            alids = []
            self.logger.info("List all alarms")
        else:
            self.logger.info("List alarms %s", alids)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 5)(alids))).get()

    def list_enabled_alarms(self):
        """List enabled alarms."""
        self.logger.info("List all enabled alarms")

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 7)())).get()

    def _on_alarm_received(self, handler, ALID, ALCD, ALTX):
        del handler, ALID, ALCD, ALTX  # unused variables
        return secsgem.secs.data_items.ACKC5.ACCEPTED

    def _on_s05f01(self, 
                   handler: secsgem.secs.SecsHandler, 
                   packet: secsgem.hsms.HsmsPacket) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 5, Function 1, Alarm request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.HsmsPacket`
        """
        s5f1 = self.secs_decode(packet)

        result = self._callback_handler.alarm_received(handler, s5f1.ALID, s5f1.ALCD, s5f1.ALTX)

        self.events.fire("alarm_received", {"code": s5f1.ALCD, "alid": s5f1.ALID, "text": s5f1.ALTX,
                                            "handler": self.connection, 'peer': self})

        return self.stream_function(5, 2)(result)

    def _on_s06f11(self, 
                   handler: secsgem.secs.SecsHandler, 
                   packet: secsgem.hsms.HsmsPacket) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 6, Function 11, Establish Communication Request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.HsmsPacket`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        for report in message.RPT:
            report_dvs = self.reportSubscriptions[report.RPTID.get()]
            report_values = report.V.get()

            values = []

            for i, s in enumerate(report_dvs):
                values.append({"dvid": s, "value": report_values[i], "name": self.get_dvid_name(s)})

            data = {"ceid": message.CEID, "rptid": report.RPTID, "values": values,
                    "name": self.get_ceid_name(message.CEID), "handler": self.connection, 'peer': self}
            self.events.fire("collection_event_received", data)

        return self.stream_function(6, 12)(0)

    def _on_terminal_received(self, handler, TID, TEXT):
        del handler, TID, TEXT  # unused variables
        return secsgem.secs.data_items.ACKC10.ACCEPTED

    def _on_s10f01(self, 
                   handler: secsgem.secs.SecsHandler, 
                   packet: secsgem.hsms.HsmsPacket) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 10, Function 1, Terminal Request.

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.HsmsPacket`
        """
        s10f1 = self.secs_decode(packet)

        result = self._callback_handler.terminal_received(handler, s10f1.TID, s10f1.TEXT)
        self.events.fire("terminal_received", {"text": s10f1.TEXT, "terminal": s10f1.TID, "handler": self.connection,
                                               'peer': self})

        return self.stream_function(10, 2)(result)
