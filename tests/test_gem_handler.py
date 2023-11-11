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
import secsgem.gem.communication_state_machine
import secsgem.gem

from mock_protocol import MockProtocol
from mock_settings import MockSettings


class GemHandlerPassiveGroup:
    def __init__(self):
        #hide warnings
        self.client = None
        self.settings = None

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
        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.NOT_COMMUNICATING
        )

        self.client.disable()

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.DISABLED
        )

        self.client.enable()

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.NOT_COMMUNICATING
        )

    def testConnection(self):
        self.settings.protocol.simulate_connect()

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.WAIT_CRA
        )

    def establishCommunication(self):
        self.settings.protocol.simulate_connect()

        packet = self.settings.protocol.expect_message(function=13)

        self.settings.protocol.simulate_message(
            self.settings.protocol.create_message_for_function(
                secsgem.secs.functions.SecsS01F14([0]),
                packet.header.system,
            )
        )

    def testReceivingS01F13(self):
        self.settings.protocol.simulate_connect()

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.WAIT_CRA
        )

        message = self.settings.protocol.expect_message(function=13)

        self.assertIsNot(message, None)
        self.assertEqual(message.header.session_id, 0x0)
        self.assertEqual(message.header.stream, 0x01)
        self.assertEqual(message.header.function, 0x0d)

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.WAIT_CRA
        )

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS01F14([0]), message.header.system))

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.COMMUNICATING
        )

    def testSendingS01F13(self):
        self.settings.protocol.simulate_connect()

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.WAIT_CRA
        )

        s01f13ReceivedPacket = self.settings.protocol.expect_message(function=13)

        self.assertIsNot(s01f13ReceivedPacket, None)
        self.assertEqual(s01f13ReceivedPacket.header.session_id, 0x0)
        self.assertEqual(s01f13ReceivedPacket.header.stream, 0x01)
        self.assertEqual(s01f13ReceivedPacket.header.function, 0x0d)

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.WAIT_CRA
        )

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS01F13(), system_id))

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.COMMUNICATING
        )

        packet = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(packet, None)
        self.assertEqual(packet.header.session_id, 0x0)
        self.assertEqual(packet.header.stream, 0x01)
        self.assertEqual(packet.header.function, 0x0e)

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.COMMUNICATING
        )

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS01F14([0]), s01f13ReceivedPacket.header.system))

        self.assertEqual(
            self.client.communication_state.current,
            secsgem.gem.communication_state_machine.CommunicationState.COMMUNICATING
        )

    def testAreYouThereHandler(self):
        self.establishCommunication()

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS01F01(), system_id))

        message = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(message, None)
        self.assertEqual(message.header.session_id, 0x0)
        self.assertEqual(message.header.stream, 1)
        self.assertEqual(message.header.function, 2)

    def testEstablishCommunicationHandler(self):
        self.establishCommunication()

        system_id = 1
        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS01F13(), system_id))

        message = self.settings.protocol.expect_message(system_id=system_id)

        self.assertIsNot(message, None)
        self.assertEqual(message.header.session_id, 0x0)
        self.assertEqual(message.header.stream, 1)
        self.assertEqual(message.header.function, 14)

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

        message = self.settings.protocol.expect_message(stream=7)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS07F04(secsgem.secs.data_items.ACKC7.ACCEPTED), message.header.system))

        clientCommandThread.join(10)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertIsNotNone(message)
        self.assertEqual(message.header.session_id, 0x0)
        self.assertEqual(message.header.stream, 7)
        self.assertEqual(message.header.function, 3)

        function = message.data

        self.assertEqual(function.PPID.get(), ppid)
        self.assertEqual(function.PPBODY.get(), ppbody)

    def testRequestProcessProgram(self):
        self.establishCommunication()

        ppid = "PPTEST"
        ppbody = "1337QwErT"

        clientCommandThread = threading.Thread(target=self.client.request_process_program, args=(ppid, ), name="GemHandler_testRequestProcessProgram")
        clientCommandThread.daemon = True  # make thread killable on program termination
        clientCommandThread.start()

        message = self.settings.protocol.expect_message(stream=7)

        self.settings.protocol.simulate_message(self.settings.protocol.create_message_for_function(secsgem.secs.functions.SecsS07F06({"PPID": ppid, "PPBODY": ppbody}), message.header.system))

        clientCommandThread.join(1)
        self.assertFalse(clientCommandThread.is_alive())

        self.assertIsNotNone(message)
        self.assertEqual(message.header.session_id, 0x0)
        self.assertEqual(message.header.stream, 7)
        self.assertEqual(message.header.function, 5)

        function = message.data

        self.assertEqual(function.get(), ppid)

class TestGemHandlerPassive(unittest.TestCase, GemHandlerPassiveGroup):
    __testClass = secsgem.gem.GemHandler

    def setUp(self):
        self.assertIsNotNone(self.__testClass)

        self.settings = MockSettings(MockProtocol)

        self.client = self.__testClass(self.settings)

        self.client.enable()

    def tearDown(self):
        self.client.disable()
