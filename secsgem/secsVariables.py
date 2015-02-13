#####################################################################
# secsVariables.py
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

import logging

import struct

from common import formatHex

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
