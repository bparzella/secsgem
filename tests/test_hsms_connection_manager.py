#####################################################################
# test_hsms_connection_manager.py
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

import secsgem.hsms

from test_connection import HsmsTestServer


class TestHsmsConnectionManager(unittest.TestCase):
    def testConstructor(self):
        manager = secsgem.hsms.HsmsConnectionManager()

        self.assertIsNotNone(manager)

    def testAddEvent(self):
        f = unittest.mock.Mock()

        manager = secsgem.hsms.HsmsConnectionManager()

        manager.events.test += f

        self.assertIn("test", manager.events) 

    def testAddPassivePeer(self):
        server = HsmsTestServer()
        manager = secsgem.hsms.HsmsConnectionManager()

        manager._test_server_object = server

        manager.add_peer("test", "127.0.0.1", 1234, False, 0)

        self.assertIsNotNone(manager.has_connection_to("test"))
        self.assertIsNotNone(manager["test"])

        manager.stop()

    def testAddActivePeer(self):
        server = HsmsTestServer()
        manager = secsgem.hsms.HsmsConnectionManager()

        manager._test_server_object = server

        manager.add_peer("test", "127.0.0.1", 1234, True, 0)

        self.assertIsNotNone(manager.has_connection_to("test"))

        manager.stop()

    def testRemoveActivePeer(self):
        server = HsmsTestServer()
        manager = secsgem.hsms.HsmsConnectionManager()

        manager._test_server_object = server

        manager.add_peer("test", "127.0.0.1", 1234, True, 0)

        self.assertIsNotNone(manager.has_connection_to("test"))

        manager.remove_peer("test", "127.0.0.1", 1234)

        self.assertIsNone(manager.has_connection_to("test"))

        manager.stop()

    def testHasConnectionToUnknownHost(self):
        manager = secsgem.hsms.HsmsConnectionManager()
        self.assertIsNone(manager.has_connection_to("test"))
        self.assertIsNone(manager["test"])
