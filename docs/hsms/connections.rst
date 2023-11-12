Connections
===========

HSMS has active and passive connections.
The active connection is the one making the connection, the passive one is waiting for the incoming connection.

The implementation for the active connection is :class:`secsgem.hsms.connections.HsmsActiveConnection`.
For the passive connection there are two implementations:

* :class:`secsgem.hsms.connections.HsmsPassiveConnection` handles one connection at a time.

All connection classes are based on the :class:`secsgem.hsms.connections.HsmsConnection` class, which provides common functionality for all connection types.

The connection process for active and passive connections can be started with the :func:`secsgem.hsms.connections.HsmsPassiveConnection.enable` function, and stopped with the :func:`secsgem.hsms.connections.HsmsPassiveConnection.disable` function.

Delegates
---------

All connections work with delegates.
When a connection is established/terminated or a message is received a method of the passed delegate object will be called.
The connections support the following delegates:

* on_connection_established(connection)
* on_connection_message_received(response)
* on_connection_before_closed(connection)
* on_connection_closed(connection)

Sample delegate class::

    class DelegateSample:
        def on_connection_established(self, connection):
            print "Connection established"

        def on_connection_message_received(self, connection, packet):
            print "Message received", message

        def on_connection_before_closed(self, connection):
            print "Connection about to be terminated"

        def on_connection_closed(self, connection):
            print "Connection terminated"

Active connection
-----------------

For the active connection the first parameter is the IP address of the peer, the second parameter is the port of the peer.
The third parameter is the session id the peer is configured for.

Example::

    >>> delegate = DelegateSample()
    >>> conn = secsgem.HsmsActiveConnection('10.211.55.33', 5000, 0, delegate)
    >>> conn.enable()
    Connection established
    Packet received header: {session_id:0x0000, stream:00, function:04, p_type:0x00, s_type:0x07, system:0x00000000, require_response:0}
    Packet received header: {session_id:0x0000, stream:00, function:01, p_type:0x00, s_type:0x07, system:0x00000000, require_response:0}
    Connection about to be terminated
    Connection terminated
    >>> conn.disable()

Passive connection
------------------

For the passive connection the first parameter is the expected IP address of the peer, the second parameter is the port to listen on.
The third parameter is the session id the peer is configured for.

Example::

    >>> delegate = DelegateSample()
    >>> conn = secsgem.HsmsPassiveConnection('10.211.55.33', 5000, 0, delegate)
    >>> conn.enable()
    Connection established
    Packet received header: {session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x01, system:0x00000001, require_response:0}
    Packet received header: {session_id:0x0000, stream:00, function:03, p_type:0x00, s_type:0x07, system:0x00000000, require_response:0}
    Connection about to be terminated
    Connection terminated
    >>> conn.disable()

