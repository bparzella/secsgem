#####################################################################
# testSecsConnectionStateModel.py
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
import unittest.mock

from transitions import MachineError

import secsgem.secs
import secsgem.hsms.connectionstatemachine

from test_connection import HsmsTestServer


class TestSecsConnectionStateModelPassive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer()

        self.client = secsgem.secs.SecsHandler(self.server.settings)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def testInitialState(self):
        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testConnect(self):
        self.server.simulate_connect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_NOT_SELECTED)


    def testUnselectedDisconnect(self):
        self.server.simulate_connect()

        self.server.simulate_disconnect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testSelection(self):
        self.server.simulate_connect()

        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectReqHeader(self.server.get_next_system_counter())))
        self.assertIsNotNone(self.server.expect_packet(s_type=2))

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_SELECTED)

    def testSelectedDisconnect(self):
        self.server.simulate_connect()

        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectReqHeader(self.server.get_next_system_counter())))
        self.assertIsNotNone(self.server.expect_packet(s_type=2))

        self.server.simulate_disconnect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)


class TestSecsConnectionStateModelActive(unittest.TestCase):
    def setUp(self):
        self.server = HsmsTestServer(secsgem.hsms.HsmsConnectMode.ACTIVE)

        self.client = secsgem.secs.SecsHandler(self.server.settings)

        self.server.start()
        self.client.enable()

    def tearDown(self):
        self.server.stop()
        self.client.disable()

    def testInitialState(self):
        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testConnect(self):
        self.server.simulate_connect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_NOT_SELECTED)

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectRspHeader(request_packet.header.system)))

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_SELECTED)

    def testSelectedDisconnect(self):
        self.server.simulate_connect()

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectRspHeader(request_packet.header.system)))

        self.server.simulate_disconnect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testUnselectedDisconnect(self):
        self.server.simulate_connect()
        self.server.simulate_disconnect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testNotYetSelected(self):
        self.server.simulate_connect()

        self.assertIsNotNone(self.server.expect_packet(s_type=1))

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_NOT_SELECTED)

    def testSelection(self):
        self.server.simulate_connect()

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectRspHeader(request_packet.header.system)))

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_SELECTED)

    def testSelectedDisconnect(self):
        self.server.simulate_connect()

        request_packet = self.server.expect_packet(s_type=1)
        self.assertIsNotNone(request_packet)
        self.server.simulate_packet(secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsSelectRspHeader(request_packet.header.system)))

        self.server.simulate_disconnect()

        self.assertEqual(self.client.protocol.connection_state.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

class TestConnectionStateMachine(unittest.TestCase):
    def setUp(self):
        self.stateMachine = secsgem.hsms.connectionstatemachine.ConnectionStateMachine()

    # tests for supported state transitions
    def testInitialState(self):
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testNotConnected2Connected(self):
        self.stateMachine.connect()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_NOT_SELECTED)

    def testConnectedNotSelected2NotConnected(self):
        self.stateMachine.connect()
        self.stateMachine.disconnect()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testConnectedSelected2NotConnected(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        self.stateMachine.disconnect()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    def testConnectedNotSelected2ConnectedSelected(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_SELECTED)

    def testConnectedSelected2ConnectedNotSelected(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        self.stateMachine.deselect()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_CONNECTED_NOT_SELECTED)

    def testConnectedNotSelected2NotConnectedT7(self):
        self.stateMachine.connect()
        self.stateMachine.timeoutT7()
        self.assertEqual(self.stateMachine.state, secsgem.hsms.connectionstatemachine.STATE_NOT_CONNECTED)

    # tests for unsupported state transitions
    def testUnconnectedDisconnect(self):
        with self.assertRaises(MachineError):
            self.stateMachine.disconnect()

    def testUnconnectedSelect(self):
        with self.assertRaises(MachineError):
            self.stateMachine.select()

    def testUnconnectedDeselect(self):
        with self.assertRaises(MachineError):
            self.stateMachine.deselect()

    def testUnconnectedTimeoutT7(self):
        with self.assertRaises(MachineError):
            self.stateMachine.timeoutT7()

    def testConnectedNotSelectedConnect(self):
        self.stateMachine.connect()
        with self.assertRaises(MachineError):
            self.stateMachine.connect()

    def testConnectedNotSelectedDeselect(self):
        self.stateMachine.connect()
        with self.assertRaises(MachineError):
            self.stateMachine.deselect()

    def testConnectedSelectedConnect(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        with self.assertRaises(MachineError):
            self.stateMachine.connect()

    def testConnectedSelectedSelect(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        with self.assertRaises(MachineError):
            self.stateMachine.select()

    def testConnectedSelectedTimeoutT7(self):
        self.stateMachine.connect()
        self.stateMachine.select()
        with self.assertRaises(MachineError):
            self.stateMachine.timeoutT7()

    # tests for callbacks
    def testOnEnterConnectedCallback(self):
        f = unittest.mock.Mock()

        self.stateMachine2 = secsgem.hsms.connectionstatemachine.ConnectionStateMachine({'on_enter_CONNECTED': f})
        self.stateMachine2.connect()

        f.assert_called()

    def testOnExitConnectedCallback(self):
        f = unittest.mock.Mock()

        self.stateMachine2 = secsgem.hsms.connectionstatemachine.ConnectionStateMachine({'on_exit_CONNECTED': f})
        self.stateMachine2.connect()
        self.stateMachine2.disconnect()

        f.assert_called()

    def testOnEnterConnectedSelectedCallback(self):
        f = unittest.mock.Mock()

        self.stateMachine2 = secsgem.hsms.connectionstatemachine.ConnectionStateMachine({'on_enter_CONNECTED_SELECTED': f})
        self.stateMachine2.connect()
        self.stateMachine2.select()

        f.assert_called()

