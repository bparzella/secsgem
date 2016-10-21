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

class TestEventProducer(unittest.TestCase):
    def testConstructor(self):
        producer = secsgem.EventProducer()

        self.assertEqual(producer._events, {})

    def testAddEvent(self):
        f = Mock()

        producer = secsgem.EventProducer()

        producer.test += f

        self.assertIn("test", producer)

    def testRemoveEvent(self):
        f = Mock()

        producer = secsgem.EventProducer()

        producer.test += f

        self.assertIn("test", producer)

        producer.test -= f

        self.assertNotIn("test", producer)

    def testEventRepr(self):
        f = Mock()

        producer = secsgem.EventProducer()

        producer.test += f

        print(producer.test)
        print(producer)

    def testJoinProducers(self):
        f1 = Mock()
        f2 = Mock()

        producer1 = secsgem.EventProducer()
        producer2 = secsgem.EventProducer()

        producer1.test1 += f1
        producer2.test2 += f2

        producer1 += producer2

        self.assertIn("test2", producer1)

    def testAddTarget(self):
        c = Mock()

        producer = secsgem.EventProducer()

        producer.targets += c

        self.assertIn(c, producer.targets)

    def testRemoveTarget(self):
        c = Mock()

        producer = secsgem.EventProducer()

        producer.targets += c

        self.assertIn(c, producer.targets)

        producer.targets -= c

        self.assertNotIn(c, producer.targets)

    def testJoinProducersTargets(self):
        c1 = Mock()
        c2 = Mock()

        producer1 = secsgem.EventProducer()
        producer2 = secsgem.EventProducer()

        producer1.targets += c1
        producer2.targets += c2

        producer1 += producer2

        self.assertIn(c2, producer1.targets)

    def testFire(self):
        f1 = Mock()
        f2 = Mock()
        c1 = Mock()
        c2 = Mock()

        producer = secsgem.EventProducer()

        producer.targets += c1
        producer.targets += c2
        producer.test += f1
        producer.test += f2

        producer.fire("test", "dummydata")

        f1.assert_called_once_with("dummydata")
        f2.assert_called_once_with("dummydata")
        c1._on_event_test.assert_called_once_with("dummydata")
        c2._on_event_test.assert_called_once_with("dummydata")
        c1._on_event.assert_called_once_with("test", "dummydata")
        c2._on_event.assert_called_once_with("test", "dummydata")

    def testInvalidTargetAssignment(self):
        test = 1

        producer = secsgem.EventProducer()

        with self.assertRaises(AttributeError):
            producer.targets = test


