#####################################################################
# testGemHostHandler.py
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

from collections import OrderedDict
import threading
import unittest

import secsgem

from testconnection import HsmsTestServer
from testGemHandler import GemHandlerPassiveGroup

class TestGemHostHandlerPassive(unittest.TestCase, GemHandlerPassiveGroup):
    __testClass = secsgem.GemHostHandler
    
    def setUp(self):
        self.assertIsNotNone(self.__testClass)

        self.server = HsmsTestServer()

        self.client = self.__testClass("127.0.0.1", 5000, False, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.client.disable()
        self.server.stop()
    
    def testClearCollectionEvents(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.clear_collection_events, name="TestGemHostHandlerPassive_testClearCollectionEvents")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=37)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 37)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["CEED"], False)
        self.assertEqual(function["CEID"].get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F38(secsgem.ERACK.ACCEPTED))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=33)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 33)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"].get(), [])

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F34(secsgem.DRACK.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def subscribeCollectionEvent(self, ceid, dvs, report_id):
        clientCommandThread = threading.Thread(target=self.client.subscribe_collection_event, args=(ceid, dvs, report_id), name="TestGemHostHandlerPassive_subscribeCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=33)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F34(secsgem.DRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=35)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F36(secsgem.LRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=37)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F38(secsgem.ERACK.ACCEPTED))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testSubscribeCollectionEvent(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.subscribe_collection_event, args=(10, [20], 30), name="TestGemHostHandlerPassive_testSubscribeCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=33)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 33)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"][0]["RPTID"], 30)
        self.assertEqual(function["DATA"][0]["VID"][0], 20)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F34(secsgem.DRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=35)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 35)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"][0]["CEID"], 10)
        self.assertEqual(function["DATA"][0]["RPTID"][0], 30)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F36(secsgem.LRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=37)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 37)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["CEED"], True)
        self.assertEqual(function["CEID"][0], 10)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F36(secsgem.LRACK.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testSubscribeCollectionEventWithoutReportId(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.subscribe_collection_event, args=(10, [20]), name="TestGemHostHandlerPassive_testSubscribeCollectionEvent")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=33)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 33)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"][0]["VID"][0], 20)

        rptid = function["DATA"][0]["RPTID"]

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F34(secsgem.DRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=35)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 35)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["DATAID"], 0)
        self.assertEqual(function["DATA"][0]["CEID"], 10)
        self.assertEqual(function["DATA"][0]["RPTID"][0], rptid)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F36(secsgem.LRACK.ACK))
        self.server.simulate_packet(packet)

        packet = self.server.expect_packet(function=37)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 37)

        function = self.client.secs_decode(packet)

        self.assertEqual(function["CEED"], True)
        self.assertEqual(function["CEID"][0], 10)

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F36(secsgem.LRACK.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def sendRemoteCommand(self, params):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.send_remote_command, args=("RCMD", params), name="TestGemHostHandlerPassive_testSendRemoteCommand")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=41)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 2)
        self.assertEqual(packet.header.function, 41)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.RCMD.get(), b"RCMD")
        self.assertEqual(function.PARAMS[0].CPNAME.get(), b"PARAM1")
        self.assertEqual(function.PARAMS[0].CPVAL.get(), b"PARAM1")
        self.assertEqual(function.PARAMS[1].CPNAME.get(), b"PARAM2")
        self.assertEqual(function.PARAMS[1].CPVAL.get(), 2)

        packetdata = {"HCACK": secsgem.HCACK.INVALID_COMMAND, "PARAMS": [{"CPNAME": "PARAM1", "CPACK": secsgem.CPACK.CPVAL_ILLEGAL_VALUE}, {"CPNAME": "PARAM2", "CPACK": secsgem.CPACK.CPVAL_ILLEGAL_FORMAT}]}
        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS02F42(packetdata))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testSendRemoteCommandDict(self):
        self.sendRemoteCommand(OrderedDict((("PARAM1", "PARAM1"), ("PARAM2", 2))))

    def testSendRemoteCommandList(self):
        self.sendRemoteCommand([["PARAM1", "PARAM1"], ["PARAM2", 2]])

    def testDeleteProcessPrograms(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.delete_process_programs, args=(["PP1", "PP2"], ), name="TestGemHostHandlerPassive_testDeleteProcessPrograms")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=17)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 7)
        self.assertEqual(packet.header.function, 17)

        function = self.client.secs_decode(packet)

        self.assertEqual(function[0].get(), b"PP1")
        self.assertEqual(function[1].get(), b"PP2")

        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS07F18(secsgem.ACKC7.ACCEPTED))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testGetProcessProgramList(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.get_process_program_list, name="TestGemHostHandlerPassive_testGetProcessProgramList")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=19)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 7)
        self.assertEqual(packet.header.function, 19)


        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS07F20(["PP1", "PP2"]))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testGoOnline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.go_online, name="TestGemHostHandlerPassive_testGoOnline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=17)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 17)


        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F18(secsgem.ONLACK.ACCEPTED))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testGoOffline(self):
        self.establishCommunication()

        clientCommandThread = threading.Thread(target=self.client.go_offline, name="TestGemHostHandlerPassive_testGoOffline")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=15)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 15)


        packet = self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F16(secsgem.OFLACK.ACK))
        self.server.simulate_packet(packet)

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testReceiveTerminal(self):
        self.establishCommunication()

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS10F01({"TID": 1, "TEXT": "HALLO"})))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 10)
        self.assertEqual(packet.header.function, 2)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.get(), 0)

    def testCollectionEventReceiving(self):
        self.establishCommunication()

        self.subscribeCollectionEvent(10, [20, 21], 30)

        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS06F11({"DATAID": 0, "CEID": 10, "RPT": [{"RPTID": 30, "V": ["1", 2]}]})))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0x0)
        self.assertEqual(packet.header.stream, 6)
        self.assertEqual(packet.header.function, 12)

        function = self.client.secs_decode(packet)

        self.assertEqual(function.get(), 0)

