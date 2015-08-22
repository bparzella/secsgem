Functions
---------

A function is inherited from :class:`secsgem.secs.functionbase.SecsStreamFunction`.
When inheriting a function only _stream, _function and _formatDescriptor must be overwritten.
Evervthing else is implemented in the base class.

**Example**::

    class SecsS02F33(secsgem.SecsStreamFunction):
        _stream = 2
        _function = 33

        _formatDescriptor = secsgem.SecsVarList(OrderedDict((
            ("DATAID", secsgem.SecsVarU4(1)),
            ("DATA", secsgem.SecsVarArray(
                secsgem.SecsVarList(OrderedDict((
                    ("RPTID", secsgem.SecsVarU4(1)),
                    ("VID", secsgem.SecsVarArray(
                        secsgem.SecsVarString()
                    )),
                )), 2)
            )),
        )), 2)

The data of a function can be read and manipulated with the same functionality as the variables.
:func:`secsgem.secs.functionbase.SecsStreamFunction.set`, :func:`secsgem.secs.functionbase.SecsStreamFunction.get`, :func:`secsgem.secs.functionbase.SecsStreamFunction.append`, the index operator and object properties.
The objects can also en- and decode themselves.

**Usage**::

    >>> f=secsgem.SecsS02F33()
    >>> f.DATAID=10
    >>> f.DATA.append({"RPTID": 5, "VID": ["Hello", "Hallo"]})
    >>> f.DATA.append({"RPTID": 6, "VID": ["1", "2"]})
    >>> f
    S2F33 { [DATAID: U4 10, DATA: [[RPTID: U4 5, VID: [A 'Hello', A 'Hallo']], [RPTID: U4 6, VID: [A '1', A '2']]]] }
    >>> f.DATA[1].VID[0]="Goodbye"
    >>> f.DATA[1].VID[1]="Auf Wiedersehen"
    >>> f
    S2F33 { [DATAID: U4 10, DATA: [[RPTID: U4 5, VID: [A 'Hello', A 'Hallo']], [RPTID: U4 6, VID: [A 'Goodbye', A 'Auf Wiedersehen']]]] }
    >>> secsgem.format_hex(f.encode())
    '01:02:b1:04:00:00:00:0a:01:02:01:02:b1:04:00:00:00:05:01:02:41:05:48:65:6c:6c:6f:41:05:48:61:6c:6c:6f:01:02:b1:04:00:00:00:06:01:02:41:07:47:6f:6f:64:62:79:65:41:0f:41:75:66:20:57:69:65:64:65:72:73:65:68:65:6e'

The encoded data can be used as data string in a :class:`secsgem.hsms.packets.HsmsPacket` together with a :class:`secsgem.hsms.packets.HsmsStreamFunctionHeader`. See :doc:`/hsms/packets`.