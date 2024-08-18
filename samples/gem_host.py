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

import secsgem.common
import secsgem.gem
import secsgem.hsms

from communication_log_file_handler import CommunicationLogFileHandler

class SampleHost(secsgem.gem.GemHostHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)

        self.MDLN = "gemhost"
        self.SOFTREV = "1.0.0"

commLogFileHandler = CommunicationLogFileHandler("log", "h")
commLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger("communication").addHandler(commLogFileHandler)
logging.getLogger("communication").propagate = False

logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)

settings = secsgem.hsms.HsmsSettings(
    address="127.0.0.1",
    port=5000,
    connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE,
    device_type=secsgem.common.DeviceType.HOST
)

h = SampleHost(settings)
h.enable()

code.interact("host object is available as variable 'h'", local=locals())

h.disable()
