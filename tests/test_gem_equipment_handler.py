#####################################################################
# test_gem_equipment_handler.py
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

import datetime
import threading
import unittest.mock

from dateutil.tz import tzlocal
from dateutil.parser import parse

import secsgem.hsms
import secsgem.secs
import secsgem.gem
import secsgem.gem.control_state_machine

import secsgem.secs.data_item
from test_gem_handler import GemHandlerPassiveGroup

from mock_protocol import MockProtocol
from mock_settings import MockSettings


class TestDataValue:
    def testConstructorWithInt(self):
        dv = secsgem.gem.DataValue(123, "TestDataValue", secsgem.secs.ItemA, False, param1="param1", param2=2)

        assert dv.dvid == 123
        assert dv.name == "TestDataValue"
        assert dv.value_type == secsgem.secs.ItemA
        assert dv.use_callback == False
        assert dv.param1 == "param1"
        assert dv.param2 == 2

    def testConstructorWithStr(self):
        dv = secsgem.gem.DataValue("DV123", "TestDataValue", secsgem.secs.ItemA, False, param1="param1", param2=2)

        assert dv.dvid == "DV123"
        assert dv.name == "TestDataValue"
        assert dv.value_type == secsgem.secs.ItemA
        assert dv.use_callback == False
        assert dv.param1 == "param1"
        assert dv.param2 == 2


class TestStatusVariable(unittest.TestCase):
    def testConstructorWithInt(self):
        sv = secsgem.gem.StatusVariable(123, "TestStatusVariable", "mm", secsgem.secs.ItemA, False, param1="param1", param2=2)

        self.assertEqual(sv.svid, 123)
        self.assertEqual(sv.name, "TestStatusVariable")
        self.assertEqual(sv.unit, "mm")
        self.assertEqual(sv.value_type, secsgem.secs.ItemA)
        self.assertEqual(sv.use_callback, False)
        self.assertEqual(sv.param1, "param1")
        self.assertEqual(sv.param2, 2)

    def testConstructorWithStr(self):
        sv = secsgem.gem.StatusVariable("SV123", "TestStatusVariable", "mm", secsgem.secs.ItemA, False, param1="param1", param2=2)

        self.assertEqual(sv.svid, "SV123")
        self.assertEqual(sv.name, "TestStatusVariable")
        self.assertEqual(sv.unit, "mm")
        self.assertEqual(sv.value_type, secsgem.secs.ItemA)
        self.assertEqual(sv.use_callback, False)
        self.assertEqual(sv.param1, "param1")
        self.assertEqual(sv.param2, 2)


class TestCollectionEvent(unittest.TestCase):
    def testConstructorWithInt(self):
        ce = secsgem.gem.CollectionEvent(123, "TestCollectionEvent", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(ce.ceid, 123)
        self.assertEqual(ce.name, "TestCollectionEvent")
        self.assertEqual(ce.data_values, [123, "DV123"])
        self.assertEqual(ce.param1, "param1")
        self.assertEqual(ce.param2, 2)

    def testConstructorWithStr(self):
        ce = secsgem.gem.CollectionEvent("CE123", "TestCollectionEvent", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(ce.ceid, "CE123")
        self.assertEqual(ce.name, "TestCollectionEvent")
        self.assertEqual(ce.data_values, [123, "DV123"])
        self.assertEqual(ce.param1, "param1")
        self.assertEqual(ce.param2, 2)


class TestCollectionEventLink(unittest.TestCase):
    def testConstructor(self):
        ce = secsgem.gem.CollectionEvent(123, "TestCollectionEvent", [123, "DV123"])
        cel = secsgem.gem.CollectionEventLink(ce, [1000], param1="param1", param2=2)

        self.assertEqual(cel.collection_event, ce)
        self.assertEqual(cel.enabled, False)
        self.assertEqual(cel.reports, [1000])
        self.assertEqual(cel.param1, "param1")
        self.assertEqual(cel.param2, 2)


class TestCollectionEventReport(unittest.TestCase):
    def testConstructorWithInt(self):
        cer = secsgem.gem.CollectionEventReport(123, [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(cer.rptid, 123)
        self.assertEqual(cer.vars, [123, "DV123"])
        self.assertEqual(cer.param1, "param1")
        self.assertEqual(cer.param2, 2)

    def testConstructorWithStr(self):
        cer = secsgem.gem.CollectionEventReport("RPT123", [123, "DV123"], param1="param1", param2=2)

        self.assertEqual(cer.rptid, "RPT123")
        self.assertEqual(cer.vars, [123, "DV123"])
        self.assertEqual(cer.param1, "param1")
        self.assertEqual(cer.param2, 2)


class TestEquipmentConstant(unittest.TestCase):
    def testConstructorWithInt(self):
        ec = secsgem.gem.EquipmentConstant(123, "TestEquipmentConstant", 0, 100, 50, "mm", secsgem.secs.ItemU4, False, param1="param1", param2=2)

        self.assertEqual(ec.ecid, 123)
        self.assertEqual(ec.name, "TestEquipmentConstant")
        self.assertEqual(ec.min_value, 0)
        self.assertEqual(ec.max_value, 100)
        self.assertEqual(ec.default_value, 50)
        self.assertEqual(ec.unit, "mm")
        self.assertEqual(ec.value_type, secsgem.secs.ItemU4)
        self.assertEqual(ec.use_callback, False)
        self.assertEqual(ec.param1, "param1")
        self.assertEqual(ec.param2, 2)

    def testConstructorWithStr(self):
        ec = secsgem.gem.EquipmentConstant("EC123", "TestEquipmentConstant", 0, 100, 50, "mm", secsgem.secs.ItemU4, False, param1="param1", param2=2)

        self.assertEqual(ec.ecid, "EC123")
        self.assertEqual(ec.name, "TestEquipmentConstant")
        self.assertEqual(ec.min_value, 0)
        self.assertEqual(ec.max_value, 100)
        self.assertEqual(ec.default_value, 50)
        self.assertEqual(ec.unit, "mm")
        self.assertEqual(ec.value_type, secsgem.secs.ItemU4)
        self.assertEqual(ec.use_callback, False)
        self.assertEqual(ec.param1, "param1")
        self.assertEqual(ec.param2, 2)


class TestAlarm:
    def setup_class(self):
        self.data_items = secsgem.secs.data_item.DataItems()

    def testConstructorWithInt(self):
        alarm = secsgem.gem.Alarm(123, "TestAlarm", "TestAlarmText", self.data_items.ALCD.PERSONAL_SAFETY |
                                  self.data_items.ALCD.EQUIPMENT_SAFETY, 100025, 200025, param1="param1", param2=2)

        assert alarm.alid == 123
        assert alarm.name == "TestAlarm"
        assert alarm.text == "TestAlarmText"
        assert alarm.code == self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY
        assert alarm.ce_on == 100025
        assert alarm.ce_off == 200025
        assert alarm.param1 == "param1"
        assert alarm.param2 == 2

    def testConstructorWithStr(self):
        alarm = secsgem.gem.Alarm("AL123", "TestAlarm", "TestAlarmText", self.data_items.ALCD.PERSONAL_SAFETY |
                                  self.data_items.ALCD.EQUIPMENT_SAFETY, 100025, 200025, param1="param1", param2=2)

        assert alarm.alid == "AL123"
        assert alarm.name == "TestAlarm"
        assert alarm.text == "TestAlarmText"
        assert alarm.code == self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY
        assert alarm.ce_on == 100025
        assert alarm.ce_off == 200025
        assert alarm.param1 == "param1"
        assert alarm.param2 == 2


class TestRemoteCommand(unittest.TestCase):
    def testConstructorWithInt(self):
        rcmd = secsgem.gem.RemoteCommand(123, "TestRCMD", [], 100025, param1="param1", param2=2)

        self.assertEqual(rcmd.rcmd, 123)
        self.assertEqual(rcmd.name, "TestRCMD")
        self.assertEqual(rcmd.params, [])
        self.assertEqual(rcmd.ce_finished, 100025)
        self.assertEqual(rcmd.param1, "param1")
        self.assertEqual(rcmd.param2, 2)

    def testConstructorWithStr(self):
        rcmd = secsgem.gem.RemoteCommand("TEST_RCMD", "TestRCMD", [], 100025, param1="param1", param2=2)

        self.assertEqual(rcmd.rcmd, "TEST_RCMD")
        self.assertEqual(rcmd.name, "TestRCMD")
        self.assertEqual(rcmd.params, [])
        self.assertEqual(rcmd.ce_finished, 100025)
        self.assertEqual(rcmd.param1, "param1")
        self.assertEqual(rcmd.param2, 2)


class TestGemEquipmentHandler(unittest.TestCase):
    def testControlInitialStateDefault(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings)

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.HOST_OFFLINE)

    def testControlInitialStateEquipmentOffline(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="EQUIPMENT_OFFLINE")

        self.assertEqual(client.control_state.current,  secsgem.gem.control_state_machine.ControlState.EQUIPMENT_OFFLINE)

    def testControlInitialStateHostOffline(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="HOST_OFFLINE")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.HOST_OFFLINE)
        self.assertEqual(client._get_control_state_id(), 3)

    def testControlInitialStateOnline(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)
        self.assertEqual(client._get_control_state_id(), 5)

    def testControlInitialStateOnlineLocal(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_LOCAL)

    def testControlRemoteToLocal(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

        client.control_switch_online_local()

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_LOCAL)

    def testControlLocalToRemote(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_LOCAL)

        client.control_switch_online_remote()

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

    def testControlOnlineToOffline(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_LOCAL)

        client.control_switch_offline()

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.EQUIPMENT_OFFLINE)

    def testSVcontrol_stateOnlineLocal(self):
        settings = MockSettings(MockProtocol)
        client = secsgem.gem.GemEquipmentHandler(settings, initial_control_state="ONLINE", initial_online_control_state="LOCAL")

        self.assertEqual(client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_LOCAL)
        self.assertEqual(client._get_control_state_id(), 4)


class TestGemEquipmentHandlerPassive(unittest.TestCase, GemHandlerPassiveGroup):
    __testClass = secsgem.gem.GemEquipmentHandler

    def setUp(self):
        self.assertIsNotNone(self.__testClass)

        self.settings = MockSettings(MockProtocol)
        self.client = self.__testClass(self.settings)

        self.client.enable()

    def tearDown(self):
        self.client.disable()


class TestGemEquipmentHandlerPassiveControlState(unittest.TestCase):
    def setUp(self):
        self.settings = MockSettings(MockProtocol)

        self.client = secsgem.gem.GemEquipmentHandler(self.settings, initial_control_state="EQUIPMENT_OFFLINE")

        self.client.enable()

    def tearDown(self):
        self.client.disable()

    def establishCommunication(self):
        self.settings.protocol.simulate_connect()

        packet = self.settings.protocol.expect_message(function=13)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(
            self.settings.streams_functions(1, 14, [0, []]), packet.header.system))

    def testControlConnect(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlConnect")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 2), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

    def testControlConnectDenied(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlConnectDenied")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.HOST_OFFLINE)

    def testControlRequestOffline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOffline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 2), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 15), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 16)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(function.value, 0)

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.HOST_OFFLINE)

    def testControlRequestOnline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOnline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 2), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 15), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 16)

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.HOST_OFFLINE)

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 17), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 18)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(function.value, 0)

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

    def testControlRequestOnlineWhileOnline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.control_switch_online, name="TestGemEquipmentHandlerPassiveControlState_testControlRequestOnline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 2), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 17), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 18)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(function.get(), 2)

        self.assertEqual(self.client.control_state.current, secsgem.gem.control_state_machine.ControlState.ONLINE_REMOTE)

    def setupTestStatusVariables(self, use_callback=False):
        self.client.status_variables.update({
            10: secsgem.gem.StatusVariable(10, "sample1, numeric SVID, U4", "meters", secsgem.secs.ItemU4, use_callback),
            "SV2": secsgem.gem.StatusVariable("SV2", "sample2, text SVID, String", "chars", secsgem.secs.ItemA, use_callback),
        })

        self.client.status_variables[10].value = 123
        self.client.status_variables["SV2"].value = "sample sv"

    def sendSVNamelistRequest(self, svs=[]):
        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 11, svs), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 12)

        return self.client.settings.streams_functions.from_message(packet)

    def testStatusVariableNameListAll(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVNamelistRequest().value

        SV2 = next((x for x in function if x.SVID == "SV2"), None)

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.SVNAME, u"sample2, text SVID, String")
        self.assertEqual(SV2.UNITS, "chars")

        SV10 = next((x for x in function if x.SVID == 10), None)

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.SVNAME, u"sample1, numeric SVID, U4")
        self.assertEqual(SV10.UNITS, "meters")

    def testStatusVariableNameListLimited(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVNamelistRequest(["SV2", 10]).value

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.SVID, u"SV2")
        self.assertEqual(SV2.SVNAME, u"sample2, text SVID, String")
        self.assertEqual(SV2.UNITS, "chars")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.SVID, 10)
        self.assertEqual(SV10.SVNAME, u"sample1, numeric SVID, U4")
        self.assertEqual(SV10.UNITS, "meters")

    def testStatusVariableNameListInvalid(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVNamelistRequest(["asdfg"]).value

        SV = function[0]

        self.assertIsNotNone(SV)
        self.assertEqual(SV.SVID, u"asdfg")
        self.assertEqual(SV.SVNAME, u"")
        self.assertEqual(SV.UNITS, "")

    def sendSVRequest(self, svs=[]):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(1, 3, svs), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 4)

        return self.client.settings.streams_functions.from_message(packet)

    def testStatusVariableAll(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVRequest()

        SV10 = next((x for x in function if x.get() == 123), None)
        self.assertIsNotNone(SV10)

        SV2 = next((x for x in function if x.get() == u"sample sv"), None)
        self.assertIsNotNone(SV2)

    def testStatusVariableLimited(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVRequest(["SV2", 10])

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.get(), u"sample sv")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.get(), 123)

    def testStatusVariableWithCallback(self):
        self.setupTestStatusVariables(True)
        self.establishCommunication()

        function = self.sendSVRequest(["SV2", 10])

        SV2 = function[0]

        self.assertIsNotNone(SV2)
        self.assertEqual(SV2.get(), u"sample sv")

        SV10 = function[1]

        self.assertIsNotNone(SV10)
        self.assertEqual(SV10.get(), 123)

    def testStatusVariableInvalid(self):
        self.setupTestStatusVariables()
        self.establishCommunication()

        function = self.sendSVRequest(["asdfg"])

        SV = function[0]

        self.assertIsNotNone(SV)
        self.assertEqual(SV.get(), [])

    def testStatusVariablePredefinedClock(self):
        self.establishCommunication()

        delta = datetime.timedelta(seconds=5)

        # timeformat 0
        function = self.sendECUpdate([{"ECID": secsgem.gem.EquipmentConstantId.TIME_FORMAT.value, "ECV": secsgem.secs.ItemU4(0)}])

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.CLOCK.value])

        equ_time = function[0]
        now = datetime.datetime.now()

        self.assertIsNotNone(equ_time)

        equ_datetime = datetime.datetime.strptime(equ_time.get(), "%y%m%d%H%M%S")

        self.assertTrue(now - delta < equ_datetime < now + delta)

        # timeformat 1
        function = self.sendECUpdate([{"ECID": secsgem.gem.EquipmentConstantId.TIME_FORMAT.value, "ECV": secsgem.secs.ItemU4(1)}])

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.CLOCK.value])

        equ_time = function[0]
        now = datetime.datetime.now()

        self.assertIsNotNone(equ_time)

        equ_datetime = datetime.datetime.strptime(equ_time.get() + "000", "%Y%m%d%H%M%S%f")

        self.assertTrue(now - delta < equ_datetime < now + delta)

        # timeformat 2
        function = self.sendECUpdate([{"ECID": secsgem.gem.EquipmentConstantId.TIME_FORMAT.value, "ECV": secsgem.secs.ItemU4(2)}])

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.CLOCK.value])

        equ_time = function[0]
        now = datetime.datetime.now(tzlocal())

        self.assertIsNotNone(equ_time)

        equ_datetime = parse(equ_time.get())

        self.assertTrue(now - delta < equ_datetime < now + delta)

    def testStatusVariablePredefinedEventsEnabled(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        function = self.sendCEDefineReport()
        function = self.sendCELinkReport()
        function = self.sendCEEnableReport()

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.EVENTS_ENABLED.value])

        self.assertEqual(function[0].get(), [50])

    def testStatusVariablePredefinedAlarmsEnabled(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.ALARMS_ENABLED.value])
        self.assertEqual(function[0].get(), [])

        function = self.sendAlarmEnable()

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.ALARMS_ENABLED.value])
        self.assertEqual(function[0].get(), [25])

    def testStatusVariablePredefinedAlarmsSet(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.ALARMS_SET.value])
        self.assertEqual(function[0].get(), [])

        function = self.sendAlarmEnable()

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testStatusVariablePredefinedAlarmsSet")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.ALARMS_SET.value])
        self.assertEqual(function[0].get(), [25])

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testStatusVariablePredefinedAlarmsSet")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        function = self.sendSVRequest([secsgem.gem.StatusVariableId.ALARMS_SET.value])
        self.assertEqual(function[0].get(), [])

    def setupTestDataValues(self, use_callbacks=False):
        self.client.data_values.update({
            30: secsgem.gem.DataValue(30, "sample1, numeric DV, U4", secsgem.secs.ItemU4, use_callbacks),
        })

        self.client.data_values[30].value = 31337

    def setupTestCollectionEvents(self):
        self.client.collection_events.update({
            50: secsgem.gem.CollectionEvent(50, "test collection event", [30]),
        })

    def setupTestAlarms(self):
        self.client.collection_events.update({
            100025: secsgem.gem.CollectionEvent(100025, "test alarm on", []),
            200025: secsgem.gem.CollectionEvent(200025, "test alarm off", []),
            100030: secsgem.gem.CollectionEvent(100030, "test alarm 2 on", []),
            200030: secsgem.gem.CollectionEvent(200030, "test alarm 2 off", []),
        })
        self.client.alarms.update({
            25: secsgem.gem.Alarm(25, "test alarm", "test text", self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY, 100025, 200025),
            30: secsgem.gem.Alarm(30, "test alarm 2", "test text 2", self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY, 100030, 200030),
        })

    def setupTestRemoteCommands(self):
        self.client.collection_events.update({
            5001: secsgem.gem.CollectionEvent(5001, "TEST_RCMD complete", []),
        })
        self.client.remote_commands.update({
            "TEST_RCMD": secsgem.gem.RemoteCommand("TEST_RCMD", "test rcmd", ["TEST_PARAMETER"], 5001),
        })

    def sendCEDefineReport(self, dataid=100, rptid=1000, vid=[30], empty_data=False):
        if not empty_data:
            data = {"DATAID": dataid, "DATA": [{"RPTID": rptid, "VID": vid}]}
        else:
            data = {"DATAID": dataid, "DATA": []}

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 33, data), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 34)

        return self.client.settings.streams_functions.from_message(packet)

    def sendCELinkReport(self, dataid=100, ceid=50, rptid=[1000], empty_data=False):
        if not empty_data:
            data = {"DATAID": dataid, "DATA": [{"CEID": ceid, "RPTID": rptid}]}
        else:
            data = {"DATAID": dataid, "DATA": []}

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 35, data), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 36)

        return self.client.settings.streams_functions.from_message(packet)

    def sendCEEnableReport(self, enable=True, ceid=[50]):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 37, {"CEED": enable, "CEID": ceid}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 38)

        return self.client.settings.streams_functions.from_message(packet)

    def sendAlarmEnable(self, enable=True, alid=25):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 3,
            {"ALED": self.data_items.ALED.ENABLE if enable else self.data_items.ALED.DISABLE, "ALID": alid}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 4)

        return self.client.settings.streams_functions.from_message(packet)

    def sendCERequestReport(self, ceid=50):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 15, ceid), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 16)

        return self.client.settings.streams_functions.from_message(packet)

    def testCollectionEventRegisterReport(self):
        self.setupTestDataValues()
        self.establishCommunication()

        oldlen = len(self.client.registered_reports)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.data)
        self.assertEqual(function.to_dict, bytes([0]))

        self.assertEqual(len(self.client.registered_reports), oldlen + 1)

    def testCollectionEventClearReports(self):
        self.setupTestDataValues()
        self.establishCommunication()

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertGreater(len(self.client.registered_reports), 0)

        function = self.sendCEDefineReport(empty_data=True)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), 0)

    def testCollectionEventRemoveReport(self):
        self.setupTestDataValues()
        self.establishCommunication()

        oldlen = len(self.client.registered_reports)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertGreater(len(self.client.registered_reports), 0)

        function = self.sendCEDefineReport(vid=[])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlen)

    def testCollectionEventRemoveReportWithLinkedCE(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCEDefineReport(vid=[])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT)
        self.assertEqual(len(self.client.registered_collection_events), oldlenCE)

    def testCollectionEventRegisterReportWithInvalidVID(self):
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[9876])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 4)

    def testCollectionEventDuplicateRegisterReport(self):
        self.setupTestDataValues()
        self.establishCommunication()

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 3)

    def testCollectionEventLinkReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

    def testCollectionEventLinkReportUnknownCEID(self):
        self.setupTestDataValues()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 4)

    def testCollectionEventDuplicateLinkReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 3)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

    def testCollectionEventLinkReportUnknown(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 5)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE)

    def testCollectionEventUnlinkReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCELinkReport(rptid=[])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE)

    def testCollectionEventLinkTwoReports(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCEDefineReport(rptid=1001)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 2)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCELinkReport(rptid=[1001])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

    def testCollectionEventEnableReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCEEnableReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

    def testCollectionEventEnableAllReports(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCEEnableReport(ceid=[])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

    def testCollectionEventEnableUnlinkedReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCEEnableReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 1)

    def testCollectionEventRequestReport(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCEEnableReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        function = self.sendCERequestReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), 50)
        self.assertEqual(function.RPT[0].RPTID.get(), 1000)
        self.assertEqual(function.RPT[0].V[0].get(), 31337)

    def testCollectionEventRequestReportCallbackSV(self):
        self.setupTestDataValues(True)
        self.setupTestCollectionEvents()
        self.setupTestStatusVariables(True)
        self.establishCommunication()

        oldlenRPT = len(self.client.registered_reports)
        oldlenCE = len(self.client.registered_collection_events)

        function = self.sendCEDefineReport(vid=[30, 10])

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_reports), oldlenRPT + 1)

        function = self.sendCELinkReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        self.assertEqual(len(self.client.registered_collection_events), oldlenCE + 1)

        function = self.sendCEEnableReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.get(), 0)

        function = self.sendCERequestReport()

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), 50)
        self.assertEqual(function.RPT[0].RPTID.get(), 1000)
        self.assertEqual(function.RPT[0].V[0].get(), 31337)
        self.assertEqual(function.RPT[0].V[1].get(), 123)

    def testCollectionEventTrigger(self):
        self.setupTestDataValues()
        self.setupTestCollectionEvents()
        self.establishCommunication()

        function = self.sendCEDefineReport()
        function = self.sendCELinkReport()
        function = self.sendCEEnableReport()

        clientCommandThread = threading.Thread(target=self.client.trigger_collection_events, args=(50,), name="TestGemEquipmentHandlerPassiveControlState_testCollectionEventTrigger")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), 50)
        self.assertEqual(function.RPT[0].RPTID.get(), 1000)
        self.assertEqual(function.RPT[0].V[0].get(), 31337)

    def setupTestEquipmentConstants(self, use_callback=False):
        self.client.equipment_constants.update({
            20: secsgem.gem.EquipmentConstant(20, "sample1, numeric ECID, I4", 0, 500, 50, "degrees", secsgem.secs.ItemI4, use_callback),
            "EC2": secsgem.gem.EquipmentConstant("EC2", "sample2, text ECID, String", None, None, "", "chars", secsgem.secs.ItemA, use_callback),
        })

        self.client.equipment_constants[20].value = 321
        self.client.equipment_constants["EC2"].value = "sample ec"

    def sendECNamelistRequest(self, ecid=[]):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 29, ecid), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 30)

        return self.client.settings.streams_functions.from_message(packet)

    def sendECRequest(self, ecid=[]):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 13, ecid), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 14)

        return self.client.settings.streams_functions.from_message(packet)

    def sendECUpdate(self, data):
        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 15, data), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 16)

        return self.client.settings.streams_functions.from_message(packet)

    def testEquipmentConstantNameListAll(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECNamelistRequest()

        EC2 = next((x for x in function if x[0].get() == "EC2"), None)

        self.assertIsNotNone(EC2)
        self.assertEqual(EC2[1].get(), u"sample2, text ECID, String")
        self.assertEqual(EC2[2].get(), "")
        self.assertEqual(EC2[3].get(), "")
        self.assertEqual(EC2[4].get(), "")
        self.assertEqual(EC2[5].get(), "chars")

        EC20 = next((x for x in function if x[0].get() == 20), None)

        self.assertIsNotNone(EC20)
        self.assertEqual(EC20[1].get(), u"sample1, numeric ECID, I4")
        self.assertEqual(EC20[2].get(), 0)
        self.assertEqual(EC20[3].get(), 500)
        self.assertEqual(EC20[4].get(), 50)
        self.assertEqual(EC20[5].get(), "degrees")

    def testEquipmentConstantNameListLimited(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECNamelistRequest(["EC2", 20])

        EC2 = function[0]

        self.assertIsNotNone(EC2)
        self.assertEqual(EC2[0].get(), u"EC2")
        self.assertEqual(EC2[1].get(), u"sample2, text ECID, String")
        self.assertEqual(EC2[2].get(), "")
        self.assertEqual(EC2[3].get(), "")
        self.assertEqual(EC2[4].get(), "")
        self.assertEqual(EC2[5].get(), "chars")

        EC20 = function[1]

        self.assertIsNotNone(EC20)
        self.assertEqual(EC20[0].get(), 20)
        self.assertEqual(EC20[1].get(), u"sample1, numeric ECID, I4")
        self.assertEqual(EC20[2].get(), 0)
        self.assertEqual(EC20[3].get(), 500)
        self.assertEqual(EC20[4].get(), 50)
        self.assertEqual(EC20[5].get(), "degrees")

    def testEquipmentConstantNameListInvalid(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECNamelistRequest(["asdfg"])

        EC2 = function[0]

        self.assertIsNotNone(EC2)
        self.assertEqual(EC2[0].get(), u"asdfg")
        self.assertEqual(EC2[1].get(), u"")
        self.assertEqual(EC2[2].get(), "")
        self.assertEqual(EC2[3].get(), "")
        self.assertEqual(EC2[4].get(), "")
        self.assertEqual(EC2[5].get(), "")

    def testEquipmentConstantGetAll(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECRequest()

        EC20 = next((x for x in function if x.get() == 321), None)
        self.assertIsNotNone(EC20)

        EC2 = next((x for x in function if x.get() == u"sample ec"), None)
        self.assertIsNotNone(EC2)

    def testEquipmentConstantGetLimited(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECRequest([20, "EC2"])

        EC20 = function[0]
        self.assertIsNotNone(EC20)
        self.assertEqual(EC20.get(), 321)

        EC2 = function[1]
        self.assertIsNotNone(EC2)
        self.assertEqual(EC2.get(), u"sample ec")

    def testEquipmentConstantGetCallback(self):
        self.setupTestEquipmentConstants(True)
        self.establishCommunication()

        function = self.sendECRequest([20, "EC2"])

        EC20 = function[0]
        self.assertIsNotNone(EC20)
        self.assertEqual(EC20.get(), 321)

        EC2 = function[1]
        self.assertIsNotNone(EC2)
        self.assertEqual(EC2.get(), u"sample ec")

    def testEquipmentConstantGetInvalid(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECRequest(["asdfg"])

        EC20 = function[0]
        self.assertIsNotNone(EC20)
        self.assertEqual(EC20.get(), [])

    def testEquipmentConstantSetLimited(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECUpdate([{"ECID": 20, "ECV": secsgem.secs.ItemI4(123)}, {"ECID": "EC2", "ECV": "ce elpmas"}])

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.equipment_constants[20].value, 123)
        self.assertEqual(self.client.equipment_constants["EC2"].value, "ce elpmas")

    def testEquipmentConstantSetTooLow(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECUpdate([{"ECID": 20, "ECV": secsgem.secs.ItemI4(-1)}])

        self.assertEqual(function.get(), 3)

        self.assertEqual(self.client.equipment_constants[20].value, 321)

    def testEquipmentConstantSetTooHigh(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECUpdate([{"ECID": 20, "ECV": secsgem.secs.ItemI4(501)}])

        self.assertEqual(function.get(), 3)

        self.assertEqual(self.client.equipment_constants[20].value, 321)

    def testEquipmentConstantSetCallback(self):
        self.setupTestEquipmentConstants(True)
        self.establishCommunication()

        function = self.sendECUpdate([{"ECID": 20, "ECV": secsgem.secs.ItemI4(123)}, {"ECID": "EC2", "ECV": "ce elpmas"}])

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.equipment_constants[20].value, 123)
        self.assertEqual(self.client.equipment_constants["EC2"].value, "ce elpmas")

    def testEquipmentConstantSetInvalid(self):
        self.setupTestEquipmentConstants()
        self.establishCommunication()

        function = self.sendECUpdate([{"ECID": "asdfg", "ECV": "ce elpmas"}])

        self.assertEqual(function.get(), 1)

    def testEquipmentConstantPredefinedEstablishCommunicationTimeout(self):
        self.client.equipment_constants[secsgem.gem.EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value].value = 10

        self.establishCommunication()

        function = self.sendECRequest([secsgem.gem.EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value])

        EC = function[0]
        self.assertIsNotNone(EC)
        self.assertEqual(EC.get(), 10)

        function = self.sendECUpdate([{"ECID": secsgem.gem.EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value, "ECV": secsgem.secs.ItemI4(20)}])

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.equipment_constants[secsgem.gem.EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value].value, 20)

    def testEquipmentConstantPredefinedTimeFormat(self):
        self.client.equipment_constants[secsgem.gem.EquipmentConstantId.TIME_FORMAT.value].value = 1

        self.establishCommunication()

        function = self.sendECRequest([secsgem.gem.EquipmentConstantId.TIME_FORMAT.value])

        EC = function[0]
        self.assertIsNotNone(EC)
        self.assertEqual(EC.get(), 1)

        function = self.sendECUpdate([{"ECID": secsgem.gem.EquipmentConstantId.TIME_FORMAT.value, "ECV": secsgem.secs.ItemI4(0)}])

        self.assertEqual(function.get(), 0)

        self.assertEqual(self.client.equipment_constants[secsgem.gem.EquipmentConstantId.TIME_FORMAT.value].value, 0)

    def testAlarmEnable(self):
        self.setupTestAlarms()
        self.establishCommunication()

        self.assertFalse(self.client.alarms[25].enabled)

        function = self.sendAlarmEnable()

        self.assertEqual(function.get(), self.data_items.ACKC5.ACCEPTED)
        self.assertTrue(self.client.alarms[25].enabled)

    def testAlarmEnableUnknown(self):
        self.establishCommunication()

        function = self.sendAlarmEnable(alid=26)

        self.assertEqual(function.get(), self.data_items.ACKC5.ERROR)

    def testAlarmDisable(self):
        self.setupTestAlarms()
        self.establishCommunication()

        self.assertFalse(self.client.alarms[25].enabled)

        function = self.sendAlarmEnable()

        self.assertEqual(function.get(), self.data_items.ACKC5.ACCEPTED)
        self.assertTrue(self.client.alarms[25].enabled)

        function = self.sendAlarmEnable(enable=False)

        self.assertEqual(function.get(), self.data_items.ACKC5.ACCEPTED)
        self.assertFalse(self.client.alarms[25].enabled)

    def testAlarmDisableUnknown(self):
        self.establishCommunication()

        function = self.sendAlarmEnable(enable=False, alid=26)

        self.assertEqual(function.get(), self.data_items.ACKC5.ERROR)

    def testAlarmTriggerOn(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOn")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 1)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(function.ALCD.get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY | self.data_items.ALCD.ALARM_SET)
        self.assertEqual(function.ALID.get(), 25)
        self.assertEqual(function.ALTX.get(), "test text")

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerOff(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOff")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOff")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 1)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(function.ALCD.get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY)
        self.assertEqual(function.ALID.get(), 25)
        self.assertEqual(function.ALTX.get(), "test text")

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmTriggerOnDisabled(self):
        self.setupTestAlarms()
        self.establishCommunication()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOnDisabled")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerOffDisabled(self):
        self.setupTestAlarms()
        self.establishCommunication()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOffDisabled")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOffDisabled")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmTriggerAlreadyOn(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOn")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOn")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerAlreadyOff(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOff")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmTriggerOnCollectionEventWithEnabledAlarm(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=100025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[100025])
        self.assertEqual(function.get(), 0)

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOnCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerOnCollectionEvent(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=100025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[100025])
        self.assertEqual(function.get(), 0)

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOnCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerOffCollectionEvent(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=200025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[200025])
        self.assertEqual(function.get(), 0)

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOffCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOffCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmDisabledTriggerOffCollectionEvent(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=200025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[200025])
        self.assertEqual(function.get(), 0)

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmDisabledTriggerOffCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerOn")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmTriggerAlreadyOnCollectionEvent(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOnCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.protocol.expect_message(function=1)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 2, self.data_items.ACKC5.ACCEPTED), packet.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=100025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[100025])
        self.assertEqual(function.get(), 0)

        clientCommandThread = threading.Thread(target=self.client.set_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOnCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertTrue(self.client.alarms[25].set)

    def testAlarmTriggerAlreadyOffCollectionEvent(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        self.assertFalse(self.client.alarms[25].set)

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=100025)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[100025])
        self.assertEqual(function.get(), 0)

        clientCommandThread = threading.Thread(target=self.client.clear_alarm, args=(25,), name="TestGemEquipmentHandlerPassiveControlState_testAlarmTriggerAlreadyOffCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertFalse(self.client.alarms[25].set)

    def testAlarmTriggerOnUnknown(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        with self.assertRaises(ValueError):
            self.client.set_alarm(26)

    def testAlarmTriggerOffUnknown(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        with self.assertRaises(ValueError):
            self.client.clear_alarm(26)

    def testAlarmListAll(self):
        self.setupTestAlarms()
        self.establishCommunication()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 5), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 6)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(len(function), 2)

        AL25 = next((x for x in function if x[1].get() == 25), None)

        self.assertIsNotNone(AL25)
        self.assertEqual(AL25[0].get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY)
        self.assertEqual(AL25[2].get(), "test text")

        AL30 = next((x for x in function if x[1].get() == 30), None)

        self.assertIsNotNone(AL30)
        self.assertEqual(AL30[0].get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY)
        self.assertEqual(AL30[2].get(), "test text 2")

    def testAlarmListSingle(self):
        self.setupTestAlarms()
        self.establishCommunication()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 5, [25]), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 6)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(len(function), 1)

        AL25 = function[0]

        self.assertIsNotNone(AL25)
        self.assertEqual(AL25[0].get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY)
        self.assertEqual(AL25[1].get(), 25)
        self.assertEqual(AL25[2].get(), "test text")

    def testAlarmListEnabled(self):
        self.setupTestAlarms()
        self.establishCommunication()

        function = self.sendAlarmEnable()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(5, 7), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 5)
        self.assertEqual(packet.header.function, 8)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertEqual(len(function), 1)

        AL25 = function[0]

        self.assertIsNotNone(AL25)
        self.assertEqual(AL25[0].get(), self.data_items.ALCD.PERSONAL_SAFETY | self.data_items.ALCD.EQUIPMENT_SAFETY)
        self.assertEqual(AL25[1].get(), 25)
        self.assertEqual(AL25[2].get(), "test text")

    def testRemoteCommand(self):
        self.setupTestRemoteCommands()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=5001)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[5001])
        self.assertEqual(function.get(), 0)

        f = unittest.mock.Mock()

        self.client.callbacks.rcmd_TEST_RCMD = f

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41,{
                                    "RCMD": "TEST_RCMD", "PARAMS": [{"CPNAME": "TEST_PARAMETER", "CPVAL": ""}]}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.ACK_FINISH_LATER)

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), 5001)

        f.assert_called_once_with(TEST_PARAMETER="")

    def testRemoteCommandUnregisteredCommand(self):
        self.establishCommunication()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41, {"RCMD": "UNKNOWN_RCMD", "PARAMS": []}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.INVALID_COMMAND)

    def testRemoteCommandUnregisteredCallback(self):
        self.setupTestRemoteCommands()
        self.establishCommunication()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41, {"RCMD": "TEST_RCMD", "PARAMS": []}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.INVALID_COMMAND)

    def testRemoteCommandUnknownParameter(self):
        self.setupTestRemoteCommands()
        self.establishCommunication()

        f = unittest.mock.Mock()

        self.client.callbacks.rcmd_TEST_RCMD = f

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41,{
                                    "RCMD": "TEST_RCMD", "PARAMS": [{"CPNAME": "INVALID_PARAMETER", "CPVAL": ""}]}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.PARAMETER_INVALID)

        assert not f.called

    def testRemoteCommandSTART(self):
        self.setupTestRemoteCommands()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=secsgem.gem.CollectionEventId.CMD_START_DONE.value)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[secsgem.gem.CollectionEventId.CMD_START_DONE.value])
        self.assertEqual(function.get(), 0)

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41, {"RCMD": "START", "PARAMS": []}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.ACK_FINISH_LATER)

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), secsgem.gem.CollectionEventId.CMD_START_DONE.value)

    def testRemoteCommandSTOP(self):
        self.setupTestRemoteCommands()
        self.establishCommunication()

        function = self.sendCEDefineReport(vid=[secsgem.gem.StatusVariableId.CLOCK.value])
        self.assertEqual(function.get(), 0)
        function = self.sendCELinkReport(ceid=secsgem.gem.CollectionEventId.CMD_STOP_DONE.value)
        self.assertEqual(function.get(), 0)
        function = self.sendCEEnableReport(ceid=[secsgem.gem.CollectionEventId.CMD_STOP_DONE.value])
        self.assertEqual(function.get(), 0)

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(2, 41, {"RCMD": "STOP", "PARAMS": []}), system_id))

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 42)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function)
        self.assertEqual(function.HCACK.get(), self.data_items.HCACK.ACK_FINISH_LATER)

        packet = self.settings.protocol.expect_message(stream=6)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(self.settings.streams_functions(6, 12, 0), packet.header.system))

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.from_message(packet)

        self.assertIsNotNone(function.get())
        self.assertEqual(function.CEID.get(), secsgem.gem.CollectionEventId.CMD_STOP_DONE.value)
