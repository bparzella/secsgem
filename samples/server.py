#####################################################################
# server.py
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

import time

from secsgem import *

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

earlyS1F13 = False

def S1F1Handler(connection, packet):
	s1f2 = secsS1F2("pysecs", "prototype")
	responsePacket = hsmsPacket(hsmsStreamFunctionHeader(1, 2, False, packet.header.system), s1f2.encode())
	
	connection.sendPacket(responsePacket)
	
def S1F13Handler(connection, packet):
	global earlyS1F13
	earlyS1F13 = True
	
	s1f14 = secsS1F14(chr(0x00), "pysecs", "prototype")
	responsePacket = hsmsPacket(hsmsStreamFunctionHeader(1, 14, False, packet.header.system), s1f14.encode())

	connection.sendPacket(responsePacket)

def S6F11Handler(connection, packet):
	s6f12 = secsS6F12(chr(0x00))
	responsePacket = hsmsPacket(hsmsStreamFunctionHeader(6, 12, False, packet.header.system), s6f12.encode())

	connection.sendPacket(responsePacket)

def S5F1Handler(connection, packet):
	s5f2 = secsS5F2(chr(0x00))
	responsePacket = hsmsPacket(hsmsStreamFunctionHeader(5, 2, False, packet.header.system), s5f2.encode())

	connection.sendPacket(responsePacket)

server = hsmsServer(13002)

server.registerCallback( 1,  1, S1F1Handler)
server.registerCallback( 1, 13, S1F13Handler)
server.registerCallback( 5,  1, S5F1Handler)
server.registerCallback( 6, 11, S6F11Handler)

server.Listen()

if not earlyS1F13:
	s1f13 = secsS1F13("pysecs", "prototype")
	packet = hsmsPacket(hsmsStreamFunctionHeader(1,13, False), s1f13.encode())

	client.sendPacket(packet)
	packet = client.waitforStreamFunction(1,14)

try:
	while server.connected:
		time.sleep(1)
except KeyboardInterrupt:
	server.Disconnect()
	del cansim



