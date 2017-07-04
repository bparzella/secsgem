# secsgem
Simple Python SECS/GEM implementation

This module is still work in progress. I'd love to get your input, your use case, whether you are experienced in SECS or not.

[![Image](https://readthedocs.org/projects/secsgem/badge/)](http://secsgem.readthedocs.org/en/latest/) 
[![Build Status](https://travis-ci.org/bparzella/secsgem.svg?branch=master)](https://travis-ci.org/bparzella/secsgem) 
[![Build status](https://ci.appveyor.com/api/projects/status/43y437avx1xkca2h?svg=true)](https://ci.appveyor.com/project/bparzella/secsgem)
[![Coverage Status](https://coveralls.io/repos/github/bparzella/secsgem/badge.svg?branch=master)](https://coveralls.io/github/bparzella/secsgem?branch=master)
[![Code Health](https://landscape.io/github/bparzella/secsgem/master/landscape.svg?style=flat)](https://landscape.io/github/bparzella/secsgem/master)


## Installation
To install the latest official release (0.0.6, 2016-10-25, https://pypi.python.org/pypi/secsgem):

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

import secsgem

from communication_log_file_handler import CommunicationLogFileHandler

class SampleHost(secsgem.GemHostHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.GemHostHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

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
