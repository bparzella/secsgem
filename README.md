# secsgem
Simple Python SECS/GEM implementation

This module is still work in progress. Feel free to contact me with some feedback

##Installation
To install the latest official release:

```bash
$ pip install secsgem
```

To install the current development code (might be instable):

```bash
$ pip install git+git://github.com/bparzella/secsgem
```

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
