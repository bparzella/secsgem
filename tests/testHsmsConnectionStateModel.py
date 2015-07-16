#####################################################################
# testSecsConnectionStateModel.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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
import time

import secsgem
import secsgem.hsmsTestConnection


class TestSecsConnectionStateModelPassive(unittest.TestCase):
    def setUp(self):
        self.server = secsgem.hsmsTestConnection.HsmsTestServer()

        self.client = secsgem.secsHandler("127.0.0.1", 5000, False, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def testInitialState(self):
        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')

    def testConnect(self):
        self.server.simulate_connect()

        self.assertEqual(self.client.connectionState.current, 'NOT_SELECTED')

    def testUnselectedDisconnect(self):
        self.server.simulate_connect()
        self.server.simulate_disconnect()

        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')

    def testSelection(self):
        self.server.simulate_connect()

        self.server.simulate_packet(secsgem.hsmsPacket(secsgem.hsmsSelectReqHeader(self.server.get_next_system_counter())))
        self.assertIsNotNone(self.server.expect_packet(s_type=2))

        self.assertEqual(self.client.connectionState.current, 'SELECTED')

    def testSelectedDisconnect(self):
        self.server.simulate_connect()

        self.server.simulate_packet(secsgem.hsmsPacket(secsgem.hsmsSelectReqHeader(self.server.get_next_system_counter())))
        self.assertIsNotNone(self.server.expect_packet(s_type=2))

        self.server.simulate_disconnect()

        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')

class TestSecsConnectionStateModelActive(unittest.TestCase):
    def setUp(self):
        self.server = secsgem.hsmsTestConnection.HsmsTestServer()

        self.client = secsgem.secsHandler("127.0.0.1", 5000, True, 0, "test", None, self.server)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def testInitialState(self):
        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')

    def testConnect(self):
        self.server.simulate_connect()

        self.assertEqual(self.client.connectionState.current, 'NOT_SELECTED')

    def testUnselectedDisconnect(self):
        self.server.simulate_connect()
        self.server.simulate_disconnect()

        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')

    def testNotYetSelected(self):
        self.server.simulate_connect()

        self.assertIsNotNone(self.server.expect_packet(s_type=1))

        self.assertEqual(self.client.connectionState.current, 'NOT_SELECTED')

    def testSelection(self):
        self.server.simulate_connect()

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsmsPacket(secsgem.hsmsSelectRspHeader(request_packet.header.system)))

        self.assertEqual(self.client.connectionState.current, 'SELECTED')

    def testSelectedDisconnect(self):
        self.server.simulate_connect()

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsmsPacket(secsgem.hsmsSelectRspHeader(request_packet.header.system)))

        self.server.simulate_disconnect()

        self.assertEqual(self.client.connectionState.current, 'NOT_CONNECTED')
