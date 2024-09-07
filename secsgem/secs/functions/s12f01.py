#####################################################################
# s12f01.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
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
"""Class for stream 12 function 01."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F01(SecsStreamFunction):
    """map setup data - send.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F01
        {
            MID: A/B[80]
            IDTYP: B[1]
            FNLOC: U2
            FFROT: U2
            ORLOC: B[1]
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

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F01({
        ...     "MID": "materialID",
        ...     "IDTYP": secsgem.secs.data_items.IDTYP.WAFER,
        ...     "FNLOC": 0,
        ...     "FFROT": 0,
        ...     "ORLOC": secsgem.secs.data_items.ORLOC.UPPER_LEFT,
        ...     "RPSEL": 0,
        ...     "REFP": [[1,2], [2,3]],
        ...     "DUTMS": "unit",
        ...     "XDIES": 100,
        ...     "YDIES": 100,
        ...     "ROWCT": 10,
        ...     "COLCT": 10,
        ...     "NULBC": "{x}",
        ...     "PRDCT": 100,
        ...     "PRAXI": secsgem.secs.data_items.PRAXI.ROWS_TOP_INCR})
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

    Data Items:
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

    """

    _stream = 12
    _function = 1

    _data_format = """
    < L
      < MID >
      < IDTYP >
      < FNLOC >
      < FFROT >
      < ORLOC >
      < RPSEL >
      < L REFP
        < REFP >
      >
      < DUTMS >
      < XDIES >
      < YDIES >
      < ROWCT >
      < COLCT >
      < NULBC >
      < PRDCT >
      < PRAXI >
    >
    """

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
