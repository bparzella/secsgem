#####################################################################
# client.py
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
	connection.sendResponse(secsS1F2("pysecs", "prototype"), packet.header.system)
	
def S1F13Handler(connection, packet):
	global earlyS1F13
	earlyS1F13 = True
	
	connection.sendResponse(secsS1F14(chr(0x00), "pysecs", "prototype"), packet.header.system)
	
def S6F11Handler(connection, packet):
	connection.sendResponse(secsS6F12(chr(0x00)), packet.header.system)

def S5F1Handler(connection, packet):
	connection.sendResponse(secsS5F2(chr(0x00)), packet.header.system)
	
client = hsmsClient("10.211.55.32", 5000)

client.registerCallback( 1,  1, S1F1Handler)
client.registerCallback( 1, 13, S1F13Handler)
client.registerCallback( 5,  1, S5F1Handler)
client.registerCallback( 6, 11, S6F11Handler)

connection = client.connect()

if not earlyS1F13:
	packet = connection.sendAndWaitForResponse(secsS1F13("pysecs", "prototype"))

#disable all ceids
packet = connection.sendAndWaitForResponse(secsS2F37(False, []))

#delete all reports
packet = connection.sendAndWaitForResponse(secsS2F33(0, []))

#create reports
packet = connection.sendAndWaitForResponse(secsS2F33(0, [[1000, [400]]]))

#link event reports
packet = connection.sendAndWaitForResponse(secsS2F35(0, [[469, [1000]]]))

#enable ceids
packet = connection.sendAndWaitForResponse(secsS2F37(True, [469]))

packet = connection.sendAndWaitForResponse(secsS1F11([]))

try:
	while connection.connected:
		time.sleep(1)
except KeyboardInterrupt:
	connection.disconnect()
