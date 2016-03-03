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

import secsgem

class SampleEquipment(secsgem.GemEquipmentHandler):
    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        secsgem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

        self.sv1 = 123
        self.sv2 = "sample sv"
        self.status_variables.update({
            1: secsgem.StatusVariable(1, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString),
        })

        self.ec1 = 321
        self.ec2 = "sample ec"
        self.equipment_constants.update({
            2: secsgem.EquipmentConstant(2, "sample1, numeric ECID, SecsVarU4", 0, 500, 50, "degrees", secsgem.SecsVarU4),
            "EC2": secsgem.EquipmentConstant("EC2", "sample2, text ECID, SecsVarString", "", "", "", "chars", secsgem.SecsVarString),
        })

    def on_sv_value_request(self, svid, sv):
        if sv.svid == 1:
            return sv.value_type(value=self.sv1)
        elif sv.svid == "SV2":
            return sv.value_type(value=self.sv2)

        return []

    def on_ec_value_request(self, ecid, ec):
        if ec.ecid == 2:
            return ec.value_type(value=self.ec1)
        elif ec.ecid == "EC2":
            return ec.value_type(value=self.ec2)

        return []

    def on_ec_value_update(self, ecid, ec, value):
        if ec.ecid == 2:
            self.ec1 = value
        elif ec.ecid == "EC2":
            self.ec2 = value


logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)

h = SampleEquipment("127.0.0.1", 5000, True, 0, "test")
h.enable()

print "equipment is available as variable 'h'"

code.interact(local=locals())

h.disable()
