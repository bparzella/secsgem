#####################################################################
# hosthandler.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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

from ..secs.dataitems import ALED, ACKC5, ACKC10
from .handler import GemHandler
from collections import OrderedDict


class GemHostHandler(GemHandler):
    """Baseclass for creating host models. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        GemHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.isHost = True

        self.reportSubscriptions = {}

    def clear_collection_events(self):
        """Clear all collection events"""
        self.logger.info("Clearing collection events")

        # clear subscribed reports
        self.reportSubscriptions = {}

        # disable all ceids
        self.disable_ceids()

        # delete all reports
        self.disable_ceid_reports()

    def subscribe_collection_event(self, ceid, dvs, report_id=None):
        """Subscribe to a collection event

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
        self.send_and_waitfor_response(self.stream_function(2, 33)({"DATAID": 0, "DATA": [{"RPTID": report_id, "VID": dvs}]}))

        # link event report to collection event
        self.send_and_waitfor_response(self.stream_function(2, 35)({"DATAID": 0, "DATA": [{"CEID": ceid, "RPTID": [report_id]}]}))

        # enable collection event
        self.send_and_waitfor_response(self.stream_function(2, 37)({"CEED": True, "CEID": [ceid]}))

    def send_remote_command(self, rcmd, params):
        """Send a remote command

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
        elif isinstance(params, OrderedDict):
            for param in params:
                s2f41.PARAMS.append({"CPNAME": param, "CPVAL": params[param]})

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(s2f41))

    def delete_process_programs(self, ppids):
        """Delete a list of process program

        :param ppids: Process programs to delete
        :type ppids: list of strings
        """
        self.logger.info("Delete process programs %s", ppids)

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 17)(ppids))).get()

    def get_process_program_list(self):
        """Get process program list"""
        self.logger.info("Get process program list")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 19)())).get()

    def go_online(self):
        """Set control state to online"""
        self.logger.info("Go online")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 17)())).get()

    def go_offline(self):
        """Set control state to offline"""
        self.logger.info("Go offline")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 15)())).get()

    def enable_alarm(self, alid):
        """Enable alarm

        :param alid: alarm id to enable
        :type alid: :class:`secsgem.secs.dataitems.ALID`
        """
        self.logger.info("Enable alarm %d", alid)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 3)({"ALED": ALED.ENABLE, "ALID": alid}))).get()

    def disable_alarm(self, alid):
        """Disable alarm

        :param alid: alarm id to disable
        :type alid: :class:`secsgem.secs.dataitems.ALID`
        """
        self.logger.info("Disable alarm %d", alid)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 3)({"ALED": ALED.DISABLE, "ALID": alid}))).get()

    def list_alarms(self, alids=None):
        """List alarms

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
        """List enabled alarms"""
        self.logger.info("List all enabled alarms")
            
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(5, 7)())).get()

    def _on_alarm_received(self, handler, ALID, ALCD, ALTX):
        del handler, ALID, ALCD, ALTX  # unused variables
        return ACKC5.ACCEPTED

    def _on_s05f01(self, handler, packet):
        """Callback handler for Stream 5, Function 1, Alarm request

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        s5f1 = self.secs_decode(packet)

        result = self._callback_handler.alarm_received(handler, s5f1.ALID, s5f1.ALCD, s5f1.ALTX)

        self.events.fire("alarm_received", {"code": s5f1.ALCD, "alid": s5f1.ALID, "text": s5f1.ALTX, "handler": self.connection, 'peer': self})

        return self.stream_function(5, 2)(result)
        
    def _on_s06f11(self, handler, packet):
        """Callback handler for Stream 6, Function 11, Establish Communication Request

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        del handler  # unused parameters

        message = self.secs_decode(packet)

        for report in message.RPT:
            report_dvs = self.reportSubscriptions[report.RPTID.get()]
            report_values = report.V.get()

            values = []

            for i, s in enumerate(report_dvs):
                values.append({"dvid": s, "value": report_values[i], "name": self.get_dvid_name(s)})

            data = {"ceid": message.CEID, "rptid": report.RPTID, "values": values, "name": self.get_ceid_name(message.CEID), \
                "handler": self.connection, 'peer': self}
            self.events.fire("collection_event_received", data)

        return self.stream_function(6, 12)(0)

    def _on_terminal_received(self, handler, TID, TEXT):
        del handler, TID, TEXT  # unused variables
        return ACKC10.ACCEPTED

    def _on_s10f01(self, handler, packet):
        """Callback handler for Stream 10, Function 1, Terminal Request

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        s10f1 = self.secs_decode(packet)

        result = self._callback_handler.terminal_received(handler, s10f1.TID, s10f1.TEXT)
        self.events.fire("terminal_received", {"text": s10f1.TEXT, "terminal": s10f1.TID, "handler": self.connection, 'peer': self})

        return self.stream_function(10, 2)(result)
