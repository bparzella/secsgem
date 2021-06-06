Testing
=======

secsgem can be used to make unit tests on your implementation of the SEMI standard.

*Example*::

    import unittest

    import secsgem.gem

    class TestExampleSecsGem(unittest.TestCase):
        def setUp(self):
            self.connection = secsgem.gem.GemHostHandler("10.211.55.33", 5000, False, 0, "test")

            self.connection.enable()
            self.connection.waitfor_communicating()

        def tearDown(self):
            self.connection.disable()

        def testLinktest(self):
            result_packet = self.connection.send_linktest_req()

            self.assertEqual(result_packet.header.sType, 6)
            self.assertEqual(result_packet.header.sessionID, 65535)


See file samples/testExample.py