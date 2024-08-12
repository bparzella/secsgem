# Packets

A HSMS packet {py:class}`secsgem.hsms.HsmsPacket` consists of a header {py:class}`secsgem.hsms.HsmsHeader` and a data part represented by a string.
The string contains the additional data encoded as ASCII characters for transmission over TCP.
The additional data is only required for a stream/function packet.

```python
>>> secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 2, 'session_id': 65535, 'require_response': False, 's_type': 5}), 'data': ''})
```

Every header has a system id to match the response to a certain request.
The system id is the first parameter to the headers constructor.
The connection keeps track of the system id, a new one can be requested with the {py:func}`secsgem.hsms.connections.HsmsConnection.get_next_system_counter` function.

HSMS packet objects can encode themselves with the {py:func}`secsgem.hsms.HsmsPacket.encode` function to a string, which can be sent over the TCP connection.

```python
>>> packet = secsgem.hsms.HsmsPacket(secsgem.hsms.HsmsLinktestReqHeader(2))
>>> secsgem.common.format_hex(packet.encode())
'00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'
```

The other way around, a HSMS packet object can be created from the ASCII string with the {py:func}`secsgem.hsms.HsmsPacket.decode` function.

```python
>>> secsgem.hsms.HsmsPacket.decode(packetData)
secsgem.hsms.HsmsPacket({'header': secsgem.hsms.HsmsHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 2, 'session_id': 65535, 'require_response': False, 's_type': 5}), 'data': ''})
```

There are classes inherited from {py:class}`secsgem.hsms.HsmsHeader` for all HSMS packet types available:

| Type | Class | SType |
|---|---|---|
| [Select Request](#select-request) | {py:class}`secsgem.hsms.HsmsSelectReqHeader` | 1 |
| [Select Response](#select-response) | {py:class}`secsgem.hsms.HsmsSelectRspHeader` | 2 |
| [Deselect Request](#deselect-request) | {py:class}`secsgem.hsms.HsmsDeselectReqHeader` | 3 |
| [Deselect Response](#deselect-response) | {py:class}`secsgem.hsms.HsmsDeselectRspHeader` | 4 |
| [Linktest Request](#linktest-request) | {py:class}`secsgem.hsms.HsmsLinktestReqHeader` | 5 |
| [Linktest Response](#linktest-response) | {py:class}`secsgem.hsms.HsmsLinktestRspHeader` | 6 |
| [Reject Request](#reject-request) | {py:class}`secsgem.hsms.HsmsRejectReqHeader` | 7 |
| [Separate Request](#separate-request) | {py:class}`secsgem.hsms.HsmsSeparateReqHeader` | 9 |
| [Data Message](#data-message) | {py:class}`secsgem.hsms.HsmsStreamFunctionHeader` | 0 |

## Select Request

Establish HSMS communication

```python
>>> secsgem.hsms.HsmsSelectReqHeader(14)
secsgem.hsms.HsmsSelectReqHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 14, 'session_id': 65535, 'require_response': False, 's_type': 1})
```

## Select Response

Result of select request

```python
>>> secsgem.hsms.HsmsSelectRspHeader(24)
secsgem.hsms.HsmsSelectRspHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 24, 'session_id': 65535, 'require_response': False, 's_type': 2})
```

## Deselect Request

Grateful close HSMS communication before disconnecting

```python
>>> secsgem.hsms.HsmsDeselectReqHeader(1)
secsgem.hsms.HsmsDeselectReqHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 1, 'session_id': 65535, 'require_response': False, 's_type': 3})
```

## Deselect Response

Result of deselect request

```python
>>> secsgem.hsms.HsmsDeselectRspHeader(1)
secsgem.hsms.HsmsDeselectRspHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 1, 'session_id': 65535, 'require_response': False, 's_type': 4})
```

## Linktest Request

Check the HSMS connection link is good

```python
>>> secsgem.hsms.HsmsLinktestReqHeader(2)
secsgem.hsms.HsmsLinktestReqHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 2, 'session_id': 65535, 'require_response': False, 's_type': 5})
```

## Linktest Response

Result of linktest request

```python
>>> secsgem.hsms.HsmsLinktestRspHeader(10)
secsgem.hsms.HsmsLinktestRspHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 10, 'session_id': 65535, 'require_response': False, 's_type': 6})
```

## Reject Request

Response to unsupported HSMS message

```python
>>> secsgem.hsms.HsmsRejectReqHeader(17, 3, 4)
secsgem.hsms.HsmsRejectReqHeader({'function': 4, 'stream': 3, 'p_type': 0, 'system': 17, 'session_id': 65535, 'require_response': False, 's_type': 7})
```

## Separate Request

Immediate termination of the HSMS connection

```python
>>> secsgem.hsms.HsmsSeparateReqHeader(17)
secsgem.hsms.HsmsSeparateReqHeader({'function': 0, 'stream': 0, 'p_type': 0, 'system': 17, 'session_id': 65535, 'require_response': False, 's_type': 9})
```

## Data Message

Secs stream and function message

```python
>>> secsgem.hsms.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
secsgem.hsms.HsmsStreamFunctionHeader({'function': 1, 'stream': 1, 'p_type': 0, 'system': 22, 'session_id': 100, 'require_response': True, 's_type': 0})
```