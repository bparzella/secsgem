Packets
=======

A HSMS packet :py:class:`secsgem.hsms.packets.HsmsPacket` consists of a header :py:class:`secsgem.hsms.packets.HsmsHeader` and a data part represented by a string.
The string contains the additional data encoded as ASCII characters for transmission over TCP. The additional data is only required for a stream/function packet.

    >>> secsgem.hsms.packets.HsmsPacket(secsgem.hsms.packets.HsmsLinktestReqHeader(2))
    secsgem.hsms.packets.HsmsPacket({'header': secsgem.hsms.packets.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

Every header has a system id to match the response to a certain request.
The system id is the first parameter to the headers constructor.
The connection keeps track of the system id, a new one can be requested with the :py:func:`secsgem.hsms.connections.HsmsConnection.get_next_system_counter` function.

HSMS packet objects can encode themselves with the :py:func:`secsgem.hsms.packets.HsmsPacket.encode` function to a string, which can be sent over the TCP connection.

    >>> packet = secsgem.hsms.packets.HsmsPacket(secsgem.hsms.packets.HsmsLinktestReqHeader(2))
    >>> secsgem.common.format_hex(packet.encode())
    '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

The other way around, a HSMS packet object can be created from the ASCII string with the :py:func:`secsgem.hsms.packets.HsmsPacket.decode` function.

    >>> secsgem.hsms.packets.HsmsPacket.decode(packetData)
    secsgem.hsms.packets.HsmsPacket({'header': secsgem.hsms.packets.HsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

There are classes inherited from :py:class:`secsgem.hsms.packets.HsmsHeader` for all HSMS packet types available:

+----------------------+-----------------------------------------------------------+-------+
| Type                 | Class                                                     | SType |
+======================+===========================================================+=======+
| `Select Request`_    | :py:class:`secsgem.hsms.packets.HsmsSelectReqHeader`      | 1     |
+----------------------+-----------------------------------------------------------+-------+
| `Select Response`_   | :py:class:`secsgem.hsms.packets.HsmsSelectRspHeader`      | 2     |
+----------------------+-----------------------------------------------------------+-------+
| `Deselect Request`_  | :py:class:`secsgem.hsms.packets.HsmsDeselectReqHeader`    | 3     |
+----------------------+-----------------------------------------------------------+-------+
| `Deselect Response`_ | :py:class:`secsgem.hsms.packets.HsmsDeselectRspHeader`    | 4     |
+----------------------+-----------------------------------------------------------+-------+
| `Linktest Request`_  | :py:class:`secsgem.hsms.packets.HsmsLinktestReqHeader`    | 5     |
+----------------------+-----------------------------------------------------------+-------+
| `Linktest Response`_ | :py:class:`secsgem.hsms.packets.HsmsLinktestRspHeader`    | 6     |
+----------------------+-----------------------------------------------------------+-------+
| `Reject Request`_    | :py:class:`secsgem.hsms.packets.HsmsRejectReqHeader`      | 7     |
+----------------------+-----------------------------------------------------------+-------+
| `Separate Request`_  | :py:class:`secsgem.hsms.packets.HsmsSeparateReqHeader`    | 9     |
+----------------------+-----------------------------------------------------------+-------+
| `Data Message`_      | :py:class:`secsgem.hsms.packets.HsmsStreamFunctionHeader` | 0     |
+----------------------+-----------------------------------------------------------+-------+

Select Request
--------------

Establish HSMS communication

    >>> secsgem.hsms.packets.HsmsSelectReqHeader(14)
    secsgem.hsms.packets.HsmsSelectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 14, 'sessionID': 65535, 'requireResponse': False, 'sType': 1})


Select Response
---------------

Result of select request

    >>> secsgem.hsms.packets.HsmsSelectRspHeader(24)
    secsgem.hsms.packets.HsmsSelectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 24, 'sessionID': 65535, 'requireResponse': False, 'sType': 2})


Deselect Request
----------------

Grateful close HSMS communication before disconnecting

    >>> secsgem.hsms.packets.HsmsDeselectReqHeader(1)
    secsgem.hsms.packets.HsmsDeselectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 3})


Deselect Response
-----------------

Result of deselect request

    >>> secsgem.hsms.packets.HsmsDeselectRspHeader(1)
    secsgem.hsms.packets.HsmsDeselectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 4})


Linktest Request
----------------

Check the HSMS connection link is good

    >>> secsgem.hsms.packets.HsmsLinktestReqHeader(2)
    secsgem.hsms.packets.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5})


Linktest Response
-----------------

Result of linktest request

    >>> secsgem.hsms.packets.HsmsLinktestRspHeader(10)
    secsgem.hsms.packets.HsmsLinktestRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 10, 'sessionID': 65535, 'requireResponse': False, 'sType': 6})


Reject Request
--------------

Response to unsupported HSMS message

    >>> secsgem.hsms.packets.HsmsRejectReqHeader(17, 3, 4)
    secsgem.hsms.packets.HsmsRejectReqHeader({'function': 4, 'stream': 3, 'pType': 0, 'system': 17, 'sessionID': 65535, 'requireResponse': False, 'sType': 7})


Separate Request
----------------

Immediate termination of the HSMS connection

    >>> secsgem.hsms.packets.HsmsSeparateReqHeader(17)
    secsgem.hsms.packets.HsmsSeparateReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 17, 'sessionID': 65535, 'requireResponse': False, 'sType': 9})


Data Message
------------

Secs stream and function message

    >>> secsgem.hsms.packets.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
    secsgem.hsms.packets.HsmsStreamFunctionHeader({'function': 1, 'stream': 1, 'pType': 0, 'system': 22, 'sessionID': 100, 'requireResponse': True, 'sType': 0})
