#####################################################################
# hsmsPackets.py
#
# (c) Copyright 2015, Benjamin Parzella. All rights reserved.
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

import struct

class hsmsHeader:
	def __init__(self, system, sessionID):
		self.sessionID = sessionID
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x01
		self.system = system
	
	def __str__(self):
		return '{sessionID:0x%04x, stream:%02d, function:%02d, pType:0x%02x, sType:0x%02x, system:0x%08x, requireResponse:%01d}' % \
			(self.sessionID, self.stream, self.function, self.pType, self.sType, self.system, self.requireResponse)

	def __repr__(self):
		return "%s(%r)" % (self.__class__, self.__dict__)

class hsmsSelectReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x01
		self.system = system

class hsmsSelectRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x02
		self.system = system

class hsmsDeselectReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x03
		self.system = system

class hsmsDeselectRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x04
		self.system = system

class hsmsLinktestReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x05
		self.system = system

class hsmsLinktestRspHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0xFFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x06
		self.system = system

class hsmsSeparateReqHeader(hsmsHeader):
	def __init__(self, system):
		self.sessionID = 0x0FFFF
		self.requireResponse = False
		self.stream = 0x00
		self.function = 0x00
		self.pType = 0x00
		self.sType = 0x09
		self.system = system

class hsmsStreamFunctionHeader(hsmsHeader):
	def __init__(self, system, stream, function, requireResponse, sessionID):
		self.sessionID = sessionID
		self.requireResponse = requireResponse
		self.stream = stream
		self.function = function
		self.pType = 0x00
		self.sType = 0x00
		self.system = system

class hsmsPacket:
	def __init__(self, header=None, data = ""):
		if header==None:
			self.header = hsmsHeader()
		else:
			self.header = header
			
		self.data = data
	
	def __str__(self):
		data = "header: " + self.header.__str__()
		return data

	def __repr__(self):
		return "%s(%r)" % (self.__class__, self.__dict__)
		
	def encode(self):
		length = 10 + len(self.data)
		dataLengthText = str(len(self.data))+"s"

		headerStream = 	self.header.stream
		if self.header.requireResponse == True:
			headerStream |= 0b10000000

		return struct.pack(">LHBBBBL"+dataLengthText, length, self.header.sessionID, headerStream, self.header.function, self.header.pType, self.header.sType, self.header.system, self.data)
		
	@staticmethod	
	def decode(text):
		dataLength = len(text) - 14
		dataLengthText = str(dataLength)+"s"

		res = struct.unpack(">LHBBBBL"+dataLengthText, text)
		
		result = hsmsPacket(hsmsHeader(res[6], res[1]))
		result.header.requireResponse = (((res[2] & 0b10000000) >> 7) == 1)
		result.header.stream = res[2] & 0b01111111
		result.header.function = res[3]
		result.header.pType = res[4]
		result.header.sType = res[5]
		result.data = res[7]
		
		return result
