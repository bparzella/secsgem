# secsgem
Simple Python SECS/GEM implementation

This module is still work in progress. I'd love to get your input, your use case, whether you are experienced in SECS or not.

[![Test Coverage](https://api.codeclimate.com/v1/badges/223821436f063223b9da/test_coverage)](https://codeclimate.com/github/bparzella/secsgem/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/223821436f063223b9da/maintainability)](https://codeclimate.com/github/bparzella/secsgem/maintainability)
[![Tests](https://github.com/bparzella/secsgem/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/bparzella/secsgem/actions/workflows/run_tests.yaml)
[![Image](https://readthedocs.org/projects/secsgem/badge/)](http://secsgem.readthedocs.org/en/latest/)


## Installation
To install the latest official release (0.1.0, 2020-05-27, https://pypi.python.org/pypi/secsgem):

```bash
$ pip install secsgem
```

To install the current development code (might be instable):

```bash
$ pip install git+git://github.com/bparzella/secsgem
```

## Sample

```python
import logging
import code

import secsgem.gem

from communication_log_file_handler import CommunicationLogFileHandler

class SampleHost(secsgem.gem.GemHostHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.gem.GemHostHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.MDLN = "gemhost"
        self.SOFTREV = "1.0.0"

commLogFileHandler = CommunicationLogFileHandler("log", "h")
commLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger("hsms_communication").addHandler(commLogFileHandler)
logging.getLogger("hsms_communication").propagate = False

logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.DEBUG)

h = SampleHost("127.0.0.1", 5000, True, 0, "samplehost")
h.enable()

code.interact("host object is available as variable 'h'", local=locals())

h.disable()
```

## Contribute

This project is still at its beginning. If you can offer suggestions, additional information or help please contact me.
