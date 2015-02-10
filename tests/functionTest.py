#####################################################################
# functionTest.py
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

from secsgem import *

def encodeString(data):
	result = ""
	for item in data:
		result += chr(item)
	return result

selectReqID = 1
selectReqEncoded = [0x00, 0x00, 0x00, 0x0A, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01]
selectReqEncodedString = encodeString(selectReqEncoded)

selectRspID = 2
selectRspEncoded = [0x00, 0x00, 0x00, 0x0A, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02]
selectRspEncodedString = encodeString(selectRspEncoded)

linktestReqID = 3
linktestReqEncoded = [0x00, 0x00, 0x00, 0x0A, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x03]
linktestReqEncodedString = encodeString(linktestReqEncoded)

linktestRspID = 4
linktestRspEncoded = [0x00, 0x00, 0x00, 0x0A, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x04]
linktestRspEncodedString = encodeString(linktestRspEncoded)

separateReqID = 5
separateReqEncoded = [0x00, 0x00, 0x00, 0x0A, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x05]
separateReqEncodedString = encodeString(separateReqEncoded)


s1f2MDLN = 'UF'
s1f2SOFTREV = 'trunk'
s1f2Encoded = [0x01, 0x02, 0x41, 0x02, 0x55, 0x46, 0x41, 0x05, 0x74, 0x72, 0x75, 0x6E, 0x6B]
s1f2EncodedString = encodeString(s1f2Encoded)

s1f13MDLN = 'UF'
s1f13SOFTREV = 'trunk'
s1f13Encoded = [0x01, 0x02, 0x41, 0x02, 0x55, 0x46, 0x41, 0x05, 0x74, 0x72, 0x75, 0x6E, 0x6B]
s1f13EncodedString = encodeString(s1f13Encoded)

s1f14COMMACK = chr(0x00)
s1f14MDLN = 'FSSP'
s1f14SOFTREV = '1.0.0'
s1f14Encoded = [0x01, 0x02, 0x21, 0x01, 0x00, 0x01, 0x02, 0x41, 0x04, 0x46, 0x53, 0x53, 0x50, 0x41, 0x05, 0x31, 0x2e, 0x30, 0x2e, 0x30]
s1f14EncodedString = encodeString(s1f14Encoded)

print "*starting tests"

print "*running S1F1 tests"
s1f1 = secsS1F1()
if s1f1.encode() != "":
	print "!s1f1.encode failed"

s1f1 = secsS1F1.decode("")
if s1f1 == None:
	print "!s1f1.decode failed"
	
print "*running S1F2 tests"
s1f2 = secsS1F2(s1f2MDLN, s1f2SOFTREV)
if s1f2.encode() != s1f2EncodedString:
	print "!s1f2.encode failed"

s1f2 = secsS1F2.decode(s1f2EncodedString)
if not ((s1f2.MDLN.value == s1f2MDLN) and (s1f2.SOFTREV.value == s1f2SOFTREV)):
	print "!s1f2.decode failed"

print "*running S1F13 tests"
s1f13 = secsS1F13(s1f13MDLN, s1f13SOFTREV)
if s1f13.encode() != s1f13EncodedString:
	print "!s1f13.encode failed"

s1f13 = secsS1F13.decode(s1f13EncodedString)
if not ((s1f13.MDLN.value == s1f13MDLN) and (s1f13.SOFTREV.value == s1f13SOFTREV)):
	print "!s1f13.decode failed"

print "*running S1F14 tests"
s1f14 = secsS1F14(s1f14COMMACK, s1f14MDLN, s1f14SOFTREV)
if s1f14.encode() != s1f14EncodedString:
	print "!s1f14.encode failed"

s1f14 = secsS1F14.decode(s1f14EncodedString)
if not ((s1f14.COMMACK.value == s1f14COMMACK) and (s1f14.MDLN.value == s1f14MDLN) and (s1f14.SOFTREV.value == s1f14SOFTREV)):
	print "!s1f14.decode failed"

print "*running hsmsSelectReqHeader tests"
packet = hsmsPacket(hsmsSelectReqHeader(selectReqID))
if packet.encode() != selectReqEncodedString:
	print "!hsmsSelectReqHeader.encode failed"

packet = hsmsPacket.decode(selectReqEncodedString)
if not ((packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.function == 0x00) and (packet.header.pType ==0x00) and (packet.header.sType == 0x01) and (packet.header.system == selectReqID)):
	print "!hsmsSelectReqHeader.decode failed"

print "*running hsmsSelectRspHeader tests"
packet = hsmsPacket(hsmsSelectRspHeader(selectRspID))
if packet.encode() != selectRspEncodedString:
	print "!hsmsSelectRspHeader.encode failed"

packet = hsmsPacket.decode(selectRspEncodedString)
if not ((packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.function == 0x00) and (packet.header.pType ==0x00) and (packet.header.sType == 0x02) and (packet.header.system == selectRspID)):
	print "!hsmsSelectRspHeader.decode failed"

print "*running hsmsLinktestReqHeader tests"
packet = hsmsPacket(hsmsLinktestReqHeader(linktestReqID))
if packet.encode() != linktestReqEncodedString:
	print "!hsmsLinktestReqHeader.encode failed"

packet = hsmsPacket.decode(linktestReqEncodedString)
if not ((packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.function == 0x00) and (packet.header.pType ==0x00) and (packet.header.sType == 0x05) and (packet.header.system == linktestReqID)):
	print "!hsmsLinktestReqHeader.decode failed"

print "*running hsmsLinktestRspHeader tests"
packet = hsmsPacket(hsmsLinktestRspHeader(linktestRspID))
if packet.encode() != linktestRspEncodedString:
	print "!hsmsLinktestRspHeader.encode failed"

packet = hsmsPacket.decode(linktestRspEncodedString)
if not ((packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.function == 0x00) and (packet.header.pType ==0x00) and (packet.header.sType == 0x06) and (packet.header.system == linktestRspID)):
	print "!hsmsLinktestRspHeader.decode failed"

print "*running hsmsSeparateReqHeader tests"
packet = hsmsPacket(hsmsSeparateReqHeader(separateReqID))
if packet.encode() != separateReqEncodedString:
	print "!hsmsSeparateReqHeader.encode failed"

packet = hsmsPacket.decode(separateReqEncodedString)
if not ((packet.header.sessionID == 0xFFFF) and (packet.header.stream == 0x00) and (packet.header.function == 0x00) and (packet.header.pType ==0x00) and (packet.header.sType == 0x09) and (packet.header.system == separateReqID)):
	print "!hsmsSeparateReqHeader.decode failed"

print "*done"
