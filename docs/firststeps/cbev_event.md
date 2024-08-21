# Events

Events will notify the implementation that things happened.
They are called asynchronously, the result will be ignored.

There are three ways to define events, by creating them in the [inherited handler](#inherited-handler), by setting [target objects](#target-objects) in the handlers events property and by [registering events](#registering-events).

## Inherited handler

When working with a inherited class, events can be implemented by creating members with a specific name:

```python
class SampleEquipment(secsgem.gem.GemEquipmentHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)

    def _on_event_communicating(self, connection):
        pass
```

In this example when the hsms connection state changes to selected the `_on_event_communicating` method will be called.

A generic representation of the function would be:

```python
def _on_event_<event_name>(self, <parameters>):
    pass
```

To catch all events, the `_on_event` method can be overridden:

```python
class SampleEquipment(secsgem.gem.GemEquipmentHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)

    def _on_event(self, *args):
        pass
```

## Target objects

These methods don\'t need to be implemented on the handler itself.
Other objects can also be registered using the event member names of the handler.
The `_on_event_<event_name>` and `_on_event` methods are then searched in that object:

```python
class TestClass:
    def _on_event_communicating(self, connection):
        pass

t = TestClass()

handler.events.targets += t
```

The event handler can work with more than one target objects.

## Registering events

Events can also be registered from outside a class:

```python
def f_communicating(connection):
    pass

handler.events.communicating += f_communicating
```

To unregister simply remove the member:

```python
handler.events.communicating -= f_communicating
```
