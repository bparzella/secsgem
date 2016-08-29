#####################################################################
# testSecsVariables.py
#
# (c) Copyright 2013-2016, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
import unittest
import nose

from secsgem.secs.variables import *
from secsgem.secs.dataitems import MDLN, OBJACK, SOFTREV

def printable_value(value):
    if isinstance(value, str):
        return value.encode('string_escape')
    elif isinstance(value, unicode):
        return value
    else:
        return str(value).encode('string_escape')

class TestSecsVar(unittest.TestCase):
    def testEncodeItemHeader(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # two bytes
        self.assertEqual(secsvar.encode_item_header(0), "\xB1\x00")
        self.assertEqual(secsvar.encode_item_header(0xFF), "\xB1\xFF")

        # three bytes
        self.assertEqual(secsvar.encode_item_header(0x100), "\xB2\x01\x00")
        self.assertEqual(secsvar.encode_item_header(0xFFFF), "\xB2\xFF\xFF")

        # four bytes
        self.assertEqual(secsvar.encode_item_header(0x10000), "\xB3\x01\x00\x00")
        self.assertEqual(secsvar.encode_item_header(0xFFFFFF), "\xB3\xFF\xFF\xFF")

    def testEncodeItemHeaderTooShort(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # negative value
        with self.assertRaises(ValueError):
            secsvar.encode_item_header(-1)

    def testEncodeItemHeaderTooLong(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # more than three length bytes worth a value
        with self.assertRaises(ValueError):
            secsvar.encode_item_header(0x1000000)

    def testDecodeItemHeader(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # two bytes
        self.assertEqual(secsvar.decode_item_header("\xB1\x00")[2], 0)
        self.assertEqual(secsvar.decode_item_header("\xB1\xFF")[2], 0xFF)

        # three bytes
        self.assertEqual(secsvar.decode_item_header("\xB2\x01\x00")[2], 0x100)
        self.assertEqual(secsvar.decode_item_header("\xB2\xFF\xFF")[2], 0xFFFF)

        # four bytes
        self.assertEqual(secsvar.decode_item_header("\xB3\x01\x00\x00")[2], 0x10000)
        self.assertEqual(secsvar.decode_item_header("\xB3\xFF\xFF\xFF")[2], 0xFFFFFF)

    def testDecodeItemHeaderEmpty(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        with self.assertRaises(ValueError):
            secsvar.decode_item_header("")

    def testDecodeItemHeaderIllegalPosition(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        with self.assertRaises(IndexError):
            secsvar.decode_item_header("\xB1\x00", 10)

    def testDecodeItemHeaderIllegalData(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # two bytes
        with self.assertRaises(ValueError):
            secsvar.decode_item_header("somerandomdata")


class TestSecsVarDynamic(unittest.TestCase):
    def testConstructorU4(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        secsvar.set(10)

        self.assertEqual(10, secsvar.get())

    def testConstructorWrongType(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        with self.assertRaises(ValueError):
            secsvar.set("testString")
        with self.assertRaises(ValueError):
            secsvar.set(SecsVarString(value="testString"))
        with self.assertRaises(ValueError):
            SecsVarDynamic([SecsVarU4], value="testString")

    def testConstructorWrongLengthString(self):
        secsvar = SecsVarDynamic([SecsVarString], length=5)

        with self.assertRaises(ValueError):
            secsvar.set("testString")

    def testConstructorLen(self):
        secsvar = SecsVarDynamic([SecsVarString])

        secsvar.set("asdfg")

        self.assertEqual(5, len(secsvar))

    def testConstructorSetGetU4(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        secsvar.set(10)

        self.assertEqual(10, secsvar.get())

    def testConstructorSetGetString(self):
        secsvar = SecsVarDynamic([SecsVarString])

        secsvar.set("testString")

        self.assertEqual("testString", secsvar.get())

    def testEncodeString(self):
        secsvar = SecsVarDynamic([SecsVarString], value="testString")

        self.assertEqual(secsvar.encode(), "A\ntestString")

    def testEncodeU4(self):
        secsvar = SecsVarDynamic([SecsVarU4], value=1337)

        self.assertEqual(secsvar.encode(), "\xB1\x04\x00\x00\x059")

    def testDecodeString(self):
        secsvar = SecsVarDynamic([SecsVarString])

        secsvar.decode("A\ntestString")

        self.assertEqual(secsvar.get(), "testString")

    def testDecodeU4(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        secsvar.decode("\xB1\x04\x00\x00\x059")

        self.assertEqual(secsvar.get(), 1337)

    def testDecodeValueTooLong(self):
        secsvar = SecsVarDynamic([SecsVarString], 5)

        with self.assertRaises(ValueError):
            secsvar.decode("A\ntestString")

    def testDecodeEmptyValue(self):
        secsvar = SecsVarDynamic([SecsVarString], 5)

        with self.assertRaises(ValueError):
            secsvar.decode("")

    def testDecodeWrongType(self):
        secsvar = SecsVarDynamic([SecsVarString], 5)

        with self.assertRaises(ValueError):
            secsvar.decode("\xB1\x04\x00\x00\x059")

    def testDecodeItemHeaderIllegalPosition(self):
        secsvar = SecsVarDynamic([SecsVarU4], value=1337)

        with self.assertRaises(IndexError):
            secsvar.decode("\xB1\x00", 10)

    def testDecodeItemHeaderIllegalData(self):
        # dummy object, just to have format code set
        secsvar = SecsVarDynamic([SecsVarU4], value=1337)

        # two bytes
        with self.assertRaises(ValueError):
            secsvar.decode("somerandomdata")

    def testListOfSameType(self):
        secsvar = SecsVarDynamic([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8])

        secsvar.set([1, 2, 3, 4, 65536])

        self.assertEqual(secsvar.get(), [1, 2, 3, 4, 65536])

    def testListItemsOverMax(self):
        secsvar = SecsVarDynamic([SecsVarU1])

        with self.assertRaises(ValueError):
            secsvar.set([1, 2, 3, 4, 65536])

    def testListItemsOverMaxDiffType(self):
        secsvar = SecsVarDynamic([SecsVarU1])

        with self.assertRaises(ValueError):
            secsvar.set([1, 2, 3, 4, "65536"])

    def testListItemsDiffType(self):
        secsvar = SecsVarDynamic([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8])

        secsvar.set([1, 2, 3, 4, "65536"])

        self.assertEqual(secsvar.get(), [1, 2, 3, 4, 65536])

    def testGetNoneValue(self):
        secsvar = SecsVarDynamic([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8])

        self.assertEqual(secsvar.get(), None)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarDynamic([SecsVarU1], value=1)
        secsvar1 = SecsVarDynamic([SecsVarU1], value=1)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarDynamic([SecsVarU1], value=1)
        secsvar1 = SecsVarU1(value=1)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarDynamic([SecsVarU1], value=1)
        secsvar1 = 1

        self.assertEqual(secsvar, secsvar1)

    def testEqualityList(self):
        secsvar = SecsVarDynamic([SecsVarU1], value=1)
        secsvar1 = [1]

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarList(unittest.TestCase):
    def testConstructor(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        self.assertEqual(secsvar.MDLN.get(), "MDLN")
        self.assertEqual(secsvar["MDLN"].get(), "MDLN")
        self.assertEqual(secsvar[0].get(), "MDLN")
        self.assertEqual(secsvar.SOFTREV.get(), "SOFTREV")
        self.assertEqual(secsvar["SOFTREV"].get(), "SOFTREV")
        self.assertEqual(secsvar[1].get(), "SOFTREV")

    def testConstructorWithoutDefaults(self):
        secsvar = SecsVarList([MDLN, SOFTREV])

        secsvar.MDLN.set("MDLN")
        secsvar.SOFTREV.set("SOFTREV")

        self.assertEqual(secsvar.MDLN.get(), "MDLN")
        self.assertEqual(secsvar["MDLN"].get(), "MDLN")
        self.assertEqual(secsvar[0].get(), "MDLN")
        self.assertEqual(secsvar.SOFTREV.get(), "SOFTREV")
        self.assertEqual(secsvar["SOFTREV"].get(), "SOFTREV")
        self.assertEqual(secsvar[1].get(), "SOFTREV")

    def testConstructorIllegalValue(self):
        with self.assertRaises(ValueError):
            secsvar = SecsVarList([OBJACK, SOFTREV], value=["MDLN", "SOFTREV"])

    def testAttributeSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar.MDLN = SecsVarString(value="NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testAttributeSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar.OBJACK = SecsVarString(value="NLDM")

    def testAttributeSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar.MDLN = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testAttributeSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar.OBJACK = "NLDM"

    def testAttributeGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(AttributeError):
            secsvar.ASDF

    def testAttributeSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(AttributeError):
            secsvar.ASDF = SecsVarString(value="NLDM")

    def testItemSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar["MDLN"] = SecsVarString(value="NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

        self.assertEqual(secsvar.MDLN, SecsVarString(value="NLDM"))
        self.assertEqual(secsvar["MDLN"], SecsVarString(value="NLDM"))
        self.assertEqual(secsvar[0], SecsVarString(value="NLDM"))

    def testItemSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar["OBJACK"] = SecsVarString(value="NLDM")

    def testItemSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar["MDLN"] = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar["OBJACK"] = "NLDM"

    def testItemGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(KeyError):
            secsvar["ASDF"]

    def testItemSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(KeyError):
            secsvar["ASDF"] = SecsVarString(value="NLDM")

    def testIndexSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar[0] = SecsVarString(value="NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testIndexSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar[0] = SecsVarString(value="NLDM")

    def testIndexSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        secsvar[0] = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testIndexSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], value=[0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar[0] = "NLDM"

    def testIndexGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3]

    def testIndexSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3] = SecsVarString(value="NLDM")

    def testIteration(self):
        secsvar = SecsVarList([MDLN, SOFTREV], value=["MDLN1", "SOFTREV1"])

        for key in secsvar:
            self.assertIn(key, ["MDLN", "SOFTREV"])
            self.assertIn(secsvar[key].get(), ["MDLN1", "SOFTREV1"])


class TestSecsVarArray(unittest.TestCase):
    def testConstructor(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN1", "MDLN2"])

        self.assertEqual(secsvar[0], "MDLN1")
        self.assertEqual(secsvar[1], "MDLN2")

    def testConstructorIllegalValue(self):
        with self.assertRaises(ValueError):
            secsvar = SecsVarArray(OBJACK, value=["MDLN1", "MDLN2"])

    def testItemSetterMatchingSecsVar(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN", "SOFTREV"])

        secsvar[0] = SecsVarString(value="NLDM")

        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalSecsVar(self):
        secsvar = SecsVarArray(OBJACK, value=[0, 1])

        with self.assertRaises(TypeError):
            secsvar[0] = SecsVarString(value="NLDM")

    def testItemSetterMatchingValue(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN", "SOFTREV"])

        secsvar[0] = "NLDM"

        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalValue(self):
        secsvar = SecsVarArray(OBJACK, value=[0, 1])

        with self.assertRaises(ValueError):
            secsvar[0] = "NLDM"

    def testItemGetterUnknown(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3]

    def testItemSetterUnknown(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3] = SecsVarString(value="NLDM")

    def testIteration(self):
        secsvar = SecsVarArray(MDLN, value=["MDLN1", "MDLN2"])

        for value in secsvar:
            self.assertIn(value, ["MDLN1", "MDLN2"])


class TestSecsVarBinary(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarBinary(value=13)
        secsvar1 = SecsVarDynamic([SecsVarBinary], value=13)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarBinary(value=13)
        secsvar1 = SecsVarBinary(value=13)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarBinary(value=13)
        secsvar1 = "\x0d"

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarBoolean(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarBoolean(value=True)
        secsvar1 = SecsVarDynamic([SecsVarBoolean], value=True)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarBoolean(value=True)
        secsvar1 = SecsVarBoolean(value=True)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarBoolean(value=True)
        secsvar1 = True

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarString(unittest.TestCase):
    def testConstructorWrongLengthString(self):
        secsvar = SecsVarString(length=5)

        with self.assertRaises(ValueError):
            secsvar.set("testString")

    def testConstructorConvertsNoneToEmptyString(self):
        secsvar = SecsVarString(value=None)

        self.assertEqual(secsvar.get(), "")

    def testSetNoneNotAllowed(self):
        secsvar = SecsVarString(length=5)

        with self.assertRaises(ValueError):
            secsvar.set(None)

    def testEncodeString(self):
        secsvar = SecsVarString(value="testString")

        self.assertEqual(secsvar.encode(), "A\ntestString")

    def testDecodeString(self):
        secsvar = SecsVarString()

        secsvar.decode("A\ntestString")

        self.assertEqual(secsvar.get(), "testString")

    def testEncodeEmptyString(self):
        secsvar = SecsVarString(value="")

        self.assertEqual(secsvar.encode(), "A\0")

    def testDecodeEmptyString(self):
        secsvar = SecsVarString()

        secsvar.decode("A\0")

        self.assertEqual(secsvar.get(), "")

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarString(value="TEST123")
        secsvar1 = SecsVarDynamic([SecsVarString], value="TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarString(value="TEST123")
        secsvar1 = SecsVarString(value="TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarString(value="TEST123")
        secsvar1 = "TEST123"

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarI8(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI8(value=17)
        secsvar1 = SecsVarDynamic([SecsVarI8], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI8(value=17)
        secsvar1 = SecsVarI8(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI8(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarI1(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI1(value=17)
        secsvar1 = SecsVarDynamic([SecsVarI1], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI1(value=17)
        secsvar1 = SecsVarI1(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI1(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarI2(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI2(value=17)
        secsvar1 = SecsVarDynamic([SecsVarI2], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI2(value=17)
        secsvar1 = SecsVarI2(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI2(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarI4(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI4(value=17)
        secsvar1 = SecsVarDynamic([SecsVarI4], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI4(value=17)
        secsvar1 = SecsVarI4(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI4(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarF8(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarF8(value=12.3)
        secsvar1 = SecsVarDynamic([SecsVarF8], value=12.3)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarF8(value=12.3)
        secsvar1 = SecsVarF8(value=12.3)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarF8(value=12.3)
        secsvar1 = 12.3

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarF4(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarF4(value=17)
        secsvar1 = SecsVarDynamic([SecsVarF4], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarF4(value=17)
        secsvar1 = SecsVarF4(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarF4(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarU8(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU8(value=17)
        secsvar1 = SecsVarDynamic([SecsVarU8], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU8(value=17)
        secsvar1 = SecsVarU8(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU8(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarU1(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU1(value=17)
        secsvar1 = SecsVarDynamic([SecsVarU1], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU1(value=17)
        secsvar1 = SecsVarU1(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU1(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarU2(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU2(value=17)
        secsvar1 = SecsVarDynamic([SecsVarU2], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU2(value=17)
        secsvar1 = SecsVarU2(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU2(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class TestSecsVarU4(unittest.TestCase):
    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU4(value=17)
        secsvar1 = SecsVarDynamic([SecsVarU4], value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU4(value=17)
        secsvar1 = SecsVarU4(value=17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU4(value=17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)


class GoodBadLists(object):
    _type = None
    goodValues = []
    badValues = []

    def goodAssignmentCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(length=value["LENGTH"])
        else:
            secsvar = self._type()

        print self._type.__name__, "testing assignment of good", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"])

        secsvar.set(value["VALUE"])
        nose.tools.eq_(secsvar.get(), value["RESULT"])

    def testGoodAssignment(self):
        for valueList in self.goodValues:
            for value in valueList:
                yield self.goodAssignmentCheck, value

    @nose.tools.raises(TypeError, ValueError)
    def badAssignmentCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(length=value["LENGTH"])
        else:
            secsvar = self._type()

        print self._type.__name__, "testing assignment of bad", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"])
        secsvar.set(value["VALUE"])
        print self._type.__name__, "unexpected bad assignment", secsvar.get()

    def testBadAssignment(self):
        for valueList in self.badValues:
            for value in valueList:
                yield self.badAssignmentCheck, value

    def goodSupportedCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(length=value["LENGTH"])
        else:
            secsvar = self._type()

        print self._type.__name__, "testing isSupported for good", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"])
        nose.tools.eq_(secsvar.supports_value(value["VALUE"]), True)

    def testGoodSupported(self):
        for valueList in self.goodValues:
            for value in valueList:
                yield self.goodSupportedCheck, value

    def badSupportedCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(length=value["LENGTH"])
        else:
            secsvar = self._type()

        print self._type.__name__, "testing isSupported for bad", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"])
        nose.tools.eq_(secsvar.supports_value(value["VALUE"]), False)

    def testBadSupported(self):
        for valueList in self.badValues:
            for value in valueList:
                yield self.badSupportedCheck, value

class TestSecsVarBinaryValues(GoodBadLists):
    _type = SecsVarBinary

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = {}
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 255, "RESULT": 255},
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 265},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 255L, "RESULT": 255},
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 265L},
    ]

    #complex
    _goodComplexValues = {}
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "TEST1", "RESULT": "TEST1"},
        {"VALUE": "1234QWERasdf.-+ \n\r\t\1 \127 \xB1", "RESULT": "1234QWERasdf.-+ \n\r\t\1 \127 \xB1"},
        {"VALUE": "TEST1", "RESULT": "TEST1", "LENGTH": 5},
    ]
    _badStringValues = [
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"TEST1", "RESULT": "TEST1"},
        {"VALUE": u"1234QWERasdf.-+ \n\r\t\1 \127", "RESULT": "1234QWERasdf.-+ \n\r\t\1 \127"},
        {"VALUE": u"TEST1", "RESULT": "TEST1", "LENGTH": 5},
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1", "RESULT": "TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": "\x00\x01\x00\x00"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [1, -1, 256, 5]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5}
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (1, -1, 256, 5)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarBooleanValues(GoodBadLists):
    _type = SecsVarBoolean

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": True},
        {"VALUE": False, "RESULT": False},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = {}
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT": False},
        {"VALUE": 1, "RESULT": True},
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 2},
        {"VALUE": 265},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT": False},
        {"VALUE": 1L, "RESULT": True},
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 2L},
        {"VALUE": 265L},
    ]

    #complex
    _goodComplexValues = {}
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "YES", "RESULT": True},
        {"VALUE": "tRuE", "RESULT": True},
        {"VALUE": "No", "RESULT": False},
        {"VALUE": "False", "RESULT": False},
    ]
    _badStringValues = [
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"YES", "RESULT": True},
        {"VALUE": u"tRuE", "RESULT": True},
        {"VALUE": u"No", "RESULT": False},
        {"VALUE": u"False", "RESULT": False},
    ]
    _badUnicodeValues = [
        {"VALUE": u"TEST1"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1", "RESULT": "TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [True, False, True], "RESULT": [True, False, True]},
        {"VALUE": [True, False, True], "RESULT": [True, False, True], "LENGTH": 3},
        {"VALUE": [1, 0, 1], "RESULT": [True, False, True]},
        {"VALUE": ["True", "False", "True"], "RESULT": [True, False, True]},
        {"VALUE": ["YES", "no", "yes"], "RESULT": [True, False, True]},
    ]
    _badListValues = [
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [1, -1, 256, 5]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [True, False, True], "LENGTH": 2},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5}
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (True, False, True), "RESULT": [True, False, True]},
    ]
    _badTupleValues = [
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 6},
        {"VALUE": (1, -1, 256, 5)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
        {"VALUE": (True, False, True), "LENGTH": 2},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x00\x01"), "RESULT": [False, True, False, True]},
        {"VALUE": bytearray("\x00\x01\x00\x01"), "RESULT": [False, True, False, True], "LENGTH": 4},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x00\x01"), "LENGTH": 3},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF")},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 6},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarStringValues(GoodBadLists):
    _type = SecsVarString

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": "True"},
        {"VALUE": False, "RESULT": "False"},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
        {"VALUE": 1.0, "RESULT": "1.0"},
        {"VALUE": 100000000.123, "RESULT": "100000000.123"},
        {"VALUE": -1.0, "RESULT": "-1.0"},
    ]
    _badFloatValues = [
        {"VALUE": 100000000.123, "LENGTH": 1},
    ]

    #int
    _goodIntValues = [
        {"VALUE": -1, "RESULT": "-1"},
        {"VALUE": 0, "RESULT": "0"},
        {"VALUE": 1, "RESULT": "1"},
        {"VALUE": 2, "RESULT": "2"},
        {"VALUE": 265, "RESULT": "265"},
    ]
    _badIntValues = [
        {"VALUE": 265, "LENGTH": 1},
    ]

    #long
    _goodLongValues = [
        {"VALUE": -1L, "RESULT": "-1"},
        {"VALUE": 0L, "RESULT": "0"},
        {"VALUE": 1L, "RESULT": "1"},
        {"VALUE": 2L, "RESULT": "2"},
        {"VALUE": 265L, "RESULT": "265"},
    ]
    _badLongValues = [
        {"VALUE": 265L, "LENGTH": 1},
    ]

    #complex
    _goodComplexValues = [
        {"VALUE": 1J, "RESULT": "1j"},
    ]
    _badComplexValues = [
    ]

    #str
    _goodStringValues = [
        {"VALUE": "YES", "RESULT": "YES"},
        {"VALUE": "tRuE", "RESULT": "tRuE"},
        {"VALUE": "No", "RESULT": "No"},
        {"VALUE": "False", "RESULT": "False"},
    ]
    _badStringValues = [
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"YES", "RESULT": "YES"},
        {"VALUE": u"tRuE", "RESULT": "tRuE"},
        {"VALUE": u"No", "RESULT": "No"},
        {"VALUE": u"False", "RESULT": "False"},
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": "\x00\x01\x00\x00"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [1, -1, 256, 5]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (1, -1, 256, 5)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": "\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": "\x00\x01\x05\x20\x10\xFF", "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarI8Values(GoodBadLists):
    _type = SecsVarI8

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": -9223372036854775808, "RESULT":-9223372036854775808},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 9223372036854775807, "RESULT": 9223372036854775807}
    ]
    _badIntValues = [
        {"VALUE": -9223372036854775809},
        {"VALUE": 9223372036854775808},
    ]

    #long
    _goodLongValues = [
        {"VALUE": -9223372036854775808L, "RESULT":-9223372036854775808},
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 9223372036854775807L, "RESULT": 9223372036854775807}
    ]
    _badLongValues = [
        {"VALUE": -9223372036854775809L},
        {"VALUE": 9223372036854775808L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "-9223372036854775808", "RESULT":-9223372036854775808},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
        {"VALUE": "9223372036854775807", "RESULT": 9223372036854775807}
    ]
    _badStringValues = [
        {"VALUE": "-9223372036854775809"},
        {"VALUE": "9223372036854775808"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-9223372036854775808", "RESULT":-9223372036854775808},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"9223372036854775807", "RESULT": 9223372036854775807}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-9223372036854775809"},
        {"VALUE": u"9223372036854775808"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [-9223372036854775808, 1, 2, 9223372036854775807], "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807]},
        {"VALUE": ["-9223372036854775808", 1, "2", "9223372036854775807"], "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807]},
        {"VALUE": ["-9223372036854775808", 1, "2", "9223372036854775807"], "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-9223372036854775809, 1, 2, 9223372036854775807]},
        {"VALUE": [-9223372036854775808, 1, 2, 9223372036854775808]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (-9223372036854775808, 1, 2, 9223372036854775807), "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807]},
        {"VALUE": ("-9223372036854775808", 1, "2", "9223372036854775807"), "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807]},
        {"VALUE": ("-9223372036854775808", 1, "2", "9223372036854775807"), "RESULT": [-9223372036854775808, 1, 2, 9223372036854775807], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-9223372036854775809, 1, 2, 9223372036854775807)},
        {"VALUE": (-9223372036854775808, 1, 2, 9223372036854775808)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarI1Values(GoodBadLists):
    _type = SecsVarI1

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": -128, "RESULT":-128},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 127, "RESULT": 127}
    ]
    _badIntValues = [
        {"VALUE": -129},
        {"VALUE": 128},
    ]

    #long
    _goodLongValues = [
        {"VALUE": -128L, "RESULT":-128},
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 127L, "RESULT": 127}
    ]
    _badLongValues = [
        {"VALUE": -129L},
        {"VALUE": 128L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "-128", "RESULT":-128},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "127", "RESULT": 127}
    ]
    _badStringValues = [
        {"VALUE": "-129"},
        {"VALUE": "128"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-128", "RESULT":-128},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"127", "RESULT": 127}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-129"},
        {"VALUE": u"128"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [-128, 1, 2, 127], "RESULT": [-128, 1, 2, 127]},
        {"VALUE": ["-128", 1, "2", "127"], "RESULT": [-128, 1, 2, 127]},
        {"VALUE": ["-128", 1, "2", "127"], "RESULT": [-128, 1, 2, 127], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-129, 1, 2, 127]},
        {"VALUE": [-128, 1, 2, 128]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (-128, 1, 2, 127), "RESULT": [-128, 1, 2, 127]},
        {"VALUE": ("-128", 1, "2", "127"), "RESULT": [-128, 1, 2, 127]},
        {"VALUE": ("-128", 1, "2", "127"), "RESULT": [-128, 1, 2, 127], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-129, 1, 2, 127)},
        {"VALUE": (-128, 1, 2, 128)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\x7F"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\x7F"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"),},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\x7F"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarI2Values(GoodBadLists):
    _type = SecsVarI2

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": -32768, "RESULT":-32768},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 32767, "RESULT": 32767}
    ]
    _badIntValues = [
        {"VALUE": -32769},
        {"VALUE": 32768},
    ]

    #long
    _goodLongValues = [
        {"VALUE": -32768L, "RESULT":-32768},
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 32767L, "RESULT": 32767}
    ]
    _badLongValues = [
        {"VALUE": -32769L},
        {"VALUE": 32768L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "-32768", "RESULT":-32768},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "32767", "RESULT": 32767}
    ]
    _badStringValues = [
        {"VALUE": "-32769"},
        {"VALUE": "32768"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-32768", "RESULT":-32768},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"32767", "RESULT": 32767}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-32769"},
        {"VALUE": u"32768"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [-32768, 1, 2, 32767], "RESULT": [-32768, 1, 2, 32767]},
        {"VALUE": ["-32768", 1, "2", "32767"], "RESULT": [-32768, 1, 2, 32767]},
        {"VALUE": ["-32768", 1, "2", "32767"], "RESULT": [-32768, 1, 2, 32767], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-32769, 1, 2, 32767]},
        {"VALUE": [-32768, 1, 2, 32768]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (-32768, 1, 2, 32767), "RESULT": [-32768, 1, 2, 32767]},
        {"VALUE": ("-32768", 1, "2", "32767"), "RESULT": [-32768, 1, 2, 32767]},
        {"VALUE": ("-32768", 1, "2", "32767"), "RESULT": [-32768, 1, 2, 32767], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-32769, 1, 2, 32767)},
        {"VALUE": (-32768, 1, 2, 32768)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarI4Values(GoodBadLists):
    _type = SecsVarI4

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": -2147483648, "RESULT":-2147483648},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 2147483647, "RESULT": 2147483647}
    ]
    _badIntValues = [
        {"VALUE": -2147483649},
        {"VALUE": 2147483648},
    ]

    #long
    _goodLongValues = [
        {"VALUE": -2147483648L, "RESULT":-2147483648},
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 2147483647L, "RESULT": 2147483647}
    ]
    _badLongValues = [
        {"VALUE": -2147483649L},
        {"VALUE": 2147483648L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "-2147483648", "RESULT":-2147483648},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
        {"VALUE": "2147483647", "RESULT": 2147483647}
    ]
    _badStringValues = [
        {"VALUE": "-2147483649"},
        {"VALUE": "2147483648"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-2147483648", "RESULT":-2147483648},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"2147483647", "RESULT": 2147483647}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-2147483649"},
        {"VALUE": u"2147483648"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [-2147483648, 1, 2, 2147483647], "RESULT": [-2147483648, 1, 2, 2147483647]},
        {"VALUE": ["-2147483648", 1, "2", "2147483647"], "RESULT": [-2147483648, 1, 2, 2147483647]},
        {"VALUE": ["-2147483648", 1, "2", "2147483647"], "RESULT": [-2147483648, 1, 2, 2147483647], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-2147483649, 1, 2, 2147483647]},
        {"VALUE": [-2147483648, 1, 2, 2147483648]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (-2147483648, 1, 2, 2147483647), "RESULT": [-2147483648, 1, 2, 2147483647]},
        {"VALUE": ("-2147483648", 1, "2", "2147483647"), "RESULT": [-2147483648, 1, 2, 2147483647]},
        {"VALUE": ("-2147483648", 1, "2", "2147483647"), "RESULT": [-2147483648, 1, 2, 2147483647], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-2147483649, 1, 2, 2147483647)},
        {"VALUE": (-2147483648, 1, 2, 2147483648)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarF8Values(GoodBadLists):
    _type = SecsVarF8

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
        {"VALUE": -1.79769e+308 + 1, "RESULT":-1.79769e+308 + 1},
        {"VALUE": 1.0, "RESULT": 1.0},
        {"VALUE": 100000000.123, "RESULT": 100000000.123},
        {"VALUE": -1.0, "RESULT": -1.0},
        {"VALUE": 1.79769e+308 - 1, "RESULT": 1.79769e+308 - 1}
    ]
    _badFloatValues = [
    ]

    #int
    _goodIntValues = [
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
    ]
    _badIntValues = [
    ]

    #long
    _goodLongValues = [
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
    ]
    _badLongValues = [
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
    ]
    _badStringValues = [
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-1.79769e+308", "RESULT":-1.79769e+308},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"1.79769e+308", "RESULT": 1.79769e+308}
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarF4Values(GoodBadLists):
    _type = SecsVarF4

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
        {"VALUE": -3.40282e+38 + 1, "RESULT":-3.40282e+38 + 1},
        {"VALUE": 1.0, "RESULT": 1.0},
        {"VALUE": 100000000.123, "RESULT": 100000000.123},
        {"VALUE": -1.0, "RESULT": -1.0},
        {"VALUE": 3.40282e+38 - 1, "RESULT": 3.40282e+38 - 1}
    ]
    _badFloatValues = [
    ]

    #int
    _goodIntValues = [
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
    ]
    _badIntValues = [
    ]

    #long
    _goodLongValues = [
        {"VALUE": -1L, "RESULT": -1},
        {"VALUE": 0L, "RESULT": 0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
    ]
    _badLongValues = [
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
    ]
    _badStringValues = [
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"-3.40282e+38", "RESULT":-3.40282e+38},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"3.40282e+38", "RESULT": 3.40282e+38}
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [-10, -100], "RESULT": [-10, -100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (-10, -100), "RESULT": [-10, -100]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarU8Values(GoodBadLists):
    _type = SecsVarU8

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 18446744073709551615, "RESULT": 18446744073709551615}
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 18446744073709551616},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT":0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 18446744073709551615L, "RESULT": 18446744073709551615}
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 18446744073709551616L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "0", "RESULT":0},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
        {"VALUE": "18446744073709551615", "RESULT": 18446744073709551615}
    ]
    _badStringValues = [
        {"VALUE": "-1"},
        {"VALUE": "18446744073709551616"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"0", "RESULT":0},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"18446744073709551615", "RESULT": 18446744073709551615}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-1"},
        {"VALUE": u"18446744073709551616"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [0, 1, 2, 18446744073709551615], "RESULT": [0, 1, 2, 18446744073709551615]},
        {"VALUE": ["0", 1, "2", "18446744073709551615"], "RESULT": [0, 1, 2, 18446744073709551615]},
        {"VALUE": ["0", 1, "2", "18446744073709551615"], "RESULT": [0, 1, 2, 18446744073709551615], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-1, 1, 2, 18446744073709551615]},
        {"VALUE": [0, 1, 2, 18446744073709551616]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0, 1, 2, 18446744073709551615), "RESULT": [0, 1, 2, 18446744073709551615]},
        {"VALUE": ("0", 1, "2", "18446744073709551615"), "RESULT": [0, 1, 2, 18446744073709551615]},
        {"VALUE": ("0", 1, "2", "18446744073709551615"), "RESULT": [0, 1, 2, 18446744073709551615], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-1, 1, 2, 18446744073709551615)},
        {"VALUE": (0, 1, 2, 18446744073709551616)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarU1Values(GoodBadLists):
    _type = SecsVarU1

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 255, "RESULT": 255}
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 256},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT":0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 255L, "RESULT": 255}
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 256L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "0", "RESULT":0},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "255", "RESULT": 255}
    ]
    _badStringValues = [
        {"VALUE": "-1"},
        {"VALUE": "256"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"0", "RESULT":0},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"255", "RESULT": 255}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-1"},
        {"VALUE": u"256"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [0, 1, 2, 255], "RESULT": [0, 1, 2, 255]},
        {"VALUE": ["0", 1, "2", "255"], "RESULT": [0, 1, 2, 255]},
        {"VALUE": ["0", 1, "2", "255"], "RESULT": [0, 1, 2, 255], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-1, 1, 2, 255]},
        {"VALUE": [0, 1, 2, 256]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0, 1, 2, 255), "RESULT": [0, 1, 2, 255]},
        {"VALUE": ("0", 1, "2", "255"), "RESULT": [0, 1, 2, 255]},
        {"VALUE": ("0", 1, "2", "255"), "RESULT": [0, 1, 2, 255], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-1, 1, 2, 255)},
        {"VALUE": (0, 1, 2, 256)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarU2Values(GoodBadLists):
    _type = SecsVarU2

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 65535, "RESULT": 65535}
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 65536},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT":0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 65535L, "RESULT": 65535}
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 65536L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "0", "RESULT":0},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
        {"VALUE": "65535", "RESULT": 65535}
    ]
    _badStringValues = [
        {"VALUE": "-1"},
        {"VALUE": "65536"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"0", "RESULT":0},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"65535", "RESULT": 65535}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-1"},
        {"VALUE": u"65536"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [0, 1, 2, 65535], "RESULT": [0, 1, 2, 65535]},
        {"VALUE": ["0", 1, "2", "65535"], "RESULT": [0, 1, 2, 65535]},
        {"VALUE": ["0", 1, "2", "65535"], "RESULT": [0, 1, 2, 65535], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-1, 1, 2, 65535]},
        {"VALUE": [0, 1, 2, 65536]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0, 1, 2, 65535), "RESULT": [0, 1, 2, 65535]},
        {"VALUE": ("0", 1, "2", "65535"), "RESULT": [0, 1, 2, 65535]},
        {"VALUE": ("0", 1, "2", "65535"), "RESULT": [0, 1, 2, 65535], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-1, 1, 2, 65535)},
        {"VALUE": (0, 1, 2, 65536)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

class TestSecsVarU4Values(GoodBadLists):
    _type = SecsVarU4

    #bool
    _goodBoolValues = [
        {"VALUE": True, "RESULT": 1},
        {"VALUE": False, "RESULT": 0},
    ]
    _badBoolValues = []

    #float
    _goodFloatValues = [
    ]
    _badFloatValues = [
        {"VALUE": 1.0},
        {"VALUE": 100000000.123},
        {"VALUE": -1.0},
    ]

    #int
    _goodIntValues = [
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 4294967295, "RESULT": 4294967295}
    ]
    _badIntValues = [
        {"VALUE": -1},
        {"VALUE": 4294967296},
    ]

    #long
    _goodLongValues = [
        {"VALUE": 0L, "RESULT":0},
        {"VALUE": 1L, "RESULT": 1},
        {"VALUE": 2L, "RESULT": 2},
        {"VALUE": 265L, "RESULT": 265},
        {"VALUE": 4294967295L, "RESULT": 4294967295}
    ]
    _badLongValues = [
        {"VALUE": -1L},
        {"VALUE": 4294967296L},
    ]

    #complex
    _goodComplexValues = [
    ]
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "0", "RESULT":0},
        {"VALUE": "1", "RESULT": 1},
        {"VALUE": "65535", "RESULT": 65535},
        {"VALUE": "4294967295", "RESULT": 4294967295}
    ]
    _badStringValues = [
        {"VALUE": "-1"},
        {"VALUE": "4294967296"},
        {"VALUE": "TEST1"},
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"0", "RESULT":0},
        {"VALUE": u"1", "RESULT": 1},
        {"VALUE": u"65535", "RESULT": 65535},
        {"VALUE": u"4294967295", "RESULT": 4294967295}
    ]
    _badUnicodeValues = [
        {"VALUE": u"-1"},
        {"VALUE": u"4294967296"},
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1"},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [0, 1, 2, 4294967295], "RESULT": [0, 1, 2, 4294967295]},
        {"VALUE": ["0", 1, "2", "4294967295"], "RESULT": [0, 1, 2, 4294967295]},
        {"VALUE": ["0", 1, "2", "4294967295"], "RESULT": [0, 1, 2, 4294967295], "LENGTH": 4},
        {"VALUE": [False, True, False, False], "RESULT": [0, 1, 0, 0]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [-1, 1, 2, 4294967295]},
        {"VALUE": [0, 1, 2, 4294967296]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0, 1, 2, 4294967295), "RESULT": [0, 1, 2, 4294967295]},
        {"VALUE": ("0", 1, "2", "4294967295"), "RESULT": [0, 1, 2, 4294967295]},
        {"VALUE": ("0", 1, "2", "4294967295"), "RESULT": [0, 1, 2, 4294967295], "LENGTH": 4},
        {"VALUE": (False, True, False, False), "RESULT": [0, 1, 0, 0]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFFFFFFFF], "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (-1, 1, 2, 4294967295)},
        {"VALUE": (0, 1, 2, 4294967296)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray("\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

