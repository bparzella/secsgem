#####################################################################
# secs.py
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

import struct
import logging
import traceback

from common import formatHex
from hsms import *

class secsVar(object):
	def __init__(self, value):
		if issubclass(type(value), secsVar):
			self.value = value.value
			return

		self.value = value

class secsVarNone(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "None"

class secsVarBinary(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "Binary %s" % (formatHex(self.value))

class secsVarBoolean(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "Boolean %s" % (self.value)

class secsVarString(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "A %s" % (self.value)

class secsVarINT1(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "I1 %d" % (self.value)

class secsVarINT2(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "I2 %d" % (self.value)

class secsVarINT4(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "I4 %d" % (self.value)

class secsVarUINT1(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "U1 %d" % (self.value)

class secsVarUINT2(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "U2 %d" % (self.value)

class secsVarUINT4(secsVar):
	def __init__(self, value):
		secsVar.__init__(self, value)

	def __repr__(self):
		return "U4 %d" % (self.value)

def secsConvertVarIfRequired(targetClass, value):
	if issubclass(type(value), secsVar):
		return value
	else:
		return targetClass(value)

class secsCoder:
	@staticmethod	
	def decode(text, returnPos = False):
		textPos = 0
		
		if text == "":
			return secsVarNone(None)
		
		#parse format byte
		formatByte = ord(text[textPos])
		itemFormat = (formatByte & 0b11111100) >> 2
		lengthBytes = (formatByte & 0b00000011)

		textPos += 1

		#read 1-3 length bytes
		length = 0
		for i in range(lengthBytes):
			length <<= 8
			length += ord(text[textPos])
			
			textPos += 1

		#handle format depending on type
		if itemFormat == 0:
			#list
			result = []
			for i in range(length):
				(decodeResult, offset) = secsCoder.decode(text[textPos:], True)
				textPos += offset
				result.append(decodeResult)
			if returnPos:
				return(result, textPos)
			else:
				return result
		elif itemFormat == 010:
			#binary
			result = None

			if length > 0:
				result = text[textPos:textPos+length]

			if returnPos:
				return(secsVarBinary(result), textPos+length)
			else:
				return secsVarBinary(result)
		elif itemFormat == 011:
			#boolean
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = bool(struct.unpack(">b", resultText)[0])

			if returnPos:
				return(secsVarBoolean(result), textPos+length)
			else:
				return secsVarBoolean(result)
		elif itemFormat == 020:
			#string
			result = None

			if length > 0:
				result = text[textPos:textPos+length]

			if returnPos:
				return(secsVarString(result), textPos+length)
			else:
				return secsVarString(result)
		elif itemFormat == 031:
			#1byte int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">b", resultText)[0]

			if returnPos:
				return(secsVarINT1(result), textPos+length)
			else:
				return secsVarINT1(result)
		elif itemFormat == 032:
			#2byte int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">h", resultText)[0]

			if returnPos:
				return(secsVarINT2(result), textPos+length)
			else:
				return secsVarINT2(result)
		elif itemFormat == 034:
			#4byte int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">l", resultText)[0]

			if returnPos:
				return(secsVarINT4(result), textPos+length)
			else:
				return secsVarINT4(result)
		elif itemFormat == 051:
			#1byte unsigned int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">B", resultText)[0]

			if returnPos:
				return(secsVarUINT1(result), textPos+length)
			else:
				return secsVarUINT1(result)
		elif itemFormat == 052:
			#2byte unsigned int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">H", resultText)[0]

			if returnPos:
				return(secsVarUINT2(result), textPos+length)
			else:
				return secsVarUINT2(result)
		elif itemFormat == 054:
			#4byte unsigned int
			result = None

			if length > 0:
				resultText = text[textPos:textPos+length]
				result = struct.unpack(">L", resultText)[0]
				
			if returnPos:
				return(secsVarUINT4(result), textPos+length)
			else:
				return secsVarUINT4(result)
		else:
			logging.error("Unknown itemFormat %d (octal %o)", itemFormat, itemFormat)

	@staticmethod	
	def encode(data, returnPos = False):
		result = ""
		if type(data) == type(list()):
			listLen = len(data)
			if (listLen > 0xFFFF):
				lengthBytes = 3
				formatByte = (0 << 2) | lengthBytes
				result += chr(formatByte) + chr((listLen & 0xFF0000) >> 16) + chr((listLen & 0x00FF00) >> 8) + chr((listLen & 0x0000FF))
			elif (listLen > 0xFF):
				lengthBytes = 2
				formatByte = (0 << 2) | lengthBytes
				result += chr(formatByte) + chr((listLen & 0x00FF00) >> 8) + chr((listLen & 0x0000FF))
			else:
				lengthBytes = 1
				formatByte = (0 << 2) | lengthBytes
				result += chr(formatByte) + chr((listLen & 0x0000FF))
				
			for item in data:
				result += secsCoder.encode(item)
		elif type(data) == type(None):
			return ""
		elif type(data) is secsVarString:
			#format code = octal 020
			formatCode = 020
			strLen = len(data.value)
			if (strLen > 0xFFFF):
				lengthBytes = 3
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0xFF0000) >> 16) + chr((strLen & 0x00FF00) >> 8) + chr((strLen & 0x0000FF))
			elif (strLen > 0xFF):
				lengthBytes = 2
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0x00FF00) >> 8) + chr((strLen & 0x0000FF))
			else:
				lengthBytes = 1
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0x0000FF))
			result += data.value
		elif type(data) is secsVarBinary:
			#format code = octal 010
			strLen = len(data.value)
			formatCode = 010
			if (strLen > 0xFFFF):
				lengthBytes = 3
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0xFF0000) >> 16) + chr((strLen & 0x00FF00) >> 8) + chr((strLen & 0x0000FF))
			elif (strLen > 0xFF):
				lengthBytes = 2
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0x00FF00) >> 8) + chr((strLen & 0x0000FF))
			else:
				lengthBytes = 1
				formatByte = (formatCode << 2) | lengthBytes
				result += chr(formatByte) + chr((strLen & 0x0000FF))
			result += data.value
		elif type(data) is secsVarBoolean:
			#format code = octal 011
			formatCode = 011
			lengthBytes = 1
			formatByte = (formatCode << 2) | lengthBytes
			result += chr(formatByte) + \
				chr(1) + \
				chr(data.value)
		elif type(data) is secsVarUINT1:
			#format code = octal 051
			formatCode = 051
			lengthBytes = 1
			formatByte = (formatCode << 2) | lengthBytes
			result += chr(formatByte) + \
				chr(1) + \
				chr(data.value)
		elif type(data) is secsVarUINT2:
			#format code = octal 052
			formatCode = 052
			lengthBytes = 1
			formatByte = (formatCode << 2) | lengthBytes
			result += chr(formatByte) + \
				chr(2) + \
				chr((data.value & 0xFF00) >>  8) + \
				chr(data.value & 0x00FF)	
		elif type(data) is secsVarUINT4:
			#format code = octal 054
			formatCode = 054
			lengthBytes = 1
			formatByte = (formatCode << 2) | lengthBytes
			result += chr(formatByte) + \
				chr(4) + \
				chr((data.value & 0xFF000000) >> 24) + \
				chr((data.value & 0x00FF0000) >> 16) + \
				chr((data.value & 0x0000FF00) >>  8) + \
				chr(data.value & 0x000000FF)	
		else:
			logging.error("Unknown type %s", type(data))
			
		return result

class secsS0F0:
	def __init__(self):
		pass
		
	def __str__(self):
		return "LL"
		
	def encode(self):
		return secsCoder.encode(None)
	
	@staticmethod	
	def decode(text):
		return secsS0F0()

class secsS1F1:
	def __init__(self):
		pass
		
	def __str__(self):
		return "S1F1 {}"
		
	def encode(self):
		return secsCoder.encode(None)
	
	@staticmethod	
	def decode(text):
		return secsS1F1()

class secsS1F2:
	def __init__(self, MDLN, SOFTREV):
		self.MDLN = secsVarString(MDLN)
		self.SOFTREV = secsVarString(SOFTREV)
		
	def __str__(self):
		return "S1F2 {MDLN: '%s', SOFTREV: '%s'}" % (self.MDLN.value, self.SOFTREV.value)
		
	def encode(self):
		return secsCoder.encode([self.MDLN, self.SOFTREV])
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS1F2(data[0], data[1])

class secsS1F3:
	def __init__(self, SVIDs):
		self.SVID = []
		for SVID in SVIDs:
			self.SVID.append(secsVarUINT4(SVID))

	def __str__(self):
		return "S1F3 {SVID: '%s'}" % (self.SVID)

	def encode(self):
		return secsCoder.encode(self.SVID)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS1F3(data)

class secsS1F4:
	def __init__(self, SV):
		self.SV = SV

	def __str__(self):
		return "S1F4 {SV: '%s'}" % (self.SV)

	def encode(self):
		return secsCoder.encode(self.SV)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS1F4(data)
		
class secsS1F11:
	def __init__(self, SVIDs):
		self.SVID = []
		for SVID in SVIDs:
			self.SVID.append(secsVarUINT4(SVID))

	def __str__(self):
		return "S1F11 {SVID: '%s'}" % (self.SVID)

	def encode(self):
		return secsCoder.encode(self.SVID)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS1F11(data)

class secsS1F12:
	def __init__(self, data):
		self.data = []
		for item in data:
			self.data.append([secsVarUINT4(item[0]), secsVarString(item[1]), secsVarString(item[2])])

	def __str__(self):
		data = "["
		for item in self.data:
			data += "[SVID: '%s', SVNAME: '%s',  UNIT: '%s']" % (item[0], item[1], item[2])
		data += "]"

		return "S1F12 {data: %s}" % (data)

	def encode(self):
		return secsCoder.encode(self.data)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS1F12(data)

class secsS1F13:
	def __init__(self, MDLN, SOFTREV):
		self.MDLN = secsVarString(MDLN)
		self.SOFTREV = secsVarString(SOFTREV)
		
	def __str__(self):
		return "S1F13 {MDLN: '%s', SOFTREV: '%s'}" % (self.MDLN.value, self.SOFTREV.value)
		
	def encode(self):
		return secsCoder.encode([self.MDLN, self.SOFTREV])
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS1F13(data[0], data[1])


class secsS1F14:
	def __init__(self, COMMACK, MDLN, SOFTREV):
		self.COMMACK = secsVarBinary(COMMACK)
		self.MDLN = secsVarString(MDLN)
		self.SOFTREV = secsVarString(SOFTREV)
		
	def __str__(self):
		return "S1F14 {COMMACK: '%s', {MDLN: '%s', SOFTREV: '%s'}}" % (self.COMMACK.value, self.MDLN.value, self.SOFTREV.value)
		
	def encode(self):
		return secsCoder.encode([self.COMMACK, [self.MDLN, self.SOFTREV]])
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS1F14(data[0], data[1][0], data[1][1])

class secsS2F13:
	def __init__(self, ECIDs):
		self.ECID = []
		for ECID in ECIDs:
			self.ECID.append(secsVarUINT4(ECID))

	def __str__(self):
		return "S2F13 {ECID: '%s'}" % (self.ECID)

	def encode(self):
		return secsCoder.encode(self.ECID)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS2F13(data)

class secsS2F14:
	def __init__(self, EC):
		self.EC = EC

	def __str__(self):
		return "S2F14 {EC: '%s'}" % (self.EC)

	def encode(self):
		return secsCoder.encode(self.EC)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		logging.debug("  %s", secsS2F14(data))
		return secsS2F14(data)

class secsS2F15:
	def __init__(self, ECIDs):
		self.ECID = []
		for ECID in ECIDs:
			self.ECID.append([secsVarUINT4(ECID[0]), secsConvertVarIfRequired(secsVarString,ECID[1])])

	def __str__(self):
		return "S2F15 {ECID: '%s'}" % (self.ECID)

	def encode(self):
		logging.debug(" %s", self)
		return secsCoder.encode(self.ECID)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS2F15(data)

class secsS2F16:
	def __init__(self, EAC):
		self.EAC = secsVarBinary(EAC)

	def __str__(self):
		return "2F16 {EAC: %s}" % (self.EAC)

	def encode(self):
		return secsCoder.encode(self.EAC)

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)

		logging.debug("  %s", secsS2F16(data))
		return secsS2F16(data)

class secsS2F29:
	def __init__(self, ECIDs):
		self.ECID = []
		for ECID in ECIDs:
			self.ECID.append(secsVarUINT4(ECID))

	def __str__(self):
		return "S2F29 {ECID: '%s'}" % (self.ECID)

	def encode(self):
		return secsCoder.encode(self.ECID)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS2F29(data)

class secsS2F30:
	def __init__(self, data):
		self.data = []
		for item in data:
			self.data.append([secsVarUINT4(item[0]), secsVarString(item[1]), secsVarString(item[2]), secsVarString(item[3]), secsVarString(item[4]), secsVarString(item[5])])

	def __str__(self):
		data = "["
		for item in self.data:
			data += "[ECID: '%s', ECNAME: '%s',  ECMIN: '%s',  ECMAX: '%s',  ECDEF: '%s',  UNITS: '%s']" % (item[0], item[1], item[2], item[3], item[4], item[5])
		data += "]"

		return "S2F30 {data: %s}" % (data)

	def encode(self):
		return secsCoder.encode(self.data)

	@staticmethod
	def decode(text):
		data = secsCoder.decode(text)

		return secsS2F30(data)

class secsS2F33:
	def __init__(self, DATAID, reports):
		self.DATAID = secsVarUINT4(DATAID)
		self.reports = []
		for report in reports:
			CEIDs = []

			for CEID in report[1]:
				CEIDs.append(secsVarUINT4(CEID))

			self.reports.append([secsVarUINT4(report[0]), CEIDs])

	def __str__(self):
		reports = "["
		for report in self.reports:
			CEIDs = "["
			for CEID in report[1]:
				CEIDs += "VID = %d," % (CEID.value)

			CEIDs += "]"

			reports += "[RPTID: '%d', %s]" % (report[0].value, CEIDs)
		reports += "]"
		return "2F33 {DATAID: '%s', %s}" % (self.DATAID.value, reports)

	def encode(self):
		return secsCoder.encode([self.DATAID, self.reports])

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS2F33(data[0], data[1][0], data[1][1])

class secsS2F34:
	def __init__(self, DRACK):
		self.DRACK = secsVarBinary(DRACK)

	def __str__(self):
		return "2F34 {DRACK: '%d'}" % (ord(self.DRACK.value[0]))

	def encode(self):
		return secsCoder.encode(self.DRACK)

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		return secsS2F34(data[0])

class secsS2F35:
	def __init__(self, DATAID, CEIDs):
		self.DATAID = secsVarUINT4(DATAID)
		self.CEIDs = []
		for CEID in CEIDs:
			RPTIDs = []

			for RPTID in CEID[1]:
				RPTIDs.append(secsVarUINT4(RPTID))

			self.CEIDs.append([secsVarUINT4(CEID[0]), RPTIDs])

	def __str__(self):
		CEIDs = "["
		for CEID in self.CEIDs:
			RPTIDs = "["
			for RPTID in CEID[1]:
				RPTIDs += "RPTID = %d," % (RPTID.value)

			RPTIDs += "]"

			CEIDs += "[CEID: '%d', %s]" % (CEID[0].value, RPTIDs)
		CEIDs += "]"
		return "2F35 {DATAID: '%s', %s}" % (self.DATAID.value, CEIDs)

	def encode(self):
		return secsCoder.encode([self.DATAID, self.CEIDs])

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS2F35(data[0], data[1][0], data[1][1])

class secsS2F36:
	def __init__(self, LRACK):
		self.LRACK = secsVarBinary(LRACK)

	def __str__(self):
		return "2F36 {LRACK: '%d'}" % (ord(self.LRACK.value[0]))

	def encode(self):
		return secsCoder.encode(self.LRACK)

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		return secsS2F36(data[0])

class secsS2F37:
	def __init__(self, CEED, CEIDs):
		self.CEED = secsVarBoolean(CEED)
		self.CEIDs = []
		for CEID in CEIDs:
			self.CEIDs.append(secsVarUINT4(CEID))

	def __str__(self):
		CEIDs = "["
		for CEID in self.CEIDs:
			CEIDs += "CEID = %d," % (CEID.value)

		CEIDs += "]"

		return "2F37 {CEED: '%s', %s}" % (self.CEED.value, CEIDs)

	def encode(self):
		return secsCoder.encode([self.CEED, self.CEIDs])

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS2F37(data[0], data[1])

class secsS2F38:
	def __init__(self, ERACK):
		self.ERACK = secsVarBinary(ERACK)

	def __str__(self):
		return "2F38 {ERACK: '%d'}" % (ord(self.ERACK.value[0]))

	def encode(self):
		return secsCoder.encode(self.ERACK)

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		return secsS2F38(data[0])

class secsS2F41:
	def __init__(self, RCMD, parameters):
		self.RCMD = secsVarString(RCMD)
		self.parameters = []
		for parameter in parameters:
			self.parameters.append([secsVarString(parameter[0]), secsVarString(parameter[1])])

	def __str__(self):
		parameters = "["
		for parameter in self.parameters:
			parameters += "[RPTID: '%s', CPVAL: '%s']" % (parameter[0].value, parameter[1].value)
		parameters += "]"
		return "2F41 {RCMD: '%s', %s}" % (self.RCMD.value, parameters)

	def encode(self):
		return secsCoder.encode([self.RCMD, self.parameters])

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS2F41(data[0], data[1][0], data[1][1])

class secsS2F42:
	def __init__(self, parameters):
		self.parameters = parameters

	def __str__(self):
		return "2F42 {%s}" % (parameters)

	def encode(self):
		return secsCoder.encode(self.parameters)

	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		return secsS2F42_generic(data)

class secsS5F1:
	def __init__(self, ALCD, ALID, ALTX):
		self.ALCD = secsVarBinary(ALCD)
		self.ALID = secsVarUINT4(ALID)
		self.ALTX = secsVarString(ALTX)
		
	def __str__(self):
		return "S5F1 {ALCD: '%s', ALID: %d, ALTX: '%s'}" % (self.ALCD.value, self.ALID.value, self.ALTX.value)
		
	def encode(self):
		return secsCoder.encode([self.ALCD, self.ALID, self.ALTX])
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS5F1(data[0], data[1], data[2])

class secsS5F2:
	def __init__(self, ACKC5):
		self.ACKC5 = secsVarBinary(ACKC5)
		
	def __str__(self):
		return "S5F2 {ACKC5: '%s'}" % (self.ACKC5.value)
		
	def encode(self):
		return secsCoder.encode(self.ACKC5)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS5F2(data[0])

class secsS6F11:
	def __init__(self, DATAID, CEID, reports = []):
		self.DATAID = secsVarUINT4(DATAID)
		self.CEID = secsVarUINT4(CEID)

		self.reports = reports
		
	def __str__(self):
		return "S6F11 {DATAID: %d, CEID: %d, %s}" % (self.DATAID.value, self.CEID.value, self.reports)
			
	def encode(self):
		return secsCoder.encode([self.DATAID.value, self.CEID.value, self.reports])
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS6F11(data[0], data[1], data[2])
		
class secsS6F12:
	def __init__(self, ACKC6):
		self.ACKC6 = secsVarBinary(ACKC6)
		
	def __str__(self):
		return "S6F12 {ACKC6: '%s'}" % (self.ACKC6.value)
		
	def encode(self):
		return secsCoder.encode(self.ACKC6)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS6F12(data[0])

class secsS9F1:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F1 ERROR: Unrecognized Device ID {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F1(data[0])

class secsS9F3:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F3 ERROR: Unrecognized Stream Type {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F3(data[0])

class secsS9F5:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F5 ERROR: Unrecognized Function Type {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F5(data[0])

class secsS9F7:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F7 ERROR: Illegal Data {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F7(data[0])

class secsS9F9:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F9 ERROR: Transaction Timer Time-out {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F9(data[0])

class secsS9F11:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F11 ERROR: Data Too Long {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F11(data[0])

class secsS9F13:
	def __init__(self, MHEAD):
		self.MHEAD = secsVarBinary(MHEAD)
		
	def __str__(self):
		return "S9F13 ERROR: Inter Block Time-out {MHEAD: '%s'}" % (self.MHEAD.value)
		
	def encode(self):
		return secsCoder.encode(self.MHEAD)
	
	@staticmethod	
	def decode(text):
		data = secsCoder.decode(text)
		
		return secsS9F13(data[0])

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

secsStreamsFunctions = {
	0: 	{
		 0: secsS0F0,
		},
	1: 	{
		 1: secsS1F1,
		 2: secsS1F2,
		 3: secsS1F3,
		 4: secsS1F4,
		11: secsS1F11,
		12: secsS1F12,
		13: secsS1F13,
		14: secsS1F14,
		},
	2: 	{
		13: secsS2F13,
		14: secsS2F14,
		15: secsS2F15,
		16: secsS2F16,
		29: secsS2F29,
		30: secsS2F30,
		33: secsS2F33,
		34: secsS2F34,
		35: secsS2F35,
		36: secsS2F36,
		37: secsS2F37,
		38: secsS2F38,
		41: secsS2F41,
		42: secsS2F42,
		},
	5:	{
		 1: secsS5F1,
		 2: secsS5F2,
		},
	6:	{
		11: secsS6F11,
		12: secsS6F12,
		},
	9:	{
		 1: secsS9F1,
		 3: secsS9F3,
		 5: secsS9F5,
		 7: secsS9F7,
		 9: secsS9F9,
		11: secsS9F11,
		13: secsS9F13,
		},
}

def secsDecode(packet):
	if not packet.header.stream in secsStreamsFunctions:
		logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
		return None
	else:
		if not packet.header.function in secsStreamsFunctions[packet.header.stream]:
			logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
			return None
		else:
			return secsStreamsFunctions[packet.header.stream][packet.header.function].decode(packet.data)

