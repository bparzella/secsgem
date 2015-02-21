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
from secsFunctions import *
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
    """

    ceids = secsDefaultHandler.ceids
    alarms = secsDefaultHandler.alarms

    def __init__(self, address, port, active, sessionID, name):
        secsDefaultHandler.__init__(self, address, port, active, sessionID, name)

        self.communicationState = gemCommunicationState.WAIT_CR_FROM_HOST
        self.communicationDelay = 10

        self.reportIDCounter = 1000

        self.reportSubscriptions = {}

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
        """Function to establish GEM communication with remote.

        :returns: 0: OK, 1: denied, -1: error
        :rtype: integer
        """
        function = secsDecode(self.connection.sendAndWaitForResponse(secsS1F13("secsgem", "0.0.3")))

        self.communicationState = gemCommunicationState.WAIT_CRA

        if function.stream == 1 and function.function == 14:
            return ord(function.COMMACK.value[0])
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
        packet = self.connection.sendAndWaitForResponse(secsS2F33(0, [[reportID, dvs]]))

        #link event report to collection event
        packet = self.connection.sendAndWaitForResponse(secsS2F35(0, [[ceid, [reportID]]]))

        #enable collection event
        packet = self.connection.sendAndWaitForResponse(secsS2F37(True, [ceid]))
     
    def S1F1Handler(self, connection, packet):
        """Callback handler for Stream 1, Function 1, Are You There

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        connection.sendResponse(secsS1F2("secsgem", "0.0.3"), packet.header.system)


    def S1F13Handler(self, connection, packet):
        """Callback handler for Stream 1, Function 13, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        connection.sendResponse(secsS1F14(chr(0x00), "secsgem", "0.0.3"), packet.header.system)

        self.communicationState = gemCommunicationState.COMMUNICATING

    def S6F11Handler(self, connection, packet):
        """Callback handler for Stream 6, Function 11, Establish Communication Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = secsDecode(packet)

        for report in message.reports:
            reportDVs = self.reportSubscriptions[report[0].value]
            reportValues = secsUnwrapVariables(report[1])

            values = []

            for i, s in enumerate(reportDVs):
                values.append({"dvid": s, "value": reportValues[i], "name": self.getDVIDName(s)})

            print values

            data = {"ceid": message.CEID.value, "rptid": report[0].value, "values": values, "name": self.getCEIDName(message.CEID.value)}
            self.postEvent("collectionevent", data)

        connection.sendResponse(secsS6F12(chr(0x00)), packet.header.system)

    def S10F1Handler(self, connection, packet):
        """Callback handler for Stream 10, Function 1, Terminal Request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        s10f1 = secsDecode(packet)

        connection.sendResponse(secsS10F2(0), packet.header.system)

        self.postEvent("terminal", {"text": s10f1.TEXT.value, "terminal": ord(s10f1.TID.value[0])})
