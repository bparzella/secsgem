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

from hsmsHandler import *
from hsmsPackets import *

from secsFunctions import *

class secsDefaultHandler(hsmsDefaultHandler):
	def __init__(self, address, port, active, sessionID, name):
		hsmsDefaultHandler.__init__(self, address, port, active, sessionID, name)

	def disableCEIDs(self):
		s2f37 = secsS2F37(False, [])
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 37, True, self.connection.sessionID), s2f37.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(2, 38)

	def disableCEIDReports(self):
		s2f33 = secsS2F33(0, [])
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 33, True, self.connection.sessionID), s2f33.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(2, 34)

	def listSVs(self):
		s1f11 = secsS1F11([])
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 1, 11, True, self.connection.sessionID), s1f11.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(1, 12)

		return secsDecode(packet).data

	def requestSVs(self, SVs):
		s1f3 = secsS1F3(SVs)
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 1, 3, True, self.connection.sessionID), s1f3.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(1, 4)

		return secsDecode(packet).SV

	def requestSV(self, SV):
		return self.requestSVs([SV])[0]

	def listECs(self):
		s2f29 = secsS2F29([])
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 29, True, self.connection.sessionID), s2f29.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(2, 30)

		return secsDecode(packet).data

	def requestECs(self, ECs):
		s2f13 = secsS2F13(ECs)
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 13, True, self.connection.sessionID), s2f13.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(2, 14)

		return secsDecode(packet).EC

	def requestEC(self, EC):
		return self.requestECs([EC])[0]

	def setECs(self, ECs):
		s2f15 = secsS2F15(ECs)
		packet = hsmsPacket(hsmsStreamFunctionHeader(self.connection.getNextSystemCounter(), 2, 15, True, self.connection.sessionID), s2f15.encode())

		self.connection.sendPacket(packet)
		packet = self.connection.waitforStreamFunction(2, 16)

		return secsDecode(packet).EAC

	def setEC(self, EC, value):
		return self.setECs([[EC, value]])
