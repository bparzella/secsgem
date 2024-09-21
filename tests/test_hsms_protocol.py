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

import secsgem.hsms

from mock_connection import MockHsmsConnection
from mock_settings import MockHsmsSettings


class TestHsmsProtocolHandlerPassive(unittest.TestCase):
    def setUp(self):
        self.settings = MockHsmsSettings(secsgem.hsms.HsmsProtocol, MockHsmsConnection, connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE)

        self.client = self.settings.create_protocol()

        self.client.enable()

    def tearDown(self):
        self.client.disable()

    def testSystemCounterWrapping(self):
        self.client._system_counter = ((2 ** 32) - 1)

        self.assertEqual(self.client.get_next_system_counter(), 0)

    def testLinktestTimer(self):
        self.client.disable()
        
        self.client._linktest_timeout = 0.1
        self.client.enable()

        self.settings.connection.simulate_connect()

        packet = self.settings.connection.expect_block(s_type=0x05)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x05)
        self.assertEqual(packet.header.device_id, 0xffff)

        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestRspHeader(packet.header.system), b""))

        packet = self.settings.connection.expect_block(s_type=0x05)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x05)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testSelect(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.device_id, 0xffff)


    def testSelectWhileDisconnecting(self):
        self.settings.connection.simulate_connect()

        # set the connection to disconnecting by brute force
        self.client._connection._disconnecting = True

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testDeselect(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.device_id, 0xffff)

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsDeselectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x04)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testDeselectWhileDisconnecting(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.device_id, 0xffff)

        # set the connection to disconnecting by brute force
        self.client._connection._disconnecting = True

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsDeselectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testLinktest(self):
        self.settings.connection.simulate_connect()

        # set the connection to disconnecting by brute force
        self.client._connection._disconnecting = True

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testLinktestWhileDisconnecting(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x06)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testRepr(self):
        self.settings.connection.simulate_connect()

        print(self.client)


class TestHsmsProtocolActive(unittest.TestCase):
    def setUp(self):
        self.settings = MockHsmsSettings(secsgem.hsms.HsmsProtocol, MockHsmsConnection, connect_mode=secsgem.hsms.HsmsConnectMode.ACTIVE)

        self.client = self.settings.create_protocol()

        self.client.enable()

    def tearDown(self):
        self.client.disable()

    def generate_stream_function_packet(self, system_id, packet, device_id=0):
        return secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsStreamFunctionHeader(system_id, packet.stream, packet.function, True, device_id), packet.encode())

    def testSelect(self):
        self.settings.connection.simulate_connect()

        packet = self.settings.connection.expect_block(s_type=0x01)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x01)
        self.assertEqual(packet.header.device_id, 0xffff)

        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectRspHeader(packet.header.system), b""))

    def testSelectSendError(self):
        self.settings.connection.fail_next_send()

        self.settings.connection.simulate_connect()

    def testDeselect(self):
        self.settings.connection.simulate_connect()

        packet = self.settings.connection.expect_block(s_type=0x01)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x01)
        self.assertEqual(packet.header.device_id, 0xffff)

        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectRspHeader(packet.header.system), b""))

        clientCommandThread = threading.Thread(target=self.client.send_deselect_req, name="TestHsmsProtocolActive_testDeselect")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        packet = self.settings.connection.expect_block(s_type=0x03)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x03)
        self.assertEqual(packet.header.device_id, 0xffff)

        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsDeselectRspHeader(packet.header.system), b""))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

    def testDeselectWhileDisconnecting(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x02)
        self.assertEqual(packet.header.device_id, 0xffff)

        # set the connection to disconnecting by brute force
        self.client._connection._disconnecting = True

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsDeselectReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testLinktest(self):
        self.settings.connection.simulate_connect()

        # set the connection to disconnecting by brute force
        self.client._connection._disconnecting = True

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x07)
        self.assertEqual(packet.header.device_id, 0xffff)


    def testLinktestWhileDisconnecting(self):
        self.settings.connection.simulate_connect()

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(system_id), b""))

        packet = self.settings.connection.expect_block(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x06)
        self.assertEqual(packet.header.device_id, 0xffff)

    def testRepr(self):
        self.settings.connection.simulate_connect()

        print(self.client)

    def testSecsPacketWithoutSecsDecode(self):
        self.settings.connection.simulate_connect()

        packet = self.settings.connection.expect_block(s_type=0x01)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.s_type.value, 0x01)
        self.assertEqual(packet.header.device_id, 0xffff)

        self.settings.connection.simulate_message(secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsSelectRspHeader(packet.header.system), b""))

        system_id = self.settings.protocol.get_next_system_counter()
        self.settings.connection.simulate_message(self.generate_stream_function_packet(system_id, secsgem.secs.functions.SecsS01F01()))

        print(self.client)

    def testPacketSendingFailed(self):
        self.settings.connection.simulate_connect()

        self.settings.connection.fail_next_send()

        self.assertEqual(self.client.send_and_waitfor_response(secsgem.secs.functions.SecsS01F01()), None)

    def testSelectReqSendingFailed(self):
        self.settings.connection.simulate_connect()

        self.settings.connection.fail_next_send()

        self.assertEqual(self.client.send_select_req(), None)

    def testLinktestReqSendingFailed(self):
        self.settings.connection.simulate_connect()

        self.settings.connection.fail_next_send()

        self.assertEqual(self.client.send_linktest_req(), None)

    def testDeselectReqSendingFailed(self):
        self.settings.connection.simulate_connect()

        self.settings.connection.fail_next_send()

        self.assertEqual(self.client.send_deselect_req(), None)

    def testPacketSendingTimeout(self):
        self.settings.connection.simulate_connect()

        self.client._settings.timeouts.t3 = 0.1

        self.assertEqual(self.client.send_and_waitfor_response(secsgem.secs.functions.SecsS01F01()), None)

    def testSelectReqSendingTimeout(self):
        self.settings.connection.simulate_connect()

        self.client._settings.timeouts.t6 = 0.1

        self.assertEqual(self.client.send_select_req(), None)

    def testLinktestReqSendingTimeout(self):
        self.settings.connection.simulate_connect()

        self.client._settings.timeouts.t6 = 0.1

        self.assertEqual(self.client.send_linktest_req(), None)

    def testDeelectReqSendingTimeout(self):
        self.settings.connection.simulate_connect()

        self.client._settings.timeouts.t6 = 0.1

        self.assertEqual(self.client.send_deselect_req(), None)

