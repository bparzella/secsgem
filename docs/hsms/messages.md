# Messages and blocks

A HSMS message {py:class}`secsgem.hsms.HsmsMessage` consists of a header {py:class}`secsgem.hsms.HsmsHeader` and a list of blocks {py:class}`secsgem.hsms.HsmsBlock`.

It is initialized with a data field which is used to automatically generate the blocks.
The blocks are parts of the data field, that are transmitted.
For HSMS data only one block exists in a message, as the message doesn't need to be split. 

```python
>>> secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(2), b"")
HsmsMessage({'header': HsmsLinktestReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x05, system:0x00000002, require_response:False}), 'data': ''})
```

Every header has a system id to match the response to a certain request.
The system id is the first parameter to the headers constructor.
The connection keeps track of the system id, a new one can be requested with the {py:func}`secsgem.hsms.HsmsProtocol.get_next_system_counter` function.

HSMS block objects can encode themselves with the {py:func}`secsgem.hsms.HsmsBlock.encode` function to a byte array, which can be sent over the TCP connection.

```python
>>> message = secsgem.hsms.HsmsMessage(secsgem.hsms.HsmsLinktestReqHeader(2), b"")
>>> secsgem.common.format_hex(message.blocks[0].encode())
'00:00:00:0a:ff:ff:00:00:00:05:00:00:00:02'
```

The other way around, a HSMS block object can be created from the byte array with the {py:func}`secsgem.hsms.HsmsBlock.decode` function.

```python
>>> secsgem.hsms.HsmsBlock.decode(packetData)
<secsgem.hsms.message.HsmsBlock object at 0x1082c4f80>
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
HsmsSelectReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x01, system:0x0000000e, require_response:False})
```

## Select Response

Result of select request

```python
>>> secsgem.hsms.HsmsSelectRspHeader(24)
HsmsSelectRspHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x02, system:0x00000018, require_response:False})
```

## Deselect Request

Grateful close HSMS communication before disconnecting

```python
>>> secsgem.hsms.HsmsDeselectReqHeader(1)
HsmsDeselectReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x03, system:0x00000001, require_response:False})
```

## Deselect Response

Result of deselect request

```python
>>> secsgem.hsms.HsmsDeselectRspHeader(1)
HsmsDeselectRspHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x04, system:0x00000001, require_response:False})
```

## Linktest Request

Check the HSMS connection link is good

```python
>>> secsgem.hsms.HsmsLinktestReqHeader(2)
HsmsLinktestReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x05, system:0x00000002, require_response:False})
```

## Linktest Response

Result of linktest request

```python
>>> secsgem.hsms.HsmsLinktestRspHeader(10)
HsmsLinktestRspHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x06, system:0x0000000a, require_response:False})
```

## Reject Request

Response to unsupported HSMS message

```python
>>> secsgem.hsms.HsmsRejectReqHeader(17, secsgem.hsms.HsmsSType.DESELECT_REQ, 4)
HsmsRejectReqHeader({session_id:0xffff, stream:03, function:04, p_type:0x00, s_type:0x07, system:0x00000011, require_response:False})
```

## Separate Request

Immediate termination of the HSMS connection

```python
>>> secsgem.hsms.HsmsSeparateReqHeader(17)
HsmsSeparateReqHeader({session_id:0xffff, stream:00, function:00, p_type:0x00, s_type:0x09, system:0x00000011, require_response:False})
```

## Data Message

Secs stream and function message

```python
>>> secsgem.hsms.HsmsStreamFunctionHeader(22, 1, 1, True, 100)
HsmsStreamFunctionHeader({session_id:0x0064, stream:01, function:01, p_type:0x00, s_type:0x00, system:0x00000016, require_response:True})
```