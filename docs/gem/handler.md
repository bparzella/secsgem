# Handlers

{py:class}`secsgem.gem.handler.GemHandler` inherits the functionality from  {py:class}`secsgem.secs.handler.SecsHandler` (see {doc}`/secs/handler`).

To distinguish between host and equipment process there are two specialized types of {py:class}`secsgem.gem.handler.GemHandler`:
{py:class}`secsgem.gem.hosthandler.GemHostHandler` and {py:class}`secsgem.gem.equipmenthandler.GemEquipmentHandler`.
Use GemHostHandler if you want to implement a host system, GemEquipmentHandler for a equipment system.

It automatically handles the whole setup and teardown of the link.
Incoming collection events and terminal messages are automatically accepted and propagated by events.
The setup of collection event reports is also simplified.
It has functionality to send remote commands and handling process programs.

The handler also implements a maintains a communication state, which is defined in the standard.

```python
>>> settings = secsgem.hsms.Settings(address="127.0.0.1", port=5000, connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE, device_type=secsgem.common.DeviceType.HOST)
>>> client = secsgem.GemHostHandler(settings)
>>>
>>> client.enable()
>>> client.waitfor_communicating()
True
>>> client.get_process_program_list()
['test1', 'test2']
>>> client.request_process_program('test1')
This is process program test1
>>> client.disable()
```

Waiting for the communicating state can also be done asynchronous

```python
>>> def on_communicating(event, data):
...     print "Communicating"
...
>>> settings = secsgem.hsms.Settings(address="127.0.0.1", port=5000, connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE, device_type=secsgem.common.DeviceType.HOST)
>>> client = secsgem.GemHostHandler(settings)
>>> client.events.handler_communicating += on_communicating
>>>
>>> client.enable()
Communicating
>>> client.get_process_program_list()
['test1', 'test2']
>>> client.request_process_program('test1')
This is process program test1
>>> client.disable()
```

Also streams/functions can be sent and received with the handler:

```python
>>> f = secsgem.secs.functions.SecsS01F01()
>>> client.send_and_waitfor_response(f)
HsmsMessage({'header': HsmsHeader({device_id:0x0000, stream:01, function:02, p_type:0x00, s_type:0x00, system:0x75b78c3e, require_response:False}), 'data': '\x01\x02A\x06EQUIPMA\x06SV n/a'})
```

## Events

GemHandler defines a few new events, that can be received with the help of {py:class}`secsgem.common.EventHandler`:

| Event name | Description |
|---|---|
| handler_communicating | Connection is setup |
| collection_event_received | Collection event was received |
| terminal_received | Terminal message was received |

For an example on how to use these events see the code fragment in {doc}`/secs/handler`.
