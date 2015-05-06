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
from secsVariables import secsVarList, secsVarArray, secsVarString, secsVarBinary, secsVarI2, secsVarI4, secsVarU1, secsVarU2, secsVarU4, secsVarBoolean, secsVarDynamic


class secsS00F00(secsStreamFunction):
    """Secs stream and function class for stream 00, function 00 - hsms communication

    **Example**::

        >>> secsgem.secsS00F00()
        S0F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 0
    _function = 0

    _formatDescriptor = None


class secsS01F00(secsStreamFunction):
    """Secs stream and function class for stream 01, function 00 - abort transaction stream 1

    **Example**::

        >>> secsgem.secsS01F00()
        S1F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 0

    _formatDescriptor = None


class secsS01F01(secsStreamFunction):
    """Secs stream and function class for stream 01, function 01 - are you online - request

    **Example**::

        >>> secsgem.secsS01F01()
        S1F1 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 1

    _formatDescriptor = None


class secsS01F02E(secsStreamFunction):
    """Secs stream and function class for stream 01, function 02 - on line data (Equipment)

    **Structure**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> secsgem.secsS01F02E({"MDLN": "secsgem", "SOFTREV": "0.0.3"})
        S1F2 { [MDLN: A 'secsgem', SOFTREV: A '0.0.3'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 2

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)


class secsS01F02H(secsStreamFunction):
    """Secs stream and function class for stream 01, function 02 - on line data (Host)

    **Example**::

        >>> secsgem.secsS01F02H()
        S1F2 { [] }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 2

    _formatDescriptor = secsVarList({}, 0)


class secsS01F03(secsStreamFunction):
    """Secs stream and function class for stream 01, function 03 - selected equipment status - request

    **Structure**::

        [
            SVID: U4[1]
            ...
        ]

    **Example**::

        >>> secsgem.secsS01F03([1, 6, 12])
        S1F3 { [U4 1, U4 6, U4 12] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 3

    _formatDescriptor = secsVarArray(secsVarU4(1))


class secsS01F04(secsStreamFunction):
    """Secs stream and function class for stream 01, function 04 - selected equipment status - data

    **Structure**::

        [
            SV: various
            ...
        ]

    **Example**::

        >>> secsgem.secsS01F04([secsgem.secsVarU1(value=1), "text", secsgem.secsVarU4(value=1337)])
        S1F4 { [U1 1, A 'text', U4 1337] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 4

    _formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))


class secsS01F11(secsStreamFunction):
    """Secs stream and function class for stream 01, function 11 - status variable namelist - request

    **Structure**::

        [
            SVID: U4[1]
            ...
        ]

    **Example**::

        >>> secsgem.secsS01F11([1, 1337])
        S1F11 { [U4 1, U4 1337] }

    An empty list will return all available status variables.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 11

    _formatDescriptor = secsVarArray(secsVarU4(1))


class secsS01F12(secsStreamFunction):
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

        >>> secsgem.secsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"}, {"SVID": 1337, "SVNAME": "SV2", "UNITS": ""}])
        S1F12 { [[SVID: U4 1, SVNAME: A 'SV1', UNITS: A 'mm'], [SVID: U4 1337, SVNAME: A 'SV2', UNITS: A '']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 12

    _formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("SVID", secsVarU4(1)),
                        ("SVNAME", secsVarString()),
                        ("UNITS", secsVarString()),
                        )), 3))


class secsS01F13E(secsStreamFunction):
    """Secs stream and function class for stream 01, function 13 - establish communication - request (Equipment)

    **Structure**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> secsgem.secsS01F13E({"MDLN": "secsgem", "SOFTREV": "0.0.3"})
        S1F13 { [MDLN: A 'secsgem', SOFTREV: A '0.0.3'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 13

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MDLN", secsVarString(20)),
                        ("SOFTREV", secsVarString(20)),
                        )), 2)


class secsS01F13H(secsStreamFunction):
    """Secs stream and function class for stream 01, function 13 - establish communication - request (Host)

    **Example**::

        >>> secsgem.secsS01F13H()
        S1F13 { [] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 13

    _formatDescriptor = secsVarList({}, 0)


class secsS01F14E(secsStreamFunction):
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

        >>> secsgem.secsS01F14E({"COMMACK": 1, "DATA": {"MDLN": "secsgem", "SOFTREV": "0.0.3"}})
        S1F14 { [COMMACK: B 1, DATA: [MDLN: A 'secsgem', SOFTREV: A '0.0.3']] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
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
    """Secs stream and function class for stream 01, function 14 - establish communication - acknowledge (Host)

    **Structure**::

        {
            COMMACK: B[1]
            DATA: {
            }
        }

    **Example**::

        >>> secsgem.secsS01F14H({"COMMACK": 1, "DATA": {}})
        S1F14 { [COMMACK: B 1, DATA: []] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 14

    _formatDescriptor = secsVarList(OrderedDict((
                            ("COMMACK", secsVarBinary(1)),
                            ("DATA", secsVarList([], 0))
                        )), 2)


class secsS02F00(secsStreamFunction):
    """Secs stream and function class for stream 02, function 00 - abort transaction stream 2

    **Example**::

        >>> secsgem.secsS02F00()
        S2F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 2
    _function = 0

    _formatDescriptor = None


class secsS02F13(secsStreamFunction):
    """Secs stream and function class for stream 02, function 13 - equipment constant - request

    **Structure**::

        [
            ECID: U4[1]
            ...
        ]

    **Example**::

        >>> secsgem.secsS02F13([1, 1337])
        S2F13 { [U4 1, U4 1337] }

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 13

    _formatDescriptor = secsVarArray(secsVarU4(1))


class secsS02F14(secsStreamFunction):
    """Secs stream and function class for stream 02, function 14 - equipment constant - data

    **Structure**::

        [
            ECV: various
            ...
        ]

    **Example**::

        >>> secsgem.secsS02F14([secsgem.secsVarU1(value=1), "text"])
        S2F14 { [U1 1, A 'text'] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 14

    _formatDescriptor = secsVarArray(secsVarDynamic(secsVarString))


class secsS02F15(secsStreamFunction):
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

        >>> secsgem.secsS02F15([{"ECID": 1, "ECV": secsgem.secsVarU4(value=10)}, {"ECID": 1337, "ECV": "text"}])
        S2F15 { [[ECID: U4 1, ECV: U4 10], [ECID: U4 1337, ECV: A 'text']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 15

    _formatDescriptor = secsVarArray(secsVarList(OrderedDict((
                        ("ECID", secsVarU4(1)),
                        ("ECV", secsVarDynamic(secsVarString)),
                        )), 2))


class secsS02F16(secsStreamFunction):
    """Secs stream and function class for stream 02, function 16 - new equipment constant - acknowledge

    **Structure**::

        EAC: B[1]

    **Example**::

        >>> secsgem.secsS02F16(1)
        S2F16 { B 1 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 16

    _formatDescriptor = secsVarBinary(1)


class secsS02F29(secsStreamFunction):
    """Secs stream and function class for stream 02, function 29 - equipment constant namelist - request

    **Structure**::

        [
            ECID: U4[1]
            ...
        ]

    **Example**::

        >>> secsgem.secsS02F29([1, 1337])
        S2F29 { [U4 1, U4 1337] }

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 29

    _formatDescriptor = secsVarArray(secsVarU4(1))


class secsS02F30(secsStreamFunction):
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

        >>> secsgem.secsS02F30([{"ECID": 1, "ECNAME": "EC1", "ECMIN": secsgem.secsVarU1(value=0), "ECMAX": secsgem.secsVarU1(value=100), "ECDEF": secsgem.secsVarU1(value=50), "UNITS": "mm"}, {"ECID": 1337, "ECNAME": "EC2", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""}])
        S2F30 { [[ECID: U4 1, ECNAME: A 'EC1', ECMIN: U1 0, ECMAX: U1 100, ECDEF: U1 50, UNITS: A 'mm'], [ECID: U4 1337, ECNAME: A 'EC2', ECMIN: A '', ECMAX: A '', ECDEF: A '', UNITS: A '']] }

    :param value: parameters for this function (see example)
    :type value: list
    """
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

        >>> secsgem.secsS02F33({"DATAID": 1, "DATA": [{"RPTID": 1000, "VID": [12, 1337]}, {"RPTID": 1001, "VID": [1, 2355]}]})
        S2F33 { [DATAID: U4 1, DATA: [[RPTID: U4 1000, VID: [A '12', A '1337']], [RPTID: U4 1001, VID: [A '1', A '2355']]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 33

    _formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("DATA", secsVarArray(
                            secsVarList(OrderedDict((
                                ("RPTID", secsVarU4(1)),
                                ("VID", secsVarArray(
                                    secsVarString()
                                )),
                            )), 2)
                        )),
                        )), 2)


class secsS02F34(secsStreamFunction):
    """Secs stream and function class for stream 02, function 34 - define report - acknowledge

    **Structure**::

        DRACK: B[1]

    **Example**::

        >>> secsgem.secsS02F34(0)
        S2F34 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 34

    _formatDescriptor = secsVarBinary(1)


class secsS02F35(secsStreamFunction):
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

        >>> secsgem.secsS02F35({"DATAID": 1, "DATA": [{"CEID": 1337, "RPTID": [1000, 1001]}]})
        S2F35 { [DATAID: U4 1, DATA: [[CEID: U4 1337, RPTID: [U4 1000, U4 1001]]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 35

    _formatDescriptor = secsVarList(OrderedDict((
                        ("DATAID", secsVarU4(1)),
                        ("DATA", secsVarArray(
                            secsVarList(OrderedDict((
                                ("CEID", secsVarU4(1)),
                                ("RPTID", secsVarArray(
                                    secsVarU4(1)
                                )),
                            )), 2)
                        )),
                        )), 2)


class secsS02F36(secsStreamFunction):
    """Secs stream and function class for stream 02, function 36 - link event report - acknowledge

    **Structure**::

        LRACK: B[1]

    **Example**::

        >>> secsgem.secsS02F36(0)
        S2F36 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 36

    _formatDescriptor = secsVarBinary(1)


class secsS02F37(secsStreamFunction):
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

        >>> secsgem.secsS02F37({"CEED": True, "CEID": [1337]})
        S2F37 { [CEED: TF True, CEID: [U4 1337]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 37

    _formatDescriptor = secsVarList(OrderedDict((
                        ("CEED", secsVarBoolean(1)),
                        ("CEID", secsVarArray(
                            secsVarU4(1)
                        )),
                        )), 2)


class secsS02F38(secsStreamFunction):
    """Secs stream and function class for stream 02, function 38 - en-/disable event report - acknowledge

    **Structure**::

        ERACK: B[1]

    **Example**::

        >>> secsgem.secsS02F38(0)
        S2F38 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 38

    _formatDescriptor = secsVarBinary(1)


class secsS02F41(secsStreamFunction):
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

        >>> secsgem.secsS02F41({"RCMD": "COMMAND", "PARAMS": [{"CPNAME": "PARAM1", "CPVAL": "VAL1"}, {"CPNAME": "PARAM2", "CPVAL": "VAL2"}]})
        S2F41 { [RCMD: A 'COMMAND', PARAMS: [[CPNAME: A 'PARAM1', CPVAL: A 'VAL1'], [CPNAME: A 'PARAM2', CPVAL: A 'VAL2']]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
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

        >>> secsgem.secsS02F42({"HCACK": 1, "PARAMS": [{"CPNAME": "PARAM1", "CPACK": 2}, {"CPNAME": "PARAM2", "CPACK": 3}]})
        S2F42 { [HCACK: B 1, PARAMS: [[CPNAME: A 'PARAM1', CPACK: B 2], [CPNAME: A 'PARAM2', CPACK: B 3]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
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
    """Secs stream and function class for stream 05, function 00 - abort transaction stream 5

    **Example**::

        >>> secsgem.secsS05F00()
        S5F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 5
    _function = 0

    _formatDescriptor = None


class secsS05F01(secsStreamFunction):
    """Secs stream and function class for stream 05, function 01 - alarm report - send

    **Structure**::

        {
            ALCD: B[1]
            ALID: U4[1]
            ALTX: A[120]
        }

    **Example**::

        >>> secsgem.secsS05F01({"ALCD": 1, "ALID": 100, "ALTX": "text"})
        S5F1 { [ALCD: B 1, ALID: U4 100, ALTX: A 'text'] }

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 5
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("ALCD", secsVarBinary(1)),
                        ("ALID", secsVarU4(1)),
                        ("ALTX", secsVarString(120)),
                        )), 3)


class secsS05F02(secsStreamFunction):
    """Secs stream and function class for stream 05, function 02 - alarm report - acknowledge

    **Structure**::

        ACKC5: B[1]

    **Example**::

        >>> secsgem.secsS05F02(0)
        S5F02 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 5
    _function = 2

    _formatDescriptor = secsVarBinary(1)


class secsS06F00(secsStreamFunction):
    """Secs stream and function class for stream 06, function 00 - abort transaction stream 6

    **Example**::

        >>> secsgem.secsS06F00()
        S6F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 6
    _function = 0

    _formatDescriptor = None


class secsS06F11(secsStreamFunction):
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

        >>> secsgem.secsS06F11({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": ["VAR", secsgem.secsVarU4(value=100)]}]})
        S6F11 { [DATAID: U4 1, CEID: U4 1337, RPT: [[RPTID: U4 1000, V: [A 'VAR', U4 100]]]] }

    :param value: parameters for this function (see example)
    :type value: list
    """
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
    """Secs stream and function class for stream 06, function 12 - event report - acknowledge

    **Structure**::

        ACKC6: B[1]

    **Example**::

        >>> secsgem.secsS06F12(0)
        S6F12 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 6
    _function = 12

    _formatDescriptor = secsVarBinary(1)


class secsS07F00(secsStreamFunction):
    """Secs stream and function class for stream 07, function 00 - abort transaction stream 7

    **Example**::

        >>> secsgem.secsS07F00()
        S7F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 7
    _function = 0

    _formatDescriptor = None


class secsS07F01(secsStreamFunction):
    """Secs stream and function class for stream 07, function 01 - process program load - inquire

    **Structure**::

        {
            PPID: A[n]
            LENGTH: U4[1]
        }

    **Example**::

        >>> secsgem.secsS07F01({"PPID": "program", "LENGTH": 4})
        S7F1 { [PPID: A 'program', LENGTH: U4 4] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("LENGTH", secsVarU4(1)),
                        )), 2)


class secsS07F02(secsStreamFunction):
    """Secs stream and function class for stream 07, function 02 - process program load - grant

    **Structure**::

        PPGNT: B[1]

    **Example**::

        >>> secsgem.secsS07F02(0)
        S7F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 2

    _formatDescriptor = secsVarBinary(1)


class secsS07F03(secsStreamFunction):
    """Secs stream and function class for stream 07, function 03 - process program - send

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> secsgem.secsS07F03({"PPID": "program", "PPBODY": "data"})
        S7F3 { [PPID: A 'program', PPBODY: B <4 bytes>] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 3

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)


class secsS07F04(secsStreamFunction):
    """Secs stream and function class for stream 07, function 04 - process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> secsgem.secsS07F04(0)
        S7F4 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 4

    _formatDescriptor = secsVarBinary(1)


class secsS07F05(secsStreamFunction):
    """Secs stream and function class for stream 07, function 05 - process program - request

    **Structure**::

        PPID: A[n]

    **Example**::

        >>> secsgem.secsS07F05("program")
        S7F5 { A 'program' }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 5

    _formatDescriptor = secsVarString()


class secsS07F06(secsStreamFunction):
    """Secs stream and function class for stream 07, function 06 - process program - data

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> secsgem.secsS07F06({"PPID": "program", "PPBODY": "data"})
        S7F6 { [PPID: A 'program', PPBODY: B <4 bytes>] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 6

    _formatDescriptor = secsVarList(OrderedDict((
                        ("PPID", secsVarString()),
                        ("PPBODY", secsVarBinary()),
                        )), 2)


class secsS07F17(secsStreamFunction):
    """Secs stream and function class for stream 07, function 17 - delete process program - send

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> secsgem.secsS07F17(["program1", "program2"])
        S7F17 { [A 'program1', A 'program2'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 17

    _formatDescriptor = secsVarArray(secsVarString())


class secsS07F18(secsStreamFunction):
    """Secs stream and function class for stream 07, function 18 - delete process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> secsgem.secsS07F18(0)
        S7F18 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 18

    _formatDescriptor = secsVarBinary(1)


class secsS07F19(secsStreamFunction):
    """Secs stream and function class for stream 07, function 19 - current equipment process program - request

    **Example**::

        >>> secsgem.secsS07F19()
        S7F19 { None }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 19

    _formatDescriptor = None


class secsS07F20(secsStreamFunction):
    """Secs stream and function class for stream 07, function 20 - current equipment process program - data

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> secsgem.secsS07F20(["program1", "program2"])
        S7F20 { [A 'program1', A 'program2'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 20

    _formatDescriptor = secsVarArray(secsVarString())


class secsS09F00(secsStreamFunction):
    """Secs stream and function class for stream 09, function 00 - abort transaction stream 9

    **Example**::

        >>> secsgem.secsS09F00()
        S9F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 9
    _function = 0

    _formatDescriptor = None


class secsS09F01(secsStreamFunction):
    """Secs stream and function class for stream 09, function 01 - unrecognized device id

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F01("HEADERDATA")
        S9F1 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 1

    _formatDescriptor = secsVarBinary(10)


class secsS09F03(secsStreamFunction):
    """Secs stream and function class for stream 09, function 03 - unrecognized stream type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F03("HEADERDATA")
        S9F3 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 3

    _formatDescriptor = secsVarBinary(10)


class secsS09F05(secsStreamFunction):
    """Secs stream and function class for stream 09, function 05 - unrecognized function type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F05("HEADERDATA")
        S9F5 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 5

    _formatDescriptor = secsVarBinary(10)


class secsS09F07(secsStreamFunction):
    """Secs stream and function class for stream 09, function 07 - illegal data

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F07("HEADERDATA")
        S9F7 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 7

    _formatDescriptor = secsVarBinary(10)


class secsS09F09(secsStreamFunction):
    """Secs stream and function class for stream 09, function 09 - transaction timer timeout

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F09("HEADERDATA")
        S9F9 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 9

    _formatDescriptor = secsVarBinary(10)


class secsS09F11(secsStreamFunction):
    """Secs stream and function class for stream 09, function 11 - data too long

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> secsgem.secsS09F11("HEADERDATA")
        S9F11 { B <10 bytes> }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 11

    _formatDescriptor = secsVarBinary(10)


class secsS09F13(secsStreamFunction):
    """Secs stream and function class for stream 09, function 13 - conversation timeout

    **Structure**::

        {
            MEXP: A[6]
            EDID: A[80]
        }

    **Example**::

        >>> secsgem.secsS09F13({"MEXP": "S01E01", "EDID": "data"})
        S9F13 { [MEXP: A 'S01E01', EDID: A 'data'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 9
    _function = 13

    _formatDescriptor = secsVarList(OrderedDict((
                        ("MEXP", secsVarString(6)),
                        ("EDID", secsVarString(80)),
                        )), 2)


class secsS10F00(secsStreamFunction):
    """Secs stream and function class for stream 10, function 00 - abort transaction stream 10

    **Example**::

        >>> secsgem.secsS10F00()
        S10F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 10
    _function = 0

    _formatDescriptor = None


class secsS10F01(secsStreamFunction):
    """Secs stream and function class for stream 10, function 01 - terminal - request

    **Structure**::

        {
            TID: B[1]
            TEXT: A[120]
        }

    **Example**::

        >>> secsgem.secsS10F01({"TID": 0, "TEXT": "hello?"})
        S10F1 { [TID: B 0, TEXT: A 'hello?'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 1

    _formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)


class secsS10F02(secsStreamFunction):
    """Secs stream and function class for stream 10, function 02 - terminal - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> secsgem.secsS10F02(0)
        S10F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 2

    _formatDescriptor = secsVarBinary(1)


class secsS10F03(secsStreamFunction):
    """Secs stream and function class for stream 10, function 03 - terminal single - display

    **Structure**::

        {
            TID: B[1]
            TEXT: A[120]
        }

    **Example**::

        >>> secsgem.secsS10F03({"TID": 0, "TEXT": "hello!"})
        S10F3 { [TID: B 0, TEXT: A 'hello!'] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 3

    _formatDescriptor = secsVarList(OrderedDict((
                        ("TID", secsVarBinary(1)),
                        ("TEXT", secsVarString(120)),
                        )), 2)


class secsS10F04(secsStreamFunction):
    """Secs stream and function class for stream 10, function 04 - terminal single - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> secsgem.secsS10F04(0)
        S10F4 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 4

    _formatDescriptor = secsVarBinary(1)


class secsS12F00(secsStreamFunction):
    """Secs stream and function class for stream 12, function 00 - abort transaction stream 12

    **Example**::

        >>> secsgem.secsS12F00()
        S12F0 { None }

    :param value: function has no parameters
    :type value: None
    """
    _stream = 12
    _function = 0

    _formatDescriptor = None


class secsS12F01(secsStreamFunction):
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

        >>> secsgem.secsS12F01({"MID": "materialID",
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

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("FNLOC", secsVarU2(1)),
                            ("FFROT", secsVarU2(1)),
                            ("ORLOC", secsVarBinary(1)),
                            ("RPSEL", secsVarU1(1)),
                            ("REF", secsVarArray(
                                secsVarI4(2)
                            )),
                            ("DUTMS", secsVarString()),
                            ("XDIES", secsVarU4(1)),
                            ("YDIES", secsVarU4(1)),
                            ("ROWCT", secsVarU4(1)),
                            ("COLCT", secsVarU4(1)),
                            ("NULBC", secsVarDynamic(secsVarU1)),
                            ("PRDCT", secsVarU4(1)),
                            ("PRAXI", secsVarBinary(1)),
                        )), 15)


class secsS12F02(secsStreamFunction):
    """Secs stream and function class for stream 12, function 02 - map setup data - acknowledge

    **Structure**::

        SDACK: B[1]

    **Example**::

        >>> secsgem.secsS12F02(0)
        S12F2 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 2

    _formatDescriptor = secsVarBinary(1)


class secsS12F03(secsStreamFunction):
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

        >>> secsgem.secsS12F03({"MID": "materialID",
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

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("MAPFT", secsVarBinary(1)),
                            ("FNLOC", secsVarU2(1)),
                            ("FFROT", secsVarU2(1)),
                            ("ORLOC", secsVarBinary(1)),
                            ("PRAXI", secsVarBinary(1)),
                            ("BCEQU", secsVarU1()),
                            ("NULBC", secsVarDynamic(secsVarU1)),
                        )), 9)


class secsS12F04(secsStreamFunction):
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

        >>> secsgem.secsS12F04({"MID": "materialID",
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

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("FNLOC", secsVarU2(1)),
                            ("ORLOC", secsVarBinary(1)),
                            ("RPSEL", secsVarU1(1)),
                            ("REF", secsVarArray(
                                secsVarI4(2)
                            )),
                            ("DUTMS", secsVarString()),
                            ("XDIES", secsVarU4(1)),
                            ("YDIES", secsVarU4(1)),
                            ("ROWCT", secsVarU4(1)),
                            ("COLCT", secsVarU4(1)),
                            ("PRDCT", secsVarU4(1)),
                            ("BCEQU", secsVarU1()),
                            ("NULBC", secsVarDynamic(secsVarU1)),
                            ("MLCL", secsVarU4(1)),
                        )), 15)


class secsS12F05(secsStreamFunction):
    """Secs stream and function class for stream 12, function 05 - map transmit inquire

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            MAPFT: B[1]
            MLCL: U4[1]
        }

    **Example**::

        >>> secsgem.secsS12F05({"MID": "materialID", "IDTYP": 0, "MAPFT": 0, "MLCL": 0})
        S12F5 { [MID: A 'materialID', IDTYP: B 0, MAPFT: B 0, MLCL: U4 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 5

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("MAPFT", secsVarBinary(1)),
                            ("MLCL", secsVarU4(1)),
                        )), 4)


class secsS12F06(secsStreamFunction):
    """Secs stream and function class for stream 12, function 06 - map transmit - grant

    **Structure**::

        GRNT1: B[1]

    **Example**::

        >>> secsgem.secsS12F06(0)
        S12F6 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 6

    _formatDescriptor = secsVarBinary(1)


class secsS12F07(secsStreamFunction):
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

        >>> secsgem.secsS12F07({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F7 { [MID: A 'materialID', IDTYP: B 0, DATA: [[RSINF: I4 [1, 2, 3], BINLT: U1 [1, 2, 3, 4]], [RSINF: I4 [4, 5, 6], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 7

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("DATA", secsVarArray(
                                secsVarList(OrderedDict((
                                    ("RSINF", secsVarI4(3)),
                                    ("BINLT", secsVarU1()),
                                )), 2)
                            )),
                        )), 3)


class secsS12F08(secsStreamFunction):
    """Secs stream and function class for stream 12, function 08 - map data type 1 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> secsgem.secsS12F08(0)
        S12F8 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 8

    _formatDescriptor = secsVarBinary(1)


class secsS12F09(secsStreamFunction):
    """Secs stream and function class for stream 12, function 09 - map data type 2 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> secsgem.secsS12F09({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F9 { [MID: A 'materialID', IDTYP: B 0, STRP: I2 [0, 1], BINLT: U2 [1, 2, 3, 4, 5, 6]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 9

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("STRP", secsVarI2(2)),
                            ("BINLT", secsVarU1()),
                        )), 4)


class secsS12F10(secsStreamFunction):
    """Secs stream and function class for stream 12, function 10 - map data type 2 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> secsgem.secsS12F10(0)
        S12F10 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 10

    _formatDescriptor = secsVarBinary(1)


class secsS12F11(secsStreamFunction):
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

        >>> secsgem.secsS12F11({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F11 { [MID: A 'materialID', IDTYP: B 0, DATA: [[XYPOS: I2 [1, 2], BINLT: U1 [1, 2, 3, 4]], [XYPOS: I2 [3, 4], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 11

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("DATA", secsVarArray(
                                secsVarList(OrderedDict((
                                    ("XYPOS", secsVarI2(2)),
                                    ("BINLT", secsVarU1()),
                                )), 2)
                            )),
                        )), 3)


class secsS12F12(secsStreamFunction):
    """Secs stream and function class for stream 12, function 12 - map data type 3 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> secsgem.secsS12F12(0)
        S12F12 { B 0 }

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 12

    _formatDescriptor = secsVarBinary(1)


class secsS12F13(secsStreamFunction):
    """Secs stream and function class for stream 12, function 13 - map data type 1 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> secsgem.secsS12F13({"MID": "materialID", "IDTYP": 0})
        S12F13 { [MID: A 'materialID', IDTYP: B 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 13

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                        )), 2)


class secsS12F14(secsStreamFunction):
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

        >>> secsgem.secsS12F14({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F14 { [MID: A 'materialID', IDTYP: B 0, DATA: [[RSINF: I4 [1, 2, 3], BINLT: U1 [1, 2, 3, 4]], [RSINF: I4 [4, 5, 6], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 14

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("DATA", secsVarArray(
                                secsVarList(OrderedDict((
                                    ("RSINF", secsVarI4(3)),
                                    ("BINLT", secsVarU1()),
                                )), 2)
                            )),
                        )), 3)


class secsS12F15(secsStreamFunction):
    """Secs stream and function class for stream 12, function 15 - map data type 2 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> secsgem.secsS12F15({"MID": "materialID", "IDTYP": 0})
        S12F15 { [MID: A 'materialID', IDTYP: B 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 15

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                        )), 2)


class secsS12F16(secsStreamFunction):
    """Secs stream and function class for stream 12, function 16 - map data type 2

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> secsgem.secsS12F16({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F16 { [MID: A 'materialID', IDTYP: B 0, STRP: I2 [0, 1], BINLT: U2 [1, 2, 3, 4, 5, 6]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 16

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("STRP", secsVarI2(2)),
                            ("BINLT", secsVarU1()),
                        )), 4)


class secsS12F17(secsStreamFunction):
    """Secs stream and function class for stream 12, function 17 - map data type 3 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            SDBIN: B[1]
        }

    **Example**::

        >>> secsgem.secsS12F17({"MID": "materialID", "IDTYP": 0, "SDBIN": 1})
        S12F17 { [MID: A 'materialID', IDTYP: B 0, SDBIN: B 1] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 17

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("SDBIN", secsVarBinary(1)),
                        )), 3)


class secsS12F18(secsStreamFunction):
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

        >>> secsgem.secsS12F18({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F18 { [MID: A 'materialID', IDTYP: B 0, DATA: [[XYPOS: I2 [1, 2], BINLT: U1 [1, 2, 3, 4]], [XYPOS: I2 [3, 4], BINLT: U1 [5, 6, 7, 8]]]] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 18

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MID", secsVarString(16)),
                            ("IDTYP", secsVarBinary(1)),
                            ("DATA", secsVarArray(
                                secsVarList(OrderedDict((
                                    ("XYPOS", secsVarI2(2)),
                                    ("BINLT", secsVarU1()),
                                )), 2)
                            )),
                        )), 3)


class secsS12F19(secsStreamFunction):
    """Secs stream and function class for stream 12, function 19 - map error report - send

    **Structure**::

        {
            MAPER: B[1]
            DATLC: U1[1]
        }

    **Example**::

        >>> secsgem.secsS12F19({"MAPER": 1, "DATLC": 0})
        S12F19 { [MAPER: B 1, DATLC: U1 0] }

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 19

    _formatDescriptor = secsVarList(OrderedDict((
                            ("MAPER", secsVarBinary(1)),
                            ("DATLC", secsVarU1(1)),
                        )), 2)

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
    12:    {
        0: secsS12F00,
        1: secsS12F01,
        2: secsS12F02,
        3: secsS12F03,
        4: secsS12F04,
        5: secsS12F05,
        6: secsS12F06,
        7: secsS12F07,
        8: secsS12F08,
        9: secsS12F09,
        10: secsS12F10,
        11: secsS12F11,
        12: secsS12F12,
        13: secsS12F13,
        14: secsS12F14,
        15: secsS12F15,
        16: secsS12F16,
        17: secsS12F17,
        18: secsS12F18,
        19: secsS12F19,
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
    12:    {
        0: secsS12F00,
        1: secsS12F01,
        2: secsS12F02,
        3: secsS12F03,
        4: secsS12F04,
        5: secsS12F05,
        6: secsS12F06,
        7: secsS12F07,
        8: secsS12F08,
        9: secsS12F09,
        10: secsS12F10,
        11: secsS12F11,
        12: secsS12F12,
        13: secsS12F13,
        14: secsS12F14,
        15: secsS12F15,
        16: secsS12F16,
        17: secsS12F17,
        18: secsS12F18,
        19: secsS12F19,
        },
}
