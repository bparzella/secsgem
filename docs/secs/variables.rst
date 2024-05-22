Variables
=========

SECS defines a few types to transmit data in.

+-------------------------+-----------------------------------+------+
| Data Type               | Class                             | Code |
+=========================+===================================+======+
| List                    | :class:`secsgem.secs.ItemL`       | L    |
+-------------------------+-----------------------------------+------+
| Binary                  | :class:`secsgem.secs.ItemB`       | B    |
+-------------------------+-----------------------------------+------+
| Boolean                 | :class:`secsgem.secs.ItemBOOLEAN` | TF   |
+-------------------------+-----------------------------------+------+
| ASCII                   | :class:`secsgem.secs.ItemA`       | A    |
+-------------------------+-----------------------------------+------+
| 8-Byte integer          | :class:`secsgem.secs.ItemI8`      | I8   |
+-------------------------+-----------------------------------+------+
| 1-Byte integer          | :class:`secsgem.secs.ItemI1`      | I1   |
+-------------------------+-----------------------------------+------+
| 2-Byte integer          | :class:`secsgem.secs.ItemI2`      | I2   |
+-------------------------+-----------------------------------+------+
| 4-Byte integer          | :class:`secsgem.secs.ItemI4`      | I4   |
+-------------------------+-----------------------------------+------+
| 8-Byte float            | :class:`secsgem.secs.ItemF8`      | F8   |
+-------------------------+-----------------------------------+------+
| 4-Byte float            | :class:`secsgem.secs.ItemF4`      | F8   |
+-------------------------+-----------------------------------+------+
| 8-Byte unsigned integer | :class:`secsgem.secs.ItemU8`      | U8   |
+-------------------------+-----------------------------------+------+
| 1-Byte unsigned integer | :class:`secsgem.secs.ItemU1`      | U1   |
+-------------------------+-----------------------------------+------+
| 2-Byte unsigned integer | :class:`secsgem.secs.ItemU2`      | U2   |
+-------------------------+-----------------------------------+------+
| 4-Byte unsigned integer | :class:`secsgem.secs.ItemU4`      | U4   |
+-------------------------+-----------------------------------+------+

Example:

    >>> secsgem.secs.ItemA("TESTString")
    <A "TESTString">
    >>> secsgem.secs.ItemBOOLEAN(True)
    <BOOLEAN True >
    >>> secsgem.secs.ItemU4(1337)
    <U4 1337 >

Type arrays
-----------

The numeric types can also be an array of that type:

    >>> secsgem.secs.ItemU1([1, 2, 3, 4])
    <U1 1 2 3 4 >
    >>> secsgem.secs.ItemBOOLEAN([True, False, False, True])
    <BOOLEAN True False False True >

The length of this array can be fixed with the length parameter:

    >>> secsgem.secs.ItemU1([1, 2, 3], count=3)
    <U1 1 2 3 >
    >>> secsgem.secs.ItemU1([1, 2, 3, 4], count=3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1439, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1537, in set
        raise ValueError("Value longer than {} chars".format(self.count))
    ValueError: Value longer than 3 chars

    >>> secsgem.secs.ItemA("Hello", count=3).get()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1220, in __init__
        self.set(value)
      File "/home/ext005207/Development/secsgem/secsgem/secs/variables.py", line 1337, in set
        raise ValueError("Value longer than {} chars ({} chars)".format(self.count, len(value)))
    ValueError: Value longer than 3 chars (5 chars)

Getting data
------------

The data can be accessed with the :func:`secsgem.secs.ItemU1.get` method, arrays can be accessed using the index operator:

    >>> secsgem.secs.ItemU1(1).get()
    1
    >>> secsgem.secs.ItemU1([1, 2, 3], count=3).get()
    [1, 2, 3]
    >>> secsgem.secs.ItemU1(1)[0]
    1
    >>> secsgem.secs.ItemU1([1, 2, 3])[1]
    2

Setting data
------------

The data can be set with the :func:`secsgem.secs.ItemA.set` method, arrays can be updated using the index operator:

    >>> v=secsgem.secs.ItemU1([1, 2, 3], count=3)
    >>> v.set([3, 2, 1])
    >>> v
    <U1 3 2 1 >
    >>> v[0] = 1
    >>> v
    <U1 1 2 1 >

En-/Decoding
------------

The variable types can :func:`secsgem.secs.Item.encode` and :func:`secsgem.secs.Item.decode` themselves to ASCII data transferrable with the HSMS protocol:

    >>> v=secsgem.secs.ItemA("Hello")
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

List
----

:class:`secsgem.secs.ItemL` is a special type for a list of the different types.
The items of the list can be accessed like properties of the object.

An ordered dictionary is required for the creation, because pythons default dictionary will be randomly sorted.
Sorting is essential because both peers need to have the data in the same order.

    >>> v=secsgem.secs.ItemA([secsgem.OBJACK, secsgem.SOFTREV])
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
