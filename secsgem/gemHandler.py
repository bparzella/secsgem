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

from hsmsHandler import *
from hsmsPackets import *

from secsHandler import *
from secsVariables import *

class gemCommunicationState:
    """hsms connection state machine states"""
    DISABLED, ENABLED, NOT_COMMUNICATING, EQUIPMENT_INITIATED_CONNECT, WAIT_CRA, WAIT_DELAY, HOST_INITIATED_CONNECT, WAIT_CR_FROM_HOST, COMMUNICATING = range(9)

class gemDefaultHandler(secsDefaultHandler):
    """Baseclass for creating Host/Equipment models. This layer contains GEM functionality. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param sessionID: session / device ID to use for connection
    :type sessionID: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """

    ceids = secsDefaultHandler.ceids
    """Dictionary of available collection events, CEID is the key

    :param name: Name of the data value
    :type name: string
    :param CEID: Collection event the data value is used for
    :type CEID: integer
    """

    dvs = secsDefaultHandler.dvs
    """Dictionary of available data values, DVID is the key

    :param name: Name of the collection event
    :type name: string
    :param dv: Data values available for collection event
    :type dv: list of integers
    """

    alarms = secsDefaultHandler.alarms
    """Dictionary of available alarms, ALID is the key

    :param alarmText: Description of the alarm
    :type alarmText: string
    :param ceidOn: Collection event for activated alarm 
    :type ceidOn: integer
    :param ceidOff: Collection event for deactivated alarm 
    :type ceidOff: integer
    """

    rcmds = secsDefaultHandler.rcmds
    """Dictionary of available remote commands, command is the key

    :param params: description of the parameters
    :type params: list of dictionary
    :param CEID: Collection events the remote command uses
    :type CEID: list of integers
    """

    def __init__(self, address, port, active, sessionID, name, eventHandler=None):
        secsDefaultHandler.__init__(self, address, port, active, sessionID, name, eventHandler)

        self.communicationState = gemCommunicationState.WAIT_CR_FROM_HOST
        self.communicationDelay = 10

        self.reportIDCounter = 1000

        self.reportSubscriptions = {}

    def _serializeData(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        data = secsDefaultHandler._serializeData(self)
        data.update({'communicationState': self.communicationState, 'communicationDelay': self.communicationDelay, 'reportIDCounter': self.reportIDCounter, 'reportSubscriptions': self.reportSubscriptions})
        return data

    def _setConnection(self, connection):
        """Set the connection of the for this models. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`.

        :param connection: The connection the model uses
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        secsDefaultHandler._setConnection(self, connection)

        self.connection.registerCallback(1, 1, self.S1F1Handler)
        self.connection.registerCallback(1, 13, self.S1F13Handler)
        self.connection.registerCallback(6, 11, self.S6F11Handler)
        self.connection.registerCallback(10, 1, self.S10F1Handler)

    def _clearConnection(self):
        """Clear the connection associated with the model instance. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`."""
        self.connection.unregisterCallback(1, 1, self.S1F1Handler)
        self.connection.unregisterCallback(1, 13, self.S1F13Handler)
        self.connection.unregisterCallback(6, 11, self.S6F11Handler)
        self.connection.unregisterCallback(10, 1, self.S10F1Handler)

        secsDefaultHandler._clearConnection(self)

    def _postInit(self):
        """Event called by :class:`secsgem.hsmsHandler.hsmsConnectionManager` after the connection is established (including Select, Linktest, ...)."""
        secsDefaultHandler._postInit(self)

        if not self.communicationState == gemCommunicationState.COMMUNICATING:
            while self.establishCommunication() != 0:
                self.communicationState = gemCommunicationState.WAIT_DELAY
                time.sleep(self.communicationDelay)

            self.communicationState = gemCommunicationState.COMMUNICATING

    def establishCommunication(self):
        """Function to establish GEM communication with equipment.

        :returns: 0: OK, 1: denied, -1: error
        :rtype: integer
        """
        if self.isHost:
            function = self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(1, 13)()))
        else:
            function = self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(1, 13)("secsgem", "0.0.3")), True)

        self.communicationState = gemCommunicationState.WAIT_CRA

        if function._stream == 1 and function._function == 14:
            return function.COMMACK
        else:
            print "establishCommunication unknown response " + function
            return -1

    def clearCollectionEvents(self):
        """Clear all collection events"""
        #clear subscribed reports
        self.reportSubscriptions = {}

        #disable all ceids
        self.disableCEIDs()

        #delete all reports
        self.disableCEIDReports()

    def subscribeCollectionEvent(self, ceid, dvs, reportID=None):
        """Subscribe to a collection event

        :param ceid: ID of the collection event
        :type ceid: integer
        :param dvs: DV IDs to add for collection event 
        :type dvs: list of integers
        :param reportID: optional - ID for report, autonumbering if None
        :type reportID: integer
        """
        if reportID == None:
            reportID = self.reportIDCounter
            self.reportIDCounter += 1

        #note subscribed reports
        self.reportSubscriptions[reportID] = dvs

        #create report
        packet = self.connection.sendAndWaitForResponse(self.streamFunction(2, 33)({"DATAID": 0, "DATA": [{"RPTID": reportID, "RPT": dvs}]}))

        #link event report to collection event
        packet = self.connection.sendAndWaitForResponse(self.streamFunction(2, 35)({"DATAID": 0, "DATA": [{"CEID": ceid, "CE": [reportID]}]}))

        #enable collection event
        packet = self.connection.sendAndWaitForResponse(self.streamFunction(2, 37)({"CEED": True, "CEID": [ceid]}))

    def sendRemoteCommand(self, RCMD, params):
        """Send a remote command

        :param RCMD: Name of command
        :type RCMD: string
        :param params: DV IDs to add for collection event 
        :type params: list of strings
        """
        s2f41 = self.streamFunction(2, 41)()
        s2f41.RCMD = RCMD
        for param in params:
            s2f41.PARAMS.append({"CPNAME": param[0], "CPVAL": param[1]})

        #send remote command
        return self.secsDecode(self.connection.sendAndWaitForResponse(s2f41))

    def sendProcessProgram(self, PPID, PPBODY):
        """Send a process program

        :param PPID: Transferred process programs ID
        :type PPID: string
        :param PPBODY: Content of process program
        :type PPBODY: string
        """
        #send remote command
        return self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(7, 3)({"PPID": PPID, "PPBODY": PPBODY}))).ACKC7

    def requestProcessProgram(self, PPID):
        """Request a process program

        :param PPID: Transferred process programs ID
        :type PPID: string
        """
        #send remote command
        s7f6 = self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(7, 5)(PPID)))
        return (s7f6.PPID, s7f6.PPBODY)

    def deleteProcessPrograms(self, PPIDs):
        """Delete a list of process program

        :param PPIDs: Process programs to delete
        :type PPIDs: list of strings
        """
        #send remote command
        return self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(7, 17)(PPIDs))).ACKC7

    def getProcessProgramList(self):
        """Get process program list
        """
        #send remote command
        return self.secsDecode(self.connection.sendAndWaitForResponse(self.streamFunction(7, 19)())).get()
     
    def S1F1Handler(self, connection, packet):
        """Callback handler for Stream 1, Function 1, Are You There

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        connection.sendResponse(self.streamFunction(1, 2)(), packet.header.system)


    def S1F13Handler(self, connection, packet):
        """Callback handler for Stream 1, Function 13, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        connection.sendResponse(self.streamFunction(1, 14)({"COMMACK": 0}), packet.header.system)

        self.communicationState = gemCommunicationState.COMMUNICATING

    def S6F11Handler(self, connection, packet):
        """Callback handler for Stream 6, Function 11, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secsDecode(packet)

        for report in message.RPT:
            reportDVs = self.reportSubscriptions[report.RPTID]
            reportValues = report.V.get()

            values = []

            for i, s in enumerate(reportDVs):
                values.append({"dvid": s, "value": reportValues[i], "name": self.getDVIDName(s)})

            print values

            data = {"ceid": message.CEID, "rptid": report.RPTID, "values": values, "name": self.getCEIDName(message.CEID), "connection": self.connection, 'peer': self}
            self.fireEvent("CollectionEventReceived", data)

        connection.sendResponse(self.streamFunction(6, 12)(0), packet.header.system)

    def S10F1Handler(self, connection, packet):
        """Callback handler for Stream 10, Function 1, Terminal Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        s10f1 = self.secsDecode(packet)

        connection.sendResponse(self.streamFunction(10, 2)(0), packet.header.system)

        self.fireEvent("TerminalReceived", {"text": s10f1.TEXT, "terminal": s10f1.TID, "connection": self.connection, 'peer': self})
