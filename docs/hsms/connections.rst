Connections
===========

HSMS has active and passive connections.
The active connection is the one making the connection, the passive one is waiting for the incoming connection.

The implementation for the active connection is :class:`secsgem.hsms.connections.HsmsActiveConnection`.
For the passive connection there are two implementations:

* :class:`secsgem.hsms.connections.HsmsPassiveConnection` handles only one connection at a time.
* :class:`secsgem.hsms.connections.HsmsMultiPassiveConnection` together with :class:`secsgem.hsms.connections.HsmsMultiPassiveServer` handle multiple connections from different peers.

All connection classes are based on the :class:`secsgem.hsms.connections.HsmsConnection` class, which provides common functionality for all connection types.

The connection process for active and passive connections can be started with the :func:`secsgem.hsms.connections.HsmsPassiveConnection.enable` function, and stopped with the :func:`secsgem.hsms.connections.HsmsPassiveConnection.disable` function.

Delegates
---------

All connections work with delegates.
When a connection is established/terminated or a packet is received a method of the passed delegate object will be called.
The connections support the following delegates:

* on_connection_established(connection)
* on_connection_packet_received(response)
* on_connection_before_closed(connection)
* on_connection_closed(connection)

Sample delegate class::

    class DelegateSample:
        def on_connection_established(self, connection):
            print "Connection established"

        def on_connection_packet_received(self, connection, packet):
            print "Packet received", packet

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
    Packet received header: {sessionID:0x0000, stream:00, function:04, pType:0x00, sType:0x07, system:0x00000000, requireResponse:0}
    Packet received header: {sessionID:0x0000, stream:00, function:01, pType:0x00, sType:0x07, system:0x00000000, requireResponse:0}
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
    Packet received header: {sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x01, system:0x00000001, requireResponse:0}
    Packet received header: {sessionID:0x0000, stream:00, function:03, pType:0x00, sType:0x07, system:0x00000000, requireResponse:0}
    Connection about to be terminated
    Connection terminated
    >>> conn.disable()

Multi-passive connection
------------------------

In this mode one listening port handles the incoming connections for more than one peer.
A instance of :class:`secsgem.hsms.connections.HsmsMultiPassiveServer` is created and connection is created using its :func:`secsgem.hsms.connections.HsmsMultiPassiveServer.create_connection` method.
The parameters of the method are the same as for the `Passive connection`_. For every available peer a connection must be created using this method.

Example::

    >>> delegate = DelegateSample()
    >>> server = secsgem.HsmsMultiPassiveServer(5000)
    >>> conn = server.create_connection('10.211.55.33', 5000, 0, delegate)
    >>> conn.enable()
    >>> server.start()
    Connection established
    Packet received header: {sessionID:0xffff, stream:00, function:00, pType:0x00, sType:0x01, system:0x00000003, requireResponse:0}
    Packet received header: {sessionID:0x0000, stream:00, function:03, pType:0x00, sType:0x07, system:0x00000000, requireResponse:0}
    Connection about to be terminated
    Connection terminated
    >>> conn.disable()
    >>> server.stop()

Connection manager
------------------

The :class:`secsgem.hsms.connectionmanager.HsmsConnectionManager` can be used to manage multiple active and passive connections.
It creates and removes :class:`secsgem.hsms.connections.HsmsActiveConnection` and :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`/:class:`secsgem.hsms.connections.HsmsMultiPassiveConnection` dynamically.

    >>> manager=secsgem.HsmsConnectionManager()
    >>> handler=manager.add_peer("connection", '10.211.55.33', 5000, False, 0)
    >>> handler.enable()
    >>> handler.send_linktest_req()
    secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 13, 'sessionID': 65535, 'requireResponse': False, 'sType': 6}), 'data': ''})
    >>> handler.disable()
    >>> manager.stop()

Connection manager works with :doc:`handlers <handler>` which take care of a lot of the required communication on the matching level (:class:`secsgem.hsms.handler.HsmsHandler`, :class:`secsgem.secs.handler.SecsHandler` and :class:`secsgem.gem.handler.GemHandler`).