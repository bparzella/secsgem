#####################################################################
# test_secs_functions.py
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

import pytest

"""
from secsgem.secs.functions import *
from secsgem.secs.functions._all import secs_streams_functions


class testSecsFunctionNoData:
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

        self.assertEqual(b"", function.encode())

    def testDecoder(self):
        if self.cls is None:
            return

        function = self.cls()
        function.decode(b"")


class testSecsFunctionSingleVariable:
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
    encoded1 = b"!\x01\xd9"


class testS02E34(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F34
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS02E36(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F36
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS02E38(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS02F38
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS05E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS05F00


class testS05E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS05F02
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS06E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS06F00


class testS06E12(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS06F12
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS07E00(unittest.TestCase, testSecsFunctionNoData):
    cls = SecsS07F00


class testS07E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F02
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS07E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F04
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


class testS07E05(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F05
    value1 = "testString"
    value2 = "135"
    encoded1 = b"A\ntestString"


class testS07E18(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS07F18
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


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
    encoded1 = b"!\x01\xd9"


class testS10E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = SecsS10F04
    value1 = 217
    value2 = 135
    encoded1 = b"!\x01\xd9"


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

    def testGetitemOnUninitializedNonArray(self):
        item = SecsS01F16()

        self.assertEqual(item[0], 0)

        with self.assertRaises(IndexError):
            self.assertEqual(item[1], 0)

    def testSetitemOnUninitializedNonArray(self):
        item = SecsS01F16()

        item[0] = 11

        with self.assertRaises(IndexError):
            item[1] = 11

    def testGetitemOnNonArray(self):
        item = SecsS01F16(10)

        self.assertEqual(item[0], 10)

        with self.assertRaises(IndexError):
            self.assertEqual(item[1], 10)

    def testSetitemOnNonArray(self):
        item = SecsS01F16(10)

        item[0] = 11

        with self.assertRaises(IndexError):
            item[1] = 11

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

    def test_repr(self):
        item = SecsS01F16(10)

        assert str(item) == "S1F16\n  <B 0xa> ."

    def test_repr_header_only(self):
        item = SecsS01F01()

        assert str(item) == "S1F1 W ."

    def test_class_repr(self):
        assert str(SecsS01F16) == "OFLACK: B[1]"

    def test_class_repr_header_only(self):
        assert str(SecsS01F01) == "Header only"


def generate_stream_list():
    return [(function.stream, function) for function in secs_streams_functions]


def generate_function_list():
    return [(function.function, function) for function in secs_streams_functions]


@pytest.mark.parametrize("stream,cls", generate_stream_list())
def test_stream_number(stream, cls):
    assert stream == cls._stream


@pytest.mark.parametrize("function,cls", generate_function_list())
def test_function_number(function, cls):
    assert function == cls._function

"""