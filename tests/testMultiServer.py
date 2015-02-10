#####################################################################
# testMultiServer.py
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
import time

from secsgem import *

running = True

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def connectionCallback(connection):
	print "testMultiServer.connectionCallback:", connection

	global running
	running = False

server = hsmsMultiServer(5000, connectionCallback)
server.start()

while running:
	time.sleep(1)

time.sleep(3)

server.stop()
