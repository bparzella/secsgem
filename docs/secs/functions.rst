Functions
=========

A function is inherited from :class:`secsgem.secs.functionbase.SecsStreamFunction`.

**Example**::

    class SecsS02F33(SecsStreamFunction):
        _stream = 2
        _function = 33

        _data_format = [
            DATAID,
            [
                [
                    RPTID,
                    [VID]
                ]
            ]
        ]

        _to_host = False
        _to_equipment = True

        _has_reply = True
        _is_reply_required = True

        _is_multi_block = True

The data of a function can be read and manipulated with the same functionality as the variables.
:func:`secsgem.secs.functionbase.SecsStreamFunction.set`, :func:`secsgem.secs.functionbase.SecsStreamFunction.get`, :func:`secsgem.secs.functionbase.SecsStreamFunction.append`, the index operator and object properties.
The objects can also en- and decode themselves.

**Usage**::

    >>> f=secsgem.secs.functions.SecsS02F33()
    >>> f.DATAID=10
    >>> f.DATA.append({"RPTID": 5, "VID": ["Hello", "Hallo"]})
    >>> f.DATA.append({"RPTID": 6, "VID": ["1", "2"]})
    >>> f
    S2F33 W
    <L [2]
        <U1 10 >
        <L [2]
        <L [2]
            <U1 5 >
            <L [2]
            <A "Hello">
            <A "Hallo">
            >
        >
        <L [2]
            <U1 6 >
            <L [2]
            <A "1">
            <A "2">
            >
        >
        >
    > .
    >>> f.DATA[1].VID[0]="Goodbye"
    >>> f.DATA[1].VID[1]="Auf Wiedersehen"
    >>> f
    S2F33 W
    <L [2]
        <U1 10 >
        <L [2]
        <L [2]
            <U1 5 >
            <L [2]
            <A "Hello">
            <A "Hallo">
            >
        >
        <L [2]
            <U1 6 >
            <L [2]
            <A "Goodbye">
            <A "Auf Wiedersehen">
            >
        >
        >
    > .
    >>> secsgem.format_hex(f.encode())
    '01:02:a5:01:0a:01:02:01:02:a5:01:05:01:02:41:05:48:65:6c:6c:6f:41:05:48:61:6c:6c:6f:01:02:a5:01:06:01:02:41:07:47:6f:6f:64:62:79:65:41:0f:41:75:66:20:57:69:65:64:65:72:73:65:68:65:6e'

The encoded data can be used as data string in a :class:`secsgem.hsms.HsmsPacket` together with a :class:`secsgem.hsms.HsmsStreamFunctionHeader`. See :doc:`/hsms/packets`.