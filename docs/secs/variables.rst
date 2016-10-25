Variables
=========

SECS defines a few types to transmit data in.

+-------------------------+------------------------------------------------+------+
| Data Type               | Class                                          | Code |
+=========================+================================================+======+
| List                    | :class:`secsgem.secs.variables.SecsVarArray`   | L    |
+-------------------------+------------------------------------------------+------+
| List                    | :class:`secsgem.secs.variables.SecsVarList`    | L    |
+-------------------------+------------------------------------------------+------+
| Binary                  | :class:`secsgem.secs.variables.SecsVarBinary`  | B    |
+-------------------------+------------------------------------------------+------+
| Boolean                 | :class:`secsgem.secs.variables.SecsVarBoolean` | TF   |
+-------------------------+------------------------------------------------+------+
| ASCII                   | :class:`secsgem.secs.variables.SecsVarString`  | A    |
+-------------------------+------------------------------------------------+------+
| 8-Byte integer          | :class:`secsgem.secs.variables.SecsVarI8`      | I8   |
+-------------------------+------------------------------------------------+------+
| 1-Byte integer          | :class:`secsgem.secs.variables.SecsVarI1`      | I1   |
+-------------------------+------------------------------------------------+------+
| 2-Byte integer          | :class:`secsgem.secs.variables.SecsVarI2`      | I2   |
+-------------------------+------------------------------------------------+------+
| 4-Byte integer          | :class:`secsgem.secs.variables.SecsVarI4`      | I4   |
+-------------------------+------------------------------------------------+------+
| 8-Byte float            | :class:`secsgem.secs.variables.SecsVarF8`      | F8   |
+-------------------------+------------------------------------------------+------+
| 4-Byte float            | :class:`secsgem.secs.variables.SecsVarF4`      | F8   |
+-------------------------+------------------------------------------------+------+
| 8-Byte unsigned integer | :class:`secsgem.secs.variables.SecsVarU8`      | U8   |
+-------------------------+------------------------------------------------+------+
| 1-Byte unsigned integer | :class:`secsgem.secs.variables.SecsVarU1`      | U1   |
+-------------------------+------------------------------------------------+------+
| 2-Byte unsigned integer | :class:`secsgem.secs.variables.SecsVarU2`      | U2   |
+-------------------------+------------------------------------------------+------+
| 4-Byte unsigned integer | :class:`secsgem.secs.variables.SecsVarU4`      | U4   |
+-------------------------+------------------------------------------------+------+

Example:

    >>> secsgem.SecsVarString("TESTString")
    <A "TESTString">
    >>> secsgem.SecsVarBoolean(True)
    <BOOLEAN True >
    >>> secsgem.SecsVarU4(1337)
    <U4 1337 >

Type arrays
-----------

The numeric types can also be an array of that type:

    >>> secsgem.SecsVarU1([1, 2, 3, 4])
    <U1 1 2 3 4 >
    >>> secsgem.SecsVarBoolean([True, False, False, True])
    <BOOLEAN True False False True >

The length of this array can be fixed with the length parameter:

    >>> secsgem.SecsVarU1([1, 2, 3], count=3)
    <U1 1 2 3 >
    >>> secsgem.SecsVarU1([1, 2, 3, 4], count=3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1439, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1537, in set
        raise ValueError("Value longer than {} chars".format(self.count))
    ValueError: Value longer than 3 chars

    >>> secsgem.SecsVarString("Hello", count=3).get()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1220, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1337, in set
        raise ValueError("Value longer than {} chars ({} chars)".format(self.count, len(value)))
    ValueError: Value longer than 3 chars (5 chars)

Getting data
------------

The data can be accessed with the :func:`secsgem.secs.variables.SecsVarU1.get` method, arrays can be accessed using the index operator:

    >>> secsgem.SecsVarU1(1).get()
    1
    >>> secsgem.SecsVarU1([1, 2, 3], count=3).get()
    [1, 2, 3]
    >>> secsgem.SecsVarU1(1)[0]
    1
    >>> secsgem.SecsVarU1([1, 2, 3])[1]
    2

Setting data
------------

The data can be set with the :func:`secsgem.secs.variables.SecsVarString.set` method, arrays can be updated using the index operator:

    >>> v=secsgem.SecsVarU1([1, 2, 3], count=3)
    >>> v.set([3, 2, 1])
    >>> v
    <U1 3 2 1 >
    >>> v[0] = 1
    >>> v
    <U1 1 2 1 >

En-/Decoding
------------

The variable types can :func:`secsgem.secs.variables.SecsVarArray.encode` and :func:`secsgem.secs.variables.SecsVarString.decode` themselves to ASCII data transferrable with the HSMS protocol:

    >>> v=secsgem.SecsVarString("Hello")
    >>> d=v.encode()
    >>> d
    'A\x05Hello'
    >>> secsgem.format_hex(d)
    '41:05:48:65:6c:6c:6f'
    >>> v.set("NewText")
    >>> v
    <A "NewText">
    >>> v.decode(d)
    7
    >>> v
    <A "Hello">

SecsVarArray
------------

:class:`secsgem.secs.variables.SecsVarArray` is a special type for a list of the same type.
The items of the array can be accessed with the index operator.

    >>> v=secsgem.SecsVarArray(secsgem.SecsVarU4)
    >>> v.set([1, 2, 3])
    >>> v
    <L [3]
    <U4 1 >
    <U4 2 >
    <U4 3 >

    >
    >>> v.get()
    [1, 2, 3]
    >>> v[1]
    <U4 2 >

A new item can be appended to the array with the :func:`secsgem.secs.variables.SecsVarArray.append` method.

SecsVarList
-----------

:class:`secsgem.secs.variables.SecsVarList` is a special type for a list of the different types.
The items of the list can be accessed like properties of the object.

An ordered dictionary is required for the creation, because pythons default dictionary will be randomly sorted.
Sorting is essential because both peers need to have the data in the same order.

    >>> v=secsgem.SecsVarList([secsgem.OBJACK, secsgem.SOFTREV])
    >>> v.OBJACK=3
    >>> v.SOFTREV="Hallo"
    >>> v
    <L [2]
    <U1 3 >
    <A "Hallo">

    >
    >>> v.SOFTREV
    <A "Hallo">
    >>> secsgem.format_hex(v.encode())
    '01:02:a5:01:03:41:05:48:61:6c:6c:6f'

SecsVarDynamic
--------------

:class:`secsgem.secs.variables.SecsVarDynamic` can take different types, if specified to a certain set of types.

    >>> v=secsgem.SecsVarDynamic([secsgem.SecsVarString, secsgem.SecsVarU1])
    >>> v.set(secsgem.SecsVarString("Hello"))
    >>> v
    <A "Hello">
    >>> v.set(secsgem.SecsVarU1(10))
    >>> v
    <U1 10 >
    >>> v.set(secsgem.SecsVarU4(10))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 255, in set
        raise ValueError("Unsupported type {} for this instance of SecsVarDynamic, allowed {}".format(value.__class__.__name__, self.types))
    ValueError: Unsupported type SecsVarU4 for this instance of SecsVarDynamic, allowed [<class 'secsgem.secs.variables.SecsVarString'>, <class 'secsgem.secs.variables.SecsVarU1'>]
