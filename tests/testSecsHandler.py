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
import unittest

import secsgem

from testconnection import HsmsTestServer

class TestSecsHandler(unittest.TestCase):
    def testSecsDecode(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        packet = server.generate_stream_function_packet(0, secsgem.SecsS01F02(["MDLN", "SOFTREV"]))

        function = client.secs_decode(packet)

        self.assertEqual(function.stream, 1)
        self.assertEqual(function.function, 2)
        self.assertEqual(function[0], "MDLN")
        self.assertEqual(function[1], "SOFTREV")

    def testSecsDecodeNone(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        function = client.secs_decode(None)

        self.assertIsNone(function)

    def testSecsDecodeInvalidStream(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        packet = secsgem.HsmsPacket()
        packet.header.stream = 99
        function = client.secs_decode(packet)

        self.assertIsNone(function)

    def testSecsDecodeInvalidFunction(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        packet = secsgem.HsmsPacket()
        packet.header.function = 99
        function = client.secs_decode(packet)

        self.assertIsNone(function)
    
    def testStreamFunction(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        function = client.stream_function(1, 1)

        self.assertIs(function, secsgem.SecsS01F01)

    def testStreamFunctionInvalidStream(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        function = client.stream_function(99, 1)

        self.assertIs(function, None)

    def testStreamFunctionInvalidFunction(self):
        server = HsmsTestServer()
        client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, server)

        function = client.stream_function(1, 99)

        self.assertIs(function, None)


class TestSecsHandlerPassive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer()

        self.client = secsgem.SecsHandler("127.0.0.1", 5000, False, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def handleS01F01(self, handler, packet):
        handler.send_response(secsgem.SecsS01F02(), packet.header.system)

    def testStreamFunctionReceiving(self):
        self.server.simulate_connect()

        self.client.register_callback(1, 1, self.handleS01F01)

        # select
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.HsmsPacket(secsgem.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x02)
        self.assertEqual(packet.header.sessionID, 0xffff)

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 2)

    def testStreamFunctionSending(self):
        self.server.simulate_connect()

        # select
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.HsmsPacket(secsgem.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x02)
        self.assertEqual(packet.header.sessionID, 0xffff)

        #send s01e01
        clientCommandThread = threading.Thread(target=self.client.send_and_waitfor_response, args=(secsgem.SecsS01F01(),), name="TestSecsHandlerPassive_testStreamFunctionSending")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.server.expect_packet(function=1)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0)
        self.assertEqual(packet.header.stream, 1)
        self.assertEqual(packet.header.function, 1)

        self.server.simulate_packet(self.server.generate_stream_function_packet(packet.header.system, secsgem.SecsS01F02()))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.isAlive())

    def testStreamFunctionReceivingUnselected(self):
        self.server.simulate_connect()

        self.client.register_callback(1, 1, self.handleS01F01)

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x07)
        self.assertEqual(packet.header.sessionID, 0xffff)

    def testStreamFunctionReceivingUnhandledFunction(self):
        self.server.simulate_connect()

        # select
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(secsgem.HsmsPacket(secsgem.HsmsSelectReqHeader(system_id)))

        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x02)
        self.assertEqual(packet.header.sessionID, 0xffff)

        #send s01e01
        system_id = self.server.get_next_system_counter()
        self.server.simulate_packet(self.server.generate_stream_function_packet(system_id, secsgem.SecsS01F01()))
        
        packet = self.server.expect_packet(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.sType, 0x00)
        self.assertEqual(packet.header.sessionID, 0)
        self.assertEqual(packet.header.stream, 9)
        self.assertEqual(packet.header.function, 5)

class TestSecsHandlerActive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer()

        self.client = secsgem.SecsHandler("127.0.0.1", 5000, True, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()
