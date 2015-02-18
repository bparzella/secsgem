#####################################################################
# secsHandler.py
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
"""Handler for SECS commands. Used in combination with :class:`secsgem.hsmsHandler.hsmsConnectionManager`"""
#TODO: isn't this more like GEM?

from hsmsHandler import *
from hsmsPackets import *

from secsFunctions import *

class secsDefaultHandler(hsmsDefaultHandler):
    """Baseclass for creating Host/Equipment models. This layer contains the SECS functionality. Inherit from this class and override required functions.

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
    def __init__(self, address, port, active, sessionID, name):
        hsmsDefaultHandler.__init__(self, address, port, active, sessionID, name)

    def disableCEIDs(self):
        """Disable all Collection Events.
        """
        s2f37 = secsS2F37(False, [])
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 37, True, self.connection.sessionID), s2f37.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s2f37.header.system)

    def disableCEIDReports(self):
        """Disable all Collection Event Reports.
        """
        s2f33 = secsS2F33(0, [])
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 33, True, self.connection.sessionID), s2f33.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s2f33.header.system)

    def listSVs(self):
        """Get list of available Service Variables.

        :returns: available Service Variables
        :rtype: list
        """
        s1f11 = secsS1F11([])
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 1, 11, True, self.connection.sessionID), s1f11.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s1f11.header.system)

        return secsDecode(packet).data

    def requestSVs(self, SVs):
        """Request contents of supplied Service Variables.

        :param SVs: Service Variables to request
        :type SVs: list
        :returns: values of requested Service Variables
        :rtype: list
        """
        s1f3 = secsS1F3(SVs)
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 1, 3, True, self.connection.sessionID), s1f3.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s1f3.header.system)

        return secsDecode(packet).SV

    def requestSV(self, SV):
        """Request contents of one Service Variable.

        :param SV: id of Service Variable
        :type SV: int
        :returns: value of requested Service Variable
        :rtype: various
        """
        return self.requestSVs([SV])[0]

    def listECs(self):
        """Get list of available Equipment Constants.

        :returns: available Equipment Constants
        :rtype: list
        """
        s2f29 = secsS2F29([])
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 29, True, self.connection.sessionID), s2f29.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s2f29.header.system)

        return secsDecode(packet).data

    def requestECs(self, ECs):
        """Request contents of supplied Equipment Constants.

        :param ECs: Equipment Constants to request
        :type ECs: list
        :returns: values of requested Equipment Constants
        :rtype: list
        """
        s2f13 = secsS2F13(ECs)
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 13, True, self.connection.sessionID), s2f13.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s2f13.header.system)

        return secsDecode(packet).EC

    def requestEC(self, EC):
        """Request contents of one Equipment Constant.

        :param EC: id of Equipment Constant
        :type EC: int
        :returns: value of requested Equipment Constant
        :rtype: various
        """
        return self.requestECs([EC])[0]

    def setECs(self, ECs):
        """Set contents of supplied Equipment Constants.

        :param ECs: list containing list of id / value pairs
        :type ECs: list
        """
        s2f15 = secsS2F15(ECs)
        packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 15, True, self.connection.sessionID), s2f15.encode())

        self.connection.sendPacket(packet)
        packet = self.connection.waitforSystem(s2f15.header.system)

        return secsDecode(packet).EAC

    def setEC(self, EC, value):
        """Set contents of one Equipment Constant.

        :param EC: id of Equipment Constant
        :type EC: int
        :param value: new content of Equipment Constant
        :type value: various
        """
        return self.setECs([[EC, value]])
