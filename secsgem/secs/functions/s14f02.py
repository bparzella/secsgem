#####################################################################
# s14f02.py
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
"""Class for stream 14 function 02."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import OBJID
from secsgem.secs.data_items import ATTRID
from secsgem.secs.data_items import ATTRDATA
from secsgem.secs.data_items import OBJACK
from secsgem.secs.data_items import ERRCODE
from secsgem.secs.data_items import ERRTEXT


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

    Example:

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS14F02({
        ...     "DATA": [{
        ...         "OBJID": "MAP001",
        ...         "ATTRIBS": [
        ...             {"ATTRID": "OriginLocation", "ATTRDATA": "0"},
        ...             {"ATTRID": "Rows", "ATTRDATA": 4},
        ...             {"ATTRID": "Columns", "ATTRDATA": 4},
        ...             {"ATTRID": "CellStatus", "ATTRDATA": 6},
        ...             {"ATTRID": "LotID", "ATTRDATA":"LOT001"}]}],
        ...         "ERRORS": {"OBJACK": 0}})
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
                        "ATTRIBS",
                        ATTRID,
                        ATTRDATA
                    ]
                ]
            ]
        ],
        [
            "ERRORS",
            OBJACK,
            [
                [
                    "ERROR",
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
