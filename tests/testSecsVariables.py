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

	def testEncodeItemHeaderTooShort (self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#negative value
		self.assertRaises(ValueError, secsvar.encodeItemHeader, -1)

	def testEncodeItemHeaderTooLong(self):
		#dummy object, just to have format code set
		secsvar = secsVarU4(1337)

		#more than three length bytes worth a value
		self.assertRaises(ValueError, secsvar.encodeItemHeader, 0x1000000)
