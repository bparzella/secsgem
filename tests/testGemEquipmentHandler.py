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

import threading
import unittest

import secsgem
from secsgem.secs.variables import SecsVarString, SecsVarU4
from secsgem.gem.equipmenthandler import DataValue, StatusVariable, CollectionEvent, \
    CollectionEventLink, CollectionEventReport, EquipmentConstant

from testGemHandler import GemHandlerPassiveGroup
from testconnection import HsmsTestServer

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

class TestGemEquipmentHandler(unittest.TestCase):
    def testControlInitialStateDefault(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        self.assertEqual(client.controlState.current, "HOST_OFFLINE")

    def testControlInitialStateEquipmentOffline(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="EQUIPMENT_OFFLINE")

        self.assertEqual(client.controlState.current, "EQUIPMENT_OFFLINE")

    def testControlInitialStateHostOffline(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="HOST_OFFLINE")

        self.assertEqual(client.controlState.current, "HOST_OFFLINE")

    def testControlInitialStateOnline(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="ONLINE")

        self.assertEqual(client.controlState.current, "ONLINE_REMOTE")

    def testControlInitialStateOnlineLocal(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.controlState.current, "ONLINE_LOCAL")

    def testControlRemoteToLocal(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="ONLINE")

        self.assertEqual(client.controlState.current, "ONLINE_REMOTE")

        client.control_switch_online_local()

        self.assertEqual(client.controlState.current, "ONLINE_LOCAL")

    def testControlLocalToRemote(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.controlState.current, "ONLINE_LOCAL")

        client.control_switch_online_remote()

        self.assertEqual(client.controlState.current, "ONLINE_REMOTE")

    def testControlOnlineToOffline(self):
        server = HsmsTestServer()
        client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, server, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.controlState.current, "ONLINE_LOCAL")

        client.control_switch_offline()
        
        self.assertEqual(client.controlState.current, "EQUIPMENT_OFFLINE")


class TestGemEquipmentHandlerPassive(unittest.TestCase, GemHandlerPassiveGroup):
    __testClass = secsgem.GemEquipmentHandler
    
    def setUp(self):
        self.assertIsNotNone(self.__testClass)

        self.server = HsmsTestServer()

        self.client = self.__testClass("127.0.0.1", 5000, False, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.client.disable()
        self.server.stop()


class TestGemEquipmentHandlerPassiveControlState(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer()

        self.client = secsgem.GemEquipmentHandler("127.0.0.1", 5000, False, 0, "test", None, self.server, initial_control_state="EQUIPMENT_OFFLINE")

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.client.disable()
        self.server.stop()

    def establishCommunication(self):
        self.server.simulate_connect()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.HsmsPacket(secsgem.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        packet = self.server.expect_packet(function=13)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F14([0])))

    def testControlConnect(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlConnect")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

    def testControlConnectDenied(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlConnectDenied")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F00()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

        self.assertEqual(self.client.controlState.current, "HOST_OFFLINE")

    def testControlRequestOffline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOffline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F15()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 16)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.controlState.current, "HOST_OFFLINE")

    def testControlRequestOnline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOnline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F15()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 16)

        self.assertEqual(self.client.controlState.current, "HOST_OFFLINE")

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F17()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 18)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

    def testControlRequestOnlineWhileOnline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOnline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F17()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 18)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.get(), 2)

        self.assertEqual(self.client.controlState.current, "ONLINE_REMOTE")

    def testStatusVariableNameListAll(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F11()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,12)

        function = self.client.secs_decode(packet)

        SV2 = next((x for x in function if x[0].get() == "SV2"), None)

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2[1].get(), u"sample2, text SVID, SecsVarString")
        self.assertEqual(SV2[2].get(), "chars")

        SV10 = next((x for x in function if x[0].get() == 10), None)

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10[1].get(), u"sample1, numeric SVID, SecsVarU4")
        self.assertEqual(SV10[2].get(), "meters")

    def testStatusVariableNameListLimited(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F11(["SV2", 10])))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,12)

        function = self.client.secs_decode(packet)

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2[0].get(), u"SV2")
        self.assertEqual(SV2[1].get(), u"sample2, text SVID, SecsVarString")
        self.assertEqual(SV2[2].get(), "chars")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10[0].get(), 10)
        self.assertEqual(SV10[1].get(), u"sample1, numeric SVID, SecsVarU4")
        self.assertEqual(SV10[2].get(), "meters")

    def testStatusVariableNameListInvalid(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F11(["asdfg"])))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,12)

        function = self.client.secs_decode(packet)

        SV = function[0]

        self.assertIsNotNone(SV)
        self.assertEqual(SV[0].get(), u"asdfg")
        self.assertEqual(SV[1].get(), u"")
        self.assertEqual(SV[2].get(), "")

    def testStatusVariableAll(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F03()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,4)

        function = self.client.secs_decode(packet)

        SV10 = next((x for x in function if x.get() == 123), None)
        self.assertIsNotNone(SV10)

        SV2 = next((x for x in function if x.get() == u"sample sv"), None)
        self.assertIsNotNone(SV2)

    def testStatusVariableLimited(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F03(["SV2", 10])))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,4)

        function = self.client.secs_decode(packet)

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.get(), u"sample sv")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.get(), 123)

    def testStatusVariableWithCallback(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, True),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, True),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F03(["SV2", 10])))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,4)

        function = self.client.secs_decode(packet)

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.get(), u"sample sv")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.get(), 123)

    def testStatusVariableInvalid(self):
        self.client.status_variables.update({
            10: secsgem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.SecsVarU4, False),
            "SV2": secsgem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.SecsVarString, False),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"
        
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F03(["asdfg"])))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function,4)

        function = self.client.secs_decode(packet)

        SV = function[0]

        self.assertIsNotNone(SV)
        self.assertEqual(SV.get(), None)
