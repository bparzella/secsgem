#####################################################################
# gem_equipment.py
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

import secsgem.secs
import secsgem.gem

from communication_log_file_handler import CommunicationLogFileHandler


class SampleEquipment(secsgem.gem.GemEquipmentHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.MDLN = "gemequp"
        self.SOFTREV = "1.0.0"

        self.sv1 = 123
        self.sv2 = "sample sv"

        self.status_variables.update({
            10: secsgem.gem.StatusVariable(10, "sample1, numeric SVID, U4", "meters", secsgem.secs.variables.U4),
            "SV2": secsgem.gem.StatusVariable("SV2", "sample2, text SVID, String", "chars", secsgem.secs.variables.String),
        })

        self.ec1 = 321
        self.ec2 = "sample ec"

        self.equipment_constants.update({
            20: secsgem.gem.EquipmentConstant(20, "sample1, numeric ECID, U4", 0, 500, 50, "degrees", secsgem.secs.variables.U4),
            "EC2": secsgem.gem.EquipmentConstant("EC2", "sample2, text ECID, String", "", "", "", "chars", secsgem.secs.variables.String),
        })

    def on_sv_value_request(self, svid, sv):
        if sv.svid == 10:
            return sv.value_type(self.sv1)
        elif sv.svid == "SV2":
            return sv.value_type(self.sv2)

        return []

    def on_ec_value_request(self, ecid, ec):
        if ec.ecid == 20:
            return ec.value_type(self.ec1)
        elif ec.ecid == "EC2":
            return ec.value_type(self.ec2)

        return []

    def on_ec_value_update(self, ecid, ec, value):
        if ec.ecid == 2:
            self.ec1 = value
        elif ec.ecid == "EC2":
            self.ec2 = value


commLogFileHandler = CommunicationLogFileHandler("log", "e")
commLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger("hsms_communication").addHandler(commLogFileHandler)
logging.getLogger("hsms_communication").propagate = False

logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)

h = SampleEquipment("127.0.0.1", 5000, False, 0, "sampleequipment")
h.enable()

code.interact("equipment object is available as variable 'h'", local=locals())

h.disable()
