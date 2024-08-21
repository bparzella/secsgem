# Handler

The SecsHandler has functionality to add callbacks for specific streams and functions.

```python
>>> def s01f13_handler(connection, packet):
...     print "S1F13 received"
...
>>> def on_connect(event, data):
...     print "Connected"
...
>>> settings = secsgem.hsms.Settings(address="127.0.0.1", port=5000, connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE, device_type=secsgem.common.DeviceType.HOST)
>>> client = secsgem.secs.SecsHandler(settings)
>>> client.events.connected += on_connect
>>> client.register_stream_function(1, 13, s01f13_handler)
>>>
>>> client.enable()
Connected
S1F13 received
>>> client.disable()
```

There is also additional functionality concerning collection events, service variables and equipment constants.
