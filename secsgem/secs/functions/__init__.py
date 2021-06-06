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
"""Wrappers for SECS stream and functions."""

from ..functionbase import SecsStreamFunction
from ..data_items import MDLN, SVID, SV, SVNAME, UNITS, COMMACK, OFLACK, ONLACK, ECID, ECV, EAC, TIME, ECNAME, ECMIN, \
    ECMAX, ECDEF, DATAID, RPTID, VID, DRACK, CEID, LRACK, CEED, ERACK, RCMD, CPNAME, CPVAL, HCACK, CPACK, ALCD, ALID, \
    ALTX, ACKC5, ALED, TIMESTAMP, EXID, EXTYPE, EXMESSAGE, EXRECVRA, ACKA, ERRCODE, ERRTEXT, DATALENGTH, GRANT6, DSID, \
    DVNAME, DVVAL, V, ACKC6, PPID, LENGTH, PPGNT, PPBODY, ACKC7, MHEAD, SHEAD, MEXP, EDID, TID, TEXT, ACKC10, MID, \
    IDTYP, FNLOC, FFROT, ORLOC, RPSEL, REFP, DUTMS, XDIES, YDIES, ROWCT, COLCT, NULBC, PRDCT, PRAXI, SDACK, MAPFT, \
    BCEQU, MLCL, GRNT1, RSINF, BINLT, MDACK, STRP, XYPOS, SDBIN, MAPER, DATLC, OBJSPEC, OBJTYPE, OBJID, ATTRID, \
    ATTRDATA, ATTRRELN, OBJACK


class SecsS00F00(SecsStreamFunction):
    """
    Hsms communication.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS00F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS00F00()
        S0F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 0
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS01F00(SecsStreamFunction):
    """
    abort transaction stream 1.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F00()
        S1F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 1
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS01F01(SecsStreamFunction):
    """
    are you online - request.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F01
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F01()
        S1F1 W .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 1
    _function = 1

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F02(SecsStreamFunction):
    """
    on line data.

    .. caution::

        This Stream/function has different structures depending on the source.
        If it is sent from the eqipment side it has the structure below, if it
        is sent from the host it is an empty list.
        Be sure to fill the array accordingly.

    **Structure E->H**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F02(['secsgem', '0.0.6']) # E->H
        S1F2
          <L [2]
            <A "secsgem">
            <A "0.0.6">
          > .
        >>> secsgem.secs.functions.SecsS01F02() #H->E
        S1F2
          <L> .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 2

    _data_format = [MDLN]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS01F03(SecsStreamFunction):
    """
    Selected equipment status - request.

    **Data Items**

    - :class:`SVID <secsgem.secs.data_items.SVID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F03
        [
            SVID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F03([1, "1337", 12])
        S1F3 W
          <L [3]
            <U1 1 >
            <A "1337">
            <U1 12 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 3

    _data_format = [SVID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F04(SecsStreamFunction):
    """
    selected equipment status - data.

    **Data Items**

    - :class:`SV <secsgem.secs.data_items.SV>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F04
        [
            SV: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F04([secsgem.secs.variables.U1(1), "text", secsgem.secs.variables.U4(1337)])
        S1F4
          <L [3]
            <U1 1 >
            <A "text">
            <U4 1337 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 4

    _data_format = [SV]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS01F11(SecsStreamFunction):
    """
    status variable namelist - request.

    **Data Items**

    - :class:`SVID <secsgem.secs.data_items.SVID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F11
        [
            SVID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F11([1, 1337])
        S1F11 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    An empty list will return all available status variables.

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 11

    _data_format = [SVID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F12(SecsStreamFunction):
    """
    status variable namelist - reply.

    **Data Items**

    - :class:`SVID <secsgem.secs.data_items.SVID>`
    - :class:`SVNAME <secsgem.secs.data_items.SVNAME>`
    - :class:`UNITS <secsgem.secs.data_items.UNITS>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F12
        [
            {
                SVID: U1/U2/U4/U8/I1/I2/I4/I8/A
                SVNAME: A
                UNITS: A
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"},
        ...     {"SVID": 1337, "SVNAME": "SV2", "UNITS": ""}])
        S1F12
          <L [2]
            <L [3]
              <U1 1 >
              <A "SV1">
              <A "mm">
            >
            <L [3]
              <U2 1337 >
              <A "SV2">
              <A>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 12

    _data_format = [
        [
            SVID,
            SVNAME,
            UNITS
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS01F13(SecsStreamFunction):
    """
    establish communication - request.

    .. caution::

        This Stream/function has different structures depending on the source.
        If it is sent from the eqipment side it has the structure below,
        if it is sent from the host it is an empty list.
        Be sure to fill the array accordingly.

    **Structure E->H**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F13(['secsgem', '0.0.6']) # E->H
        S1F13 W
          <L [2]
            <A "secsgem">
            <A "0.0.6">
          > .
        >>> secsgem.secs.functions.SecsS01F13() #H->E
        S1F13 W
          <L> .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 1
    _function = 13

    _data_format = [MDLN]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F14(SecsStreamFunction):
    """
    establish communication - acknowledge.

    .. caution::

        This Stream/function has different structures depending on the source.
        See structure definition below for details.
        Be sure to fill the array accordingly.

    **Data Items**

    - :class:`COMMACK <secsgem.secs.data_items.COMMACK>`

    **Structure E->H**::

        {
            COMMACK: B[1]
            DATA: {
                MDLN: A[20]
                SOFTREV: A[20]
            }
        }

    **Structure H->E**::

        {
            COMMACK: B[1]
            DATA: []
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F14({"COMMACK": secsgem.secs.data_items.COMMACK.ACCEPTED, \
                                               "MDLN": ["secsgem", "0.0.6"]})
        S1F14
          <L [2]
            <B 0x0>
            <L [2]
              <A "secsgem">
              <A "0.0.6">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 1
    _function = 14

    _data_format = [
        COMMACK,
        [MDLN]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS01F15(SecsStreamFunction):
    """
    request offline.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F15
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F15()
        S1F15 W .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 1
    _function = 15

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F16(SecsStreamFunction):
    """
    offline acknowledge.

    **Data Items**

    - :class:`OFLACK <secsgem.secs.data_items.OFLACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F16
        OFLACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F16(secsgem.secs.data_items.OFLACK.ACK)
        S1F16
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 1
    _function = 16

    _data_format = OFLACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS01F17(SecsStreamFunction):
    """
    request online.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F17
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F17()
        S1F17 W .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 1
    _function = 17

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS01F18(SecsStreamFunction):
    """
    online acknowledge.

    **Data Items**

    - :class:`ONLACK <secsgem.secs.data_items.ONLACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F18
        ONLACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F18(secsgem.secs.data_items.ONLACK.ALREADY_ON)
        S1F18
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 1
    _function = 18

    _data_format = ONLACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F00(SecsStreamFunction):
    """
    abort transaction stream 2.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F00()
        S2F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 2
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F13(SecsStreamFunction):
    """
    equipment constant - request.

    **Data Items**

    - :class:`ECID <secsgem.secs.data_items.ECID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F13
        [
            ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F13([1, 1337])
        S2F13 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 13

    _data_format = [ECID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F14(SecsStreamFunction):
    """
    equipment constant - data.

    **Data Items**

    - :class:`ECV <secsgem.secs.data_items.ECV>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F14
        [
            ECV: L/BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F14([secsgem.secs.variables.U1(1), "text"])
        S2F14
          <L [2]
            <U1 1 >
            <A "text">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 14

    _data_format = [ECV]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS02F15(SecsStreamFunction):
    """
    new equipment constant - send.

    **Data Items**

    - :class:`ECID <secsgem.secs.data_items.ECID>`
    - :class:`ECV <secsgem.secs.data_items.ECV>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F15
        [
            {
                ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
                ECV: L/BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F15([ \
                {"ECID": 1, "ECV": secsgem.secs.variables.U4(10)}, \
                {"ECID": "1337", "ECV": "text"}])
        S2F15 W
          <L [2]
            <L [2]
              <U1 1 >
              <U4 10 >
            >
            <L [2]
              <A "1337">
              <A "text">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 15

    _data_format = [
        [
            ECID,
            ECV
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F16(SecsStreamFunction):
    """
    new equipment constant - acknowledge.

    **Data Items**

    - :class:`EAC <secsgem.secs.data_items.EAC>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F16
        EAC: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F16(secsgem.secs.data_items.EAC.BUSY)
        S2F16
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 2
    _function = 16

    _data_format = EAC

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F17(SecsStreamFunction):
    """
    date and time - request.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F17
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F17()
        S2F17 W .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 2
    _function = 17

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F18(SecsStreamFunction):
    """
    date and time - data.

    **Data Items**

    - :class:`TIME <secsgem.secs.data_items.TIME>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F18
        TIME: A[32]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F18("160816205942")
        S2F18
          <A "160816205942"> .

    :param value: parameters for this function (see example)
    :type value: ASCII string
    """

    _stream = 2
    _function = 18

    _data_format = TIME

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F29(SecsStreamFunction):
    """
    equipment constant namelist - request.

    **Data Items**

    - :class:`ECID <secsgem.secs.data_items.ECID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F29
        [
            ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F29([1, 1337])
        S2F29 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 29

    _data_format = [ECID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F30(SecsStreamFunction):
    """
    equipment constant namelist.

    **Data Items**

    - :class:`ECID <secsgem.secs.data_items.ECID>`
    - :class:`ECNAME <secsgem.secs.data_items.ECNAME>`
    - :class:`ECMIN <secsgem.secs.data_items.ECMIN>`
    - :class:`ECMAX <secsgem.secs.data_items.ECMAX>`
    - :class:`ECDEF <secsgem.secs.data_items.ECDEF>`
    - :class:`UNITS <secsgem.secs.data_items.UNITS>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F30
        [
            {
                ECID: U1/U2/U4/U8/I1/I2/I4/I8/A
                ECNAME: A
                ECMIN: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
                ECMAX: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
                ECDEF: BOOLEAN/I8/I1/I2/I4/F8/F4/U8/U1/U2/U4/A/B
                UNITS: A
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F30([ \
            {"ECID": 1, \
             "ECNAME": "EC1", \
             "ECMIN": secsgem.secs.variables.U1(0), \
             "ECMAX": secsgem.secs.variables.U1(100), \
             "ECDEF": secsgem.secs.variables.U1(50), \
             "UNITS": "mm"}, \
            {"ECID": 1337, \
             "ECNAME": "EC2", \
             "ECMIN": "", \
             "ECMAX": "", \
             "ECDEF": "", \
             "UNITS": ""}])
        S2F30
          <L [2]
            <L [6]
              <U1 1 >
              <A "EC1">
              <U1 0 >
              <U1 100 >
              <U1 50 >
              <A "mm">
            >
            <L [6]
              <U2 1337 >
              <A "EC2">
              <A>
              <A>
              <A>
              <A>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 30

    _data_format = [
        [
            ECID,
            ECNAME,
            ECMIN,
            ECMAX,
            ECDEF,
            UNITS
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS02F33(SecsStreamFunction):
    """
    define report.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`RPTID <secsgem.secs.data_items.RPTID>`
    - :class:`VID <secsgem.secs.data_items.VID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F33
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATA: [
                {
                    RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    VID: [
                        DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F33({"DATAID": 1, "DATA": [{"RPTID": 1000, "VID": [12, 1337]}, \
{"RPTID": 1001, "VID": [1, 2355]}]})
        S2F33 W
          <L [2]
            <U1 1 >
            <L [2]
              <L [2]
                <U2 1000 >
                <L [2]
                  <U1 12 >
                  <U2 1337 >
                >
              >
              <L [2]
                <U2 1001 >
                <L [2]
                  <U1 1 >
                  <U2 2355 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

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


class SecsS02F34(SecsStreamFunction):
    """
    define report - acknowledge.

    **Data Items**

    - :class:`DRACK <secsgem.secs.data_items.DRACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F34
        DRACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F34(secsgem.secs.data_items.DRACK.INVALID_FORMAT)
        S2F34
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 2
    _function = 34

    _data_format = DRACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F35(SecsStreamFunction):
    """
    link event report.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`
    - :class:`RPTID <secsgem.secs.data_items.RPTID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F35
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATA: [
                {
                    CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    RPTID: [
                        DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F35({"DATAID": 1, "DATA": [{"CEID": 1337, "RPTID": [1000, 1001]}]})
        S2F35 W
          <L [2]
            <U1 1 >
            <L [1]
              <L [2]
                <U2 1337 >
                <L [2]
                  <U2 1000 >
                  <U2 1001 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 35

    _data_format = [
        DATAID,
        [
            [
                CEID,
                [RPTID]
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS02F36(SecsStreamFunction):
    """
    link event report - acknowledge.

    **Data Items**

    - :class:`LRACK <secsgem.secs.data_items.LRACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F36
        LRACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F36(secsgem.secs.data_items.LRACK.CEID_UNKNOWN)
        S2F36
          <B 0x4> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 2
    _function = 36

    _data_format = LRACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F37(SecsStreamFunction):
    """
    en-/disable event report.

    **Data Items**

    - :class:`CEED <secsgem.secs.data_items.CEED>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F37
        {
            CEED: BOOLEAN[1]
            CEID: [
                DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F37({"CEED": True, "CEID": [1337]})
        S2F37 W
          <L [2]
            <BOOLEAN True >
            <L [1]
              <U2 1337 >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 37

    _data_format = [
        CEED,
        [CEID]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F38(SecsStreamFunction):
    """
    en-/disable event report - acknowledge.

    **Data Items**

    - :class:`ERACK <secsgem.secs.data_items.ERACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F38
        ERACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F38(secsgem.secs.data_items.ERACK.CEID_UNKNOWN)
        S2F38
          <B 0x1> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 2
    _function = 38

    _data_format = ERACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS02F41(SecsStreamFunction):
    """
    host command - send.

    **Data Items**

    - :class:`RCMD <secsgem.secs.data_items.RCMD>`
    - :class:`CPNAME <secsgem.secs.data_items.CPNAME>`
    - :class:`CPVAL <secsgem.secs.data_items.CPVAL>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F41
        {
            RCMD: U1/I1/A
            PARAMS: [
                {
                    CPNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                    CPVAL: BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/A/B
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F41({"RCMD": "COMMAND", "PARAMS": [{"CPNAME": "PARAM1", "CPVAL": "VAL1"}, \
{"CPNAME": "PARAM2", "CPVAL": "VAL2"}]})
        S2F41 W
          <L [2]
            <A "COMMAND">
            <L [2]
              <L [2]
                <A "PARAM1">
                <A "VAL1">
              >
              <L [2]
                <A "PARAM2">
                <A "VAL2">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 41

    _data_format = [
        RCMD,
        [
            [
                "PARAMS",   # name of the list
                CPNAME,
                CPVAL
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS02F42(SecsStreamFunction):
    """
    host command - acknowledge.

    **Data Items**

    - :class:`HCACK <secsgem.secs.data_items.HCACK>`
    - :class:`CPNAME <secsgem.secs.data_items.CPNAME>`
    - :class:`CPACK <secsgem.secs.data_items.CPACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F42
        {
            HCACK: B[1]
            PARAMS: [
                {
                    CPNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                    CPACK: B[1]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS02F42({ \
            "HCACK": secsgem.secs.data_items.HCACK.INVALID_COMMAND, \
            "PARAMS": [ \
                {"CPNAME": "PARAM1", "CPACK": secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_VALUE}, \
                {"CPNAME": "PARAM2", "CPACK": secsgem.secs.data_items.CPACK.CPVAL_ILLEGAL_FORMAT}]})
        S2F42
          <L [2]
            <B 0x1>
            <L [2]
              <L [2]
                <A "PARAM1">
                <B 0x2>
              >
              <L [2]
                <A "PARAM2">
                <B 0x3>
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 42

    _data_format = [
        HCACK,
        [
            [
                "PARAMS",   # name of the list
                CPNAME,
                CPACK
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F00(SecsStreamFunction):
    """
    abort transaction stream 5.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F00()
        S5F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 5
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F01(SecsStreamFunction):
    """
    alarm report - send.

    **Data Items**

    - :class:`ALCD <secsgem.secs.data_items.ALCD>`
    - :class:`ALID <secsgem.secs.data_items.ALID>`
    - :class:`ALTX <secsgem.secs.data_items.ALTX>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F01
        {
            ALCD: B[1]
            ALID: U1/U2/U4/U8/I1/I2/I4/I8
            ALTX: A[120]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F01({"ALCD": secsgem.secs.data_items.ALCD.PERSONAL_SAFETY | \
                                                       secsgem.secs.data_items.ALCD.ALARM_SET, \
                                               "ALID": 100, \
                                               "ALTX": "text"})
        S5F1
          <L [3]
            <B 0x81>
            <U1 100 >
            <A "text">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 1

    _data_format = [
        ALCD,
        ALID,
        ALTX
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F02(SecsStreamFunction):
    """
    alarm report - acknowledge.

    **Data Items**

    - :class:`ACKC5 <secsgem.secs.data_items.ACKC5>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F02
        ACKC5: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F02(secsgem.secs.data_items.ACKC5.ACCEPTED)
        S5F2
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 5
    _function = 2

    _data_format = ACKC5

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F03(SecsStreamFunction):
    """
    en-/disable alarm - send.

    **Data Items**

    - :class:`ALED <secsgem.secs.data_items.ALED>`
    - :class:`ALID <secsgem.secs.data_items.ALID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F03
        {
            ALED: B[1]
            ALID: U1/U2/U4/U8/I1/I2/I4/I8
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F03({"ALED": secsgem.secs.data_items.ALED.ENABLE, "ALID": 100})
        S5F3
          <L [2]
            <B 0x80>
            <U1 100 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 3

    _data_format = [
        ALED,
        ALID
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F04(SecsStreamFunction):
    """
    en-/disable alarm - acknowledge.

    **Data Items**

    - :class:`ACKC5 <secsgem.secs.data_items.ACKC5>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F04
        ACKC5: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F04(secsgem.secs.data_items.ACKC5.ACCEPTED)
        S5F4
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 5
    _function = 4

    _data_format = ACKC5

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F05(SecsStreamFunction):
    """
    list alarms - request.

    **Data Items**

    - :class:`ALID <secsgem.secs.data_items.ALID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F05
        [
            ALID: U1/U2/U4/U8/I1/I2/I4/I8
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F05([100, 200])
        S5F5 W
          <L [2]
            <U1 100 >
            <U1 200 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 5

    _data_format = [ALID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS05F06(SecsStreamFunction):
    """
    list alarms - data.

    **Data Items**

    - :class:`ALCD <secsgem.secs.data_items.ALCD>`
    - :class:`ALID <secsgem.secs.data_items.ALID>`
    - :class:`ALTX <secsgem.secs.data_items.ALTX>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F06
        [
            {
                ALCD: B[1]
                ALID: U1/U2/U4/U8/I1/I2/I4/I8
                ALTX: A[120]
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F06([{"ALCD": secsgem.secs.data_items.ALCD.PERSONAL_SAFETY | \
                                                        secsgem.secs.data_items.ALCD.ALARM_SET, \
                                                "ALID": 100, \
                                                "ALTX": "text"}])
        S5F6
          <L [1]
            <L [3]
              <B 0x81>
              <U1 100 >
              <A "text">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 6

    _data_format = [[
        ALCD,
        ALID,
        ALTX
    ]]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS05F07(SecsStreamFunction):
    """
    list enabled alarms - request.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F07
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F07()
        S5F7 W .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 7

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS05F08(SecsStreamFunction):
    """
    list enabled alarms - data.

    **Data Items**

    - :class:`ALCD <secsgem.secs.data_items.ALCD>`
    - :class:`ALID <secsgem.secs.data_items.ALID>`
    - :class:`ALTX <secsgem.secs.data_items.ALTX>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F08
        [
            {
                ALCD: B[1]
                ALID: U1/U2/U4/U8/I1/I2/I4/I8
                ALTX: A[120]
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F08([{"ALCD": secsgem.secs.data_items.ALCD.PERSONAL_SAFETY | \
                                                        secsgem.secs.data_items.ALCD.ALARM_SET, \
                                                "ALID": 100, \
                                                "ALTX": "text"}])
        S5F8
          <L [1]
            <L [3]
              <B 0x81>
              <U1 100 >
              <A "text">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 8

    _data_format = [[
        ALCD,
        ALID,
        ALTX
    ]]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS05F09(SecsStreamFunction):
    """
    exception post - notify.

    **Data Items**

    - :class:`TIMESTAMP <secsgem.secs.data_items.TIMESTAMP>`
    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`EXTYPE <secsgem.secs.data_items.EXTYPE>`
    - :class:`EXMESSAGE <secsgem.secs.data_items.EXMESSAGE>`
    - :class:`EXRECVRA <secsgem.secs.data_items.EXRECVRA>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F09
        {
            TIMESTAMP: A[32]
            EXID: A[20]
            EXTYPE: A
            EXMESSAGE: A
            EXRECVRA: [
                DATA: A[40]
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F09({ \
            "TIMESTAMP": "161006221500", \
            "EXID": "EX123", \
            "EXTYPE": "ALARM", \
            "EXMESSAGE": "Exception", \
            "EXRECVRA": ["EXRECVRA1", "EXRECVRA2"] })
        S5F9
          <L [5]
            <A "161006221500">
            <A "EX123">
            <A "ALARM">
            <A "Exception">
            <L [2]
              <A "EXRECVRA1">
              <A "EXRECVRA2">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 9

    _data_format = [
        TIMESTAMP,
        EXID,
        EXTYPE,
        EXMESSAGE,
        [EXRECVRA]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F10(SecsStreamFunction):
    """
    exception post - confirm.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F10
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F10()
        S5F10 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 5
    _function = 10

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F11(SecsStreamFunction):
    """
    exception clear - notify.

    **Data Items**

    - :class:`TIMESTAMP <secsgem.secs.data_items.TIMESTAMP>`
    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`EXTYPE <secsgem.secs.data_items.EXTYPE>`
    - :class:`EXMESSAGE <secsgem.secs.data_items.EXMESSAGE>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F11
        {
            TIMESTAMP: A[32]
            EXID: A[20]
            EXTYPE: A
            EXMESSAGE: A
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F11({"TIMESTAMP": "161006221500", "EXID": "EX123", "EXTYPE": "ALARM", \
"EXMESSAGE": "Exception"})
        S5F11
          <L [4]
            <A "161006221500">
            <A "EX123">
            <A "ALARM">
            <A "Exception">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 11

    _data_format = [
        TIMESTAMP,
        EXID,
        EXTYPE,
        EXMESSAGE,
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F12(SecsStreamFunction):
    """
    exception clear - confirm.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F12
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F12()
        S5F12 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 5
    _function = 12

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F13(SecsStreamFunction):
    """
    exception recover - request.

    **Data Items**

    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`EXRECVRA <secsgem.secs.data_items.EXRECVRA>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F13
        {
            EXID: A[20]
            EXRECVRA: A[40]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F13({"EXID": "EX123", "EXRECVRA": "EXRECVRA2"})
        S5F13 W
          <L [2]
            <A "EX123">
            <A "EXRECVRA2">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 13

    _data_format = [
        EXID,
        EXRECVRA
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS05F14(SecsStreamFunction):
    """
    exception recover - acknowledge.

    **Data Items**

    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`ACKA <secsgem.secs.data_items.ACKA>`
    - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
    - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F14
        {
            EXID: A[20]
            DATA: {
                ACKA: BOOLEAN[1]
                DATA: {
                    ERRCODE: I1/I2/I4/I8
                    ERRTEXT: A[120]
                }
            }
        }

    **Example**::
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F14({"EXID": "EX123", \
                                               "DATA": {"ACKA": False, \
                                                        "DATA": {"ERRCODE": 10, \
                                                                 "ERRTEXT": "Error"}}})
        S5F14
          <L [2]
            <A "EX123">
            <L [2]
              <BOOLEAN False >
              <L [2]
                <I1 10 >
                <A "Error">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 14

    _data_format = [
        EXID,
        [
            ACKA,
            [
                ERRCODE,
                ERRTEXT
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F15(SecsStreamFunction):
    """
    exception recover complete - notify.

    **Data Items**

    - :class:`TIMESTAMP <secsgem.secs.data_items.TIMESTAMP>`
    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`ACKA <secsgem.secs.data_items.ACKA>`
    - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
    - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F15
        {
            TIMESTAMP: A[32]
            EXID: A[20]
            DATA: {
                ACKA: BOOLEAN[1]
                DATA: {
                    ERRCODE: I1/I2/I4/I8
                    ERRTEXT: A[120]
                }
            }
        }

    **Example**::
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F15({"TIMESTAMP": "161006221500", "EXID": "EX123", "DATA": \
{"ACKA": False, "DATA": {"ERRCODE": 10, "ERRTEXT": "Error"}}})
        S5F15
          <L [3]
            <A "161006221500">
            <A "EX123">
            <L [2]
              <BOOLEAN False >
              <L [2]
                <I1 10 >
                <A "Error">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 15

    _data_format = [
        TIMESTAMP,
        EXID,
        [
            ACKA,
            [
                ERRCODE,
                ERRTEXT
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F16(SecsStreamFunction):
    """
    exception recover complete - confirm.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F16
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F16()
        S5F16 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 5
    _function = 16

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS05F17(SecsStreamFunction):
    """
    exception recover abort - request.

    **Data Items**

    - :class:`EXID <secsgem.secs.data_items.EXID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F17
        EXID: A[20]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F17("EX123")
        S5F17 W
          <A "EX123"> .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 17

    _data_format = EXID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS05F18(SecsStreamFunction):
    """
    exception recover abort - acknowledge.

    **Data Items**

    - :class:`EXID <secsgem.secs.data_items.EXID>`
    - :class:`ACKA <secsgem.secs.data_items.ACKA>`
    - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
    - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F18
        {
            EXID: A[20]
            DATA: {
                ACKA: BOOLEAN[1]
                DATA: {
                    ERRCODE: I1/I2/I4/I8
                    ERRTEXT: A[120]
                }
            }
        }

    **Example**::
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS05F18({"EXID": "EX123", \
                                               "DATA": {"ACKA": False, \
                                                        "DATA": {"ERRCODE": 10, \
                                                                 "ERRTEXT": "Error"}}})
        S5F18
          <L [2]
            <A "EX123">
            <L [2]
              <BOOLEAN False >
              <L [2]
                <I1 10 >
                <A "Error">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 5
    _function = 18

    _data_format = [
        EXID,
        [
            ACKA,
            [
                ERRCODE,
                ERRTEXT
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS06F00(SecsStreamFunction):
    """
    abort transaction stream 6.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F00()
        S6F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 6
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS06F05(SecsStreamFunction):
    """
    multi block data inquiry.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`DATALENGTH <secsgem.secs.data_items.DATALENGTH>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F05
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DATALENGTH: U1/U2/U4/U8/I1/I2/I4/I8
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F05({"DATAID": 1, "DATALENGTH": 1337})
        S6F5 W
          <L [2]
            <U1 1 >
            <U2 1337 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 5

    _data_format = [
        DATAID,
        DATALENGTH
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS06F06(SecsStreamFunction):
    """
    multi block data grant.

    **Data Items**

    - :class:`GRANT6 <secsgem.secs.data_items.GRANT6>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F06
        GRANT6: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F06(secsgem.secs.data_items.GRANT6.BUSY)
        S6F6
          <B 0x1> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 6
    _function = 6

    _data_format = GRANT6

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS06F07(SecsStreamFunction):
    """
    data transfer request.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F07
        DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F07(1)
        S6F7 W
          <U1 1 > .

    :param value: parameters for this function (see example)
    :type value: integer
    """

    _stream = 6
    _function = 7

    _data_format = DATAID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS06F08(SecsStreamFunction):
    """
    data transfer data.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`
    - :class:`DSID <secsgem.secs.data_items.DSID>`
    - :class:`DVNAME <secsgem.secs.data_items.DVNAME>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F08
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            DS: [
                {
                    DSID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    DV: [
                        {
                            DVNAME: U1/U2/U4/U8/I1/I2/I4/I8/A
                            DVVAL: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        }
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F08({ \
            "DATAID": 1, \
            "CEID": 1337, \
            "DS": [{ \
                "DSID": 1000, \
                "DV": [ \
                    {"DVNAME": "VAR1", "DVVAL": "VAR"}, \
                    {"DVNAME": "VAR2", "DVVAL": secsgem.secs.variables.U4(100)}]}]})
        S6F8
          <L [3]
            <U1 1 >
            <U2 1337 >
            <L [1]
              <L [2]
                <U2 1000 >
                <L [2]
                  <L [2]
                    <A "VAR1">
                    <A "VAR">
                  >
                  <L [2]
                    <A "VAR2">
                    <U4 100 >
                  >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 6
    _function = 8

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "DS",   # name of the list
                DSID,
                [
                    [
                        "DV",   # name of the list
                        DVNAME,
                        DVVAL
                    ]
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS06F11(SecsStreamFunction):
    """
    event report.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`
    - :class:`RPTID <secsgem.secs.data_items.RPTID>`
    - :class:`V <secsgem.secs.data_items.V>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F11
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            RPT: [
                {
                    RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    V: [
                        DATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F11({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": \
["VAR", secsgem.secs.variables.U4(100)]}]})
        S6F11 W
          <L [3]
            <U1 1 >
            <U2 1337 >
            <L [1]
              <L [2]
                <U2 1000 >
                <L [2]
                  <A "VAR">
                  <U4 100 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 11

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "RPT",   # name of the list
                RPTID,
                [V]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS06F12(SecsStreamFunction):
    """
    event report - acknowledge.

    **Data Items**

    - :class:`ACKC6 <secsgem.secs.data_items.ACKC6>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F12
        ACKC6: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F12(secsgem.secs.data_items.ACKC6.ACCEPTED)
        S6F12
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 6
    _function = 12

    _data_format = ACKC6

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS06F15(SecsStreamFunction):
    """
    event report request.

    **Data Items**

    - :class:`CEID <secsgem.secs.data_items.CEID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F15
        CEID: U1/U2/U4/U8/I1/I2/I4/I8/A

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F15(1337)
        S6F15 W
          <U2 1337 > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 15

    _data_format = CEID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS06F16(SecsStreamFunction):
    """
    event report data.

    **Data Items**

    - :class:`DATAID <secsgem.secs.data_items.DATAID>`
    - :class:`CEID <secsgem.secs.data_items.CEID>`
    - :class:`RPTID <secsgem.secs.data_items.RPTID>`
    - :class:`V <secsgem.secs.data_items.V>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F16
        {
            DATAID: U1/U2/U4/U8/I1/I2/I4/I8/A
            CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
            RPT: [
                {
                    RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A
                    V: [
                        DATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F16({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": \
["VAR", secsgem.secs.variables.U4(100)]}]})
        S6F16
          <L [3]
            <U1 1 >
            <U2 1337 >
            <L [1]
              <L [2]
                <U2 1000 >
                <L [2]
                  <A "VAR">
                  <U4 100 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 16

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "RPT",   # name of the list
                RPTID,
                [V]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS06F19(SecsStreamFunction):
    """
    individual report request.

    **Data Items**

    - :class:`RPTID <secsgem.secs.data_items.RPTID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F19
        RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F19(secsgem.secs.variables.U4(1337))
        S6F19 W
          <U4 1337 > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 19

    _data_format = RPTID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS06F20(SecsStreamFunction):
    """
    individual report data.

    **Data Items**

    - :class:`V <secsgem.secs.data_items.V>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F20
        [
            V: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F20(["ASD", 1337])
        S6F20
          <L [2]
            <A "ASD">
            <U2 1337 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 20

    _data_format = [V]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS06F21(SecsStreamFunction):
    """
    annotated individual report request.

    **Data Items**

    - :class:`RPTID <secsgem.secs.data_items.RPTID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F21
        RPTID: U1/U2/U4/U8/I1/I2/I4/I8/A

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F21(secsgem.secs.variables.U4(1337))
        S6F21 W
          <U4 1337 > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 21

    _data_format = RPTID

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS06F22(SecsStreamFunction):
    """
    annotated individual report data.

    **Data Items**

    - :class:`VID <secsgem.secs.data_items.VID>`
    - :class:`V <secsgem.secs.data_items.V>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F22
        [
            {
                VID: U1/U2/U4/U8/I1/I2/I4/I8/A
                V: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            }
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F22([{"VID": "VID1", "V": "ASD"}, {"VID": 2, "V": 1337}])
        S6F22
          <L [2]
            <L [2]
              <A "VID1">
              <A "ASD">
            >
            <L [2]
              <U1 2 >
              <U2 1337 >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 6
    _function = 22

    _data_format = [
        [
            VID,
            V
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS07F00(SecsStreamFunction):
    """
    abort transaction stream 7.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F00()
        S7F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 7
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS07F01(SecsStreamFunction):
    """
    process program load - inquire.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`
    - :class:`LENGTH <secsgem.secs.data_items.LENGTH>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F01
        {
            PPID: A/B[120]
            LENGTH: U1/U2/U4/U8/I1/I2/I4/I8
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F01({"PPID": "program", "LENGTH": 4})
        S7F1 W
          <L [2]
            <A "program">
            <U1 4 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 1

    _data_format = [
        PPID,
        LENGTH
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS07F02(SecsStreamFunction):
    """
    process program load - grant.

    **Data Items**

    - :class:`PPGNT <secsgem.secs.data_items.PPGNT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F02
        PPGNT: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F02(secsgem.secs.data_items.PPGNT.OK)
        S7F2
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 7
    _function = 2

    _data_format = PPGNT

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS07F03(SecsStreamFunction):
    """
    process program - send.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`
    - :class:`PPBODY <secsgem.secs.data_items.PPBODY>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F03
        {
            PPID: A/B[120]
            PPBODY: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F03({"PPID": "program", "PPBODY": secsgem.secs.variables.Binary("data")})
        S7F3 W
          <L [2]
            <A "program">
            <B 0x64 0x61 0x74 0x61>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 3

    _data_format = [
        PPID,
        PPBODY
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS07F04(SecsStreamFunction):
    """
    process program - acknowledge.

    **Data Items**

    - :class:`ACKC7 <secsgem.secs.data_items.ACKC7>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F04
        ACKC7: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F04(secsgem.secs.data_items.ACKC7.MATRIX_OVERFLOW)
        S7F4
          <B 0x3> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 7
    _function = 4

    _data_format = ACKC7

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS07F05(SecsStreamFunction):
    """
    process program - request.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F05
        PPID: A/B[120]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F05("program")
        S7F5 W
          <A "program"> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 7
    _function = 5

    _data_format = PPID

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS07F06(SecsStreamFunction):
    """
    process program - data.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`
    - :class:`PPBODY <secsgem.secs.data_items.PPBODY>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F06
        {
            PPID: A/B[120]
            PPBODY: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F06({"PPID": "program", "PPBODY": secsgem.secs.variables.Binary("data")})
        S7F6
          <L [2]
            <A "program">
            <B 0x64 0x61 0x74 0x61>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 6

    _data_format = [
        PPID,
        PPBODY
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS07F17(SecsStreamFunction):
    """
    delete process program - send.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F17
        [
            PPID: A/B[120]
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F17(["program1", "program2"])
        S7F17 W
          <L [2]
            <A "program1">
            <A "program2">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 17

    _data_format = [PPID]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS07F18(SecsStreamFunction):
    """
    delete process program - acknowledge.

    **Data Items**

    - :class:`ACKC7 <secsgem.secs.data_items.ACKC7>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F18
        ACKC7: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F18(secsgem.secs.data_items.ACKC7.MODE_UNSUPPORTED)
        S7F18
          <B 0x5> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 7
    _function = 18

    _data_format = ACKC7

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS07F19(SecsStreamFunction):
    """
    current equipment process program - request.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F19
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F19()
        S7F19 W .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 19

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS07F20(SecsStreamFunction):
    """
    current equipment process program - data.

    **Data Items**

    - :class:`PPID <secsgem.secs.data_items.PPID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F20
        [
            PPID: A/B[120]
            ...
        ]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS07F20(["program1", "program2"])
        S7F20
          <L [2]
            <A "program1">
            <A "program2">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 7
    _function = 20

    _data_format = [PPID]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS09F00(SecsStreamFunction):
    """
    abort transaction stream 9.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F00()
        S9F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 9
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F01(SecsStreamFunction):
    """
    unrecognized device id.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F01
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F01("HEADERDATA")
        S9F1
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 1

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F03(SecsStreamFunction):
    """
    unrecognized stream type.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F03
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F03("HEADERDATA")
        S9F3
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 3

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F05(SecsStreamFunction):
    """
    unrecognized function type.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F05
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F05("HEADERDATA")
        S9F5
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 5

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F07(SecsStreamFunction):
    """
    illegal data.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F07
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F07("HEADERDATA")
        S9F7
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 7

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F09(SecsStreamFunction):
    """
    transaction timer timeout.

    **Data Items**

    - :class:`SHEAD <secsgem.secs.data_items.SHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F09
        SHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F09("HEADERDATA")
        S9F9
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 9

    _data_format = SHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F11(SecsStreamFunction):
    """
    data too long.

    **Data Items**

    - :class:`MHEAD <secsgem.secs.data_items.MHEAD>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F11
        MHEAD: B[10]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F11("HEADERDATA")
        S9F11
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 9
    _function = 11

    _data_format = MHEAD

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS09F13(SecsStreamFunction):
    """
    conversation timeout.

    **Data Items**

    - :class:`MEXP <secsgem.secs.data_items.MEXP>`
    - :class:`EDID <secsgem.secs.data_items.EDID>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F13
        {
            MEXP: A[6]
            EDID: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS09F13({"MEXP": "S01E01", "EDID": "data"})
        S9F13
          <L [2]
            <A "S01E01">
            <A "data">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 9
    _function = 13

    _data_format = [
        MEXP,
        EDID
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS10F00(SecsStreamFunction):
    """
    abort transaction stream 10.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F00()
        S10F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 10
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS10F01(SecsStreamFunction):
    """
    terminal - request.

    **Data Items**

    - :class:`TID <secsgem.secs.data_items.TID>`
    - :class:`TEXT <secsgem.secs.data_items.TEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F01
        {
            TID: B[1]
            TEXT: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F01({"TID": 0, "TEXT": "hello?"})
        S10F1
          <L [2]
            <B 0x0>
            <A "hello?">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 10
    _function = 1

    _data_format = [
        TID,
        TEXT
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS10F02(SecsStreamFunction):
    """
    terminal - acknowledge.

    **Data Items**

    - :class:`ACKC10 <secsgem.secs.data_items.ACKC10>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F02
        ACKC10: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F02(secsgem.secs.data_items.ACKC10.ACCEPTED)
        S10F2
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 10
    _function = 2

    _data_format = ACKC10

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS10F03(SecsStreamFunction):
    """
    terminal single - display.

    **Data Items**

    - :class:`TID <secsgem.secs.data_items.TID>`
    - :class:`TEXT <secsgem.secs.data_items.TEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F03
        {
            TID: B[1]
            TEXT: U1/U2/U4/U8/I1/I2/I4/I8/A/B
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F03({"TID": 0, "TEXT": "hello!"})
        S10F3
          <L [2]
            <B 0x0>
            <A "hello!">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 10
    _function = 3

    _data_format = [
        TID,
        TEXT
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = False

    _is_multi_block = False


class SecsS10F04(SecsStreamFunction):
    """
    terminal single - acknowledge.

    **Data Items**

    - :class:`ACKC10 <secsgem.secs.data_items.ACKC10>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F04
        ACKC10: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS10F04(secsgem.secs.data_items.ACKC10.TERMINAL_NOT_AVAILABLE)
        S10F4
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 10
    _function = 4

    _data_format = ACKC10

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F00(SecsStreamFunction):
    """
    abort transaction stream 12.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F00()
        S12F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 12
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F01(SecsStreamFunction):
    """
    map setup data - send.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`FNLOC <secsgem.secs.data_items.FNLOC>`
    - :class:`FFROT <secsgem.secs.data_items.FFROT>`
    - :class:`ORLOC <secsgem.secs.data_items.ORLOC>`
    - :class:`RPSEL <secsgem.secs.data_items.RPSEL>`
    - :class:`REFP <secsgem.secs.data_items.REFP>`
    - :class:`DUTMS <secsgem.secs.data_items.DUTMS>`
    - :class:`XDIES <secsgem.secs.data_items.XDIES>`
    - :class:`YDIES <secsgem.secs.data_items.YDIES>`
    - :class:`ROWCT <secsgem.secs.data_items.ROWCT>`
    - :class:`COLCT <secsgem.secs.data_items.COLCT>`
    - :class:`NULBC <secsgem.secs.data_items.NULBC>`
    - :class:`PRDCT <secsgem.secs.data_items.PRDCT>`
    - :class:`PRAXI <secsgem.secs.data_items.PRAXI>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F01
        {
            MID: A/B[80]
            IDTYP: B[1]
            FNLOC: U2
            FFROT: U2
            ORLOC: B
            RPSEL: U1
            REFP: [
                DATA: I1/I2/I4/I8
                ...
            ]
            DUTMS: A
            XDIES: U1/U2/U4/U8/F4/F8
            YDIES: U1/U2/U4/U8/F4/F8
            ROWCT: U1/U2/U4/U8
            COLCT: U1/U2/U4/U8
            NULBC: U1/A
            PRDCT: U1/U2/U4/U8
            PRAXI: B[1]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F01({"MID": "materialID", \
                "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                "FNLOC": 0, \
                "FFROT": 0, \
                "ORLOC": secsgem.secs.data_items.ORLOC.UPPER_LEFT, \
                "RPSEL": 0, \
                "REFP": [[1,2], [2,3]], \
                "DUTMS": "unit", \
                "XDIES": 100, \
                "YDIES": 100, \
                "ROWCT": 10, \
                "COLCT": 10, \
                "NULBC": "{x}", \
                "PRDCT": 100, \
                "PRAXI": secsgem.secs.data_items.PRAXI.ROWS_TOP_INCR, \
                })
        S12F1 W
          <L [15]
            <A "materialID">
            <B 0x0>
            <U2 0 >
            <U2 0 >
            <B 0x2>
            <U1 0 >
            <L [2]
              <I1 1 2 >
              <I1 2 3 >
            >
            <A "unit">
            <U1 100 >
            <U1 100 >
            <U1 10 >
            <U1 10 >
            <A "{x}">
            <U1 100 >
            <B 0x0>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 1

    _data_format = [
        MID,
        IDTYP,
        FNLOC,
        FFROT,
        ORLOC,
        RPSEL,
        [REFP],
        DUTMS,
        XDIES,
        YDIES,
        ROWCT,
        COLCT,
        NULBC,
        PRDCT,
        PRAXI
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F02(SecsStreamFunction):
    """
    map setup data - acknowledge.

    **Data Items**

    - :class:`SDACK <secsgem.secs.data_items.SDACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F02
        SDACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F02(secsgem.secs.data_items.SDACK.ACK)
        S12F2
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 2

    _data_format = SDACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F03(SecsStreamFunction):
    """
    map setup data - request.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`MAPFT <secsgem.secs.data_items.MAPFT>`
    - :class:`FNLOC <secsgem.secs.data_items.FNLOC>`
    - :class:`FFROT <secsgem.secs.data_items.FFROT>`
    - :class:`ORLOC <secsgem.secs.data_items.ORLOC>`
    - :class:`PRAXI <secsgem.secs.data_items.PRAXI>`
    - :class:`BCEQU <secsgem.secs.data_items.BCEQU>`
    - :class:`NULBC <secsgem.secs.data_items.NULBC>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F03
        {
            MID: A/B[80]
            IDTYP: B[1]
            MAPFT: B[1]
            FNLOC: U2
            FFROT: U2
            ORLOC: B
            PRAXI: B[1]
            BCEQU: U1/A
            NULBC: U1/A
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F03({"MID": "materialID", \
                "IDTYP": secsgem.secs.data_items.IDTYP.WAFER_CASSETTE, \
                "MAPFT": secsgem.secs.data_items.MAPFT.ROW, \
                "FNLOC": 0, \
                "FFROT": 0, \
                "ORLOC": secsgem.secs.data_items.ORLOC.LOWER_LEFT, \
                "PRAXI": secsgem.secs.data_items.PRAXI.COLS_LEFT_INCR, \
                "BCEQU": [1, 3, 5, 7], \
                "NULBC": "{x}", \
                })
        S12F3 W
          <L [9]
            <A "materialID">
            <B 0x1>
            <B 0x0>
            <U2 0 >
            <U2 0 >
            <B 0x3>
            <B 0x4>
            <U1 1 3 5 7 >
            <A "{x}">
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 3

    _data_format = [
        MID,
        IDTYP,
        MAPFT,
        FNLOC,
        FFROT,
        ORLOC,
        PRAXI,
        BCEQU,
        NULBC
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F04(SecsStreamFunction):
    """
    map setup data.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`FNLOC <secsgem.secs.data_items.FNLOC>`
    - :class:`ORLOC <secsgem.secs.data_items.ORLOC>`
    - :class:`RPSEL <secsgem.secs.data_items.RPSEL>`
    - :class:`REFP <secsgem.secs.data_items.REFP>`
    - :class:`DUTMS <secsgem.secs.data_items.DUTMS>`
    - :class:`XDIES <secsgem.secs.data_items.XDIES>`
    - :class:`YDIES <secsgem.secs.data_items.YDIES>`
    - :class:`ROWCT <secsgem.secs.data_items.ROWCT>`
    - :class:`COLCT <secsgem.secs.data_items.COLCT>`
    - :class:`PRDCT <secsgem.secs.data_items.PRDCT>`
    - :class:`BCEQU <secsgem.secs.data_items.BCEQU>`
    - :class:`NULBC <secsgem.secs.data_items.NULBC>`
    - :class:`MLCL <secsgem.secs.data_items.MLCL>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F04
        {
            MID: A/B[80]
            IDTYP: B[1]
            FNLOC: U2
            ORLOC: B
            RPSEL: U1
            REFP: [
                DATA: I1/I2/I4/I8
                ...
            ]
            DUTMS: A
            XDIES: U1/U2/U4/U8/F4/F8
            YDIES: U1/U2/U4/U8/F4/F8
            ROWCT: U1/U2/U4/U8
            COLCT: U1/U2/U4/U8
            PRDCT: U1/U2/U4/U8
            BCEQU: U1/A
            NULBC: U1/A
            MLCL: U1/U2/U4/U8
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F04({"MID": "materialID", \
                "IDTYP": secsgem.secs.data_items.IDTYP.FILM_FRAME, \
                "FNLOC": 0, \
                "ORLOC": secsgem.secs.data_items.ORLOC.CENTER_DIE, \
                "RPSEL": 0, \
                "REFP": [[1,2], [2,3]], \
                "DUTMS": "unit", \
                "XDIES": 100, \
                "YDIES": 100, \
                "ROWCT": 10, \
                "COLCT": 10, \
                "PRDCT": 100, \
                "BCEQU": [1, 3, 5, 7], \
                "NULBC": "{x}", \
                "MLCL": 0, \
                })
        S12F4
          <L [15]
            <A "materialID">
            <B 0x2>
            <U2 0 >
            <B 0x0>
            <U1 0 >
            <L [2]
              <I1 1 2 >
              <I1 2 3 >
            >
            <A "unit">
            <U1 100 >
            <U1 100 >
            <U1 10 >
            <U1 10 >
            <U1 100 >
            <U1 1 3 5 7 >
            <A "{x}">
            <U1 0 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 4

    _data_format = [
        MID,
        IDTYP,
        FNLOC,
        ORLOC,
        RPSEL,
        [REFP],
        DUTMS,
        XDIES,
        YDIES,
        ROWCT,
        COLCT,
        PRDCT,
        BCEQU,
        NULBC,
        MLCL
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F05(SecsStreamFunction):
    """
    map transmit inquire.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`MAPFT <secsgem.secs.data_items.MAPFT>`
    - :class:`MLCL <secsgem.secs.data_items.MLCL>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F05
        {
            MID: A/B[80]
            IDTYP: B[1]
            MAPFT: B[1]
            MLCL: U1/U2/U4/U8
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F05({"MID": "materialID", \
                                               "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                                               "MAPFT": secsgem.secs.data_items.MAPFT.ARRAY, \
                                               "MLCL": 0})
        S12F5 W
          <L [4]
            <A "materialID">
            <B 0x0>
            <B 0x1>
            <U1 0 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 5

    _data_format = [
        MID,
        IDTYP,
        MAPFT,
        MLCL
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F06(SecsStreamFunction):
    """
    map transmit - grant.

    **Data Items**

    - :class:`GRNT1 <secsgem.secs.data_items.GRNT1>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F06
        GRNT1: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F06(secsgem.secs.data_items.GRNT1.MATERIALID_UNKNOWN)
        S12F6
          <B 0x5> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 6

    _data_format = GRNT1

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F07(SecsStreamFunction):
    """
    map data type 1 - send.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`RSINF <secsgem.secs.data_items.RSINF>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F07
        {
            MID: A/B[80]
            IDTYP: B[1]
            DATA: [
                {
                    RSINF: I1/I2/I4/I8[3]
                    BINLT: U1/A
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F07({ \
            "MID": "materialID", \
            "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
            "DATA": [ \
                {"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, \
                {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F7 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I1 1 2 3 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I1 4 5 6 >
                <U1 5 6 7 8 >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 7

    _data_format = [
        MID,
        IDTYP,
        [
            [
                RSINF,
                BINLT
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS12F08(SecsStreamFunction):
    """
    map data type 1 - acknowledge.

    **Data Items**

    - :class:`MDACK <secsgem.secs.data_items.MDACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F08
        MDACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F08(secsgem.secs.data_items.MDACK.ABORT_MAP)
        S12F8
          <B 0x3> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 8

    _data_format = MDACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F09(SecsStreamFunction):
    """
    map data type 2 - send.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`STRP <secsgem.secs.data_items.STRP>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F09
        {
            MID: A/B[80]
            IDTYP: B[1]
            STRP: I1/I2/I4/I8[2]
            BINLT: U1/A
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F09({"MID": "materialID", \
                                               "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                                               "STRP": [0, 1], \
                                               "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F9 W
          <L [4]
            <A "materialID">
            <B 0x0>
            <I1 0 1 >
            <U1 1 2 3 4 5 6 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 9

    _data_format = [
        MID,
        IDTYP,
        STRP,
        BINLT
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS12F10(SecsStreamFunction):
    """
    map data type 2 - acknowledge.

    **Data Items**

    - :class:`MDACK <secsgem.secs.data_items.MDACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F10
        MDACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F10(secsgem.secs.data_items.MDACK.ACK)
        S12F10
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 10

    _data_format = MDACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F11(SecsStreamFunction):
    """
    map data type 3 - send.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`XYPOS <secsgem.secs.data_items.XYPOS>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F11
        {
            MID: A/B[80]
            IDTYP: B[1]
            DATA: [
                {
                    XYPOS: I1/I2/I4/I8[2]
                    BINLT: U1/A
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F11({ \
            "MID": "materialID", \
            "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
            "DATA": [ \
                {"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, \
                {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F11 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I1 1 2 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I1 3 4 >
                <U1 5 6 7 8 >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 11

    _data_format = [
        MID,
        IDTYP,
        [
            [
                XYPOS,
                BINLT
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = True


class SecsS12F12(SecsStreamFunction):
    """
    map data type 3 - acknowledge.

    **Data Items**

    - :class:`MDACK <secsgem.secs.data_items.MDACK>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F12
        MDACK: B[1]

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F12(secsgem.secs.data_items.MDACK.FORMAT_ERROR)
        S12F12
          <B 0x1> .

    :param value: parameters for this function (see example)
    :type value: byte
    """

    _stream = 12
    _function = 12

    _data_format = MDACK

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS12F13(SecsStreamFunction):
    """
    map data type 1 - request.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F13
        {
            MID: A/B[80]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F13({"MID": "materialID", "IDTYP": secsgem.secs.data_items.IDTYP.WAFER})
        S12F13 W
          <L [2]
            <A "materialID">
            <B 0x0>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 13

    _data_format = [
        MID,
        IDTYP
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F14(SecsStreamFunction):
    """
    map data type 1.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`RSINF <secsgem.secs.data_items.RSINF>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F14
        {
            MID: A/B[80]
            IDTYP: B[1]
            DATA: [
                {
                    RSINF: I1/I2/I4/I8[3]
                    BINLT: U1/A
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F14({ \
            "MID": "materialID", \
            "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
            "DATA": [ \
                {"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, \
                {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F14
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I1 1 2 3 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I1 4 5 6 >
                <U1 5 6 7 8 >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 14

    _data_format = [
        MID,
        IDTYP,
        [
            [
                RSINF,
                BINLT
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS12F15(SecsStreamFunction):
    """
    map data type 2 - request.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F15
        {
            MID: A/B[80]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F15({"MID": "materialID", "IDTYP": secsgem.secs.data_items.IDTYP.WAFER})
        S12F15 W
          <L [2]
            <A "materialID">
            <B 0x0>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 15

    _data_format = [
        MID,
        IDTYP
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F16(SecsStreamFunction):
    """
    map data type 2.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`STRP <secsgem.secs.data_items.STRP>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F16
        {
            MID: A/B[80]
            IDTYP: B[1]
            STRP: I1/I2/I4/I8[2]
            BINLT: U1/A
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F16({"MID": "materialID", \
                                               "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                                               "STRP": [0, 1], \
                                               "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F16
          <L [4]
            <A "materialID">
            <B 0x0>
            <I1 0 1 >
            <U1 1 2 3 4 5 6 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 16

    _data_format = [
        MID,
        IDTYP,
        STRP,
        BINLT
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS12F17(SecsStreamFunction):
    """
    map data type 3 - request.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`SDBIN <secsgem.secs.data_items.SDBIN>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F17
        {
            MID: A/B[80]
            IDTYP: B[1]
            SDBIN: B[1]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F17({"MID": "materialID", \
                                               "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                                               "SDBIN": secsgem.secs.data_items.SDBIN.DONT_SEND})
        S12F17 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <B 0x1>
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 17

    _data_format = [
        MID,
        IDTYP,
        SDBIN
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS12F18(SecsStreamFunction):
    """
    map data type 3.

    **Data Items**

    - :class:`MID <secsgem.secs.data_items.MID>`
    - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
    - :class:`XYPOS <secsgem.secs.data_items.XYPOS>`
    - :class:`BINLT <secsgem.secs.data_items.BINLT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F18
        {
            MID: A/B[80]
            IDTYP: B[1]
            DATA: [
                {
                    XYPOS: I1/I2/I4/I8[2]
                    BINLT: U1/A
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F18({ \
                "MID": "materialID", \
                "IDTYP": secsgem.secs.data_items.IDTYP.WAFER, \
                "DATA": [ \
                    {"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, \
                    {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F18
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I1 1 2 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I1 3 4 >
                <U1 5 6 7 8 >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 18

    _data_format = [
        MID,
        IDTYP,
        [
            [
                XYPOS,
                BINLT
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS12F19(SecsStreamFunction):
    """
    map error report - send.

    **Data Items**

    - :class:`MAPER <secsgem.secs.data_items.MAPER>`
    - :class:`DATLC <secsgem.secs.data_items.DATLC>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F19
        {
            MAPER: B[1]
            DATLC: U1
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F19({"MAPER": secsgem.secs.data_items.MAPER.INVALID_DATA, "DATLC": 0})
        S12F19
          <L [2]
            <B 0x1>
            <U1 0 >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 12
    _function = 19

    _data_format = [
        MAPER,
        DATLC
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS14F00(SecsStreamFunction):
    """
    abort transaction stream 14.

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F00
        Header only

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F00()
        S14F0 .

    :param value: function has no parameters
    :type value: None
    """

    _stream = 14
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class SecsS14F01(SecsStreamFunction):
    """
    GetAttr request.

    **Data Items**

    - :class:`OBJSPEC <secsgem.secs.data_items.OBJSPEC>`
    - :class:`OBJTYPE <secsgem.secs.data_items.OBJTYPE>`
    - :class:`OBJID <secsgem.secs.data_items.OBJID>`
    - :class:`ATTRID <secsgem.secs.data_items.ATTRID>`
    - :class:`ATTRDATA <secsgem.secs.data_items.ATTRDATA>`
    - :class:`ATTRRELN <secsgem.secs.data_items.ATTRRELN>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F01
        {
            OBJSPEC: A
            OBJTYPE: U1/U2/U4/U8/A
            OBJID: [
                DATA: U1/U2/U4/U8/A
                ...
            ]
            FILTER: [
                {
                    ATTRID: U1/U2/U4/U8/A
                    ATTRDATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                    ATTRRELN: U1
                }
                ...
            ]
            ATTRID: [
                DATA: U1/U2/U4/U8/A
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F01({ \
            "OBJSPEC": '', \
            "OBJTYPE": 'StripMap', \
            "OBJID": ['MAP001'], \
            "FILTER": [], \
            "ATTRID": ['OriginLocation', 'Rows', 'Columns', 'CellStatus', 'LotID']})
        S14F1 W
          <L [5]
            <A>
            <A "StripMap">
            <L [1]
              <A "MAP001">
            >
            <L>
            <L [5]
              <A "OriginLocation">
              <A "Rows">
              <A "Columns">
              <A "CellStatus">
              <A "LotID">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 14
    _function = 1

    _data_format = [
        OBJSPEC,
        OBJTYPE,
        [OBJID],
        [
            [
                "FILTER",   # name of the list
                ATTRID,
                ATTRDATA,
                ATTRRELN
            ]
        ],
        [ATTRID]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False

    RELATION = {
        "EQUAL": 0,
        "NOTEQUAL": 1,
        "LESS": 2,
        "LESSEQUAL": 3,
        "GREATER": 4,
        "GREATEREQUAL": 5,
        "PRESENT": 6,
        "NOTPRESENT": 7,
    }


class SecsS14F02(SecsStreamFunction):
    """
    GetAttr data.

    **Data Items**

    - :class:`OBJID <secsgem.secs.data_items.OBJID>`
    - :class:`ATTRID <secsgem.secs.data_items.ATTRID>`
    - :class:`ATTRDATA <secsgem.secs.data_items.ATTRDATA>`
    - :class:`OBJACK <secsgem.secs.data_items.OBJACK>`
    - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
    - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F02
        {
            DATA: [
                {
                    OBJID: U1/U2/U4/U8/A
                    ATTRIBS: [
                        {
                            ATTRID: U1/U2/U4/U8/A
                            ATTRDATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        }
                        ...
                    ]
                }
                ...
            ]
            ERRORS: {
                OBJACK: U1[1]
                ERROR: [
                    {
                        ERRCODE: I1/I2/I4/I8
                        ERRTEXT: A[120]
                    }
                    ...
                ]
            }
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F02({ \
            "DATA": [{ \
                "OBJID": "MAP001", \
                "ATTRIBS": [ \
                    {"ATTRID": "OriginLocation", "ATTRDATA": "0"}, \
                    {"ATTRID": "Rows", "ATTRDATA": 4}, \
                    {"ATTRID": "Columns", "ATTRDATA": 4}, \
                    {"ATTRID": "CellStatus", "ATTRDATA": 6}, \
                    {"ATTRID": "LotID", "ATTRDATA":"LOT001"}]}], \
                "ERRORS": {"OBJACK": 0}})
        S14F2
          <L [2]
            <L [1]
              <L [2]
                <A "MAP001">
                <L [5]
                  <L [2]
                    <A "OriginLocation">
                    <A "0">
                  >
                  <L [2]
                    <A "Rows">
                    <U1 4 >
                  >
                  <L [2]
                    <A "Columns">
                    <U1 4 >
                  >
                  <L [2]
                    <A "CellStatus">
                    <U1 6 >
                  >
                  <L [2]
                    <A "LotID">
                    <A "LOT001">
                  >
                >
              >
            >
            <L [2]
              <U1 0 >
              <L>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 14
    _function = 2

    _data_format = [
        [
            [
                OBJID,
                [
                    [
                        "ATTRIBS",   # name of the list
                        ATTRID,
                        ATTRDATA
                    ]
                ]
            ]
        ],
        [
            "ERRORS",   # name of the list
            OBJACK,
            [
                [
                    "ERROR",   # name of the list
                    ERRCODE,
                    ERRTEXT
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


class SecsS14F03(SecsStreamFunction):
    """
    SetAttr request.

    **Data Items**

    - :class:`OBJSPEC <secsgem.secs.data_items.OBJSPEC>`
    - :class:`OBJTYPE <secsgem.secs.data_items.OBJTYPE>`
    - :class:`OBJID <secsgem.secs.data_items.OBJID>`
    - :class:`ATTRID <secsgem.secs.data_items.ATTRID>`
    - :class:`ATTRDATA <secsgem.secs.data_items.ATTRDATA>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F03
        {
            OBJSPEC: A
            OBJTYPE: U1/U2/U4/U8/A
            OBJID: [
                DATA: U1/U2/U4/U8/A
                ...
            ]
            ATTRIBS: [
                {
                    ATTRID: U1/U2/U4/U8/A
                    ATTRDATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F03({"OBJSPEC": '', "OBJTYPE": 'StripMap', "OBJID": ['MAP001'], \
"ATTRIBS": [ {"ATTRID": "CellStatus", "ATTRDATA": "3"} ] })
        S14F3 W
          <L [4]
            <A>
            <A "StripMap">
            <L [1]
              <A "MAP001">
            >
            <L [1]
              <L [2]
                <A "CellStatus">
                <A "3">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 14
    _function = 3

    _data_format = [
        OBJSPEC,
        OBJTYPE,
        [OBJID],
        [
            [
                "ATTRIBS",   # name of the list
                ATTRID,
                ATTRDATA
            ]
        ]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False


class SecsS14F04(SecsStreamFunction):
    """
    SetAttr data.

    **Data Items**

    - :class:`OBJID <secsgem.secs.data_items.OBJID>`
    - :class:`ATTRID <secsgem.secs.data_items.ATTRID>`
    - :class:`ATTRDATA <secsgem.secs.data_items.ATTRDATA>`
    - :class:`OBJACK <secsgem.secs.data_items.OBJACK>`
    - :class:`ERRCODE <secsgem.secs.data_items.ERRCODE>`
    - :class:`ERRTEXT <secsgem.secs.data_items.ERRTEXT>`

    **Structure**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F04
        {
            DATA: [
                {
                    OBJID: U1/U2/U4/U8/A
                    ATTRIBS: [
                        {
                            ATTRID: U1/U2/U4/U8/A
                            ATTRDATA: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
                        }
                        ...
                    ]
                }
                ...
            ]
            ERRORS: {
                OBJACK: U1[1]
                ERROR: [
                    {
                        ERRCODE: I1/I2/I4/I8
                        ERRTEXT: A[120]
                    }
                    ...
                ]
            }
        }

    **Example**::

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F04({ \
            "DATA": [{ \
                "OBJID": "MAP001", \
                "ATTRIBS": [ \
                    {"ATTRID": "OriginLocation", "ATTRDATA": "0"}, \
                    {"ATTRID": "Rows", "ATTRDATA": 4}, \
                    {"ATTRID": "Columns", "ATTRDATA": 4}, \
                    {"ATTRID": "CellStatus", "ATTRDATA": 6}, \
                    {"ATTRID": "LotID", "ATTRDATA":"LOT001"}]}], \
                "ERRORS": {"OBJACK": 0}})
        S14F4
          <L [2]
            <L [1]
              <L [2]
                <A "MAP001">
                <L [5]
                  <L [2]
                    <A "OriginLocation">
                    <A "0">
                  >
                  <L [2]
                    <A "Rows">
                    <U1 4 >
                  >
                  <L [2]
                    <A "Columns">
                    <U1 4 >
                  >
                  <L [2]
                    <A "CellStatus">
                    <U1 6 >
                  >
                  <L [2]
                    <A "LotID">
                    <A "LOT001">
                  >
                >
              >
            >
            <L [2]
              <U1 0 >
              <L>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """

    _stream = 14
    _function = 4

    _data_format = [
        [
            [
                OBJID,
                [
                    [
                        "ATTRIBS",   # name of the list
                        ATTRID,
                        ATTRDATA
                    ]
                ]
            ]
        ],
        [
            "ERRORS",   # name of the list
            OBJACK,
            [
                [
                    "ERROR",   # name of the list
                    ERRCODE,
                    ERRTEXT
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True


secs_streams_functions = {
    0: {
        0: SecsS00F00,
    },
    1: {
        0: SecsS01F00,
        1: SecsS01F01,
        2: SecsS01F02,
        3: SecsS01F03,
        4: SecsS01F04,
        11: SecsS01F11,
        12: SecsS01F12,
        13: SecsS01F13,
        14: SecsS01F14,
        15: SecsS01F15,
        16: SecsS01F16,
        17: SecsS01F17,
        18: SecsS01F18,
    },
    2: {
        0: SecsS02F00,
        13: SecsS02F13,
        14: SecsS02F14,
        15: SecsS02F15,
        16: SecsS02F16,
        17: SecsS02F17,
        18: SecsS02F18,
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
        3: SecsS05F03,
        4: SecsS05F04,
        5: SecsS05F05,
        6: SecsS05F06,
        7: SecsS05F07,
        8: SecsS05F08,
        9: SecsS05F09,
        10: SecsS05F10,
        11: SecsS05F11,
        12: SecsS05F12,
        13: SecsS05F13,
        14: SecsS05F14,
        15: SecsS05F15,
        16: SecsS05F16,
        17: SecsS05F17,
        18: SecsS05F18,
    },
    6: {
        0: SecsS06F00,
        5: SecsS06F05,
        6: SecsS06F06,
        7: SecsS06F07,
        8: SecsS06F08,
        11: SecsS06F11,
        12: SecsS06F12,
        15: SecsS06F15,
        16: SecsS06F16,
        19: SecsS06F19,
        20: SecsS06F20,
        21: SecsS06F21,
        22: SecsS06F22,
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
    14: {
        0: SecsS14F00,
        1: SecsS14F01,
        2: SecsS14F02,
        3: SecsS14F03,
        4: SecsS14F04,
    },
}
