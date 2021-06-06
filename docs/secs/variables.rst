Variables
=========

SECS defines a few types to transmit data in.

+-------------------------+-----------------------------------------+------+
| Data Type               | Class                                   | Code |
+=========================+=========================================+======+
| List                    | :class:`secsgem.secs.variables.Array`   | L    |
+-------------------------+-----------------------------------------+------+
| List                    | :class:`secsgem.secs.variables.List`    | L    |
+-------------------------+-----------------------------------------+------+
| Binary                  | :class:`secsgem.secs.variables.Binary`  | B    |
+-------------------------+-----------------------------------------+------+
| Boolean                 | :class:`secsgem.secs.variables.Boolean` | TF   |
+-------------------------+-----------------------------------------+------+
| ASCII                   | :class:`secsgem.secs.variables.String`  | A    |
+-------------------------+-----------------------------------------+------+
| 8-Byte integer          | :class:`secsgem.secs.variables.I8`      | I8   |
+-------------------------+-----------------------------------------+------+
| 1-Byte integer          | :class:`secsgem.secs.variables.I1`      | I1   |
+-------------------------+-----------------------------------------+------+
| 2-Byte integer          | :class:`secsgem.secs.variables.I2`      | I2   |
+-------------------------+-----------------------------------------+------+
| 4-Byte integer          | :class:`secsgem.secs.variables.I4`      | I4   |
+-------------------------+-----------------------------------------+------+
| 8-Byte float            | :class:`secsgem.secs.variables.F8`      | F8   |
+-------------------------+-----------------------------------------+------+
| 4-Byte float            | :class:`secsgem.secs.variables.F4`      | F8   |
+-------------------------+-----------------------------------------+------+
| 8-Byte unsigned integer | :class:`secsgem.secs.variables.U8`      | U8   |
+-------------------------+-----------------------------------------+------+
| 1-Byte unsigned integer | :class:`secsgem.secs.variables.U1`      | U1   |
+-------------------------+-----------------------------------------+------+
| 2-Byte unsigned integer | :class:`secsgem.secs.variables.U2`      | U2   |
+-------------------------+-----------------------------------------+------+
| 4-Byte unsigned integer | :class:`secsgem.secs.variables.U4`      | U4   |
+-------------------------+-----------------------------------------+------+

Example:

    >>> secsgem.String("TESTString")
    <A "TESTString">
    >>> secsgem.Boolean(True)
    <BOOLEAN True >
    >>> secsgem.U4(1337)
    <U4 1337 >

Type arrays
-----------

The numeric types can also be an array of that type:

    >>> secsgem.U1([1, 2, 3, 4])
    <U1 1 2 3 4 >
    >>> secsgem.Boolean([True, False, False, True])
    <BOOLEAN True False False True >

The length of this array can be fixed with the length parameter:

    >>> secsgem.U1([1, 2, 3], count=3)
    <U1 1 2 3 >
    >>> secsgem.U1([1, 2, 3, 4], count=3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1439, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1537, in set
        raise ValueError("Value longer than {} chars".format(self.count))
    ValueError: Value longer than 3 chars

    >>> secsgem.String("Hello", count=3).get()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1220, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1337, in set
        raise ValueError("Value longer than {} chars ({} chars)".format(self.count, len(value)))
    ValueError: Value longer than 3 chars (5 chars)

Getting data
------------

The data can be accessed with the :func:`secsgem.secs.variables.U1.get` method, arrays can be accessed using the index operator:

    >>> secsgem.U1(1).get()
    1
    >>> secsgem.U1([1, 2, 3], count=3).get()
    [1, 2, 3]
    >>> secsgem.U1(1)[0]
    1
    >>> secsgem.U1([1, 2, 3])[1]
    2

Setting data
------------

The data can be set with the :func:`secsgem.secs.variables.String.set` method, arrays can be updated using the index operator:

    >>> v=secsgem.U1([1, 2, 3], count=3)
    >>> v.set([3, 2, 1])
    >>> v
    <U1 3 2 1 >
    >>> v[0] = 1
    >>> v
    <U1 1 2 1 >

En-/Decoding
------------

The variable types can :func:`secsgem.secs.variables.Array.encode` and :func:`secsgem.secs.variables.String.decode` themselves to ASCII data transferrable with the HSMS protocol:

    >>> v=secsgem.String("Hello")
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

Array
-----

:class:`secsgem.secs.variables.Array` is a special type for a list of the same type.
The items of the array can be accessed with the index operator.

    >>> v=secsgem.Array(secsgem.U4)
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

A new item can be appended to the array with the :func:`secsgem.secs.variables.Array.append` method.

List
----

:class:`secsgem.secs.variables.List` is a special type for a list of the different types.
The items of the list can be accessed like properties of the object.

An ordered dictionary is required for the creation, because pythons default dictionary will be randomly sorted.
Sorting is essential because both peers need to have the data in the same order.

    >>> v=secsgem.List([secsgem.OBJACK, secsgem.SOFTREV])
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

Dynamic
-------

:class:`secsgem.secs.variables.Dynamic` can take different types, if specified to a certain set of types.

    >>> v=secsgem.Dynamic([secsgem.String, secsgem.U1])
    >>> v.set(secsgem.String("Hello"))
    >>> v
    <A "Hello">
    >>> v.set(secsgem.U1(10))
    >>> v
    <U1 10 >
    >>> v.set(secsgem.U4(10))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 255, in set
        raise ValueError("Unsupported type {} for this instance of Dynamic, allowed {}".format(value.__class__.__name__, self.types))
    ValueError: Unsupported type U4 for this instance of Dynamic, allowed [<class 'secsgem.secs.variables.String'>, <class 'secsgem.secs.variables.U1'>]
