#####################################################################
# testCommonEvent.py
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
        
        self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithDefaultHandlerFalse(self):
        f = Mock(return_value=False)

        eventHandler = secsgem.EventHandler(generic_handler=f)

        self.assertEqual(eventHandler.genericHandler, f)

        self.assertFalse(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithSpecificHandler(self):
        f = Mock(return_value=True)

        eventHandler = secsgem.EventHandler(events={"test_event": f})

        self.assertIn(f, eventHandler.eventHandlers["test_event"])

        self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventWithSpecificHandlerTarget(self):
        c = Mock()
        c._on_event_test_event.return_value = True

        eventHandler = secsgem.EventHandler(target=c)

        self.assertEqual(eventHandler.target, c)

        self.assertTrue(eventHandler.fire_event("test_event", {"PARAM1": "Param1Data"}))

        c._on_event_test_event.assert_called_once_with({"PARAM1": "Param1Data"})

    def testFireEventWithGenericHandlerTarget(self):
        c = Mock()
        c._on_event.return_value = True

        eventHandler = secsgem.EventHandler(target=c)

        self.assertEqual(eventHandler.target, c)

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

        producer.fire_event("test_event", {"PARAM1": "Param1Data"})

        f.assert_called_once_with("test_event", {"PARAM1": "Param1Data"})

    def testFireEventAsync(self):
        def dummyFunc(event_name, params):
            return True

        eventHandler = secsgem.EventHandler(events={"test_event": dummyFunc})
        producer = secsgem.EventProducer(eventHandler)

        producer.fire_event("test_event", {"PARAM1": "Param1Data"}, True)
