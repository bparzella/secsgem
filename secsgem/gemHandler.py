#####################################################################
# gemHandler.py
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
"""Handler for GEM commands. Used in combination with :class:`secsgem.hsmsHandler.hsmsConnectionManager`"""


import logging
import threading

from fysom import Fysom

from secsHandler import secsHandler


class gemHandler(secsHandler):
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
    :type custom_connection_handler: :class:`secsgem.hsmsConnections.HsmsMultiPassiveServer`
    """

    ceids = secsHandler.ceids
    """Dictionary of available collection events, CEID is the key

    :param name: Name of the data value
    :type name: string
    :param CEID: Collection event the data value is used for
    :type CEID: integer
    """

    dvs = secsHandler.dvs
    """Dictionary of available data values, DVID is the key

    :param name: Name of the collection event
    :type name: string
    :param dv: Data values available for collection event
    :type dv: list of integers
    """

    alarms = secsHandler.alarms
    """Dictionary of available alarms, ALID is the key

    :param alarmText: Description of the alarm
    :type alarmText: string
    :param ceidOn: Collection event for activated alarm
    :type ceidOn: integer
    :param ceidOff: Collection event for deactivated alarm
    :type ceidOff: integer
    """

    rcmds = secsHandler.rcmds
    """Dictionary of available remote commands, command is the key

    :param params: description of the parameters
    :type params: list of dictionary
    :param CEID: Collection events the remote command uses
    :type CEID: list of integers
    """

    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        secsHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

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
                'onWAIT_CRA': self._onStateWaitCRA,
                'onWAIT_DELAY': self._onStateWaitDelay,
                'onleaveWAIT_CRA': self._onStateLeaveWaitCRA,
                'onleaveWAIT_DELAY': self._onStateLeaveWaitDelay,
                'onCOMMUNICATING': self._onStateCommunicating,
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

        self.registerCallback(1, 1, self.S1F1Handler)
        self.registerCallback(1, 13, self.S1F13Handler)
        self.registerCallback(6, 11, self.S6F11Handler)
        self.registerCallback(10, 1, self.S10F1Handler)

    def _serializeData(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        data = secsHandler._serializeData(self)
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

    def _onHsmsPacketReceived(self, packet):
        """Packet received from hsms layer

        :param packet: received data packet
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secsDecode(packet)

        if message is None:
            self.logger.info("< %s", packet)
        else:
            self.logger.info("< %s\n%s", packet, message)

        if self.communicationState.isstate('WAIT_CRA'):
            if packet.header.stream == 1 and packet.header.function == 13:
                if self.isHost:
                    self.sendStreamFunction(self.streamFunction(1, 14)({"COMMACK": 1, "DATA": {}}))
                else:
                    self.sendStreamFunction(self.streamFunction(1, 14)({"COMMACK": 1, "DATA": {"MDLN": "secsgem", "SOFTREV": "0.0.3"}}))

                self.communicationState.s1f13received()
            elif packet.header.stream == 1 and packet.header.function == 14:
                self.communicationState.s1f14received()
        elif self.communicationState.isstate('WAIT_DELAY'):
            pass
        elif self.communicationState.isstate('COMMUNICATING'):
            # check if callbacks available for this stream and function
            callback_index = "s" + str(packet.header.stream) + "f" + str(packet.header.function)
            if callback_index in self.callbacks:
                threading.Thread(target=self._runCallbacks, args=(callback_index, packet), name="secsgem_gemHandler_callback_{}".format(callback_index)).start()
            else:
                self._queuePacket(packet)

    def _onHsmsSelect(self):
        """Selected received from hsms layer"""
        self.communicationState.select()

    def _onWaitCRATimeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.communicationreqfail()

    def _onWaitCommDelayTimeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.delayexpired()

    def _onStateWaitCRA(self, data):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_CRA")

        self.waitCRATimer = threading.Timer(self.connection.T3, self._onWaitCRATimeout)
        self.waitCRATimer.start()

        if self.isHost:
            self.sendStreamFunction(self.streamFunction(1, 13)())
        else:
            self.sendStreamFunction(self.streamFunction(1, 13)("secsgem", "0.0.3"))

    def _onStateWaitDelay(self, data):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_DELAY")

        self.commDelayTimer = threading.Timer(self.commDelayTimeout, self._onWaitCommDelayTimeout)
        self.commDelayTimer.start()

    def _onStateLeaveWaitCRA(self, data):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        if self.waitCRATimer is not None:
            self.waitCRATimer.cancel()

    def _onStateLeaveWaitDelay(self, data):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        if self.commDelayTimer is not None:
            self.commDelayTimer.cancel()

    def _onStateCommunicating(self, data):
        """Connection state model changed to state COMMUNICATING

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> COMMUNICATING")

        self.fireEvent("HandlerCommunicating", {'handler': self}, True)

    def on_connection_closed(self):
        """Connection was closed"""
        self.logger.info("Connection was closed")

        # call parent handlers
        secsHandler.on_connection_closed(self)

        # update communication state
        self.communicationState.communicationfail()

    def clearCollectionEvents(self):
        """Clear all collection events"""
        self.logger.info("Clearing collection events")

        # clear subscribed reports
        self.reportSubscriptions = {}

        # disable all ceids
        self.disableCEIDs()

        # delete all reports
        self.disableCEIDReports()

    def subscribeCollectionEvent(self, ceid, dvs, report_id=None):
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
        self.sendAndWaitForResponse(self.streamFunction(2, 33)({"DATAID": 0, "DATA": [{"RPTID": report_id, "VID": dvs}]}))

        # link event report to collection event
        self.sendAndWaitForResponse(self.streamFunction(2, 35)({"DATAID": 0, "DATA": [{"CEID": ceid, "RPTID": [report_id]}]}))

        # enable collection event
        self.sendAndWaitForResponse(self.streamFunction(2, 37)({"CEED": True, "CEID": [ceid]}))

    def sendRemoteCommand(self, rcmd, params):
        """Send a remote command

        :param rcmd: Name of command
        :type rcmd: string
        :param params: DV IDs to add for collection event
        :type params: list of strings
        """
        self.logger.info("Send RCMD {0}".format(rcmd))

        s2f41 = self.streamFunction(2, 41)()
        s2f41.RCMD = rcmd
        for param in params:
            s2f41.PARAMS.append({"CPNAME": param[0], "CPVAL": param[1]})

        # send remote command
        return self.secsDecode(self.sendAndWaitForResponse(s2f41))

    def sendProcessProgram(self, ppid, ppbody):
        """Send a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        :param ppbody: Content of process program
        :type ppbody: string
        """
        # send remote command
        self.logger.info("Send process program {0}".format(ppid))

        return self.secsDecode(self.sendAndWaitForResponse(self.streamFunction(7, 3)({"ppid": ppid, "ppbody": ppbody}))).ACKC7

    def requestProcessProgram(self, ppid):
        """Request a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        """
        self.logger.info("Request process program {0}".format(ppid))

        # send remote command
        s7f6 = self.secsDecode(self.sendAndWaitForResponse(self.streamFunction(7, 5)(ppid)))
        return s7f6.PPID, s7f6.PPBODY

    def deleteProcessPrograms(self, ppids):
        """Delete a list of process program

        :param ppids: Process programs to delete
        :type ppids: list of strings
        """
        self.logger.info("Delete process programs {0}".format(ppids))

        # send remote command
        return self.secsDecode(self.sendAndWaitForResponse(self.streamFunction(7, 17)(ppids))).ACKC7

    def getProcessProgramList(self):
        """Get process program list
        """
        self.logger.info("Get process program list")

        # send remote command
        return self.secsDecode(self.sendAndWaitForResponse(self.streamFunction(7, 19)())).get()

    def S1F1Handler(self, handler, packet):
        """Callback handler for Stream 1, Function 1, Are You There

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsmsHandler.hsmsHandler
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        handler.sendResponse(self.streamFunction(1, 2)(), packet.header.system)

    def S1F13Handler(self, handler, packet):
        """Callback handler for Stream 1, Function 13, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsmsHandler.hsmsHandler
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        handler.sendResponse(self.streamFunction(1, 14)({"COMMACK": 0}), packet.header.system)

    def S6F11Handler(self, handler, packet):
        """Callback handler for Stream 6, Function 11, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsmsHandler.hsmsHandler
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secsDecode(packet)

        for report in message.RPT:
            report_dvs = self.reportSubscriptions[report.RPTID]
            report_values = report.V.get()

            values = []

            for i, s in enumerate(report_dvs):
                values.append({"dvid": s, "value": report_values[i], "name": self.getDVIDName(s)})

            print values

            data = {"ceid": message.CEID, "rptid": report.RPTID, "values": values, "name": self.getCEIDName(message.CEID), "handler": self.connection, 'peer': self}
            self.fireEvent("CollectionEventReceived", data)

        handler.sendResponse(self.streamFunction(6, 12)(0), packet.header.system)

    def S10F1Handler(self, handler, packet):
        """Callback handler for Stream 10, Function 1, Terminal Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsmsHandler.hsmsHandler
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        s10f1 = self.secsDecode(packet)

        handler.sendResponse(self.streamFunction(10, 2)(0), packet.header.system)

        self.fireEvent("TerminalReceived", {"text": s10f1.TEXT, "terminal": s10f1.TID, "handler": self.connection, 'peer': self})
