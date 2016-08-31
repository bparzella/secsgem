#####################################################################
# testGemEquipmentHandler.py
#
# (c) Copyright 2013-2016, Benjamin Parzella. All rights reserved.
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

import unittest

from secsgem.secs.variables import SecsVarString, SecsVarU4
from secsgem.gem.equipmenthandler import DataValue, StatusVariable, CollectionEvent, \
    CollectionEventLink, CollectionEventReport, EquipmentConstant

class TestDataValue(unittest.TestCase):
    def testConstructorWithInt(self):
        dv = DataValue(123, "TestDataValue", SecsVarString, False, param1="param1", param2=2)

        self.assertEqual(dv.dvid, 123)
        self.assertEqual(dv.name, "TestDataValue")
        self.assertEqual(dv.value_type, SecsVarString)
        self.assertEqual(dv.use_callback, False)
        self.assertEqual(dv.param1, "param1")
        self.assertEqual(dv.param2, 2)

    def testConstructorWithStr(self):
        dv = DataValue("DV123", "TestDataValue", SecsVarString, False, param1="param1", param2=2)

        self.assertEqual(dv.dvid, "DV123")
        self.assertEqual(dv.name, "TestDataValue")
        self.assertEqual(dv.value_type, SecsVarString)
        self.assertEqual(dv.use_callback, False)
        self.assertEqual(dv.param1, "param1")
        self.assertEqual(dv.param2, 2)


class TestStatusVariable(unittest.TestCase):
    def testConstructorWithInt(self):
        sv = StatusVariable(123, "TestStatusVariable", "mm", SecsVarString, False, param1="param1", param2=2)

        self.assertEqual(sv.svid, 123)
        self.assertEqual(sv.name, "TestStatusVariable")
        self.assertEqual(sv.unit, "mm")
        self.assertEqual(sv.value_type, SecsVarString)
        self.assertEqual(sv.use_callback, False)
        self.assertEqual(sv.param1, "param1")
        self.assertEqual(sv.param2, 2)

    def testConstructorWithStr(self):
        sv = StatusVariable("SV123", "TestStatusVariable", "mm", SecsVarString, False, param1="param1", param2=2)

        self.assertEqual(sv.svid, "SV123")
        self.assertEqual(sv.name, "TestStatusVariable")
        self.assertEqual(sv.unit, "mm")
        self.assertEqual(sv.value_type, SecsVarString)
        self.assertEqual(sv.use_callback, False)
        self.assertEqual(sv.param1, "param1")
        self.assertEqual(sv.param2, 2)


class TestCollectionEvent(unittest.TestCase):
    def testConstructorWithInt(self):
        ce = CollectionEvent(123, "TestCollectionEvent", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(ce.ceid, 123)
        self.assertEqual(ce.name, "TestCollectionEvent")
        self.assertEqual(ce.data_values, [123, "DV123"])
        self.assertEqual(ce.param1, "param1")
        self.assertEqual(ce.param2, 2)

    def testConstructorWithStr(self):
        ce = CollectionEvent("CE123", "TestCollectionEvent", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(ce.ceid, "CE123")
        self.assertEqual(ce.name, "TestCollectionEvent")
        self.assertEqual(ce.data_values, [123, "DV123"])
        self.assertEqual(ce.param1, "param1")
        self.assertEqual(ce.param2, 2)


class TestCollectionEventLink(unittest.TestCase):
    def testConstructor(self):
        ce = CollectionEvent(123, "TestCollectionEvent", [123, "DV123"])
        cel = CollectionEventLink(ce, [1000], param1="param1", param2=2)

        self.assertEqual(cel.ce, ce)
        self.assertEqual(cel.enabled, False)
        self.assertEqual(cel.reports, [1000])
        self.assertEqual(cel.param1, "param1")
        self.assertEqual(cel.param2, 2)


class TestCollectionEventReport(unittest.TestCase):
    def testConstructorWithInt(self):
        cer = CollectionEventReport(123, [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(cer.rptid, 123)
        self.assertEqual(cer.vars, [123, "DV123"])
        self.assertEqual(cer.param1, "param1")
        self.assertEqual(cer.param2, 2)

    def testConstructorWithStr(self):
        cer = CollectionEventReport("RPT123", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(cer.rptid, "RPT123")
        self.assertEqual(cer.vars, [123, "DV123"])
        self.assertEqual(cer.param1, "param1")
        self.assertEqual(cer.param2, 2)


class TestEquipmentConstant(unittest.TestCase):
    def testConstructorWithInt(self):
        ec = EquipmentConstant(123, "TestEquipmentConstant", 0, 100, 50, "mm", SecsVarU4, False, param1="param1", param2=2)

        self.assertEqual(ec.ecid, 123)
        self.assertEqual(ec.name, "TestEquipmentConstant")
        self.assertEqual(ec.min_value, 0)
        self.assertEqual(ec.max_value, 100)
        self.assertEqual(ec.default_value, 50)
        self.assertEqual(ec.unit, "mm")
        self.assertEqual(ec.value_type, SecsVarU4)
        self.assertEqual(ec.use_callback, False)
        self.assertEqual(ec.param1, "param1")
        self.assertEqual(ec.param2, 2)

    def testConstructorWithStr(self):
        ec = EquipmentConstant("EC123", "TestEquipmentConstant", 0, 100, 50, "mm", SecsVarU4, False, param1="param1", param2=2)

        self.assertEqual(ec.ecid, "EC123")
        self.assertEqual(ec.name, "TestEquipmentConstant")
        self.assertEqual(ec.min_value, 0)
        self.assertEqual(ec.max_value, 100)
        self.assertEqual(ec.default_value, 50)
        self.assertEqual(ec.unit, "mm")
        self.assertEqual(ec.value_type, SecsVarU4)
        self.assertEqual(ec.use_callback, False)
        self.assertEqual(ec.param1, "param1")
        self.assertEqual(ec.param2, 2)


