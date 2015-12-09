Testing
=======

secsgem can be used to make unit tests on your implementation of the SEMI standard.

*Example*::

    import unittest

    import secsgem

    class TestExampleSecsGem(unittest.TestCase):
        def setUp(self):
            self.connection = secsgem.GemHostHandler("10.211.55.33", 5000, False, 0, "test", event_handler=secsgem.EventHandler())

            self.connection.enable()
            self.connection.waitfor_communicating()

        def tearDown(self):
            self.connection.disable()

        def testLinktest(self):
            linktestid = self.connection.send_linktest_req()
            result_packet = self.connection.waitfor_linktest_rsp(linktestid)

            self.assertEqual(result_packet.header.sType, 6)
            self.assertEqual(result_packet.header.sessionID, 65535)
            self.assertEqual(result_packet.header.system, linktestid)


See file samples/testExample.py