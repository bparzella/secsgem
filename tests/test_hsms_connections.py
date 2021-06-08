#####################################################################
# test_hsms_connections.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
import errno

import secsgem.common

class TestTopLevelFunctions(unittest.TestCase):
    def testIsErrorcodeEwouldBlock(self):
        self.assertFalse(secsgem.common.is_errorcode_ewouldblock(0))
        self.assertFalse(secsgem.common.is_errorcode_ewouldblock(errno.EPERM))
        self.assertFalse(secsgem.common.is_errorcode_ewouldblock(errno.EBADF))
        self.assertTrue(secsgem.common.is_errorcode_ewouldblock(errno.EAGAIN))
        self.assertTrue(secsgem.common.is_errorcode_ewouldblock(errno.EWOULDBLOCK))
