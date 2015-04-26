#####################################################################
# secsFunctions.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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
"""Wrappers for SECS stream and functions"""

from collections import OrderedDict

from secsFunctionBase import secsStreamFunction
from secsVariables import secsVarList, secsVarArray, secsVarString, secsVarBinary, secsVarU4, secsVarBoolean, secsVarDynamic

class secsS00F00(secsStreamFunction):
    _stream = 0
    _function = 0

    _formatDescriptor = None

class secsS01F00(secsStreamFunction):
    _stream = 1
    _function = 0

    _formatDescriptor = None

class secsS01F01(secsStreamFunction):
    _stream = 1
    _function = 1

    _formatDescriptor = None

class secsS01F02E(secsStreamFunction):
    _stream = 1
    _function = 2

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)

class secsS01F02H(secsStreamFunction):
    _stream = 1
    _function = 2

    _formatDescriptor = None

class secsS01F03(secsStreamFunction):
    _stream = 1
    _function = 3

    _formatDescriptor = secsVarArray(secsVarU4(1))

class secsS01F04(secsStreamFunction):
    _stream = 1
    _function = 4

    _formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))

class secsS01F11(secsStreamFunction):
    _stream = 1
    _function = 11

    _formatDescriptor = secsVarArray(secsVarU4(1))

class secsS01F12(secsStreamFunction):
    _stream = 1
    _function = 12

    _formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("SVID", secsVarU4(1)),
                        ("SVNAME", secsVarString()),
                        ("UNITS", secsVarString()),
                        )), 3))

class secsS01F13E(secsStreamFunction):
    _stream = 1
    _function = 13

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)

class secsS01F13H(secsStreamFunction):
    _stream = 1
    _function = 13

    _formatDescriptor = None

class secsS01F14E(secsStreamFunction):
    _stream = 1
    _function = 14

    _formatDescriptor = secsVarList(OrderedDict((
                            ("COMMACK", secsVarBinary(1)),
                            ("DATA", secsVarList(OrderedDict((
                                ("MDLN", secsVarString(20)),
                                ("SOFTREV", secsVarString(20)),
                            )), 2))
                        )), 2)

class secsS01F14H(secsStreamFunction):
    _stream = 1
    _function = 14

    _formatDescriptor = secsVarList(OrderedDict((
                            ("COMMACK", secsVarBinary(1)),
                            ("DATA", secsVarList([], 0))
                        )), 2)

class secsS02F00(secsStreamFunction):
    _stream = 2
    _function = 0

    _formatDescriptor = None

class secsS02F13(secsStreamFunction):
    _stream = 2
    _function = 13

    _formatDescriptor = secsVarArray(secsVarU4(1))


class secsS02F14(secsStreamFunction):
    _stream = 2
    _function = 14

    _formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))

class secsS02F15(secsStreamFunction):
    _stream = 2
    _function = 15

    _formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("ECID", secsVarU4(1)),
                        ("ECV", secsVarDynamic(secsVarString)),
                        )), 2))

class secsS02F16(secsStreamFunction):
    _stream = 2
    _function = 16

    _formatDescriptor = secsVarBinary(1)

class secsS02F29(secsStreamFunction):
    _stream = 2
    _function = 29

    _formatDescriptor = secsVarArray(secsVarU4(1))

class secsS02F30(secsStreamFunction):
    _stream = 2
    _function = 30

    _formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("ECID", secsVarU4(1)),
                        ("ECNAME", secsVarString()),
                        ("ECMIN", secsVarDynamic(secsVarString)),
                        ("ECMAX", secsVarDynamic(secsVarString)),
                        ("ECDEF", secsVarDynamic(secsVarString)),
                        ("UNITS", secsVarString()),
                        )), 6))

class secsS02F33(secsStreamFunction):
    _stream = 2
    _function = 33

    _formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("DATA", secsVarArray(
                            secsVarList(OrderedDict((
                                ("RPTID", secsVarU4(1)),
                                ("RPT", secsVarArray(
                                    secsVarString()
                                )),
                            )), 2)
                        )),
                        )), 2)

class secsS02F34(secsStreamFunction):
    _stream = 2
    _function = 34

    _formatDescriptor = secsVarBinary(1)

class secsS02F35(secsStreamFunction):
    _stream = 2
    _function = 35

    _formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("DATA", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CEID", secsVarU4(1)),
                                ("CE", secsVarArray(
                                    secsVarU4(1)
                                )),
                            )), 2)
                        )),
                        )), 2)

class secsS02F36(secsStreamFunction):
    _stream = 2
    _function = 36

    _formatDescriptor = secsVarBinary(1)

class secsS02F37(secsStreamFunction):
    _stream = 2
    _function = 37

    _formatDescriptor = secsVarList(OrderedDict((
                        ("CEED", secsVarBoolean(1)),
                        ("CEID", secsVarArray(
                            secsVarU4(1)
                        )),
                        )), 2)

class secsS02F38(secsStreamFunction):
    _stream = 2
    _function = 38

    _formatDescriptor = secsVarBinary(1)

class secsS02F41(secsStreamFunction):
    _stream = 2
    _function = 41

    _formatDescriptor = secsVarList(OrderedDict((
                        ("RCMD", secsVarString()),
                        ("PARAMS", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CPNAME", secsVarString()),
                                ("CPVAL", secsVarString()),
                            )), 2)
                        )),
                        )), 2)

class secsS02F42(secsStreamFunction):
    _stream = 2
    _function = 42

    _formatDescriptor = secsVarList(OrderedDict((
                        ("HCACK", secsVarBinary(1)),
                        ("PARAMS", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CPNAME", secsVarString()),
                                ("CPACK", secsVarBinary(1)),
                            )), 2)
                        )),
                        )), 2)

class secsS05F00(secsStreamFunction):
    _stream = 5
    _function = 0

    _formatDescriptor = None

class secsS05F01(secsStreamFunction):
    _stream = 5
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("ALCD", secsVarBinary(1)),
                        ("ALID", secsVarU4(1)),
                        ("ALTX", secsVarString(120)),
                        )), 3)

class secsS05F02(secsStreamFunction):
    _stream = 5
    _function = 2

    _formatDescriptor = secsVarBinary(1)

class secsS06F00(secsStreamFunction):
    _stream = 6
    _function = 0

    _formatDescriptor = None

class secsS06F11(secsStreamFunction):
    _stream = 6
    _function = 11

    _formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("CEID", secsVarU4(1)),
                        ("RPT", secsVarArray(
                            secsVarList(OrderedDict((
                                ("RPTID", secsVarU4(1)),
                                ("V", secsVarArray(
                                    secsVarDynamic(secsVarString)
                                )),
                            )), 2)
                        )),
                        )), 3)

class secsS06F12(secsStreamFunction):
    _stream = 6
    _function = 12

    _formatDescriptor = secsVarBinary(1)

class secsS07F00(secsStreamFunction):
    _stream = 7
    _function = 0

    _formatDescriptor = None

class secsS07F01(secsStreamFunction):
    _stream = 7
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("LENGTH", secsVarU4(1)),
                        )), 2)

class secsS07F02(secsStreamFunction):
    _stream = 7
    _function = 2

    _formatDescriptor = secsVarBinary(1)

class secsS07F03(secsStreamFunction):
    _stream = 7
    _function = 3

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)

class secsS07F04(secsStreamFunction):
    _stream = 7
    _function = 4

    _formatDescriptor = secsVarBinary(1)

class secsS07F05(secsStreamFunction):
    _stream = 7
    _function = 5

    _formatDescriptor = secsVarString()

class secsS07F06(secsStreamFunction):
    _stream = 7
    _function = 6

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)

class secsS07F17(secsStreamFunction):
    _stream = 7
    _function = 17

    _formatDescriptor = secsVarArray(secsVarString())

class secsS07F18(secsStreamFunction):
    _stream = 7
    _function = 18

    _formatDescriptor = secsVarBinary(1)

class secsS07F19(secsStreamFunction):
    _stream = 7
    _function = 19

    _formatDescriptor = None

class secsS07F20(secsStreamFunction):
    _stream = 7
    _function = 20

    _formatDescriptor = secsVarArray(secsVarString())

class secsS09F00(secsStreamFunction):
    _stream = 9
    _function = 0

    _formatDescriptor = None

class secsS09F01(secsStreamFunction):
    _stream = 9
    _function = 1

    _formatDescriptor = secsVarBinary(10)

class secsS09F03(secsStreamFunction):
    _stream = 9
    _function = 3

    _formatDescriptor = secsVarBinary(10)

class secsS09F05(secsStreamFunction):
    _stream = 9
    _function = 5

    _formatDescriptor = secsVarBinary(10)

class secsS09F07(secsStreamFunction):
    _stream = 9
    _function = 7

    _formatDescriptor = secsVarBinary(10)

class secsS09F09(secsStreamFunction):
    _stream = 9
    _function = 9

    _formatDescriptor = secsVarBinary(10)

class secsS09F11(secsStreamFunction):
    _stream = 9
    _function = 11

    _formatDescriptor = secsVarBinary(10)

class secsS09F13(secsStreamFunction):
    _stream = 9
    _function = 13

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MEXP", secsVarString(6)),
                        ("EDID", secsVarString(80)),
                        )), 2)

class secsS10F00(secsStreamFunction):
    _stream = 10
    _function = 0

    _formatDescriptor = None

class secsS10F01(secsStreamFunction):
    _stream = 10
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)

class secsS10F02(secsStreamFunction):
    _stream = 10
    _function = 2

    _formatDescriptor = secsVarBinary(1)

class secsS10F03(secsStreamFunction):
    _stream = 10
    _function = 3

    _formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)

class secsS10F04(secsStreamFunction):
    _stream = 10
    _function = 4

    _formatDescriptor = secsVarBinary(10)

secsStreamsFunctionsHost = {
     0:     {
         0: secsS00F00,
        },
     1:     {
         0: secsS01F00,
         1: secsS01F01,
         2: secsS01F02H,
         3: secsS01F03,
         4: secsS01F04,
        11: secsS01F11,
        12: secsS01F12,
        13: secsS01F13H,
        14: secsS01F14H,
        },
     2:     {
         0: secsS02F00,
        13: secsS02F13,
        14: secsS02F14,
        15: secsS02F15,
        16: secsS02F16,
        29: secsS02F29,
        30: secsS02F30,
        33: secsS02F33,
        34: secsS02F34,
        35: secsS02F35,
        36: secsS02F36,
        37: secsS02F37,
        38: secsS02F38,
        41: secsS02F41,
        42: secsS02F42,
        },
     5:    {
         0: secsS05F00,
         1: secsS05F01,
         2: secsS05F02,
        },
     6:    {
         0: secsS06F00,
        11: secsS06F11,
        12: secsS06F12,
        },
     7:    {
         1: secsS07F01,
         2: secsS07F02,
         3: secsS07F03,
         4: secsS07F04,
         5: secsS07F05,
         6: secsS07F06,
        17: secsS07F17,
        18: secsS07F18,
        19: secsS07F19,
        20: secsS07F20,
        },
     9:    {
         0: secsS09F00,
         1: secsS09F01,
         3: secsS09F03,
         5: secsS09F05,
         7: secsS09F07,
         9: secsS09F09,
        11: secsS09F11,
        13: secsS09F13,
        },
    10:    {
         0: secsS10F00,
         1: secsS10F01,
         2: secsS10F02,
         3: secsS10F03,
         4: secsS10F04,
        },
}

secsStreamsFunctionsEquipment = {
     0:     {
         0: secsS00F00,
        },
     1:     {
         0: secsS01F00,
         1: secsS01F01,
         2: secsS01F02E,
         3: secsS01F03,
         4: secsS01F04,
        11: secsS01F11,
        12: secsS01F12,
        13: secsS01F13E,
        14: secsS01F14E,
        },
     2:     {
         0: secsS02F00,
        13: secsS02F13,
        14: secsS02F14,
        15: secsS02F15,
        16: secsS02F16,
        29: secsS02F29,
        30: secsS02F30,
        33: secsS02F33,
        34: secsS02F34,
        35: secsS02F35,
        36: secsS02F36,
        37: secsS02F37,
        38: secsS02F38,
        41: secsS02F41,
        42: secsS02F42,
        },
     5:    {
         0: secsS05F00,
         1: secsS05F01,
         2: secsS05F02,
        },
     6:    {
         0: secsS06F00,
        11: secsS06F11,
        12: secsS06F12,
        },
     7:    {
         1: secsS07F01,
         2: secsS07F02,
         3: secsS07F03,
         4: secsS07F04,
         5: secsS07F05,
         6: secsS07F06,
        17: secsS07F17,
        18: secsS07F18,
        19: secsS07F19,
        20: secsS07F20,
        },
     9:    {
         0: secsS09F00,
         1: secsS09F01,
         3: secsS09F03,
         5: secsS09F05,
         7: secsS09F07,
         9: secsS09F09,
        11: secsS09F11,
        13: secsS09F13,
        },
    10:    {
         0: secsS10F00,
         1: secsS10F01,
         2: secsS10F02,
         3: secsS10F03,
         4: secsS10F04,
        },
}
