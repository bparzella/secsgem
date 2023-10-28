#####################################################################
# test_gem_handler.py
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

import secsgem.hsms
import secsgem.secs
import secsgem.gem

from test_connection import HsmsTestServer

class GemHandlerPassiveGroup:
    def __init__(self):
        #hide warnings
        self.client = None
        self.server = None

    #hide warnings
    def assertEqual(self, par1, par2):
        raise Exception("Not implemented")

    #hide warnings
    def assertIsNotNone(self, par1):
        raise Exception("Not implemented")

    #hide warnings
    def assertTrue(self, par1):
        raise Exception("Not implemented")

    #hide warnings
    def assertFalse(self, par1):
        raise Exception("Not implemented")

    #hide warnings
    def assertIsNot(self, par1, par2):
        raise Exception("Not implemented")

    def testConstructor(self):
        self.assertIsNotNone(self.client)

        print(self.client)    # cover repr and serialize_data

    def testEnableDisable(self):
        self.assertEqual(self.client.communication_state.current, "NOT_COMMUNICATING")

        self.server.stop()
        self.client.disable()

        self.assertEqual(self.client.communication_state.current, "DISABLED")

        self.server.start()
        self.client.enable()

        self.assertEqual(self.client.communication_state.current, "NOT_COMMUNICATING")

    def testConnection(self):
        self.server.simulate_connect()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.session_id, 0xffff)

        self.assertEqual(self.client.communication_state.current, "WAIT_CRA")

    def establishCommunication(self):
        self.server.simulate_connect()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        packet = self.server.expect_packet(function=13)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F14([0])))

    def testReceivingS01F13(self):
        self.server.simulate_connect()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.session_id, 0xffff)

        self.assertEqual(self.client.communication_state.current, "WAIT_CRA")

        packet = self.server.expect_packet(function=13)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 0x01)
        self.assertEqual(packet.header.function, 0x0d)

        self.assertEqual(self.client.communication_state.current, "WAIT_CRA")

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS01F14([0])))

        self.assertEqual(self.client.communication_state.current, "COMMUNICATING")

    def testSendingS01F13(self):
        self.server.simulate_connect()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.session_id, 0xffff)

        self.assertEqual(self.client.communication_state.current, "WAIT_CRA")

        s01f13ReceivedPacket = self.server.expect_packet(function=13)

        self.assertIsNot(s01f13ReceivedPacket, None)
        self.assertEqual(s01f13ReceivedPacket.header.s_type.value, 0x00)
        self.assertEqual(s01f13ReceivedPacket.header.session_id, 0x0)
        self.assertEqual(s01f13ReceivedPacket.header.stream, 0x01)
        self.assertEqual(s01f13ReceivedPacket.header.function, 0x0d)

        self.assertEqual(self.client.communication_state.current, "WAIT_CRA")

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F13()))

        self.assertEqual(self.client.communication_state.current, "COMMUNICATING")

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 0x01)
        self.assertEqual(packet.header.function, 0x0e)

        self.assertEqual(self.client.communication_state.current, "COMMUNICATING")

        self.server.simulate_packet(self.server.generate_stream_function_packet(s01f13ReceivedPacket.header.system, secsgem.secs.functions.SecsS01F14([0])))

        self.assertEqual(self.client.communication_state.current, "COMMUNICATING")

    def testAreYouThereHandler(self):
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 2)

    def testEstablishCommunicationHandler(self):
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F13()))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 14)

    def testWaitForCommunicatingAlreadyCommunicating(self):
        self.establishCommunication()

        self.assertTrue(self.client.waitfor_communicating())

    def testWaitForCommunicating(self):
        clientCommandThread = threading.Thread(target=self.client.waitfor_communicating, name="GemHandler_testWaitForCommunicating")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        self.establishCommunication()

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testSendProcessProgram(self):
        self.establishCommunication()

        ppid = "PPTEST"
        ppbody = "1337QwErT"

        clientCommandThread = threading.Thread(target=self.client.send_process_program, args=(ppid, ppbody), name="GemHandler_testSendProcessProgram")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(stream=7)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS07F04(secsgem.secs.data_items.ACKC7.ACCEPTED)))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 7)
        self.assertEqual(packet.header.function, 3)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.PPID.get(), ppid)
        self.assertEqual(function.PPBODY.get(), ppbody)

    def testRequestProcessProgram(self):
        self.establishCommunication()

        ppid = "PPTEST"
        ppbody = "1337QwErT"

        clientCommandThread = threading.Thread(target=self.client.request_process_program, args=(ppid, ), name="GemHandler_testRequestProcessProgram")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(stream=7)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.secs.functions.SecsS07F06({"PPID": ppid, "PPBODY": ppbody})))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertIsNotNone(packet)
        self.assertEqual(packet.header.s_type.value, 0x00)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 7)
        self.assertEqual(packet.header.function, 5)

        function = self.client.settings.streams_functions.decode(packet)

        self.assertEqual(function.get(), ppid)

class TestGemHandlerPassive(unittest.TestCase, GemHandlerPassiveGroup):
    __testClass = secsgem.gem.GemHandler

    def setUp(self):
        self.assertIsNotNone(self.__testClass)

        self.server = HsmsTestServer()

        self.client = self.__testClass(self.server.settings)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.client.disable()
        self.server.stop()
