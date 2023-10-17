#####################################################################
# testHsmsEquipmentHandler.py
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
import unittest.mock

import secsgem.hsms
import secsgem.secs

from test_connection import HsmsTestServer


class TestSecsHandler(unittest.TestCase):
    def testSecsDecode(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        packet = server.generate_stream_function_packet(0, secsgem.secs.functions.SecsS01F02(["MDLN", "SOFTREV"]))

        function = client.settings.streams_functions.decode(packet)

        self.assertEqual(function.stream, 1)
        self.assertEqual(function.function, 2)
        self.assertEqual(function[0], "MDLN")
        self.assertEqual(function[1], "SOFTREV")

    def testSecsDecodeNone(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        function = client.settings.streams_functions.decode(None)

        self.assertIsNone(function)

    def testSecsDecodeInvalidStream(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        packet = secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsHeader(0, 0, 99))
        function = client.settings.streams_functions.decode(packet)

        self.assertIsNone(function)

    def testSecsDecodeInvalidFunction(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        packet = secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsHeader(0, 0, 99))
        function = client.settings.streams_functions.decode(packet)

        self.assertIsNone(function)
    
    def testStreamFunction(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        function = client.stream_function(1, 1)

        self.assertIs(function, secsgem.secs.functions.SecsS01F01)

    def testStreamFunctionInvalidStream(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        function = client.stream_function(99, 1)

        self.assertIs(function, None)

    def testStreamFunctionInvalidFunction(self):
        server = HsmsTestServer()
        client = secsgem.secs.SecsHandler(server.settings)

        function = client.stream_function(1, 99)

        self.assertIs(function, None)


class TestSecsHandlerPassive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer()

        self.client = secsgem.secs.SecsHandler(self.server.settings)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def handleS01F01(self, handler, packet):
        handler.send_response(secsgem.secs.functions.SecsS01F02(), packet.header.system)

    def performSelect(self):
        # select
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.session_id, 0xffff)

    def testStreamFunctionReceiving(self):
        self.server.simulate_connect()

        self.client.register_stream_function(1, 1, self.handleS01F01)

        self.performSelect()

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 2)

    def testStreamFunctionSending(self):
        self.server.simulate_connect()

        self.performSelect()

        #send s01e01
        clientCommandThread = threading.Thread(target=self.client.send_and_waitfor_response, args=(secsgem.secs.functions.SecsS01F01(),), \
            name="TestSecsHandlerPassive_testStreamFunctionSending")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testStreamFunctionReceivingUnselected(self):
        self.server.simulate_connect()

        self.client.register_stream_function(1, 1, self.handleS01F01)

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.session_id, 0xffff)

    def testStreamFunctionReceivingUnhandledFunction(self):
        self.server.simulate_connect()

        self.performSelect()

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0)
        self.assertEqual(packet.header.stream, 9)
        self.assertEqual(packet.header.function, 5)

    def testStreamFunctionReceivingExceptingCallback(self):
        self.server.simulate_connect()

        f = unittest.mock.Mock(side_effect=Exception("testException"))

        self.client.register_stream_function(1, 1, f)

        self.performSelect()

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 0)

    def testDisableCeids(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.disable_ceids, name="TestSecsHandlerPassive_testDisableCeids")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=37)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 37)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function["CEED"], False)
        self.assertEqual(function["CEID"].get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F38(secsgem.secs.data_items.ERACK.ACCEPTED))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testDisableCeidReports(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.disable_ceid_reports, name="TestSecsHandlerPassive_testDisableCeidReports")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=33)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 33)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"].get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F34(secsgem.secs.data_items.DRACK.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testListSVsAll(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.list_svs, name="TestSecsHandlerPassive_testListSVsAll")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=11)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"}]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testListSVsSpecific(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.list_svs, args=([1], ), name="TestSecsHandlerPassive_testListSVsSpecific")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=11)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 11)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"}]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testRequestSVs(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.request_svs, args=([1], ), name="TestSecsHandlerPassive_testRequestSVs")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=3)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 3)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F04([1337]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testRequestSV(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.request_sv, args=(1, ), name="TestSecsHandlerPassive_testRequestSV")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=3)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 3)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F04([1337]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testListECsAll(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.list_ecs, name="TestSecsHandlerPassive_testListECsAll")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=29)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 29)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F30([{"ECID": 1, "ECNAME": "EC1", \
            "ECMIN": secsgem.secs.variables.U1(0), "ECMAX": secsgem.secs.variables.U1(100), "ECDEF": secsgem.secs.variables.U1(50), "UNITS": "mm"}]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testListECsSpecific(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.list_ecs, args=([1], ), name="TestSecsHandlerPassive_testListECsSpecific")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=29)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 29)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F30([{"ECID": 1, "ECNAME": "EC1", \
            "ECMIN": secsgem.secs.variables.U1(0), "ECMAX": secsgem.secs.variables.U1(100), "ECDEF": secsgem.secs.variables.U1(50), "UNITS": "mm"}]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testRequestECs(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.request_ecs, args=([1], ), name="TestSecsHandlerPassive_testRequestECs")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=13)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 13)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F14([1337]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testRequestEC(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.request_ec, args=(1, ), name="TestSecsHandlerPassive_testRequestEC")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=13)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 13)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [1])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F14([1337]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testSetECs(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.set_ecs, args=([[1, "1337"]], ), name="TestSecsHandlerPassive_testSetECs")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=15)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 15)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [{'ECID': 1, 'ECV': u'1337'}])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F16(secsgem.secs.data_items.EAC.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testSetEC(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.set_ec, args=(1, 1337), name="TestSecsHandlerPassive_testSetEC")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=15)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 15)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), [{'ECV': 1337, 'ECID': 1}])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS02F16(secsgem.secs.data_items.EAC.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testSendEquipmentTerminal(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.send_equipment_terminal, args=(0, "Hello World"), \
            name="TestSecsHandlerPassive_testSendEquipmentTerminal")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=3)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 10)
        self.assertEqual(packet.header.function, 3)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.TID.get(), 0)
        self.assertEqual(function.TEXT.get(), "Hello World")

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS10F04(secsgem.secs.data_items.ACKC10.ACCEPTED))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testAreYouThere(self):
        self.server.simulate_connect()

        self.performSelect()

        clientCommandThread = threading.Thread(target=self.client.are_you_there, name="TestSecsHandlerPassive_testAreYouThere")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 1)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F02([]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testUnhandeledFunctionCallback(self):
        self.server.simulate_connect()

        f = unittest.mock.Mock(return_value=False)
        self.client.register_stream_function(1, 2, f)

        self.performSelect()

        system_id = self.server.get_next_system_counter()
        packet = self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F02([]))
        self.server.simulate_packet(packet)

    def testExceptionFunctionCallback(self):
        self.server.simulate_connect()

        f = unittest.mock.Mock(side_effect=Exception("testException"))
        self.client.register_stream_function(1, 2, f)

        self.performSelect()

        system_id = self.server.get_next_system_counter()
        packet = self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F02([]))
        self.server.simulate_packet(packet)

    def testGetCeidName(self):
        self.client._collection_events = {
            0: {"name": "CollectionEvent0", "description": "Collection event #0", "dvids": []},
        }

        self.assertEqual(self.client.get_ceid_name(0), "CollectionEvent0")

    def testGetCeidNameMissingName(self):
        self.client._collection_events = {
            0: {"description": "Collection event #0", "dvids": []},
        }

        self.assertEqual(self.client.get_ceid_name(0), "")

    def testGetCeidNameMissingCeid(self):
        self.assertEqual(self.client.get_ceid_name(0), "")

    def testGetDvidName(self):
        self.client._data_values = {
            0: {"name": "DataValue0", "description": "Data Value #0"},
        }

        self.assertEqual(self.client.get_dvid_name(0), "DataValue0")

    def testGetDvidNameMissingName(self):
        self.client._data_values = {
            0: {"description": "Data Value #0"},
        }

        self.assertEqual(self.client.get_dvid_name(0), "")

    def testGetDvidNameMissingDvid(self):
        self.assertEqual(self.client.get_dvid_name(0), "")

    def testUnregisterStreamFunctionCallback(self):
        f = unittest.mock.Mock()

        self.client.register_stream_function(0, 0, f)
        self.assertIn(self.client._generate_sf_callback_name(0, 0), self.client._callback_handler._callbacks)

        self.client.unregister_stream_function(0, 0)
        self.assertNotIn(self.client._generate_sf_callback_name(0, 0), self.client._callback_handler._callbacks)

    def testRegisterCallback(self):
        f = unittest.mock.Mock()

        self.client.callbacks.test = f
        self.assertIn("test", self.client.callbacks._callbacks)

    def testCallbackIn(self):
        f = unittest.mock.Mock()

        self.client.callbacks.test = f
        self.assertIn("test", self.client.callbacks)

    def testCallCallback(self):
        f = unittest.mock.Mock()

        self.client.callbacks.test = f
        self.assertIn("test", self.client._callback_handler._callbacks)

        self.client.callbacks.test()

        f.assert_called_once()

    def testUnRegisterCallback(self):
        f = unittest.mock.Mock()

        self.client.callbacks.test = f
        self.assertIn("test", self.client._callback_handler._callbacks)

        self.client.callbacks.test = None
        self.assertNotIn("test", self.client._callback_handler._callbacks)

class TestSecsHandlerActive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer(secsgem.hsms.HsmsConnectMode.ACTIVE)

        self.client = secsgem.secs.SecsHandler(self.server.settings)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()
