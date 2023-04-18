Testing
=======

secsgem can be used to make unit tests on your implementation of the SEMI standard.

*Example*::

    import unittest

    import secsgem.gem

    class TestExampleSecsGem(unittest.TestCase):
        def setUp(self):
            self.handler = secsgem.gem.GemHostHandler.hsms("10.211.55.33", 5000, False, 0, "test")

            self.handler.enable()
            self.handler.waitfor_communicating()

        def tearDown(self):
            self.handler.disable()

        def testLinktest(self):
            result_packet = self.handler.send_linktest_req()

            self.assertEqual(result_packet.header.s_type, 6)
            self.assertEqual(result_packet.header.session_id, 65535)


See file samples/testExample.py