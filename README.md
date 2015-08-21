# secsgem
Simple Python SECS/GEM implementation

This module is still work in progress. I'd love to get your input, your use case, whether you are experienced or not in SECS.

##Installation
To install the latest official release (might be old):

```bash
$ pip install secsgem
```

To install the current development code (might be instable):

```bash
$ pip install git+git://github.com/bparzella/secsgem
```

##Documentation
[ ![Image](https://readthedocs.org/projects/secsgem/badge/) ](http://secsgem.readthedocs.org/en/latest/)

##Sample

```python
from secsgem import *

client = hsmsClient("10.211.55.32", 5000)
connection = client.connect()

time.sleep(3)

connection.disconnect()
```

##Contribute

This project is still at its beginning. If you can offer suggestions, additional information or help please contact me.
