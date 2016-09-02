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

from ..gem.handler import GemHandler
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
    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        GemHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

        self.isHost = True

        self.reportSubscriptions = {}

        self.register_callback(6, 11, self.s06f11_handler)
        self.register_callback(10, 1, self.s10f01_handler)

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
        self.logger.info("Subscribing to collection event {0}".format(ceid))

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
        self.logger.info("Send RCMD {0}".format(rcmd))

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
        self.logger.info("Delete process programs {0}".format(ppids))

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 17)(ppids))).get()

    def get_process_program_list(self):
        """Get process program list
        """
        self.logger.info("Get process program list")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 19)())).get()

    def go_online(self):
        """Set control state to online
        """
        self.logger.info("Go online")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 17)())).get()

    def go_offline(self):
        """Set control state to offline
        """
        self.logger.info("Go offline")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(1, 15)())).get()

    def s06f11_handler(self, handler, packet):
        """Callback handler for Stream 6, Function 11, Establish Communication Request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        for report in message.RPT:
            report_dvs = self.reportSubscriptions[report.RPTID.get()]
            report_values = report.V.get()

            values = []

            for i, s in enumerate(report_dvs):
                values.append({"dvid": s, "value": report_values[i], "name": self.get_dvid_name(s)})

            data = {"ceid": message.CEID, "rptid": report.RPTID, "values": values, "name": self.get_ceid_name(message.CEID), "handler": self.connection, 'peer': self}
            self.fire_event("collection_event_received", data)

        handler.send_response(self.stream_function(6, 12)(0), packet.header.system)

    def s10f01_handler(self, handler, packet):
        """Callback handler for Stream 10, Function 1, Terminal Request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        s10f1 = self.secs_decode(packet)

        handler.send_response(self.stream_function(10, 2)(0), packet.header.system)

        self.fire_event("terminal_received", {"text": s10f1.TEXT, "terminal": s10f1.TID, "handler": self.connection, 'peer': self})
