#####################################################################
# testExample.py
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

import secsgem.gem


class TestExampleSecsGem(unittest.TestCase):
    def setUp(self):
        self.handler = secsgem.gem.GemHandler.hsms("10.211.55.33", 5000, False, 0, "test")

        self.handler.enable()
        self.handler.waitfor_communicating()

    def tearDown(self):
        self.handler.disable()

    def testLinktest(self):
        result_message = self.handler.send_linktest_req()

        self.assertEqual(result_message.header.s_type.value, 6)
        self.assertEqual(result_message.header.device_id, 65535)


