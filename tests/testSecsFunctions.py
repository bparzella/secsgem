#####################################################################
# testSecsFunctions.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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

from secsgem.secsFunctions import *

class testSecsFunctionNoData(object):
    cls = None
    
    #test constructor
    def testConstructor(self):
        if self.cls == None:
            return

        function = self.cls()

    #test en-/decoding
    def testEncoder(self):
        if self.cls == None:
            return

        function = self.cls()

        self.assertEqual("", function.encode())

    def testDecoder(self):
        if self.cls == None:
            return

        function = self.cls()
        function.decode("")

class testSecsFunctionSingleVariable(object):
    cls = None
    
    #test constructor
    def testConstructor(self):
        if self.cls == None:
            return

        function = self.cls(self.value1)

        self.assertEqual(function.get(), self.value1)

    #test constructor
    def testMultipleInstances(self):
        if self.cls == None:
            return

        function1 = self.cls()
        function2 = self.cls()

        function1.set(self.value1)
        function2.set(self.value2)

        self.assertEqual(function1.get(), self.value1)
        self.assertEqual(function2.get(), self.value2)

    #test en-/decoding
    def testEncoder(self):
        if self.cls == None:
            return

        function = self.cls(self.value1)

        self.assertEqual(self.encoded1, function.encode())

    def testDecoder(self):
        if self.cls == None:
            return

        function = self.cls()
        function.decode(self.encoded1)

        self.assertEqual(self.value1, function.get())


class testS00E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS00F00

class testS01E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS01F00

class testS01E01(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS01F01

class testS02E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS02F00

class testS02E16(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS02F16
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS02E34(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS02F34
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS02E36(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS02F36
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS02E38(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS02F38
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS05E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS05F00

class testS05E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS05F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS06E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS06F00

class testS06E12(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS06F12
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS07E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS07F00

class testS07E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS07F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS07E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS07F04
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS07E05(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS07F05
    value1 = "testString"
    value2 = "135"
    encoded1 = "A\ntestString"

class testS07E18(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS07F18
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS07E19(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS07F19

class testS09E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS09F00

class testS10E00(unittest.TestCase, testSecsFunctionNoData):
    cls = secsS10F00

class testS10E02(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS10F02
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"

class testS10E04(unittest.TestCase, testSecsFunctionSingleVariable):
    cls = secsS10F04
    value1 = 217
    value2 = 135
    encoded1 = "!\x01\xd9"
