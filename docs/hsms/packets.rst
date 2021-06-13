Packets
=======

A HSMS packet :class:`secsgem.hsms.HsmsPacket` consists of a header :class:`secsgem.hsms.HsmsHeader` and a data part represented by a string.
The string contains the additional data encoded as ASCII characters for transmission over TCP. The additional data is only required for a stream/function packet.

    >>> secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
    secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

Every header has a system id to match the response to a certain request.
The system id is the first parameter to the headers constructor.
The connection keeps track of the system id, a new one can be requested with the :func:`secsgem.hsms.connections.HsmsConnection.get_next_system_counter` function.

HSMS packet objects can encode themselves with the :func:`secsgem.hsms.HsmsPacket.encode` function to a string, which can be sent over the TCP connection.

    >>> packet = secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
    >>> secsgem.common.format_hex(packet.encode())
    '00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'

The other way around, a HSMS packet object can be created from the ASCII string with the :func:`secsgem.hsms.HsmsPacket.decode` function.

    >>> secsgem.hsms.HsmsPacket.decode(packetData)
    secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5}), 'data': ''})

There are classes inherited from :class:`secsgem.hsms.HsmsHeader` for all HSMS packet types available:

+----------------------+--------------------------------------------------------+-------+
| Type                 | Class                                                  | SType |
+======================+========================================================+=======+
| `Select Request`_    | :class:`secsgem.hsms.HsmsSelectReqHeader`      | 1     |
+----------------------+--------------------------------------------------------+-------+
| `Select Response`_   | :class:`secsgem.hsms.HsmsSelectRspHeader`      | 2     |
+----------------------+--------------------------------------------------------+-------+
| `Deselect Request`_  | :class:`secsgem.hsms.HsmsDeselectReqHeader`    | 3     |
+----------------------+--------------------------------------------------------+-------+
| `Deselect Response`_ | :class:`secsgem.hsms.HsmsDeselectRspHeader`    | 4     |
+----------------------+--------------------------------------------------------+-------+
| `Linktest Request`_  | :class:`secsgem.hsms.HsmsLinktestReqHeader`    | 5     |
+----------------------+--------------------------------------------------------+-------+
| `Linktest Response`_ | :class:`secsgem.hsms.HsmsLinktestRspHeader`    | 6     |
+----------------------+--------------------------------------------------------+-------+
| `Reject Request`_    | :class:`secsgem.hsms.HsmsRejectReqHeader`      | 7     |
+----------------------+--------------------------------------------------------+-------+
| `Separate Request`_  | :class:`secsgem.hsms.HsmsSeparateReqHeader`    | 9     |
+----------------------+--------------------------------------------------------+-------+
| `Data Message`_      | :class:`secsgem.hsms.HsmsStreamFunctionHeader` | 0     |
+----------------------+--------------------------------------------------------+-------+

Select Request
--------------

Establish HSMS communication

    >>> secsgem.hsms.HsmsSelectReqHeader(14)
    secsgem.hsms.HsmsSelectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 14, 'sessionID': 65535, 'requireResponse': False, 'sType': 1})


Select Response
---------------

Result of select request

    >>> secsgem.hsms.HsmsSelectRspHeader(24)
    secsgem.hsms.HsmsSelectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 24, 'sessionID': 65535, 'requireResponse': False, 'sType': 2})


Deselect Request
----------------

Grateful close HSMS communication before disconnecting

    >>> secsgem.hsms.HsmsDeselectReqHeader(1)
    secsgem.hsms.HsmsDeselectReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 3})


Deselect Response
-----------------

Result of deselect request

    >>> secsgem.hsms.HsmsDeselectRspHeader(1)
    secsgem.hsms.HsmsDeselectRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 1, 'sessionID': 65535, 'requireResponse': False, 'sType': 4})


Linktest Request
----------------

Check the HSMS connection link is good

    >>> secsgem.hsms.HsmsLinktestReqHeader(2)
    secsgem.hsms.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 2, 'sessionID': 65535, 'requireResponse': False, 'sType': 5})


Linktest Response
-----------------

Result of linktest request

    >>> secsgem.hsms.HsmsLinktestRspHeader(10)
    secsgem.hsms.HsmsLinktestRspHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 10, 'sessionID': 65535, 'requireResponse': False, 'sType': 6})


Reject Request
--------------

Response to unsupported HSMS message

    >>> secsgem.hsms.HsmsRejectReqHeader(17, 3, 4)
    secsgem.hsms.HsmsRejectReqHeader({'function': 4, 'stream': 3, 'pType': 0, 'system': 17, 'sessionID': 65535, 'requireResponse': False, 'sType': 7})


Separate Request
----------------

Immediate termination of the HSMS connection

    >>> secsgem.hsms.HsmsSeparateReqHeader(17)
    secsgem.hsms.HsmsSeparateReqHeader({'function': 0, 'stream': 0, 'pType': 0, 'system': 17, 'sessionID': 65535, 'requireResponse': False, 'sType': 9})


Data Message
------------

Secs stream and function message

    >>> secsgem.hsms.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
    secsgem.hsms.HsmsStreamFunctionHeader({'function': 1, 'stream': 1, 'pType': 0, 'system': 22, 'sessionID': 100, 'requireResponse': True, 'sType': 0})
