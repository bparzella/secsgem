Handler
=======

:class:`secsgem.secs.handler.SecsHandler` inherits the functionality from :class:`secsgem.hsms.handler.HsmsHandler` (see :doc:`/hsms/handler`).

The SecsHandler has additional functionality to add callbacks for specific streams and functions.

    >>> def s01f13_handler(connection, packet):
    ...     print "S1F13 received"
    ...
    >>> def on_connect(event, data):
    ...     print "Connected"
    ...
    >>> client = secsgem.SecsHandler("10.211.55.33", 5000, False, 0, "test")
    >>> client.events.hsms_connected += on_connect
    >>> client.register_stream_function(1, 13, s01f13_handler)
    >>>
    >>> client.enable()
    Connected
    S1F13 received
    >>> client.disable()

There is also additional functionality concerning collection events, service variables and equipment constants.
