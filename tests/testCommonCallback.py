#####################################################################
# testCommonCallback.py
#
# (c) Copyright 2016, Benjamin Parzella. All rights reserved.
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

from mock import Mock

import secsgem

class TestCallbackHandler(unittest.TestCase):
    def testRegisterCallback(self):
        f = Mock()

        callbackHandler = secsgem.CallbackHandler()

        callbackHandler.register("test", f)

        self.assertIn("test", callbackHandler._callbacks)
        self.assertEqual(callbackHandler._callbacks["test"], f)

    def testDoubleRegisterCallback(self):
        f1 = Mock()
        f2 = Mock()

        callbackHandler = secsgem.CallbackHandler()

        callbackHandler.register("test", f1)
        callbackHandler.register("test", f2)

        self.assertIn("test", callbackHandler._callbacks)
        self.assertEqual(callbackHandler._callbacks["test"], f2)

    def testUnregisterCallback(self):
        f = Mock()

        callbackHandler = secsgem.CallbackHandler()

        callbackHandler.register("test", f)

        self.assertIn("test", callbackHandler._callbacks)
        self.assertEqual(callbackHandler._callbacks["test"], f)

        self.assertTrue(callbackHandler.unregister("test"))

        self.assertNotIn("test", callbackHandler._callbacks)

    def testUnregisterUnregisteredCallback(self):
        callbackHandler = secsgem.CallbackHandler()

        self.assertFalse(callbackHandler.unregister("test"))

        self.assertNotIn("test", callbackHandler._callbacks)

    def testHasWithCallback(self):
        f = Mock()

        callbackHandler = secsgem.CallbackHandler()

        callbackHandler.register("test", f)

        self.assertTrue(callbackHandler.has("test"))

    def testHasWithDelegate(self):
        c = Mock()

        callbackHandler = secsgem.CallbackHandler(c)

        self.assertTrue(callbackHandler.has("test"))

    def testHasWithNone(self):
        callbackHandler = secsgem.CallbackHandler()

        self.assertFalse(callbackHandler.has("test"))

    def testCallWithCallback(self):
        f = Mock()
        f.return_value = "testvalue"

        callbackHandler = secsgem.CallbackHandler()

        callbackHandler.register("test", f)

        self.assertEqual(callbackHandler.call("test", self, "data"), "testvalue")

        f.assert_called_once_with(self, "data")

    def testCallWithDelegate(self):
        c = Mock()
        c._on_test.return_value = "testvalue"

        callbackHandler = secsgem.CallbackHandler(c)

        callbackHandler.call("test", self, "data")

        c._on_test.assert_called_once_with(self, "data")

    def testCallWithNone(self):
        callbackHandler = secsgem.CallbackHandler()

        self.assertIsNone(callbackHandler.call("test", self, "data"))
