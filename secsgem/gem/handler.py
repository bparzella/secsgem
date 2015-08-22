#####################################################################
# handler.py
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
"""Handler for GEM commands. Used in combination with :class:`secsgem.HsmsHandler.HsmsConnectionManager`"""

import logging
import threading

from secsgem.common.fysom import Fysom
from secsgem.secs.handler import SecsHandler


class GemHandler(SecsHandler):
    """Baseclass for creating Host/Equipment models. This layer contains GEM functionality. Inherit from this class and override required functions.

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

    ceids = SecsHandler.ceids
    """Dictionary of available collection events, CEID is the key

    :param name: Name of the data value
    :type name: string
    :param CEID: Collection event the data value is used for
    :type CEID: integer
    """

    dvs = SecsHandler.dvs
    """Dictionary of available data values, DVID is the key

    :param name: Name of the collection event
    :type name: string
    :param dv: Data values available for collection event
    :type dv: list of integers
    """

    alarms = SecsHandler.alarms
    """Dictionary of available alarms, ALID is the key

    :param alarmText: Description of the alarm
    :type alarmText: string
    :param ceidOn: Collection event for activated alarm
    :type ceidOn: integer
    :param ceidOff: Collection event for deactivated alarm
    :type ceidOff: integer
    """

    rcmds = SecsHandler.rcmds
    """Dictionary of available remote commands, command is the key

    :param params: description of the parameters
    :type params: list of dictionary
    :param CEID: Collection events the remote command uses
    :type CEID: list of integers
    """

    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        SecsHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        # not going to HOST_INITIATED_CONNECT because fysom doesn't support two states. but there is a transistion to get out of EQUIPMENT_INITIATED_CONNECT when the HOST_INITIATED_CONNECT happens
        self.communicationState = Fysom({
            'initial': 'DISABLED',  # 1
            'events': [
                {'name': 'enable', 'src': 'DISABLED', 'dst': 'ENABLED'},  # 2
                {'name': 'disable', 'src': ['ENABLED', 'NOT_COMMUNICATING', 'COMMUNICATING', 'EQUIPMENT_INITIATED_CONNECT', 'WAIT_DELAY', 'WAIT_CRA', "HOST_INITIATED_CONNECT", "WAIT_CR_FROM_HOST"], 'dst': 'DISABLED'},  # 3
                {'name': 'select', 'src': 'NOT_COMMUNICATING', 'dst': 'EQUIPMENT_INITIATED_CONNECT'},  # 5
                {'name': 'communicationreqfail', 'src': 'WAIT_CRA', 'dst': 'WAIT_DELAY'},  # 6
                {'name': 'delayexpired', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 7
                {'name': 'messagereceived', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 8
                {'name': 's1f14received', 'src': 'WAIT_CRA', 'dst': 'COMMUNICATING'},  # 9
                {'name': 'communicationfail', 'src': 'COMMUNICATING', 'dst': 'NOT_COMMUNICATING'},  # 14
                {'name': 's1f13received', 'src': ['WAIT_CR_FROM_HOST', 'WAIT_DELAY', 'WAIT_CRA'], 'dst': 'COMMUNICATING'},  # 15 (WAIT_CR_FROM_HOST is running in background - AND state - so if s1f13 is received we go all communicating)
            ],
            'callbacks': {
                'onWAIT_CRA': self._on_state_wait_cra,
                'onWAIT_DELAY': self._on_state_wait_delay,
                'onleaveWAIT_CRA': self._on_state_leave_wait_cra,
                'onleaveWAIT_DELAY': self._on_state_leave_wait_delay,
                'onCOMMUNICATING': self._on_state_communicating,
                # 'onselect': self.onStateSelect,
            },
            'autoforward': [
                {'src': 'ENABLED', 'dst': 'NOT_COMMUNICATING'},  # 4
                {'src': 'EQUIPMENT_INITIATED_CONNECT', 'dst': 'WAIT_CRA'},  # 5
                {'src': 'HOST_INITIATED_CONNECT', 'dst': 'WAIT_CR_FROM_HOST'},  # 10
            ]
        })

        self.waitCRATimer = None
        self.commDelayTimer = None
        self.commDelayTimeout = 10

        self.reportIDCounter = 1000

        self.reportSubscriptions = {}

        self.register_callback(1, 1, self.s01f01_handler)
        self.register_callback(1, 13, self.s01f13_handler)
        self.register_callback(6, 11, self.s06f11_handler)
        self.register_callback(10, 1, self.s10f01_handler)

    def _serialize_data(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        data = SecsHandler._serialize_data(self)
        data.update({'communicationState': self.communicationState.current, 'commDelayTimeout': self.commDelayTimeout, 'reportIDCounter': self.reportIDCounter, 'reportSubscriptions': self.reportSubscriptions})
        return data

    def enable(self):
        """Enables the connection"""
        self.connection.enable()
        self.communicationState.enable()

        self.logger.info("Connection enabled")

    def disable(self):
        """Disables the connection"""
        self.connection.disable()
        self.communicationState.disable()

        self.logger.info("Connection disabled")

    def _on_hsms_packet_received(self, packet):
        """Packet received from hsms layer

        :param packet: received data packet
        :type packet: :class:`secsgem.HsmsPacket`
        """
        message = self.secs_decode(packet)

        if message is None:
            self.logger.info("< %s", packet)
        else:
            self.logger.info("< %s\n%s", packet, message)

        if self.communicationState.isstate('WAIT_CRA'):
            if packet.header.stream == 1 and packet.header.function == 13:
                if self.isHost:
                    self.send_stream_function(self.stream_function(1, 14)({"COMMACK": 1, "DATA": {}}))
                else:
                    self.send_stream_function(self.stream_function(1, 14)({"COMMACK": 1, "DATA": {"MDLN": "secsgem", "SOFTREV": "0.0.3"}}))

                self.communicationState.s1f13received()
            elif packet.header.stream == 1 and packet.header.function == 14:
                self.communicationState.s1f14received()
        elif self.communicationState.isstate('WAIT_DELAY'):
            pass
        elif self.communicationState.isstate('COMMUNICATING'):
            # check if callbacks available for this stream and function
            callback_index = "s" + str(packet.header.stream) + "f" + str(packet.header.function)
            if callback_index in self.callbacks:
                threading.Thread(target=self._run_callbacks, args=(callback_index, packet), name="secsgem_gemHandler_callback_{}".format(callback_index)).start()
            else:
                self._queue_packet(packet)

    def _on_hsms_select(self):
        """Selected received from hsms layer"""
        self.communicationState.select()

    def _on_wait_cra_timeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.communicationreqfail()

    def _on_wait_comm_delay_timeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.delayexpired()

    def _on_state_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_CRA")

        self.waitCRATimer = threading.Timer(self.connection.T3, self._on_wait_cra_timeout)
        self.waitCRATimer.start()

        if self.isHost:
            self.send_stream_function(self.stream_function(1, 13)())
        else:
            self.send_stream_function(self.stream_function(1, 13)("secsgem", "0.0.3"))

    def _on_state_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_DELAY")

        self.commDelayTimer = threading.Timer(self.commDelayTimeout, self._on_wait_comm_delay_timeout)
        self.commDelayTimer.start()

    def _on_state_leave_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        if self.waitCRATimer is not None:
            self.waitCRATimer.cancel()

    def _on_state_leave_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        if self.commDelayTimer is not None:
            self.commDelayTimer.cancel()

    def _on_state_communicating(self, _):
        """Connection state model changed to state COMMUNICATING

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> COMMUNICATING")

        self.fire_event("handler_communicating", {'handler': self}, True)

    def on_connection_closed(self, connection):
        """Connection was closed"""
        self.logger.info("Connection was closed")

        # call parent handlers
        SecsHandler.on_connection_closed(self, connection)

        # update communication state
        self.communicationState.communicationfail()

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
        for param in params:
            s2f41.PARAMS.append({"CPNAME": param[0], "CPVAL": param[1]})

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(s2f41))

    def send_process_program(self, ppid, ppbody):
        """Send a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        :param ppbody: Content of process program
        :type ppbody: string
        """
        # send remote command
        self.logger.info("Send process program {0}".format(ppid))

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 3)({"ppid": ppid, "ppbody": ppbody}))).ACKC7

    def request_process_program(self, ppid):
        """Request a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        """
        self.logger.info("Request process program {0}".format(ppid))

        # send remote command
        s7f6 = self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 5)(ppid)))
        return s7f6.PPID, s7f6.PPBODY

    def delete_process_programs(self, ppids):
        """Delete a list of process program

        :param ppids: Process programs to delete
        :type ppids: list of strings
        """
        self.logger.info("Delete process programs {0}".format(ppids))

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 17)(ppids))).ACKC7

    def get_process_program_list(self):
        """Get process program list
        """
        self.logger.info("Get process program list")

        # send remote command
        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 19)())).get()

    def s01f01_handler(self, handler, packet):
        """Callback handler for Stream 1, Function 1, Are You There

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        handler.send_response(self.stream_function(1, 2)(), packet.header.system)

    def s01f13_handler(self, handler, packet):
        """Callback handler for Stream 1, Function 13, Establish Communication Request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        handler.send_response(self.stream_function(1, 14)({"COMMACK": 0}), packet.header.system)

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
            report_dvs = self.reportSubscriptions[report.RPTID]
            report_values = report.V.get()

            values = []

            for i, s in enumerate(report_dvs):
                values.append({"dvid": s, "value": report_values[i], "name": self.get_dvid_name(s)})

            print values

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
