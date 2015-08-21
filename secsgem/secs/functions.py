#####################################################################
# functions.py
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

from functionbase import SecsStreamFunction
from variables import SecsVarList, SecsVarArray, SecsVarString, SecsVarBinary, SecsVarI1, SecsVarI2, SecsVarI4,\
    SecsVarI8, SecsVarF4, SecsVarF8, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarBoolean, SecsVarDynamic


class SecsS00F00(SecsStreamFunction):
    """Secs stream and function class for stream 00, function 00 - hsms communication

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS00F00()
        S0F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 0
    _function = 0

    _formatDescriptor = None


class SecsS01F00(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 00 - abort transaction stream 1

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F00()
        S1F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 0

    _formatDescriptor = None


class SecsS01F01(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 01 - are you online - request

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F01()
        S1F1 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 1

    _formatDescriptor = None


class SecsS01F02E(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 02 - on line data (Equipment)

    **Structure**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F02E({"MDLN": "secsgem", "SOFTREV": "0.0.3"})
        S1F2 { [MDLN: A 'secsgem', SOFTREV: A '0.0.3'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 2

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MDLN", SecsVarString(20)),
        ("SOFTREV", SecsVarString(20)),
    )), 2)


class SecsS01F02H(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 02 - on line data (Host)

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F02H()
        S1F2 { [] }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 2

    _formatDescriptor = SecsVarList(OrderedDict(()), 0)


class SecsS01F03(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 03 - selected equipment status - request

    **Structure**::

        [
            SVID: U4[1]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F03([1, 6, 12])
        S1F3 { [U4 1, U4 6, U4 12] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 3

    _formatDescriptor = SecsVarArray(SecsVarU4(1))


class SecsS01F04(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 04 - selected equipment status - data

    **Structure**::

        [
            SV: various
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F04([secsgem.SecsVarU1(value=1), "text", secsgem.SecsVarU4(value=1337)])
        S1F4 { [U1 1, A 'text', U4 1337] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 4

    _formatDescriptor = SecsVarArray(SecsVarDynamic([]))


class SecsS01F11(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 11 - status variable namelist - request

    **Structure**::

        [
            SVID: U4[1]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F11([1, 1337])
        S1F11 { [U4 1, U4 1337] }

    An empty list will return all available status variables.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 11

    _formatDescriptor = SecsVarArray(SecsVarU4(1))


class SecsS01F12(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 12 - status variable namelist - reply

    **Structure**::

        [
            {
                SVID: U4[1]
                SVNAME: A[n]
                UNITS: A[n]
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"}, {"SVID": 1337, "SVNAME": "SV2", "UNITS": ""}])
        S1F12 { [[SVID: U4 1, SVNAME: A 'SV1', UNITS: A 'mm'], [SVID: U4 1337, SVNAME: A 'SV2', UNITS: A '']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 12

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("SVID", SecsVarU4(1)),
        ("SVNAME", SecsVarString()),
        ("UNITS", SecsVarString()),
    )), 3))


class SecsS01F13E(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 13 - establish communication - request (Equipment)

    **Structure**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F13E({"MDLN": "secsgem", "SOFTREV": "0.0.3"})
        S1F13 { [MDLN: A 'secsgem', SOFTREV: A '0.0.3'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MDLN", SecsVarString(20)),
        ("SOFTREV", SecsVarString(20)),
    )), 2)


class SecsS01F13H(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 13 - establish communication - request (Host)

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F13H()
        S1F13 { [] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict(()), 0)


class SecsS01F14E(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 14 - establish communication - acknowledge (Equipment)

    **Structure**::

        {
            COMMACK: B[1]
            DATA: {
                MDLN: A[20]
                SOFTREV: A[20]
            }
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F14E({"COMMACK": 1, "DATA": {"MDLN": "secsgem", "SOFTREV": "0.0.3"}})
        S1F14 { [COMMACK: B 1, DATA: [MDLN: A 'secsgem', SOFTREV: A '0.0.3']] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 14

    _formatDescriptor = SecsVarList(OrderedDict((
        ("COMMACK", SecsVarBinary(1)),
        ("DATA", SecsVarList(OrderedDict((
            ("MDLN", SecsVarString(20)),
            ("SOFTREV", SecsVarString(20)),
        )), 2))
    )), 2)


class SecsS01F14H(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 14 - establish communication - acknowledge (Host)

    **Structure**::

        {
            COMMACK: B[1]
            DATA: {
            }
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F14H({"COMMACK": 1, "DATA": {}})
        S1F14 { [COMMACK: B 1, DATA: []] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 14

    _formatDescriptor = SecsVarList(OrderedDict((
        ("COMMACK", SecsVarBinary(1)),
        ("DATA", SecsVarList(OrderedDict(()), 0))
    )), 2)


class SecsS02F00(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 00 - abort transaction stream 2

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F00()
        S2F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 2
    _function = 0

    _formatDescriptor = None


class SecsS02F13(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 13 - equipment constant - request

    **Structure**::

        [
            ECID: U4[1]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F13([1, 1337])
        S2F13 { [U4 1, U4 1337] }

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 13

    _formatDescriptor = SecsVarArray(SecsVarU4(1))


class SecsS02F14(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 14 - equipment constant - data

    **Structure**::

        [
            ECV: various
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F14([secsgem.SecsVarU1(value=1), "text"])
        S2F14 { [U1 1, A 'text'] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 14

    _formatDescriptor = SecsVarArray(SecsVarDynamic([SecsVarString,
                                                     SecsVarBinary,
                                                     SecsVarBoolean,
                                                     SecsVarU1,
                                                     SecsVarU2,
                                                     SecsVarU4,
                                                     SecsVarU8,
                                                     SecsVarF4,
                                                     SecsVarF8,
                                                     SecsVarI1,
                                                     SecsVarI2,
                                                     SecsVarI4,
                                                     SecsVarI8]))


class SecsS02F15(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 15 - new equipment constant - send

    **Structure**::

        [
            {
                ECID: U4[1]
                ECV: various
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F15([{"ECID": 1, "ECV": secsgem.SecsVarU4(value=10)}, {"ECID": 1337, "ECV": "text"}])
        S2F15 { [[ECID: U4 1, ECV: U4 10], [ECID: U4 1337, ECV: A 'text']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 15

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("ECID", SecsVarU4(1)),
        ("ECV", SecsVarDynamic([SecsVarString,
                                SecsVarBinary,
                                SecsVarBoolean,
                                SecsVarU1,
                                SecsVarU2,
                                SecsVarU4,
                                SecsVarU8,
                                SecsVarF4,
                                SecsVarF8,
                                SecsVarI1,
                                SecsVarI2,
                                SecsVarI4,
                                SecsVarI8])),
    )), 2))


class SecsS02F16(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 16 - new equipment constant - acknowledge

    **Structure**::

        EAC: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F16(1)
        S2F16 { B 1 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 16

    _formatDescriptor = SecsVarBinary(1)


class SecsS02F29(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 29 - equipment constant namelist - request

    **Structure**::

        [
            ECID: U4[1]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F29([1, 1337])
        S2F29 { [U4 1, U4 1337] }

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 29

    _formatDescriptor = SecsVarArray(SecsVarU4(1))


class SecsS02F30(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 30 - equipment constant namelist

    **Structure**::

        [
            {
                ECID: U4[1]
                ECNAME: A[n]
                ECMIN: various
                ECMAX: various
                ECDEF: various
                UNITS: A[n]
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F30([{"ECID": 1, "ECNAME": "EC1", "ECMIN": secsgem.SecsVarU1(value=0), "ECMAX": secsgem.SecsVarU1(value=100), "ECDEF": secsgem.SecsVarU1(value=50), "UNITS": "mm"}, {"ECID": 1337, "ECNAME": "EC2", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""}])
        S2F30 { [[ECID: U4 1, ECNAME: A 'EC1', ECMIN: U1 0, ECMAX: U1 100, ECDEF: U1 50, UNITS: A 'mm'], [ECID: U4 1337, ECNAME: A 'EC2', ECMIN: A '', ECMAX: A '', ECDEF: A '', UNITS: A '']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 30

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("ECID", SecsVarU4(1)),
        ("ECNAME", SecsVarString()),
        ("ECMIN", SecsVarDynamic([SecsVarString,
                                  SecsVarBinary,
                                  SecsVarBoolean,
                                  SecsVarU1,
                                  SecsVarU2,
                                  SecsVarU4,
                                  SecsVarU8,
                                  SecsVarF4,
                                  SecsVarF8,
                                  SecsVarI1,
                                  SecsVarI2,
                                  SecsVarI4,
                                  SecsVarI8])),
        ("ECMAX", SecsVarDynamic([SecsVarString,
                                  SecsVarBinary,
                                  SecsVarBoolean,
                                  SecsVarU1,
                                  SecsVarU2,
                                  SecsVarU4,
                                  SecsVarU8,
                                  SecsVarF4,
                                  SecsVarF8,
                                  SecsVarI1,
                                  SecsVarI2,
                                  SecsVarI4,
                                  SecsVarI8])),
        ("ECDEF", SecsVarDynamic([SecsVarString,
                                  SecsVarBinary,
                                  SecsVarBoolean,
                                  SecsVarU1,
                                  SecsVarU2,
                                  SecsVarU4,
                                  SecsVarU8,
                                  SecsVarF4,
                                  SecsVarF8,
                                  SecsVarI1,
                                  SecsVarI2,
                                  SecsVarI4,
                                  SecsVarI8])),
        ("UNITS", SecsVarString()),
    )), 6))


class SecsS02F33(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 33 - define report

    **Structure**::

        {
            DATAID: U4[1]
            DATA: [
                {
                    RPTID: U4[1]
                    RPT: [
                        VID: A[n]
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F33({"DATAID": 1, "DATA": [{"RPTID": 1000, "VID": [12, 1337]}, {"RPTID": 1001, "VID": [1, 2355]}]})
        S2F33 { [DATAID: U4 1, DATA: [[RPTID: U4 1000, VID: [A '12', A '1337']], [RPTID: U4 1001, VID: [A '1', A '2355']]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 33

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", SecsVarU4(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RPTID", SecsVarU4(1)),
                ("VID", SecsVarArray(
                    SecsVarString()
                )),
            )), 2)
        )),
    )), 2)


class SecsS02F34(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 34 - define report - acknowledge

    **Structure**::

        DRACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F34(0)
        S2F34 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 34

    _formatDescriptor = SecsVarBinary(1)


class SecsS02F35(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 35 - link event report

    **Structure**::

        {
            DATAID: U4[1]
            DATA: [
                {
                    CEID: U4[1]
                    RPTID: [
                        ID: U4[1]
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F35({"DATAID": 1, "DATA": [{"CEID": 1337, "RPTID": [1000, 1001]}]})
        S2F35 { [DATAID: U4 1, DATA: [[CEID: U4 1337, RPTID: [U4 1000, U4 1001]]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 35

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", SecsVarU4(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CEID", SecsVarU4(1)),
                ("RPTID", SecsVarArray(
                    SecsVarU4(1)
                )),
            )), 2)
        )),
    )), 2)


class SecsS02F36(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 36 - link event report - acknowledge

    **Structure**::

        LRACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F36(0)
        S2F36 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 36

    _formatDescriptor = SecsVarBinary(1)


class SecsS02F37(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 37 - en-/disable event report

    **Structure**::

        {
            CEED: BOOL[1]
            CEID: [
                ID: U4[1]
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F37({"CEED": True, "CEID": [1337]})
        S2F37 { [CEED: TF True, CEID: [U4 1337]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 37

    _formatDescriptor = SecsVarList(OrderedDict((
        ("CEED", SecsVarBoolean(1)),
        ("CEID", SecsVarArray(
            SecsVarU4(1)
        )),
    )), 2)


class SecsS02F38(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 38 - en-/disable event report - acknowledge

    **Structure**::

        ERACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F38(0)
        S2F38 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 38

    _formatDescriptor = SecsVarBinary(1)


class SecsS02F41(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 41 - host command - send

    **Structure**::

        {
            RCMD: A[n]
            PARAMS: [
                {
                    CPNAME: A[n]
                    CPVAL: A[n]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F41({"RCMD": "COMMAND", "PARAMS": [{"CPNAME": "PARAM1", "CPVAL": "VAL1"}, {"CPNAME": "PARAM2", "CPVAL": "VAL2"}]})
        S2F41 { [RCMD: A 'COMMAND', PARAMS: [[CPNAME: A 'PARAM1', CPVAL: A 'VAL1'], [CPNAME: A 'PARAM2', CPVAL: A 'VAL2']]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 41

    _formatDescriptor = SecsVarList(OrderedDict((
        ("RCMD", SecsVarString()),
        ("PARAMS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CPNAME", SecsVarString()),
                ("CPVAL", SecsVarString()),
            )), 2)
        )),
    )), 2)


class SecsS02F42(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 42 - host command - acknowledge

    **Structure**::

        {
            HCACK: B[1]
            PARAMS: [
                {
                    CPNAME: A[n]
                    CPACK: B[1]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F42({"HCACK": 1, "PARAMS": [{"CPNAME": "PARAM1", "CPACK": 2}, {"CPNAME": "PARAM2", "CPACK": 3}]})
        S2F42 { [HCACK: B 1, PARAMS: [[CPNAME: A 'PARAM1', CPACK: B 2], [CPNAME: A 'PARAM2', CPACK: B 3]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 42

    _formatDescriptor = SecsVarList(OrderedDict((
        ("HCACK", SecsVarBinary(1)),
        ("PARAMS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CPNAME", SecsVarString()),
                ("CPACK", SecsVarBinary(1)),
            )), 2)
        )),
    )), 2)


class SecsS05F00(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 00 - abort transaction stream 5

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F00()
        S5F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 5
    _function = 0

    _formatDescriptor = None


class SecsS05F01(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 01 - alarm report - send

    **Structure**::

        {
            ALCD: B[1]
            ALID: U4[1]
            ALTX: A[120]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F01({"ALCD": 1, "ALID": 100, "ALTX": "text"})
        S5F1 { [ALCD: B 1, ALID: U4 100, ALTX: A 'text'] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 5
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("ALCD", SecsVarBinary(1)),
        ("ALID", SecsVarU4(1)),
        ("ALTX", SecsVarString(120)),
    )), 3)


class SecsS05F02(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 02 - alarm report - acknowledge

    **Structure**::

        ACKC5: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F02(0)
        S5F02 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 5
    _function = 2

    _formatDescriptor = SecsVarBinary(1)


class SecsS06F00(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 00 - abort transaction stream 6

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F00()
        S6F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 6
    _function = 0

    _formatDescriptor = None


class SecsS06F11(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 11 - event report

    **Structure**::

        {
            DATAID: U4[1]
            CEID: U4[1]
            RPT: [
                {
                    RPTID: U4[1]
                    V: [
                        DATA: various
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F11({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": ["VAR", secsgem.SecsVarU4(value=100)]}]})
        S6F11 { [DATAID: U4 1, CEID: U4 1337, RPT: [[RPTID: U4 1000, V: [A 'VAR', U4 100]]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 11

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", SecsVarU4(1)),
        ("CEID", SecsVarU4(1)),
        ("RPT", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RPTID", SecsVarU4(1)),
                ("V", SecsVarArray(
                    SecsVarDynamic([])
                )),
            )), 2)
        )),
    )), 3)


class SecsS06F12(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 12 - event report - acknowledge

    **Structure**::

        ACKC6: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F12(0)
        S6F12 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 6
    _function = 12

    _formatDescriptor = SecsVarBinary(1)


class SecsS07F00(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 00 - abort transaction stream 7

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F00()
        S7F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 7
    _function = 0

    _formatDescriptor = None


class SecsS07F01(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 01 - process program load - inquire

    **Structure**::

        {
            PPID: A[n]
            LENGTH: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F01({"PPID": "program", "LENGTH": 4})
        S7F1 { [PPID: A 'program', LENGTH: U4 4] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("LENGTH", SecsVarU4(1)),
    )), 2)


class SecsS07F02(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 02 - process program load - grant

    **Structure**::

        PPGNT: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F02(0)
        S7F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 2

    _formatDescriptor = SecsVarBinary(1)


class SecsS07F03(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 03 - process program - send

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F03({"PPID": "program", "PPBODY": "data"})
        S7F3 { [PPID: A 'program', PPBODY: B <4 bytes>] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("PPBODY", SecsVarBinary()),
    )), 2)


class SecsS07F04(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 04 - process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F04(0)
        S7F4 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 4

    _formatDescriptor = SecsVarBinary(1)


class SecsS07F05(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 05 - process program - request

    **Structure**::

        PPID: A[n]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F05("program")
        S7F5 { A 'program' }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 5

    _formatDescriptor = SecsVarString()


class SecsS07F06(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 06 - process program - data

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F06({"PPID": "program", "PPBODY": "data"})
        S7F6 { [PPID: A 'program', PPBODY: B <4 bytes>] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 6

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("PPBODY", SecsVarBinary()),
    )), 2)


class SecsS07F17(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 17 - delete process program - send

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F17(["program1", "program2"])
        S7F17 { [A 'program1', A 'program2'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 17

    _formatDescriptor = SecsVarArray(SecsVarString())


class SecsS07F18(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 18 - delete process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F18(0)
        S7F18 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 18

    _formatDescriptor = SecsVarBinary(1)


class SecsS07F19(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 19 - current equipment process program - request

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F19()
        S7F19 { None }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 19

    _formatDescriptor = None


class SecsS07F20(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 20 - current equipment process program - data

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F20(["program1", "program2"])
        S7F20 { [A 'program1', A 'program2'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 20

    _formatDescriptor = SecsVarArray(SecsVarString())


class SecsS09F00(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 00 - abort transaction stream 9

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F00()
        S9F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 9
    _function = 0

    _formatDescriptor = None


class SecsS09F01(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 01 - unrecognized device id

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F01("HEADERDATA")
        S9F1 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 1

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F03(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 03 - unrecognized stream type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F03("HEADERDATA")
        S9F3 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 3

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F05(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 05 - unrecognized function type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F05("HEADERDATA")
        S9F5 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 5

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F07(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 07 - illegal data

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F07("HEADERDATA")
        S9F7 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 7

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F09(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 09 - transaction timer timeout

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F09("HEADERDATA")
        S9F9 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 9

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F11(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 11 - data too long

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F11("HEADERDATA")
        S9F11 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 11

    _formatDescriptor = SecsVarBinary(10)


class SecsS09F13(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 13 - conversation timeout

    **Structure**::

        {
            MEXP: A[6]
            EDID: A[80]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F13({"MEXP": "S01E01", "EDID": "data"})
        S9F13 { [MEXP: A 'S01E01', EDID: A 'data'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 9
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MEXP", SecsVarString(6)),
        ("EDID", SecsVarString(80)),
    )), 2)


class SecsS10F00(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 00 - abort transaction stream 10

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F00()
        S10F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 10
    _function = 0

    _formatDescriptor = None


class SecsS10F01(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 01 - terminal - request

    **Structure**::

        {
            TID: B[1]
            TEXT: A[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F01({"TID": 0, "TEXT": "hello?"})
        S10F1 { [TID: B 0, TEXT: A 'hello?'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("TID", SecsVarBinary(1)),
        ("TEXT", SecsVarString()),
    )), 2)


class SecsS10F02(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 02 - terminal - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F02(0)
        S10F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 2

    _formatDescriptor = SecsVarBinary(1)


class SecsS10F03(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 03 - terminal single - display

    **Structure**::

        {
            TID: B[1]
            TEXT: A[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F03({"TID": 0, "TEXT": "hello!"})
        S10F3 { [TID: B 0, TEXT: A 'hello!'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("TID", SecsVarBinary(1)),
        ("TEXT", SecsVarString()),
    )), 2)


class SecsS10F04(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 04 - terminal single - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F04(0)
        S10F4 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 4

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F00(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 00 - abort transaction stream 12

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F00()
        S12F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 12
    _function = 0

    _formatDescriptor = None


class SecsS12F01(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 01 - map setup data - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            FNLOC: U2[1]
            FFROT: U2[1]
            ORLOC: B[1]
            RPSEL: U1[1]
            REF: [
                REFP: I4[2]
                ...
            ]
            DUTMS: A[n]
            XDIES: U4[1]
            YDIES: U4[1]
            ROWCT: U4[1]
            COLCT: U4[1]
            NULBC: A[n]
            PRDCT: U4[1]
            PRAXI: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F01({"MID": "materialID",
                "IDTYP": 0,
                "FNLOC": 0,
                "FFROT": 0,
                "ORLOC": 0,
                "RPSEL": 0,
                "REF": [[1,2], [2,3]],
                "DUTMS": "unit",
                "XDIES": 100,
                "YDIES": 100,
                "ROWCT": 10,
                "COLCT": 10,
                "NULBC": "{x}",
                "PRDCT": 100,
                "PRAXI": 0,
                })
        S12F1 { [MID: A 'materialID', IDTYP: B 0, FNLOC: U2 0, FFROT: U2 0, ORLOC: B 0, RPSEL: U1 0, REF: [I4 [1, 2], I4 [2, 3]], DUTMS: A 'unit', XDIES: U4 100, YDIES: U4 100, ROWCT: U4 10, COLCT: U4 10, NULBC: A '{x}', PRDCT: U4 100, PRAXI: B 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("FFROT", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("RPSEL", SecsVarU1(1)),
        ("REF", SecsVarArray(
            SecsVarI4(2)
        )),
        ("DUTMS", SecsVarString()),
        ("XDIES", SecsVarU4(1)),
        ("YDIES", SecsVarU4(1)),
        ("ROWCT", SecsVarU4(1)),
        ("COLCT", SecsVarU4(1)),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
        ("PRDCT", SecsVarU4(1)),
        ("PRAXI", SecsVarBinary(1)),
    )), 15)


class SecsS12F02(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 02 - map setup data - acknowledge

    **Structure**::

        SDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F02(0)
        S12F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 2

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F03(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 03 - map setup data - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            MAPFT: B[1]
            FNLOC: U2[1]
            FFROT: U2[1]
            ORLOC: B[1]
            PRAXI: B[1]
            BCEQU: U1[n]
            NULBC: A[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F03({"MID": "materialID",
                "IDTYP": 0,
                "MAPFT": 0,
                "FNLOC": 0,
                "FFROT": 0,
                "ORLOC": 0,
                "PRAXI": 0,
                "BCEQU": [1, 3, 5, 7],
                "NULBC": "{x}",
                })
        S12F3 { [MID: A 'materialID', IDTYP: B 0, MAPFT: B 0, FNLOC: U2 0, FFROT: U2 0, ORLOC: B 0, PRAXI: B 0, BCEQU: U1 [1, 3, 5, 7], NULBC: A '{x}'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("MAPFT", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("FFROT", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("PRAXI", SecsVarBinary(1)),
        ("BCEQU", SecsVarU1()),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
    )), 9)


class SecsS12F04(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 04 - map setup data

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            FNLOC: U2[1]
            ORLOC: B[1]
            RPSEL: U1[1]
            REF: [
                REFP: I4[2]
                ...
            ]
            DUTMS: A[n]
            XDIES: U4[1]
            YDIES: U4[1]
            ROWCT: U4[1]
            COLCT: U4[1]
            PRDCT: U4[1]
            BCEQU: U1[n]
            NULBC: A[n]
            MLCL: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F04({"MID": "materialID",
                "IDTYP": 0,
                "FNLOC": 0,
                "ORLOC": 0,
                "RPSEL": 0,
                "REF": [[1,2], [2,3]],
                "DUTMS": "unit",
                "XDIES": 100,
                "YDIES": 100,
                "ROWCT": 10,
                "COLCT": 10,
                "PRDCT": 100,
                "BCEQU": [1, 3, 5, 7],
                "NULBC": "{x}",
                "MLCL": 0,
                })
        S12F4 { [MID: A 'materialID', IDTYP: B 0, FNLOC: U2 0, ORLOC: B 0, RPSEL: U1 0, REF: [I4 [1, 2], I4 [2, 3]], DUTMS: A 'unit', XDIES: U4 100, YDIES: U4 100, ROWCT: U4 10, COLCT: U4 10, PRDCT: U4 100, BCEQU: U1 [1, 3, 5, 7], NULBC: A '{x}', MLCL: U4 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 4

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("RPSEL", SecsVarU1(1)),
        ("REF", SecsVarArray(
            SecsVarI4(2)
        )),
        ("DUTMS", SecsVarString()),
        ("XDIES", SecsVarU4(1)),
        ("YDIES", SecsVarU4(1)),
        ("ROWCT", SecsVarU4(1)),
        ("COLCT", SecsVarU4(1)),
        ("PRDCT", SecsVarU4(1)),
        ("BCEQU", SecsVarU1()),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
        ("MLCL", SecsVarU4(1)),
    )), 15)


class SecsS12F05(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 05 - map transmit inquire

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            MAPFT: B[1]
            MLCL: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F05({"MID": "materialID", "IDTYP": 0, "MAPFT": 0, "MLCL": 0})
        S12F5 { [MID: A 'materialID', IDTYP: B 0, MAPFT: B 0, MLCL: U4 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 5

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("MAPFT", SecsVarBinary(1)),
        ("MLCL", SecsVarU4(1)),
    )), 4)


class SecsS12F06(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 06 - map transmit - grant

    **Structure**::

        GRNT1: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F06(0)
        S12F6 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 6

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F07(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 07 - map data type 1 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    RSINF: I4[3]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F07({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F7 { [MID: A 'materialID', IDTYP: B 0, DATA: [[RSINF: I4 [1, 2, 3], BINLT: U1 [1, 2, 3, 4]], [RSINF: I4 [4, 5, 6], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 7

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RSINF", SecsVarI4(3)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)


class SecsS12F08(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 08 - map data type 1 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F08(0)
        S12F8 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 8

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F09(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 09 - map data type 2 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F09({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F9 { [MID: A 'materialID', IDTYP: B 0, STRP: I2 [0, 1], BINLT: U2 [1, 2, 3, 4, 5, 6]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 9

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("STRP", SecsVarI2(2)),
        ("BINLT", SecsVarU1()),
    )), 4)


class SecsS12F10(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 10 - map data type 2 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F10(0)
        S12F10 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 10

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F11(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 11 - map data type 3 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    XYPOS: I2[2]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F11({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F11 { [MID: A 'materialID', IDTYP: B 0, DATA: [[XYPOS: I2 [1, 2], BINLT: U1 [1, 2, 3, 4]], [XYPOS: I2 [3, 4], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 11

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("XYPOS", SecsVarI2(2)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)


class SecsS12F12(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 12 - map data type 3 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F12(0)
        S12F12 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 12

    _formatDescriptor = SecsVarBinary(1)


class SecsS12F13(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 13 - map data type 1 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F13({"MID": "materialID", "IDTYP": 0})
        S12F13 { [MID: A 'materialID', IDTYP: B 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
    )), 2)


class SecsS12F14(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 14 - map data type 1

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    RSINF: I4[3]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F14({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F14 { [MID: A 'materialID', IDTYP: B 0, DATA: [[RSINF: I4 [1, 2, 3], BINLT: U1 [1, 2, 3, 4]], [RSINF: I4 [4, 5, 6], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 14

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RSINF", SecsVarI4(3)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)


class SecsS12F15(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 15 - map data type 2 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F15({"MID": "materialID", "IDTYP": 0})
        S12F15 { [MID: A 'materialID', IDTYP: B 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 15

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
    )), 2)


class SecsS12F16(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 16 - map data type 2

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F16({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F16 { [MID: A 'materialID', IDTYP: B 0, STRP: I2 [0, 1], BINLT: U2 [1, 2, 3, 4, 5, 6]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 16

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("STRP", SecsVarI2(2)),
        ("BINLT", SecsVarU1()),
    )), 4)


class SecsS12F17(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 17 - map data type 3 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            SDBIN: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F17({"MID": "materialID", "IDTYP": 0, "SDBIN": 1})
        S12F17 { [MID: A 'materialID', IDTYP: B 0, SDBIN: B 1] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 17

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("SDBIN", SecsVarBinary(1)),
    )), 3)


class SecsS12F18(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 18 - map data type 3

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    XYPOS: I2[2]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F18({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F18 { [MID: A 'materialID', IDTYP: B 0, DATA: [[XYPOS: I2 [1, 2], BINLT: U1 [1, 2, 3, 4]], [XYPOS: I2 [3, 4], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 18

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("XYPOS", SecsVarI2(2)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)


class SecsS12F19(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 19 - map error report - send

    **Structure**::

        {
            MAPER: B[1]
            DATLC: U1[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F19({"MAPER": 1, "DATLC": 0})
        S12F19 { [MAPER: B 1, DATLC: U1 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 19

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MAPER", SecsVarBinary(1)),
        ("DATLC", SecsVarU1(1)),
    )), 2)


secsStreamsFunctionsHost = {
    0: {
        0: SecsS00F00,
    },
    1: {
        0: SecsS01F00,
        1: SecsS01F01,
        2: SecsS01F02H,
        3: SecsS01F03,
        4: SecsS01F04,
        11: SecsS01F11,
        12: SecsS01F12,
        13: SecsS01F13H,
        14: SecsS01F14H,
    },
    2: {
        0: SecsS02F00,
        13: SecsS02F13,
        14: SecsS02F14,
        15: SecsS02F15,
        16: SecsS02F16,
        29: SecsS02F29,
        30: SecsS02F30,
        33: SecsS02F33,
        34: SecsS02F34,
        35: SecsS02F35,
        36: SecsS02F36,
        37: SecsS02F37,
        38: SecsS02F38,
        41: SecsS02F41,
        42: SecsS02F42,
    },
    5: {
        0: SecsS05F00,
        1: SecsS05F01,
        2: SecsS05F02,
    },
    6: {
        0: SecsS06F00,
        11: SecsS06F11,
        12: SecsS06F12,
    },
    7: {
        1: SecsS07F01,
        2: SecsS07F02,
        3: SecsS07F03,
        4: SecsS07F04,
        5: SecsS07F05,
        6: SecsS07F06,
        17: SecsS07F17,
        18: SecsS07F18,
        19: SecsS07F19,
        20: SecsS07F20,
    },
    9: {
        0: SecsS09F00,
        1: SecsS09F01,
        3: SecsS09F03,
        5: SecsS09F05,
        7: SecsS09F07,
        9: SecsS09F09,
        11: SecsS09F11,
        13: SecsS09F13,
    },
    10: {
        0: SecsS10F00,
        1: SecsS10F01,
        2: SecsS10F02,
        3: SecsS10F03,
        4: SecsS10F04,
    },
    12: {
        0: SecsS12F00,
        1: SecsS12F01,
        2: SecsS12F02,
        3: SecsS12F03,
        4: SecsS12F04,
        5: SecsS12F05,
        6: SecsS12F06,
        7: SecsS12F07,
        8: SecsS12F08,
        9: SecsS12F09,
        10: SecsS12F10,
        11: SecsS12F11,
        12: SecsS12F12,
        13: SecsS12F13,
        14: SecsS12F14,
        15: SecsS12F15,
        16: SecsS12F16,
        17: SecsS12F17,
        18: SecsS12F18,
        19: SecsS12F19,
    },
}

secsStreamsFunctionsEquipment = {
    0: {
        0: SecsS00F00,
    },
    1: {
        0: SecsS01F00,
        1: SecsS01F01,
        2: SecsS01F02E,
        3: SecsS01F03,
        4: SecsS01F04,
        11: SecsS01F11,
        12: SecsS01F12,
        13: SecsS01F13E,
        14: SecsS01F14E,
    },
    2: {
        0: SecsS02F00,
        13: SecsS02F13,
        14: SecsS02F14,
        15: SecsS02F15,
        16: SecsS02F16,
        29: SecsS02F29,
        30: SecsS02F30,
        33: SecsS02F33,
        34: SecsS02F34,
        35: SecsS02F35,
        36: SecsS02F36,
        37: SecsS02F37,
        38: SecsS02F38,
        41: SecsS02F41,
        42: SecsS02F42,
    },
    5: {
        0: SecsS05F00,
        1: SecsS05F01,
        2: SecsS05F02,
    },
    6: {
        0: SecsS06F00,
        11: SecsS06F11,
        12: SecsS06F12,
    },
    7: {
        1: SecsS07F01,
        2: SecsS07F02,
        3: SecsS07F03,
        4: SecsS07F04,
        5: SecsS07F05,
        6: SecsS07F06,
        17: SecsS07F17,
        18: SecsS07F18,
        19: SecsS07F19,
        20: SecsS07F20,
    },
    9: {
        0: SecsS09F00,
        1: SecsS09F01,
        3: SecsS09F03,
        5: SecsS09F05,
        7: SecsS09F07,
        9: SecsS09F09,
        11: SecsS09F11,
        13: SecsS09F13,
    },
    10: {
        0: SecsS10F00,
        1: SecsS10F01,
        2: SecsS10F02,
        3: SecsS10F03,
        4: SecsS10F04,
    },
    12: {
        0: SecsS12F00,
        1: SecsS12F01,
        2: SecsS12F02,
        3: SecsS12F03,
        4: SecsS12F04,
        5: SecsS12F05,
        6: SecsS12F06,
        7: SecsS12F07,
        8: SecsS12F08,
        9: SecsS12F09,
        10: SecsS12F10,
        11: SecsS12F11,
        12: SecsS12F12,
        13: SecsS12F13,
        14: SecsS12F14,
        15: SecsS12F15,
        16: SecsS12F16,
        17: SecsS12F17,
        18: SecsS12F18,
        19: SecsS12F19,
    },
}
