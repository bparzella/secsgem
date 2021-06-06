#####################################################################
# gem_host.py
#
# (c) Copyright 2016, Benjamin Parzella. All rights reserved.
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
import code

import secsgem.gem

from communication_log_file_handler import CommunicationLogFileHandler

class SampleHost(secsgem.gem.GemHostHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.gem.GemHostHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.MDLN = "gemhost"
        self.SOFTREV = "1.0.0"

commLogFileHandler = CommunicationLogFileHandler("log", "h")
commLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger("hsms_communication").addHandler(commLogFileHandler)
logging.getLogger("hsms_communication").propagate = False

logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)

h = SampleHost("127.0.0.1", 5000, False, 0, "samplehost")
h.enable()

code.interact("host object is available as variable 'h'", local=locals())

h.disable()
