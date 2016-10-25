Events
------

Events will notify the implementation that things happened.
They are called asynchronously, the result will be ignored.

There are three ways to define events, by creating them in the `inherited handler`_,
by setting `target objects`_ in the handlers events property and 
by `registering events`_.

Inherited handler
+++++++++++++++++
When working with a inherited class, events can be implemented by creating members with a specific name::

    class SampleEquipment(secsgem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)
        
        def _on_event_hsms_selected(self, connection):
            pass

In this example when the hsms connection state changes to selected the :code:`_on_event_hsms_selected` method will be called.

A generic representation of the function would be::
    
    def _on_event_<event_name>(self, <parameters>):
        pass

To catch all events, the :code:`_on_event` method can be overridden::

    class SampleEquipment(secsgem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)
        
        def _on_event(self, *args):
            pass

Target objects
++++++++++++++

These methods don't need to be implemented on the handler itself.
Other objects can also be registered using the event member names of the handler.
The :code:`_on_event_<event_name>` and :code:`_on_event` methods are then searched in that object::

    class TestClass(object):
        def _on_event_hsms_selected(self, connection):
            pass
    
    t = TestClass()

    handler.events.targets += t

The event handler can work with more than one target objects.

Registering events
++++++++++++++++++

Events can also be registered from outside a class::

    def f_hsms_selected(connection):
        pass

    handler.events.hsms_selected += f_hsms_selected

To unregister simply remove the member::

    handler.events.hsms_selected -= f_hsms_selected

Available events
++++++++++++++++
