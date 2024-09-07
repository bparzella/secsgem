#####################################################################
# s12f03.py
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
"""Class for stream 12 function 03."""

from secsgem.secs.data_items import BCEQU, FFROT, FNLOC, IDTYP, MAPFT, MID, NULBC, ORLOC, PRAXI
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS12F03(SecsStreamFunction):
    """map setup data - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F03
        {
            MID: A/B[80]
            IDTYP: B[1]
            MAPFT: B[1]
            FNLOC: U2
            FFROT: U2
            ORLOC: B[1]
            PRAXI: B[1]
            BCEQU: U1/A
            NULBC: U1/A
        }

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS12F03({
        ...     "MID": "materialID",
        ...     "IDTYP": secsgem.secs.data_items.IDTYP.WAFER_CASSETTE,
        ...     "MAPFT": secsgem.secs.data_items.MAPFT.ROW,
        ...     "FNLOC": 0,
        ...     "FFROT": 0,
        ...     "ORLOC": secsgem.secs.data_items.ORLOC.LOWER_LEFT,
        ...     "PRAXI": secsgem.secs.data_items.PRAXI.COLS_LEFT_INCR,
        ...     "BCEQU": [1, 3, 5, 7],
        ...     "NULBC": "{x}"})
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

    Data Items:
        - :class:`MID <secsgem.secs.data_items.MID>`
        - :class:`IDTYP <secsgem.secs.data_items.IDTYP>`
        - :class:`MAPFT <secsgem.secs.data_items.MAPFT>`
        - :class:`FNLOC <secsgem.secs.data_items.FNLOC>`
        - :class:`FFROT <secsgem.secs.data_items.FFROT>`
        - :class:`ORLOC <secsgem.secs.data_items.ORLOC>`
        - :class:`PRAXI <secsgem.secs.data_items.PRAXI>`
        - :class:`BCEQU <secsgem.secs.data_items.BCEQU>`
        - :class:`NULBC <secsgem.secs.data_items.NULBC>`

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
        NULBC,
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
