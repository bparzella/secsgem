Handler
=======

:class:`secsgem.hsms.handler.HsmsHandler` has the basic HSMS connection handling build in.
It automatically selects and deselects the link and performs a periodic linktest.
It also replies to incoming HSMS requests like linktest automatically.

    >>> def on_connect(event, data):
    ...     print "Connected"
    ...
    >>> client = secsgem.HsmsHandler("10.211.55.33", 5000, False, 0, "test")
    >>> client.events.hsms_connected += on_connect
    >>> client.enable()
    Connected
    >>> client.send_linktest_req()
    secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 7, 'sessionID': 65535, 'requireResponse': False, 'sType': 6}), 'data': ''})
    >>> client.disable()

The handler has functions to send requests and responses and wait for a certain response.

Events
------

Events of the handler can be received with the help of :class:`secsgem.common.EventHandler`.
The handler sends the following events:

+-------------------+----------------------------+
| Event name        | Description                |
+===================+============================+
| hsms_connected    | Connection was established |
+-------------------+----------------------------+
| hsms_selected     | Connection was selected    |
+-------------------+----------------------------+
| hsms_disconnected | Connection was terminated  |
+-------------------+----------------------------+

For an example on how to use these events see the code fragment above.