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

    def _setConnection(self, connection):
        secsDefaultHandler._setConnection(self, connection)

        self.connection.registerCallback(  1, 13, self.S1F13Handler)

    def _clearConnection(self):
        self.connection.unregisterCallback(  1, 13, self.S1F13Handler)

        secsDefaultHandler._clearConnection(self)

    def _postInit(self):
        secsDefaultHandler._postInit(self)

        if not self.communicationState == gemCommunicationState.COMMUNICATING:
            while self.establishCommunication() != 0:
                self.communicationState = gemCommunicationState.WAIT_DELAY
                time.sleep(self.communicationDelay)

            self.communicationState = gemCommunicationState.COMMUNICATING


    def establishCommunication(self):
        function = secsDecode(self.connection.sendAndWaitForResponse(secsS1F13("secsgem", "0.0.3")))

        self.communicationState = gemCommunicationState.WAIT_CRA

        if function.stream == 1 and function.function == 14:
            return ord(function.COMMACK.value[0])
        else:
            print "establishCommunication unknown response " + function
            return -1

    def S1F13Handler(self, connection, packet):
        connection.sendResponse(secsS1F14(chr(0x00), "secsgem", "0.0.3"), packet.header.system)

        self.communicationState = gemCommunicationState.COMMUNICATING



