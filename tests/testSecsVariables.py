# -*- coding: utf-8 -*-
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

import sys

import unittest
import nose

from secsgem.secs.variables import *
from secsgem.secs.dataitems import MDLN, OBJACK, SOFTREV, SVID

def printable_value(value):
    if sys.version_info < (3, ):
        if isinstance(value, str):
            return value.encode('string_escape')
        elif isinstance(value, unicode):
            return value
        else:
            return str(value).encode('string_escape')
    else:
        if isinstance(value, bytes):
            return value.decode('unicode_escape')
        elif isinstance(value, str):
            return value
        else:
            return value

class TestSecsVar(unittest.TestCase):
    def testEncodeItemHeader(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # two bytes
        self.assertEqual(secsvar.encode_item_header(0), b"\xB1\x00")
        self.assertEqual(secsvar.encode_item_header(0xFF), b"\xB1\xFF")

        # three bytes
        self.assertEqual(secsvar.encode_item_header(0x100), b"\xB2\x01\x00")
        self.assertEqual(secsvar.encode_item_header(0xFFFF), b"\xB2\xFF\xFF")

        # four bytes
        self.assertEqual(secsvar.encode_item_header(0x10000), b"\xB3\x01\x00\x00")
        self.assertEqual(secsvar.encode_item_header(0xFFFFFF), b"\xB3\xFF\xFF\xFF")

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
        self.assertEqual(secsvar.decode_item_header(b"\xB1\x00")[2], 0)
        self.assertEqual(secsvar.decode_item_header(b"\xB1\xFF")[2], 0xFF)

        # three bytes
        self.assertEqual(secsvar.decode_item_header(b"\xB2\x01\x00")[2], 0x100)
        self.assertEqual(secsvar.decode_item_header(b"\xB2\xFF\xFF")[2], 0xFFFF)

        # four bytes
        self.assertEqual(secsvar.decode_item_header(b"\xB3\x01\x00\x00")[2], 0x10000)
        self.assertEqual(secsvar.decode_item_header(b"\xB3\xFF\xFF\xFF")[2], 0xFFFFFF)

    def testDecodeItemHeaderEmpty(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        with self.assertRaises(ValueError):
            secsvar.decode_item_header(b"")

    def testDecodeItemHeaderIllegalPosition(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        with self.assertRaises(IndexError):
            secsvar.decode_item_header(b"\xB1\x00", 10)

    def testDecodeItemHeaderIllegalData(self):
        # dummy object, just to have format code set
        secsvar = SecsVarU4(1337)

        # two bytes
        with self.assertRaises(ValueError):
            secsvar.decode_item_header(b"somerandomdata")

    def testGenerateWithNonSecsVarClass(self):
        with self.assertRaises(TypeError):
            SecsVar.generate(int)

    def testGenerateWithNonClass(self):
        dummy = 10

        with self.assertRaises(TypeError):
            SecsVar.generate(dummy)

    def testSetNotImplemented(self):
        secsvar = SecsVar()

        with self.assertRaises(NotImplementedError):
            secsvar.set(b"test")

    def testGetFormatWithNone(self):
        self.assertEqual(SecsVar.get_format(None), None)

    def testGetFormatWithNonSecsVarClass(self):
        with self.assertRaises(TypeError):
            SecsVar.get_format(int)

    def testGetFormatWithNonClass(self):
        with self.assertRaises(TypeError):
            SecsVar.get_format(10)


class TestSecsVarDynamic(unittest.TestCase):
    def testConstructorU4(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        secsvar.set(10)

        self.assertEqual(10, secsvar.get())

    def testConstructorWrongType(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        with self.assertRaises(ValueError):
            secsvar.set(b"testString")
        with self.assertRaises(ValueError):
            secsvar.set(SecsVarString(b"testString"))
        with self.assertRaises(ValueError):
            SecsVarDynamic([SecsVarU4], b"testString")

    def testConstructorWrongLengthString(self):
        secsvar = SecsVarDynamic([SecsVarString], count=5)

        with self.assertRaises(ValueError):
            secsvar.set(b"testString")

    def testConstructorLen(self):
        secsvar = SecsVarDynamic([SecsVarString])

        secsvar.set(b"asdfg")

        self.assertEqual(5, len(secsvar))

    def testConstructorSetGetU4(self):
        secsvar = SecsVarDynamic([SecsVarU4])

        secsvar.set(10)

        self.assertEqual(10, secsvar.get())

    def testConstructorSetGetString(self):
        secsvar = SecsVarDynamic([SecsVarString])

        secsvar.set("testString")

        self.assertEqual("testString", secsvar.get())

    def testHash(self):
        secsvar = SecsVarDynamic([SecsVarString], value="test")
        hash(secsvar)

    def testEncodeString(self):
        secsvar = SecsVarDynamic([SecsVarString], "testString")

        self.assertEqual(secsvar.encode(), b"A\ntestString")

    def testEncodeU4(self):
        secsvar = SecsVarDynamic([SecsVarU4], 1337)

        self.assertEqual(secsvar.encode(), b"\xB1\x04\x00\x00\x059")

    def testDecodeValueTooLong(self):
        secsvar = SecsVarDynamic([SecsVarString], count=5)

        with self.assertRaises(ValueError):
            secsvar.decode(b"A\ntestString")

    def testDecodeEmptyValue(self):
        secsvar = SecsVarDynamic([SecsVarString], count=5)

        with self.assertRaises(ValueError):
            secsvar.decode(b"")

    def testDecodeWrongType(self):
        secsvar = SecsVarDynamic([SecsVarString], count=5)

        with self.assertRaises(ValueError):
            secsvar.decode(b"\xB1\x04\x00\x00\x059")

    def testDecodeItemHeaderIllegalPosition(self):
        secsvar = SecsVarDynamic([SecsVarU4], 1337)

        with self.assertRaises(IndexError):
            secsvar.decode(b"\xB1\x00", 10)

    def testDecodeItemHeaderIllegalData(self):
        # dummy object, just to have format code set
        secsvar = SecsVarDynamic([SecsVarU4], 1337)

        # two bytes
        with self.assertRaises(ValueError):
            secsvar.decode(b"somerandomdata")

    def testDecodeWithAllTypesAllowed(self):
        secsvar = SecsVarDynamic([])

        secsvar.decode(b"\xB1\x04\x00\x00\x059")

        self.assertEqual(secsvar[0], 1337)

    def testDecodeArray(self):
        secsvar = SecsVarDynamic([SecsVarArray])
        encodevar = SecsVarArray(SecsVarU4)
        encodevar.append(1337)
        encodevar.append(1338)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar[0], 1337)
        self.assertEqual(secsvar[1], 1338)

    def testDecodeBinary(self):
        value = b"testBinary"

        secsvar = SecsVarDynamic([SecsVarBinary])
        encodevar = SecsVarBinary(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeBoolean(self):
        value = True

        secsvar = SecsVarDynamic([SecsVarBoolean])
        encodevar = SecsVarBoolean(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeString(self):
        value = "testString"

        secsvar = SecsVarDynamic([SecsVarString])
        encodevar = SecsVarString(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeI8(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarI8])
        encodevar = SecsVarI8(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeI1(self):
        value = 13

        secsvar = SecsVarDynamic([SecsVarI1])
        encodevar = SecsVarI1(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeI2(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarI2])
        encodevar = SecsVarI2(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeI4(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarI4])
        encodevar = SecsVarI4(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeF8(self):
        value = 1337.1

        secsvar = SecsVarDynamic([SecsVarF8])
        encodevar = SecsVarF8(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeF4(self):
        value = 1337.0

        secsvar = SecsVarDynamic([SecsVarF4])
        encodevar = SecsVarF4(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeU8(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarU8])
        encodevar = SecsVarU8(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeU1(self):
        value = 13

        secsvar = SecsVarDynamic([SecsVarU1])
        encodevar = SecsVarU1(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeU2(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarU2])
        encodevar = SecsVarU2(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

    def testDecodeU4(self):
        value = 1337

        secsvar = SecsVarDynamic([SecsVarU4])
        encodevar = SecsVarU4(value)

        secsvar.decode(encodevar.encode())

        self.assertEqual(secsvar.get(), value)

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
        secsvar = SecsVarDynamic([SecsVarU1], 1)
        secsvar1 = SecsVarDynamic([SecsVarU1], 1)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarDynamic([SecsVarU1], 1)
        secsvar1 = SecsVarU1(1)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarDynamic([SecsVarU1], 1)
        secsvar1 = 1

        self.assertEqual(secsvar, secsvar1)

    def testEqualityList(self):
        secsvar = SecsVarDynamic([SecsVarU1], 1)
        secsvar1 = [1]

        self.assertEqual(secsvar, secsvar1)

    def testGetItem(self):
        secsvar = SecsVarDynamic([SecsVarU1], 1)

        self.assertEqual(secsvar[0], 1)

    def testSetItem(self):
        secsvar = SecsVarDynamic([SecsVarU1], 1)

        secsvar[0] = 2

        self.assertEqual(secsvar[0], 2)

    def testAllTypesAllowed(self):
        secsvar = SecsVarDynamic([], 1)

        self.assertEqual(secsvar[0], 1)

    def testSetDerivedItem(self):
        secsvar = SecsVarDynamic([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString])

        secsvar.set(SVID(10))

        self.assertEqual(secsvar, 10)

    def testSetDerivedUnsupportedItem(self):
        secsvar = SecsVarDynamic([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])

        with self.assertRaises(ValueError):
            secsvar.set(SVID("asdfg"))


class TestSecsVarList(unittest.TestCase):
    def testConstructor(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

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
            secsvar = SecsVarList([OBJACK, SOFTREV], ["MDLN", "SOFTREV"])

    def testHash(self):
        secsvar = SecsVarList([MDLN, SOFTREV])
        hash(secsvar)

    def testAttributeSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar.MDLN = SecsVarString("NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testAttributeSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar.OBJACK = SecsVarString("NLDM")

    def testAttributeSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar.MDLN = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testAttributeSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar.OBJACK = "NLDM"

    def testAttributeGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(AttributeError):
            secsvar.ASDF

    def testAttributeSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(AttributeError):
            secsvar.ASDF = SecsVarString("NLDM")

    def testItemSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar["MDLN"] = SecsVarString("NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

        self.assertEqual(secsvar.MDLN, SecsVarString("NLDM"))
        self.assertEqual(secsvar["MDLN"], SecsVarString("NLDM"))
        self.assertEqual(secsvar[0], SecsVarString("NLDM"))

    def testItemSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar["OBJACK"] = SecsVarString("NLDM")

    def testItemSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar["MDLN"] = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar["OBJACK"] = "NLDM"

    def testItemGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(KeyError):
            secsvar["ASDF"]

    def testItemSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(KeyError):
            secsvar["ASDF"] = SecsVarString("NLDM")

    def testIndexSetterMatchingSecsVar(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar[0] = SecsVarString("NLDM")

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testIndexSetterIllegalSecsVar(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(TypeError):
            secsvar[0] = SecsVarString("NLDM")

    def testIndexSetterMatchingValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        secsvar[0] = "NLDM"

        self.assertEqual(secsvar.MDLN.get(), "NLDM")
        self.assertEqual(secsvar["MDLN"].get(), "NLDM")
        self.assertEqual(secsvar[0].get(), "NLDM")

    def testIndexSetterIllegalValue(self):
        secsvar = SecsVarList([OBJACK, SOFTREV], [0, "SOFTREV"])

        with self.assertRaises(ValueError):
            secsvar[0] = "NLDM"

    def testIndexGetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3]

    def testIndexSetterUnknown(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3] = SecsVarString("NLDM")

    def testIteration(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])

        for key in secsvar:
            self.assertIn(key, ["MDLN", "SOFTREV"])
            self.assertIn(secsvar[key].get(), ["MDLN1", "SOFTREV1"])

    def testIteratorsIterator(self):
        # does not need to be tested, but raises coverage
        iter(iter(SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])))

    def testRepr(self):
        print(SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"]))

    def testEmptyRepr(self):
        print(SecsVarList([]))

    def testLen(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])

        self.assertEqual(len(secsvar), 2)

    def testNoneDataFormat(self):
        secsvar = SecsVarList(None)

    def testUnknownDataFormat(self):
        with self.assertRaises(TypeError):
            secsvar = SecsVarList([None])

    def testGetNameFromFormatWithIllegalType(self):
        with self.assertRaises(TypeError):
            SecsVarList.get_name_from_format(None)

    def testSettingListToSmall(self):
        secsvar = SecsVarList([MDLN, SOFTREV])

        secsvar.set(["MDLN"])

    def testSettingListMatchingLength(self):
        secsvar = SecsVarList([MDLN, SOFTREV])

        secsvar.set(["MDLN", "SOFTREV"])

    def testSettingListToBig(self):
        secsvar = SecsVarList([MDLN, SOFTREV])

        with self.assertRaises(ValueError):
            secsvar.set(["MDLN", "SOFTREV", "MDLN2"])

    def testSettingInvalidValue(self):
        secsvar = SecsVarList([MDLN, SOFTREV])

        with self.assertRaises(ValueError):
            secsvar.set("MDLN")

    def testGettingList(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])

        var = secsvar.get()

        self.assertEqual(var["MDLN"], "MDLN1")
        self.assertEqual(var["SOFTREV"], "SOFTREV1")

    def testEncode(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])

        self.assertEqual(secsvar.encode(), b"\x01\x02A\x05MDLN1A\x08SOFTREV1")

    def testDecode(self):
        secsvar = SecsVarList([MDLN, SOFTREV], ["MDLN1", "SOFTREV1"])

        secsvar.MDLN = ""
        secsvar.SOFTREV = ""

        self.assertEqual(secsvar.MDLN, "")
        self.assertEqual(secsvar.SOFTREV, "")

        secsvar.decode(b"\x01\x02A\x05MDLN1A\x08SOFTREV1")

        self.assertEqual(secsvar.MDLN, "MDLN1")
        self.assertEqual(secsvar.SOFTREV, "SOFTREV1")
        

class TestSecsVarArray(unittest.TestCase):
    def testConstructor(self):
        secsvar = SecsVarArray(MDLN, ["MDLN1", "MDLN2"])

        self.assertEqual(secsvar[0], "MDLN1")
        self.assertEqual(secsvar[1], "MDLN2")

    def testConstructorIllegalValue(self):
        with self.assertRaises(ValueError):
            secsvar = SecsVarArray(OBJACK, ["MDLN1", "MDLN2"])

    def testHash(self):
        secsvar = SecsVarArray(MDLN)
        hash(secsvar)

    def testItemSetterMatchingSecsVar(self):
        secsvar = SecsVarArray(MDLN, ["MDLN", "SOFTREV"])

        secsvar[0] = SecsVarString("NLDM")

        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalSecsVar(self):
        secsvar = SecsVarArray(OBJACK, [0, 1])

        with self.assertRaises(TypeError):
            secsvar[0] = SecsVarString("NLDM")

    def testItemSetterMatchingValue(self):
        secsvar = SecsVarArray(MDLN, ["MDLN", "SOFTREV"])

        secsvar[0] = "NLDM"

        self.assertEqual(secsvar[0].get(), "NLDM")

    def testItemSetterIllegalValue(self):
        secsvar = SecsVarArray(OBJACK, [0, 1])

        with self.assertRaises(ValueError):
            secsvar[0] = "NLDM"

    def testItemGetterUnknown(self):
        secsvar = SecsVarArray(MDLN, ["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3]

    def testItemSetterUnknown(self):
        secsvar = SecsVarArray(MDLN, ["MDLN", "SOFTREV"])

        with self.assertRaises(IndexError):
            secsvar[3] = SecsVarString("NLDM")

    def testIteration(self):
        secsvar = SecsVarArray(MDLN, ["MDLN1", "MDLN2"])

        for value in secsvar:
            self.assertIn(value, ["MDLN1", "MDLN2"])

    def testIteratorsIterator(self):
        # does not need to be tested, but raises coverage
        iter(iter(SecsVarArray(MDLN, ["MDLN1", "MDLN2"])))

    def testSettingListToSmall(self):
        secsvar = SecsVarArray(MDLN, count=2)

        with self.assertRaises(ValueError):
            secsvar.set(["MDLN"])

    def testSettingListMatchingLength(self):
        secsvar = SecsVarArray(MDLN, count=2)

        secsvar.set(["MDLN", "SOFTREV"])

    def testSettingListToBig(self):
        secsvar = SecsVarArray(MDLN, count=2)

        with self.assertRaises(ValueError):
            secsvar.set(["MDLN", "SOFTREV", "MDLN2"])

    def testSettingInvalidValue(self):
        secsvar = SecsVarArray(MDLN, count=2)

        with self.assertRaises(ValueError):
            secsvar.set("MDLN")

    def testGettingList(self):
        secsvar = SecsVarArray(MDLN, ["MDLN1", "SOFTREV1"])

        var = secsvar.get()

        self.assertEqual(var[0], "MDLN1")
        self.assertEqual(var[1], "SOFTREV1")

    def testEncode(self):
        secsvar = SecsVarArray(MDLN, ["MDLN1", "SOFTREV1"])

        self.assertEqual(secsvar.encode(), b"\x01\x02A\x05MDLN1A\x08SOFTREV1")

    def testDecode(self):
        secsvar = SecsVarArray(MDLN, ["MDLN1", "SOFTREV1"])

        secsvar[0] = ""
        secsvar[1] = ""

        self.assertEqual(secsvar[0], "")
        self.assertEqual(secsvar[1], "")

        secsvar.decode(b"\x01\x02A\x05MDLN1A\x08SOFTREV1")

        self.assertEqual(secsvar[0], "MDLN1")
        self.assertEqual(secsvar[1], "SOFTREV1")
        self.assertEqual(len(secsvar), 2)


class TestSecsVarBinary(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarBinary(1)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarBinary(13)
        secsvar1 = SecsVarDynamic([SecsVarBinary], 13)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarBinary(13)
        secsvar1 = SecsVarBinary(13)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarBinary(13)
        secsvar1 = b"\x0d"

        self.assertEqual(secsvar, secsvar1)

    def testRepr(self):
        print(SecsVarBinary(13))

    def testEmptyRepr(self):
        print(SecsVarBinary([]))

    def testNoneRepr(self):
        print(SecsVarBinary(None))

    def testSettingNone(self):
        secsvar = SecsVarBinary()

        secsvar.set(None)

    def testGettingUninitialized(self):
        secsvar = SecsVarBinary()
        
        self.assertEqual(secsvar.get(), b"")

    def testEncodeEmpty(self):
        secsvar = SecsVarBinary("")

        self.assertEqual(secsvar.encode(), b"!\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarBinary(13)

        self.assertEqual(secsvar.encode(), b"!\x01\r")

    def testEncodeMulti(self):
        secsvar = SecsVarBinary(b"\x01\x0b\x19")

        self.assertEqual(secsvar.encode(), b"!\x03\x01\x0b\x19")

    def testDecodeEmpty(self):
        secsvar = SecsVarBinary()

        secsvar.decode(b"!\x00")

        self.assertEqual(secsvar.get(), b"")

    def testDecodeSingle(self):
        secsvar = SecsVarBinary()

        secsvar.decode(b"!\x01\r")

        self.assertEqual(secsvar.get(), 13)

    def testDecodeMulti(self):
        secsvar = SecsVarBinary()

        secsvar.decode(b"!\x03\x01\x0b\x19")

        self.assertEqual(secsvar.get(), b"\x01\x0b\x19")


class TestSecsVarBoolean(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarBoolean(True)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarBoolean(True)
        secsvar1 = SecsVarDynamic([SecsVarBoolean], True)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarBoolean(True)
        secsvar1 = SecsVarBoolean(True)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarBoolean(True)
        secsvar1 = True

        self.assertEqual(secsvar, secsvar1)

    def testEqualityList(self):
        secsvar = SecsVarBoolean([True, False, True])
        secsvar1 = [True, False, True]

        self.assertEqual(secsvar, secsvar1)

    def testRepr(self):
        print(SecsVarBoolean(True))

    def testEmptyRepr(self):
        print(SecsVarBoolean([]))

    def testGettingItem(self):
        secsvar = SecsVarBoolean([True, False, True])

        self.assertEqual(secsvar[0], True)

    def testSettingItem(self):
        secsvar = SecsVarBoolean([True, False, True])

        secsvar[0] = False

        self.assertEqual(secsvar[0], False)

    def testGettingUninitialized(self):
        secsvar = SecsVarBoolean()
        
        self.assertEqual(secsvar.get(), [])

    def testEncodeEmpty(self):
        secsvar = SecsVarBoolean([])

        self.assertEqual(secsvar.encode(), b"%\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarBoolean(True)

        self.assertEqual(secsvar.encode(), b"%\x01\x01")

    def testEncodeMulti(self):
        secsvar = SecsVarBoolean([True, True, False])

        self.assertEqual(secsvar.encode(), b"%\x03\x01\x01\x00")

    def testDecodeEmpty(self):
        secsvar = SecsVarBoolean()

        secsvar.decode(b"%\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarBoolean()

        secsvar.decode(b"%\x01\x01")

        self.assertEqual(secsvar.get(), True)

    def testDecodeMulti(self):
        secsvar = SecsVarBoolean()

        secsvar.decode(b"%\x03\x01\x01\x00")

        self.assertEqual(secsvar.get(), [True, True, False])

    def testLen(self):
        secsvar = SecsVarBoolean([True, False, True])

        self.assertEqual(len(secsvar), 3)


class TestSecsVarString(unittest.TestCase):
    def testConstructorWrongLengthString(self):
        secsvar = SecsVarString(count=5)

        with self.assertRaises(ValueError):
            secsvar.set("testString")

    def testConstructorConvertsNoneToEmptyString(self):
        secsvar = SecsVarString(None)

        self.assertEqual(secsvar.get(), "")

    def testHash(self):
        secsvar = SecsVarString("Test")
        hash(secsvar)

    def testSetNoneNotAllowed(self):
        secsvar = SecsVarString(count=5)

        with self.assertRaises(ValueError):
            secsvar.set(None)

    def testSetWithIllegalType(self):
        secsvar = SecsVarString()

        with self.assertRaises(TypeError):
            secsvar.set(SecsVarBoolean(True))

    def testEncodeString(self):
        secsvar = SecsVarString("testString")

        self.assertEqual(secsvar.encode(), b"A\ntestString")

    def testDecodeString(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\ntestString")

        self.assertEqual(secsvar.get(), "testString")

    def testDecodeStringNonPrinting(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\ntestStrin\xc2")

        self.assertEqual(secsvar.get(), u"testStrin\xc2")

    def testEncodeEmptyString(self):
        secsvar = SecsVarString("")

        self.assertEqual(secsvar.encode(), b"A\0")

    def testDecodeEmptyString(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\0")

        self.assertEqual(secsvar.get(), "")

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarString("TEST123")
        secsvar1 = SecsVarDynamic([SecsVarString], "TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarString("TEST123")
        secsvar1 = SecsVarString("TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarString("TEST123")
        secsvar1 = "TEST123"

        self.assertEqual(secsvar, secsvar1)

    def testRepr(self):
        print(SecsVarString("TEST123\1\2\3TEST123\1\2\3"))

    def testEncodeEmpty(self):
        secsvar = SecsVarString("")

        self.assertEqual(secsvar.encode(), b"A\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarString("a")

        self.assertEqual(secsvar.encode(), b"A\x01a")

    def testEncodeMulti(self):
        secsvar = SecsVarString("asdfg")

        self.assertEqual(secsvar.encode(), b"A\x05asdfg")

    def testDecodeEmpty(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\x00")

        self.assertEqual(secsvar.get(), "")

    def testDecodeSingle(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\x01a")

        self.assertEqual(secsvar.get(), "a")

    def testDecodeMulti(self):
        secsvar = SecsVarString()

        secsvar.decode(b"A\x05asdfg")

        self.assertEqual(secsvar.get(), "asdfg")

class TestSecsVarJIS8(unittest.TestCase):
    def testConstructorWrongLengthString(self):
        secsvar = SecsVarJIS8(count=5)

        with self.assertRaises(ValueError):
            secsvar.set(u"testString")

    def testConstructorConvertsNoneToEmptyString(self):
        secsvar = SecsVarJIS8(None)

        self.assertEqual(secsvar.get(), u"")

    def testHash(self):
        secsvar = SecsVarJIS8("Test")
        hash(secsvar)

    def testSetNoneNotAllowed(self):
        secsvar = SecsVarJIS8(count=5)

        with self.assertRaises(ValueError):
            secsvar.set(None)

    def testSetWithIllegalType(self):
        secsvar = SecsVarJIS8()

        with self.assertRaises(TypeError):
            secsvar.set(SecsVarBoolean(True))

    def testEncodeString(self):
        secsvar = SecsVarJIS8(u"testString¥")

        self.assertEqual(secsvar.encode(), b"E\x0btestString\\")

    def testDecodeString(self):
        secsvar = SecsVarJIS8()

        secsvar.decode(b"E\ntestString")

        self.assertEqual(secsvar.get(), "testString")

    def testEncodeEmptyString(self):
        secsvar = SecsVarJIS8("")

        self.assertEqual(secsvar.encode(), b"E\0")

    def testDecodeEmptyString(self):
        secsvar = SecsVarJIS8()

        secsvar.decode(b"E\0")

        self.assertEqual(secsvar.get(), "")

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarJIS8("TEST123")
        secsvar1 = SecsVarDynamic([SecsVarJIS8], "TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarJIS8("TEST123")
        secsvar1 = SecsVarJIS8("TEST123")

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarJIS8("TEST123")
        secsvar1 = "TEST123"

        self.assertEqual(secsvar, secsvar1)

    def testRepr(self):
        print(SecsVarJIS8("TEST123\1\2\3TEST123\1\2\3"))

    def testEncodeEmpty(self):
        secsvar = SecsVarJIS8("")

        self.assertEqual(secsvar.encode(), b"E\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarJIS8("a")

        self.assertEqual(secsvar.encode(), b"E\x01a")

    def testEncodeMulti(self):
        secsvar = SecsVarJIS8("asdfg")

        self.assertEqual(secsvar.encode(), b"E\x05asdfg")

    def testDecodeEmpty(self):
        secsvar = SecsVarJIS8()

        secsvar.decode(b"E\x00")

        self.assertEqual(secsvar.get(), "")

    def testDecodeSingle(self):
        secsvar = SecsVarJIS8()

        secsvar.decode(b"E\x01a")

        self.assertEqual(secsvar.get(), "a")

    def testDecodeMulti(self):
        secsvar = SecsVarJIS8()

        secsvar.decode(b"E\x05asdfg")

        self.assertEqual(secsvar.get(), "asdfg")


class TestSecsVarI8(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarI8(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI8(17)
        secsvar1 = SecsVarDynamic([SecsVarI8], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI8(17)
        secsvar1 = SecsVarI8(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI8(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testRepr(self):
        print(SecsVarI8(8))

    def testEmptyRepr(self):
        print(SecsVarI8([]))

    def testEqualityList(self):
        secsvar = SecsVarU8([1, 2, 3])
        secsvar1 = [1, 2, 3]

        self.assertEqual(secsvar, secsvar1)

    def testGettingUninitialized(self):
        secsvar = SecsVarI8()
        
        self.assertEqual(secsvar.get(), [])

    def testEncode(self):
        secsvar = SecsVarI8(1337)
        
        self.assertEqual(secsvar.encode(), b"a\x08\x00\x00\x00\x00\x00\x00\x059")

    def testWrongLengthDecode(self):
        secsvar = SecsVarI8(0)
        
        with self.assertRaises(ValueError):
            secsvar.decode(b"a\x08\x00\x00\x00\x00\x00\x00")

    def testEncodeEmpty(self):
        secsvar = SecsVarI8([])

        self.assertEqual(secsvar.encode(), b"a\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarI8(123)

        self.assertEqual(secsvar.encode(), b"a\x08\x00\x00\x00\x00\x00\x00\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarI8([123, 234, -345])

        self.assertEqual(secsvar.encode(), b"a\x18\x00\x00\x00\x00\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00\xea\xff\xff\xff\xff\xff\xff\xfe\xa7")

    def testDecodeEmpty(self):
        secsvar = SecsVarI8()

        secsvar.decode(b"a\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarI8()

        secsvar.decode(b"a\x08\x00\x00\x00\x00\x00\x00\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarI8()

        secsvar.decode(b"a\x18\x00\x00\x00\x00\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00\xea\xff\xff\xff\xff\xff\xff\xfe\xa7")

        self.assertEqual(secsvar.get(), [123, 234, -345])

    def testLen(self):
        secsvar = SecsVarI8([1, 2, 3])

        self.assertEqual(len(secsvar), 3)


class TestSecsVarI1(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarI1(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI1(17)
        secsvar1 = SecsVarDynamic([SecsVarI1], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI1(17)
        secsvar1 = SecsVarI1(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI1(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarI1([])

        self.assertEqual(secsvar.encode(), b"e\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarI1(123)

        self.assertEqual(secsvar.encode(), b"e\x01{")

    def testEncodeMulti(self):
        secsvar = SecsVarI1([12, 23, -34])

        self.assertEqual(secsvar.encode(), b"e\x03\x0c\x17\xde")

    def testDecodeEmpty(self):
        secsvar = SecsVarI1()

        secsvar.decode(b"e\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarI1()

        secsvar.decode(b"e\x01{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarI1()

        secsvar.decode(b"e\x03\x0c\x17\xde")

        self.assertEqual(secsvar.get(), [12, 23, -34])


class TestSecsVarI2(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarI2(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI2(17)
        secsvar1 = SecsVarDynamic([SecsVarI2], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI2(17)
        secsvar1 = SecsVarI2(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI2(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarI2([])

        self.assertEqual(secsvar.encode(), b"i\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarI2(123)

        self.assertEqual(secsvar.encode(), b"i\x02\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarI2([123, 234, -345])

        self.assertEqual(secsvar.encode(), b"i\x06\x00{\x00\xea\xfe\xa7")

    def testDecodeEmpty(self):
        secsvar = SecsVarI2()

        secsvar.decode(b"i\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarI2()

        secsvar.decode(b"i\x02\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarI2()

        secsvar.decode(b"i\x06\x00{\x00\xea\xfe\xa7")

        self.assertEqual(secsvar.get(), [123, 234, -345])


class TestSecsVarI4(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarI4(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarI4(17)
        secsvar1 = SecsVarDynamic([SecsVarI4], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarI4(17)
        secsvar1 = SecsVarI4(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarI4(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarI4([])

        self.assertEqual(secsvar.encode(), b"q\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarI4(123)

        self.assertEqual(secsvar.encode(), b"q\x04\x00\x00\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarI4([123, 234, -345])

        self.assertEqual(secsvar.encode(), b"q\x0c\x00\x00\x00{\x00\x00\x00\xea\xff\xff\xfe\xa7")

    def testDecodeEmpty(self):
        secsvar = SecsVarI4()

        secsvar.decode(b"q\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarI4()

        secsvar.decode(b"q\x04\x00\x00\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarI4()

        secsvar.decode(b"q\x0c\x00\x00\x00{\x00\x00\x00\xea\xff\xff\xfe\xa7")

        self.assertEqual(secsvar.get(), [123, 234, -345])


class TestSecsVarF8(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarF8(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarF8(12.3)
        secsvar1 = SecsVarDynamic([SecsVarF8], 12.3)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarF8(12.3)
        secsvar1 = SecsVarF8(12.3)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarF8(12.3)
        secsvar1 = 12.3

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarF8([])

        self.assertEqual(secsvar.encode(), b"\x81\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarF8(123)

        self.assertEqual(secsvar.encode(), b"\x81\x08@^\xc0\x00\x00\x00\x00\x00")

    def testEncodeMulti(self):
        secsvar = SecsVarF8([123, 234, -345])

        self.assertEqual(secsvar.encode(), b"\x81\x18@^\xc0\x00\x00\x00\x00\x00@m@\x00\x00\x00\x00\x00\xc0u\x90\x00\x00\x00\x00\x00")

    def testDecodeEmpty(self):
        secsvar = SecsVarF8()

        secsvar.decode(b"\x81\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarF8()

        secsvar.decode(b"\x81\x08@^\xc0\x00\x00\x00\x00\x00")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarF8()

        secsvar.decode(b"\x81\x18@^\xc0\x00\x00\x00\x00\x00@m@\x00\x00\x00\x00\x00\xc0u\x90\x00\x00\x00\x00\x00")

        self.assertEqual(secsvar.get(), [123, 234, -345])


class TestSecsVarF4(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarF4(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarF4(17)
        secsvar1 = SecsVarDynamic([SecsVarF4], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarF4(17)
        secsvar1 = SecsVarF4(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarF4(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarF4([])

        self.assertEqual(secsvar.encode(), b"\x91\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarF4(123)

        self.assertEqual(secsvar.encode(), b"\x91\x04B\xf6\x00\x00")

    def testEncodeMulti(self):
        secsvar = SecsVarF4([123, 234, -345])

        self.assertEqual(secsvar.encode(), b"\x91\x0cB\xf6\x00\x00Cj\x00\x00\xc3\xac\x80\x00")

    def testDecodeEmpty(self):
        secsvar = SecsVarF4()

        secsvar.decode(b"\x91\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarF4()

        secsvar.decode(b"\x91\x04B\xf6\x00\x00")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarF4()

        secsvar.decode(b"\x91\x0cB\xf6\x00\x00Cj\x00\x00\xc3\xac\x80\x00")

        self.assertEqual(secsvar.get(), [123, 234, -345])


class TestSecsVarU8(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarU8(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU8(17)
        secsvar1 = SecsVarDynamic([SecsVarU8], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU8(17)
        secsvar1 = SecsVarU8(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU8(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarU8([])

        self.assertEqual(secsvar.encode(), b"\xa1\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarU8(123)

        self.assertEqual(secsvar.encode(), b"\xa1\x08\x00\x00\x00\x00\x00\x00\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarU8([123, 234, 345])

        self.assertEqual(secsvar.encode(), b"\xa1\x18\x00\x00\x00\x00\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00\xea\x00\x00\x00\x00\x00\x00\x01Y")

    def testDecodeEmpty(self):
        secsvar = SecsVarU8()

        secsvar.decode(b"\xa1\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarU8()

        secsvar.decode(b"\xa1\x08\x00\x00\x00\x00\x00\x00\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarU8()

        secsvar.decode(b"\xa1\x18\x00\x00\x00\x00\x00\x00\x00{\x00\x00\x00\x00\x00\x00\x00\xea\x00\x00\x00\x00\x00\x00\x01Y")

        self.assertEqual(secsvar.get(), [123, 234, 345])


class TestSecsVarU1(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarU1(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU1(17)
        secsvar1 = SecsVarDynamic([SecsVarU1], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU1(17)
        secsvar1 = SecsVarU1(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU1(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarU1([])

        self.assertEqual(secsvar.encode(), b"\xa5\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarU1(123)

        self.assertEqual(secsvar.encode(), b"\xa5\x01{")

    def testEncodeMulti(self):
        secsvar = SecsVarU1([12, 23, 34])

        self.assertEqual(secsvar.encode(), b"\xa5\x03\x0c\x17\"")

    def testDecodeEmpty(self):
        secsvar = SecsVarU1()

        secsvar.decode(b"\xa5\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarU1()

        secsvar.decode(b"\xa5\x01{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarU1()

        secsvar.decode(b"\xa5\x03\x0c\x17\"")

        self.assertEqual(secsvar.get(), [12, 23, 34])


class TestSecsVarU2(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarU2(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU2(17)
        secsvar1 = SecsVarDynamic([SecsVarU2], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU2(17)
        secsvar1 = SecsVarU2(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU2(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarU2([])

        self.assertEqual(secsvar.encode(), b"\xa9\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarU2(123)

        self.assertEqual(secsvar.encode(), b"\xa9\x02\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarU2([123, 234, 345])

        self.assertEqual(secsvar.encode(), b"\xa9\x06\x00{\x00\xea\x01Y")

    def testDecodeEmpty(self):
        secsvar = SecsVarU2()

        secsvar.decode(b"\xa9\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarU2()

        secsvar.decode(b"\xa9\x02\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarU2()

        secsvar.decode(b"\xa9\x06\x00{\x00\xea\x01Y")

        self.assertEqual(secsvar.get(), [123, 234, 345])


class TestSecsVarU4(unittest.TestCase):
    def testHash(self):
        secsvar = SecsVarU4(123)
        hash(secsvar)

    def testEqualitySecsVarDynamic(self):
        secsvar = SecsVarU4(17)
        secsvar1 = SecsVarDynamic([SecsVarU4], 17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualitySecsVar(self):
        secsvar = SecsVarU4(17)
        secsvar1 = SecsVarU4(17)

        self.assertEqual(secsvar, secsvar1)

    def testEqualityVar(self):
        secsvar = SecsVarU4(17)
        secsvar1 = 17

        self.assertEqual(secsvar, secsvar1)

    def testEncodeEmpty(self):
        secsvar = SecsVarU4([])

        self.assertEqual(secsvar.encode(), b"\xb1\x00")

    def testEncodeSingle(self):
        secsvar = SecsVarU4(123)

        self.assertEqual(secsvar.encode(), b"\xb1\x04\x00\x00\x00{")

    def testEncodeMulti(self):
        secsvar = SecsVarU4([123, 234, 345])

        self.assertEqual(secsvar.encode(), b"\xb1\x0c\x00\x00\x00{\x00\x00\x00\xea\x00\x00\x01Y")

    def testDecodeEmpty(self):
        secsvar = SecsVarU4()

        secsvar.decode(b"\xb1\x00")

        self.assertEqual(secsvar.get(), [])

    def testDecodeSingle(self):
        secsvar = SecsVarU4()

        secsvar.decode(b"\xb1\x04\x00\x00\x00{")

        self.assertEqual(secsvar.get(), 123)

    def testDecodeMulti(self):
        secsvar = SecsVarU4()

        secsvar.decode(b"\xb1\x0c\x00\x00\x00{\x00\x00\x00\xea\x00\x00\x01Y")

        self.assertEqual(secsvar.get(), [123, 234, 345])


class GoodBadLists(object):
    _type = None
    goodValues = []
    badValues = []

    def goodAssignmentCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(count=value["LENGTH"])
        else:
            secsvar = self._type()

        print(self._type.__name__, "testing assignment of good", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"]))

        secsvar.set(value["VALUE"])
        nose.tools.eq_(secsvar.get(), value["RESULT"])

    def testGoodAssignment(self):
        for valueList in self.goodValues:
            for value in valueList:
                yield self.goodAssignmentCheck, value

    @nose.tools.raises(TypeError, ValueError)
    def badAssignmentCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(count=value["LENGTH"])
        else:
            secsvar = self._type()

        print(self._type.__name__, "testing assignment of bad", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"]))
        secsvar.set(value["VALUE"])
        print(self._type.__name__, "unexpected bad assignment", secsvar.get())

    def testBadAssignment(self):
        for valueList in self.badValues:
            for value in valueList:
                yield self.badAssignmentCheck, value

    def goodSupportedCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(count=value["LENGTH"])
        else:
            secsvar = self._type()

        print(self._type.__name__, "testing isSupported for good", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"]))
        nose.tools.eq_(secsvar.supports_value(value["VALUE"]), True)

    def testGoodSupported(self):
        for valueList in self.goodValues:
            for value in valueList:
                yield self.goodSupportedCheck, value

    def badSupportedCheck(self, value):
        if "LENGTH" in value:
            secsvar = self._type(count=value["LENGTH"])
        else:
            secsvar = self._type()

        print(self._type.__name__, "testing isSupported for bad", type(value["VALUE"]).__name__, "value", printable_value(value["VALUE"]))
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
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 255, "RESULT": 255},
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 265},
    ]

    #complex
    _goodComplexValues = {}
    _badComplexValues = [
        {"VALUE": 1J},
    ]

    #str
    _goodStringValues = [
        {"VALUE": "TEST1", "RESULT": b"TEST1"},
        {"VALUE": b"1234QWERasdf.-+ \n\r\t\1 \127 \xB1", "RESULT": b"1234QWERasdf.-+ \n\r\t\1 \127 \xB1"},
        {"VALUE": "TEST1", "RESULT": b"TEST1", "LENGTH": 5},
    ]
    _badStringValues = [
        {"VALUE": "TEST1", "LENGTH": 4},
    ]

    #unicode
    _goodUnicodeValues = [
        {"VALUE": u"TEST1", "RESULT": b"TEST1"},
        {"VALUE": u"1234QWERasdf.-+ \n\r\t\1 \127", "RESULT": b"1234QWERasdf.-+ \n\r\t\1 \127"},
        {"VALUE": u"TEST1", "RESULT": b"TEST1", "LENGTH": 5},
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\xc3O JOS\xc9'},
        {"VALUE": u"TEST1", "RESULT": b"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": b"\x00\x01\x00\x00"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": b"\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": b"\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [1, -1, 256, 5]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH": 5}
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": b"\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": b"\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (1, -1, 256, 5)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": b"\x00\x01\x05\x20\x10\xFF"},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": b"\x00\x01\x05\x20\x10\xFF", "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": 0, "RESULT": False},
        {"VALUE": 1, "RESULT": True},
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 2},
        {"VALUE": 265},
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
        {"VALUE": u"TEST1"},
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
        {"VALUE": bytearray(b"\x00\x01\x00\x01"), "RESULT": [False, True, False, True]},
        {"VALUE": bytearray(b"\x00\x01\x00\x01"), "RESULT": [False, True, False, True], "LENGTH": 4},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x00\x01"), "LENGTH": 3},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF")},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 6},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": -1, "RESULT": "-1"},
        {"VALUE": 0, "RESULT": "0"},
        {"VALUE": 1, "RESULT": "1"},
        {"VALUE": 2, "RESULT": "2"},
        {"VALUE": 265, "RESULT": "265"},
    ]
    _badLongValues = [
        {"VALUE": 265, "LENGTH": 1},
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
        {"VALUE": u"JOS\xc9", "RESULT": u"JOS\xc9"}, # CP1252
    ]
    _badUnicodeValues = [
        {"VALUE": u'ABRA\u0103 JOS\xc9'},
        {"VALUE": u"TEST1", "LENGTH": 4},
    ]

    #list
    _goodListValues = [
        {"VALUE": [False, True, False, False], "RESULT": "\x00\x01\x00\x00"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "RESULT": "\x00\x01\x05\x20\x10\x7F"},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "RESULT": "\x00\x01\x05\x20\x10\x7F", "LENGTH": 6},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "RESULT": u"\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badListValues = [
        {"VALUE": [1, -1, 256, 5]},
        {"VALUE": ["Test", "ASDF"]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x100]},
        {"VALUE": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH": 5},
    ]

    #tuple
    _goodTupleValues = [
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "RESULT": "\x00\x01\x05\x20\x10\x7F"},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "RESULT": "\x00\x01\x05\x20\x10\x7F", "LENGTH": 6},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0xFF), "RESULT": u"\x00\x01\x05\x20\x10\xFF", "LENGTH": 6},
    ]
    _badTupleValues = [
        {"VALUE": (1, -1, 256, 5)},
        {"VALUE": ("Test", "ASDF")},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x100)},
        {"VALUE": (0x0, 0x1, 0x5, 0x20, 0x10, 0x7F), "LENGTH": 5},
    ]

    #bytearray
    _goodByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "RESULT": "\x00\x01\x05\x20\x10\x7F"},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "RESULT": "\x00\x01\x05\x20\x10\x7F", "LENGTH" : 6},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": u"\x00\x01\x05\x20\x10\xFF", "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "LENGTH" : 5},
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
        {"VALUE": -9223372036854775808, "RESULT":-9223372036854775808},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 9223372036854775807, "RESULT": 9223372036854775807}
    ]
    _badLongValues = [
        {"VALUE": -9223372036854775809},
        {"VALUE": 9223372036854775808},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": -128, "RESULT":-128},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 127, "RESULT": 127}
    ]
    _badLongValues = [
        {"VALUE": -129},
        {"VALUE": 128},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0x7F], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"),},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\x7F"), "LENGTH" : 5},
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
        {"VALUE": -32768, "RESULT":-32768},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 32767, "RESULT": 32767}
    ]
    _badLongValues = [
        {"VALUE": -32769},
        {"VALUE": 32768},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": -2147483648, "RESULT":-2147483648},
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 2147483647, "RESULT": 2147483647}
    ]
    _badLongValues = [
        {"VALUE": -2147483649},
        {"VALUE": 2147483648},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": -1, "RESULT": -1},
        {"VALUE": 0, "RESULT": 0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 18446744073709551615, "RESULT": 18446744073709551615}
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 18446744073709551616},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 255, "RESULT": 255}
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 256},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 65535, "RESULT": 65535}
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 65536},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
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
        {"VALUE": 0, "RESULT":0},
        {"VALUE": 1, "RESULT": 1},
        {"VALUE": 2, "RESULT": 2},
        {"VALUE": 265, "RESULT": 265},
        {"VALUE": 4294967295, "RESULT": 4294967295}
    ]
    _badLongValues = [
        {"VALUE": -1},
        {"VALUE": 4294967296},
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
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF]},
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "RESULT": [0x0, 0x1, 0x5, 0x20, 0x10, 0xFF], "LENGTH" : 6},
    ]
    _badByteArrayValues = [
        {"VALUE": bytearray(b"\x00\x01\x05\x20\x10\xFF"), "LENGTH" : 5},
    ]

    goodValues = [_goodBoolValues, _goodFloatValues, _goodIntValues, _goodLongValues, _goodComplexValues, _goodStringValues, _goodUnicodeValues, _goodListValues, _goodTupleValues, _goodByteArrayValues]
    badValues = [_badBoolValues, _badFloatValues, _badIntValues, _badLongValues, _badComplexValues, _badStringValues, _badUnicodeValues, _badListValues, _badTupleValues, _badByteArrayValues]

