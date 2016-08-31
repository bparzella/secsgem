#####################################################################
# testCommon.py
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

import unittest

from mock import Mock, patch

import secsgem


class TestTopLevelFunctions(unittest.TestCase):
    def testIsWindows(self):
        self.assertEqual(secsgem.common.is_windows(), False)  # tests run on a linux system

    def testFunctionName(self):
        self.assertEqual(secsgem.common.function_name(secsgem.common.is_windows), "is_windows")
        self.assertEqual(secsgem.common.function_name(self.testIsWindows), "TestTopLevelFunctions.testIsWindows")


class TestStreamFunctionCallbackHandler(unittest.TestCase):
    def testRegisterCallback(self):
        f = Mock()

        functionHandler = secsgem.StreamFunctionCallbackHandler()

        functionHandler.register_callback(0, 0, f)

        self.assertIn(f, functionHandler.callbacks[functionHandler._generate_callback_name(0, 0)])

    def testDoubleRegisterCallback(self):
        f1 = Mock()
        f2 = Mock()

        functionHandler = secsgem.StreamFunctionCallbackHandler()

        functionHandler.register_callback(0, 0, f1)
        functionHandler.register_callback(0, 0, f2)

        self.assertIn(f1, functionHandler.callbacks[functionHandler._generate_callback_name(0, 0)])
        self.assertIn(f2, functionHandler.callbacks[functionHandler._generate_callback_name(0, 0)])

    def testUnregisterCallback(self):
        f = Mock()

        functionHandler = secsgem.StreamFunctionCallbackHandler()

        functionHandler.register_callback(0, 0, f)
        self.assertIn(f, functionHandler.callbacks[functionHandler._generate_callback_name(0, 0)])

        functionHandler.unregister_callback(0, 0, f)
        self.assertNotIn(f, functionHandler.callbacks[functionHandler._generate_callback_name(0, 0)])


class TestEventHandler(unittest.TestCase):
    def testConstructorNoParams(self):
        eventHandler = secsgem.EventHandler()

        self.assertEqual(eventHandler.eventHandlers, {})
        self.assertEqual(eventHandler.target, None)
        self.assertEqual(eventHandler.genericHandler, None)

    def testFireEventWithoutHandler(self):
        eventHandler = secsgem.EventHandler()

        self.assertFalse(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

    def testFireEventWithDefaultHandlerTrue(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(generic_handler=f)

        self.assertEqual(eventHandler.genericHandler, f)

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithDefaultHandlerFalse(self):
        f = Mock(return_value=False)

        eventHandler = secsgem.EventHandler(generic_handler=f)

        self.assertEqual(eventHandler.genericHandler, f)

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            self.assertFalse(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithSpecificHandler(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(events={"test_event": f})

        self.assertIn(f, eventHandler.eventHandlers["test_event"])

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithSpecificHandlerTarget(self):
        c = Mock()
        c._on_event_test_event.return_value = True

        eventHandler = secsgem.EventHandler(target=c)

        self.assertEqual(eventHandler.target, c)

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        c._on_event_test_event.assert_called_once_with({"PARAM1": "Param1Data"})

    def testFireEventWithGenericHandlerTarget(self):
        c = Mock()
        c._on_event.return_value = True

        eventHandler = secsgem.EventHandler(target=c)

        self.assertEqual(eventHandler.target, c)

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        c._on_event.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testRemoveExistingHandler(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(events={"test_event": f})

        self.assertIn(f, eventHandler.eventHandlers["test_event"])

        eventHandler.remove_event_handler("test_event", f)

        self.assertNotIn(f, eventHandler.eventHandlers["test_event"])

    def testRemoveUnknownHandler(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler()

        eventHandler.remove_event_handler("test_event", f)


class TestEventProducer(unittest.TestCase):
    def testConstructor(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(events={"test_event": f})
        producer = secsgem.EventProducer(eventHandler)

        self.assertEqual(producer.parentEventHandler, eventHandler)

    def testFireEvent(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(events={"test_event": f})
        producer = secsgem.EventProducer(eventHandler)

        with patch('secsgem.common.function_name') as mock:
            mock.return_value = "dummy"
            producer.fire_event("test_event", {"PARAM1": "Param1Data"})

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventAsync(self):
        def dummyFunc(event_name, params):
            return True

        eventHandler = secsgem.EventHandler(events={"test_event": dummyFunc})
        producer = secsgem.EventProducer(eventHandler)

        producer.fire_event("test_event", {"PARAM1": "Param1Data"}, True)
