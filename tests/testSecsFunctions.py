#####################################################################
# testSecsFunctions.py
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

from secsgem.secs.functions import *


class testSecsFunctionNoData(object):
    cls = None

    # test constructor
    def testConstructor(self):
        if self.cls is None:
            return

        self.cls()

    # test en-/decoding
    def testEncoder(self):
        if self.cls is None:
            return

        function = self.cls()

        self.assertEqual("", function.encode())

    def testDecoder(self):
        if self.cls is None:
            return

        function = self.cls()
        function.decode("")


class testSecsFunctionSingleVariable(object):
    cls = None

    # test constructor
    def testConstructor(self):
        if self.cls is None:
            return

        function = self.cls(self.value1)

        self.assertEqual(function.get(), self.value1)

    # test constructor
    def testMultipleInstances(self):
        if self.cls is None:
            return

        function1 = self.cls()
        function2 = self.cls()

        function1.set(self.value1)
        function2.set(self.value2)

        self.assertEqual(function1.get(), self.value1)
        self.assertEqual(function2.get(), self.value2)

    # test en-/decoding
    def testEncoder(self):
        if self.cls is None:
            return

        function = self.cls(self.value1)

        self.assertEqual(self.encoded1, function.encode())

    def testDecoder(self):
        if self.cls is None:
            return

        function = self.cls()
        function.decode(self.encoded1)

        self.assertEqual(self.value1, function.get())


class testS00E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS00F00


class testS01E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS01F00


class testS01E01(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS01F01


class testS02E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS02F00


class testS02E16(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F16
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS02E34(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F34
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS02E36(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F36
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS02E38(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F38
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS05E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS05F00


class testS05E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS05F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS06E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS06F00


class testS06E12(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS06F12
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS07E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS07F00


class testS07E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS07E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F04
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS07E05(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F05
    value1 = "testString"
    value2 = "135"
    encoded1 = "A\ntestString"


class testS07E18(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F18
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS07E19(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS07F19


class testS09E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS09F00


class testS10E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS10F00


class testS10E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS10F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testS10E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS10F04
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"


class testFunctionBase(unittest.TestCase):
    def testGetitemOnArray(self):
        item = SecsS01F03(["test1", "test2"])

        self.assertEqual(item[0].get(), "test1")

    def testSetitemOnArray(self):
        item = SecsS01F03(["test1", "test2"])

        item[0] = "test3"

        self.assertEqual(item[0].get(), "test3")

    def testLenOnArray(self):
        item = SecsS01F03(["test1", "test2"])

        self.assertEqual(len(item), 2)

    def testAppendOnArray(self):
        item = SecsS01F03(["test1", "test2"])

        item.append("test3")

        self.assertEqual(item[2].get(), "test3")

    def testGetitemOnNonArray(self):
        item = SecsS01F16(10)

        self.assertEqual(item[0], 10)

    def testSetitemOnNonArray(self):
        item = SecsS01F16(10)

        with self.assertRaises(TypeError):
            item[0] = 11

    def testLenOnNonArray(self):
        item = SecsS01F16(10)

        len(item)

    def testAppendOnNonArray(self):
        item = SecsS01F16(10)

        with self.assertRaises(AttributeError):
            item.append(20)

    def testGetAttrOnNonList(self):
        item = SecsS01F16(10)

        with self.assertRaises(AttributeError):
            item.Item1

    def testSetAttrOnNonList(self):
        item = SecsS01F16(10)

        with self.assertRaises(AttributeError):
            item.Item1 = 11

def check_stream_number(stream, cls):
    assert stream == cls._stream

def check_function_number(function, cls):
    assert function == cls._function

def test_streams_functions():
    for stream in secsStreamsFunctions:
        for function in secsStreamsFunctions[stream]:
            yield (check_stream_number, stream, secsStreamsFunctions[stream][function])
            yield (check_function_number, function, secsStreamsFunctions[stream][function])
