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
    stream = 0
    function = 0

    formatDescriptor = None

class secsS01F00(secsStreamFunction):
    stream = 1
    function = 0

    formatDescriptor = None

class secsS01F01(secsStreamFunction):
    stream = 1
    function = 1

    formatDescriptor = None

class secsS01F02E(secsStreamFunction):
    stream = 1
    function = 2

    formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)

class secsS01F02H(secsStreamFunction):
    stream = 1
    function = 2

    formatDescriptor = None

class secsS01F03(secsStreamFunction):
    stream = 1
    function = 3

    formatDescriptor = secsVarArray(secsVarU4(1))

class secsS01F04(secsStreamFunction):
    stream = 1
    function = 4

    formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))

class secsS01F11(secsStreamFunction):
    stream = 1
    function = 11

    formatDescriptor = secsVarArray(secsVarU4(1))

class secsS01F12(secsStreamFunction):
    stream = 1
    function = 12

    formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("SVID", secsVarU4(1)),
                        ("SVNAME", secsVarString()),
                        ("UNITS", secsVarString()),
                        )), 3))

class secsS01F13E(secsStreamFunction):
    stream = 1
    function = 13

    formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)

class secsS01F13H(secsStreamFunction):
    stream = 1
    function = 13

    formatDescriptor = None

class secsS01F14E(secsStreamFunction):
    stream = 1
    function = 14

    formatDescriptor = secsVarList(OrderedDict((
                            ("COMMACK", secsVarBinary(1)),
                            ("DATA", secsVarList(OrderedDict((
                                ("MDLN", secsVarString(20)),
                                ("SOFTREV", secsVarString(20)),
                            )), 2))
                        )), 2)

class secsS01F14H(secsStreamFunction):
    stream = 1
    function = 14

    formatDescriptor = secsVarList(OrderedDict((
                            ("COMMACK", secsVarBinary(1)),
                            ("DATA", secsVarList([], 0))
                        )), 2)

class secsS02F00(secsStreamFunction):
    stream = 2
    function = 0

    formatDescriptor = None

class secsS02F13(secsStreamFunction):
    stream = 2
    function = 13

    formatDescriptor = secsVarArray(secsVarU4(1))


class secsS02F14(secsStreamFunction):
    stream = 2
    function = 14

    formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))

class secsS02F15(secsStreamFunction):
    stream = 2
    function = 15

    formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("ECID", secsVarU4(1)),
                        ("ECV", secsVarDynamic(secsVarString)),
                        )), 2))

class secsS02F16(secsStreamFunction):
    stream = 2
    function = 16

    formatDescriptor = secsVarBinary(1)

class secsS02F29(secsStreamFunction):
    stream = 2
    function = 29

    formatDescriptor = secsVarArray(secsVarU4(1))

class secsS02F30(secsStreamFunction):
    stream = 2
    function = 30

    formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("ECID", secsVarU4(1)),
                        ("ECNAME", secsVarString()),
                        ("ECMIN", secsVarDynamic(secsVarString)),
                        ("ECMAX", secsVarDynamic(secsVarString)),
                        ("ECDEF", secsVarDynamic(secsVarString)),
                        ("UNITS", secsVarString()),
                        )), 6))

class secsS02F33(secsStreamFunction):
    stream = 2
    function = 33

    formatDescriptor = secsVarList(OrderedDict((
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
    stream = 2
    function = 34

    formatDescriptor = secsVarBinary(1)

class secsS02F35(secsStreamFunction):
    stream = 2
    function = 35

    formatDescriptor = secsVarList(OrderedDict((
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
    stream = 2
    function = 36

    formatDescriptor = secsVarBinary(1)

class secsS02F37(secsStreamFunction):
    stream = 2
    function = 37

    formatDescriptor = secsVarList(OrderedDict((
                        ("CEED", secsVarBoolean(1)),
                        ("CEID", secsVarArray(
                            secsVarU4(1)
                        )),
                        )), 2)

class secsS02F38(secsStreamFunction):
    stream = 2
    function = 38

    formatDescriptor = secsVarBinary(1)

class secsS02F41(secsStreamFunction):
    stream = 2
    function = 41

    formatDescriptor = secsVarList(OrderedDict((
                        ("RCMD", secsVarString()),
                        ("PARAMS", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CPNAME", secsVarString()),
                                ("CPVAL", secsVarString()),
                            )), 2)
                        )),
                        )), 2)

class secsS02F42(secsStreamFunction):
    stream = 2
    function = 42

    formatDescriptor = secsVarList(OrderedDict((
                        ("HCACK", secsVarBinary(1)),
                        ("PARAMS", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CPNAME", secsVarString()),
                                ("CPACK", secsVarBinary(1)),
                            )), 2)
                        )),
                        )), 2)

class secsS05F00(secsStreamFunction):
    stream = 5
    function = 0

    formatDescriptor = None

class secsS05F01(secsStreamFunction):
    stream = 5
    function = 1

    formatDescriptor = secsVarList(OrderedDict((
                        ("ALCD", secsVarBinary(1)),
                        ("ALID", secsVarU4(1)),
                        ("ALTX", secsVarString(120)),
                        )), 3)

class secsS05F02(secsStreamFunction):
    stream = 5
    function = 2

    formatDescriptor = secsVarBinary(1)

class secsS06F00(secsStreamFunction):
    stream = 6
    function = 0

    formatDescriptor = None

class secsS06F11(secsStreamFunction):
    stream = 6
    function = 11

    formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("CEID", secsVarU4(1)),
                        ("RPT", secsVarArray(
                            secsVarList(OrderedDict((
                                ("RPTID", secsVarU4(1)),
                                ("V", secsVarArray(
                                    secsVarString()
                                )),
                            )), 2)
                        )),
                        )), 3)

class secsS06F12(secsStreamFunction):
    stream = 6
    function = 12

    formatDescriptor = secsVarBinary(1)

class secsS07F00(secsStreamFunction):
    stream = 7
    function = 0

    formatDescriptor = None

class secsS07F01(secsStreamFunction):
    stream = 7
    function = 1

    formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("LENGTH", secsVarU4(1)),
                        )), 2)

class secsS07F02(secsStreamFunction):
    stream = 7
    function = 2

    formatDescriptor = secsVarBinary(1)

class secsS07F03(secsStreamFunction):
    stream = 7
    function = 3

    formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)

class secsS07F04(secsStreamFunction):
    stream = 7
    function = 4

    formatDescriptor = secsVarBinary(1)

class secsS07F05(secsStreamFunction):
    stream = 7
    function = 5

    formatDescriptor = secsVarString()

class secsS07F06(secsStreamFunction):
    stream = 7
    function = 6

    formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)

class secsS07F17(secsStreamFunction):
    stream = 7
    function = 17

    formatDescriptor = secsVarArray(secsVarString())

class secsS07F18(secsStreamFunction):
    stream = 7
    function = 18

    formatDescriptor = secsVarBinary(1)

class secsS07F19(secsStreamFunction):
    stream = 7
    function = 19

    formatDescriptor = None

class secsS07F20(secsStreamFunction):
    stream = 7
    function = 20

    formatDescriptor = secsVarArray(secsVarString())

class secsS09F00(secsStreamFunction):
    stream = 9
    function = 0

    formatDescriptor = None

class secsS09F01(secsStreamFunction):
    stream = 9
    function = 1

    formatDescriptor = secsVarBinary(10)

class secsS09F03(secsStreamFunction):
    stream = 9
    function = 3

    formatDescriptor = secsVarBinary(10)

class secsS09F05(secsStreamFunction):
    stream = 9
    function = 5

    formatDescriptor = secsVarBinary(10)

class secsS09F07(secsStreamFunction):
    stream = 9
    function = 7

    formatDescriptor = secsVarBinary(10)

class secsS09F09(secsStreamFunction):
    stream = 9
    function = 9

    formatDescriptor = secsVarBinary(10)

class secsS09F11(secsStreamFunction):
    stream = 9
    function = 11

    formatDescriptor = secsVarBinary(10)

class secsS09F13(secsStreamFunction):
    stream = 9
    function = 13

    formatDescriptor = secsVarList(OrderedDict((
                        ("MEXP", secsVarString(6)),
                        ("EDID", secsVarString(80)),
                        )), 2)

class secsS10F00(secsStreamFunction):
    stream = 10
    function = 0

    formatDescriptor = None

class secsS10F01(secsStreamFunction):
    stream = 10
    function = 1

    formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)

class secsS10F02(secsStreamFunction):
    stream = 10
    function = 2

    formatDescriptor = secsVarBinary(1)

class secsS10F03(secsStreamFunction):
    stream = 10
    function = 3

    formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)

class secsS10F04(secsStreamFunction):
    stream = 10
    function = 4

    formatDescriptor = secsVarBinary(10)

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

def secsDecode(packet, host=False):
    """Get object of decoded stream and function class, or None if no class is available.

    :param packet: packet to get object for
    :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
    :param host: decode packet comming from host
    :type host: boolean
    :return: matching stream and function object
    :rtype: secsSxFx object
    """
    if host:
        secsStreamsFunctions = secsStreamsFunctionsHost
    else:
        secsStreamsFunctions = secsStreamsFunctionsEquipment

    if not packet.header.stream in secsStreamsFunctions:
        logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
        return None
    else:
        if not packet.header.function in secsStreamsFunctions[packet.header.stream]:
            logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None
        else:
            function = secsStreamsFunctions[packet.header.stream][packet.header.function]()
            function.decode(packet.data)
            return function