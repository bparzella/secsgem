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

import sys
import unittest

import secsgem

class TestTopLevelFunctions(unittest.TestCase):
    def testIsWindows(self):
        if sys.platform == "win32":
            self.assertEqual(secsgem.common.is_windows(), True)
        else:
            self.assertEqual(secsgem.common.is_windows(), False)

    def testFunctionName(self):
        self.assertEqual(secsgem.common.function_name(secsgem.common.is_windows), "is_windows")
        self.assertEqual(secsgem.common.function_name(self.testIsWindows), "TestTopLevelFunctions.testIsWindows")

