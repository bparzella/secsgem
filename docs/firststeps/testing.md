# Testing

secsgem can be used to make unit tests on your implementation of the SEMI standard.

*Example*:
```{code} python
import unittest

import secsgem.common
import secsgem.gem
import secsgem.hsms

class TestExampleSecsGem(unittest.TestCase):
    def setUp(self):
        settings = secsgem.hsms.Settings(
            address="127.0.0.1",
            port=5000,
            connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE,
            device_type=secsgem.common.DeviceType.HOST
        )

        self.handler = secsgem.gem.GemHostHandler.hsms(settings)

        self.handler.enable()
        self.handler.waitfor_communicating()

    def tearDown(self):
        self.handler.disable()

    def testLinktest(self):
        result_packet = self.handler.send_linktest_req()

        self.assertEqual(result_packet.header.s_type.value, 6)
        self.assertEqual(result_packet.header.device_id, 65535)
```

See file samples/testExample.py
