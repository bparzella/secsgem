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
	connection.send_response(SecsS01F02(), packet.header.system)
	
def S1F13Handler(connection, packet):
	global earlyS1F13
	earlyS1F13 = True
	
	connection.send_response(SecsS01F14H({"COMMACK": 0}), packet.header.system)
	
def S6F11Handler(connection, packet):
	connection.send_response(SecsS06F12(0), packet.header.system)

def S5F1Handler(connection, packet):
	connection.send_response(SecsS05F02(0), packet.header.system)
	
client = hsmsClient("10.211.55.32", 5000)

client.register_callback( 1,  1, S1F1Handler)
client.register_callback( 1, 13, S1F13Handler)
client.register_callback( 5,  1, S5F1Handler)
client.register_callback( 6, 11, S6F11Handler)

connection = client.connect()

if not earlyS1F13:
	packet = connection.send_and_waitfor_response(SecsS01F13H())

#disable all ceids
packet = connection.send_and_waitfor_response(SecsS02F37({"CEED": False, "CEID": []}))

#delete all reports
packet = connection.send_and_waitfor_response(SecsS02F33({"DATAID": 0, "DATA": []}))

#create reports
packet = connection.send_and_waitfor_response(SecsS02F33({"DATAID": 0, "DATA": [{"RPTID": 1000, "RPT": [400]}]}))

#link event reports
packet = connection.send_and_waitfor_response(SecsS02F35({"DATAID": 0, "DATA": [{"CEID": 469, "CE": [1000]}]}))

#enable ceids
packet = connection.send_and_waitfor_response(SecsS02F37({"CEED": True, "CEID": [469]}))

packet = connection.send_and_waitfor_response(secsS10F11())

try:
	while connection.connected:
		time.sleep(1)
except KeyboardInterrupt:
	connection.disconnect()
