#####################################################################
# testSecsVariables.py
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

from secsgem.secsVariables import *

class testSecsVar(unittest.TestCase):
	def testEncodeItemHeader(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#two bytes
		self.assertEqual(secsvar.encodeItemHeader(0), "\xB1\x00")
		self.assertEqual(secsvar.encodeItemHeader(0xFF), "\xB1\xFF")

		#three bytes
		self.assertEqual(secsvar.encodeItemHeader(0x100), "\xB2\x01\x00")
		self.assertEqual(secsvar.encodeItemHeader(0xFFFF), "\xB2\xFF\xFF")

		#four bytes
		self.assertEqual(secsvar.encodeItemHeader(0x10000), "\xB3\x01\x00\x00")
		self.assertEqual(secsvar.encodeItemHeader(0xFFFFFF), "\xB3\xFF\xFF\xFF")

	def testEncodeItemHeaderTooShort(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#negative value
		self.assertRaises(ValueError, secsvar.encodeItemHeader, -1)

	def testEncodeItemHeaderTooLong(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#more than three length bytes worth a value
		self.assertRaises(ValueError, secsvar.encodeItemHeader, 0x1000000)

	def testDecodeItemHeader(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#two bytes
		self.assertEqual(secsvar.decodeItemHeader("\xB1\x00")[2], 0)
		self.assertEqual(secsvar.decodeItemHeader("\xB1\xFF")[2], 0xFF)

		#three bytes
		self.assertEqual(secsvar.decodeItemHeader("\xB2\x01\x00")[2], 0x100)
		self.assertEqual(secsvar.decodeItemHeader("\xB2\xFF\xFF")[2], 0xFFFF)

		#four bytes
		self.assertEqual(secsvar.decodeItemHeader("\xB3\x01\x00\x00")[2], 0x10000)
		self.assertEqual(secsvar.decodeItemHeader("\xB3\xFF\xFF\xFF")[2], 0xFFFFFF)

	def testDecodeItemHeaderEmpty(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		self.assertRaises(ValueError, secsvar.decodeItemHeader, "")

	def testDecodeItemHeaderIllegalPosition(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		self.assertRaises(IndexError, secsvar.decodeItemHeader, "\xB1\x00", 10)

	def testDecodeItemHeaderIllegalData(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#two bytes
		self.assertRaises(ValueError, secsvar.decodeItemHeader, "somerandomdata")

class testSecsVarDynamic(unittest.TestCase):
	def testConstructorU4(self):
		secsvar = secsVarDynamic(secsVarU4)

		secsvar.set(10)

		self.assertEqual(10, secsvar.get())

	def testConstructorWrongType(self):
		secsvar = secsVarDynamic(secsVarU4)

		self.assertRaises(ValueError, secsvar.set, "testString")
		self.assertRaises(ValueError, secsVarDynamic, secsVarU4, value="testString")

	def testConstructorWrongLengthString(self):
		secsvar = secsVarDynamic(secsVarString, length=5)

		self.assertRaises(ValueError, secsvar.set, "testString")

	def testConstructorLen(self):
		secsvar = secsVarDynamic(secsVarString)

		secsvar.set("asdfg")

		self.assertEqual(5, len(secsvar))

	def testConstructorSetGetU4(self):
		secsvar = secsVarDynamic(secsVarU4)

		secsvar.set(10)

		self.assertEqual(10, secsvar.get())

	def testConstructorSetGetString(self):
		secsvar = secsVarDynamic(secsVarString)

		secsvar.set("testString")

		self.assertEqual("testString", secsvar.get())

	def testEncodeString(self):
		secsvar = secsVarDynamic(secsVarString, value="testString")

		self.assertEqual(secsvar.encode(), "A\ntestString")

	def testEncodeU4(self):
		secsvar = secsVarDynamic(secsVarU4, value=1337)

		self.assertEqual(secsvar.encode(), "\xB1\x04\x00\x00\x059")

	def testDecodeString(self):
		secsvar = secsVarDynamic(secsVarString)

		secsvar.decode("A\ntestString")

		self.assertEqual(secsvar.get(), "testString")

	def testDecodeU4(self):
		secsvar = secsVarDynamic(secsVarU4)

		secsvar.decode("\xB1\x04\x00\x00\x059")

		self.assertEqual(secsvar.get(), 1337)

	def testDecodeValueTooLong(self):
		secsvar = secsVarDynamic(secsVarString, 5)

		self.assertRaises(ValueError, secsvar.decode, ("A\ntestString"))

	def testDecodeEmptyValue(self):
		secsvar = secsVarDynamic(secsVarString, 5)

		self.assertRaises(ValueError, secsvar.decode, (""))

	def testDecodeItemHeaderIllegalPosition(self):
		secsvar = secsVarDynamic(secsVarU4, value=1337)

		self.assertRaises(IndexError, secsvar.decode, ("\xB1\x00"), 10)

	def testDecodeItemHeaderIllegalData(self):
		#dummy object, just to have format code set
		secsvar = secsVarDynamic(secsVarU4, value=1337)

		#two bytes
		self.assertRaises(ValueError, secsvar.decode, "somerandomdata")
