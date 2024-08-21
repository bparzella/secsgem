# Callbacks

Callbacks are used to request information from a specific implementation.
They can be used to process the passed information and present a result to the peer.
Only one function can be registered for one callback.

The process will wait for the callback to return the result of the calculation.
Because of that the callback should run as performant as possible.

There are three ways to define the callback functions, by creating them in the [inherited handler](#inherited-handler), by setting a [target object](#target-object) and by [registering callbacks](#registering-callbacks).
Registered callbacks superseed target and overridden functions.

## Inherited handler

When working with a inherited class, callbacks can be implemented by creating callback members with a specific name:

```python
class SampleEquipment(secsgem.gem.GemEquipmentHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)

    def _on_alarm_received(self, handler, ALID, ALCD, ALTX):
        return ACKC5.ACCEPTED
```

In this example when an alarm was received (callback name is alarm_received) the `_on_alarm_received` method will be called.
The result (in this case `ACKC5.ACCEPTED`) will be passed to the host sending the alarm.

A generic representation of the function would be:

```python
def _on_<callback_name>(self, handler, <parameters>):
    return <result>
```

Callbacks for streams/functions can also be overriden this way by following a specific naming:

```python
def _on_s05f01(self, handler, message):
    return self.stream_function(5, 2)(ACKC5.ACCEPTED)
```

Note that the stream and function numbers are formated to have a leading zero if they are only one character long.
In this case the reply stream/function must be returned.

## Target object

These methods don\'t need to be implemented on the handler itself.
Another object can also be registered using the callbacks member names of the handler.
The `_on_<callback_name>` methods are then searched in that object:

```python
class TestClass:
    def _on_alarm_received(self, handler, ALID, ALCD, ALTX):
        return ACKC5.ACCEPTED

t = TestClass()

handler.callbacks.target = t
```

## Registering callbacks

Callbacks can also be registered from outside a class:

```python
def f_alarm_received(handler, ALID, ALCD, ALTX):
    return ACKC5.ACCEPTED

handler.callbacks.alarm_received = f_alarm_received
```

To unregister simply clear the member:

```python
handler.callbacks.alarm_received = None
```
