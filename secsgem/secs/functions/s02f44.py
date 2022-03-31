#####################################################################
# s02f44.py
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
"""Class for stream 02 function 44."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import RSPACK, STRID, STRACK, FCNID


class SecsS02F44(SecsStreamFunction):
    """
    reset spooling - acknowledge.

    **Data Items**

    - :class:`RSPACK <secsgem.secs.dataitems.RSPACK>`
    - :class:`STRID <secsgem.secs.dataitems.STRID>`
    - :class:`STRACK <secsgem.secs.dataitems.STRACK>`
    - :class:`FCNID <secsgem.secs.dataitems.FCNID>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS02F44
        {
            RSPACK: B[1]
            ERRORS: [
                {
                    STRID: U1
                    STRACK: B[1]
                    FCNIDS: [
                        FCNID: U1
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F44({ \
            "RSPACK": 0x01 (spooling setup rejected), \
            "ERRORS": [ \
                {"STRID": "STRID1", "STRACK": 0x01 (spooling not allowed), "FCNIDS": ["FCNID2"]}, \
                {"STRID": "STRID2", "STRACK": 0x04 (requested message is secondary message), "FCNIDS": ["FCNID3"]}]})
        S2F44
          <L [2]
            <B 0x01 ("RSPACK")>
            <L [2]
              <L [3]
                <U1 "STRID1">
                <B 0x01 ("STRACK")>
                <L [1]
                  <U1 "FCNID2">
                >
              >
              <L [3]
                <U1 "STRID2">
                <B 0x04 ("STRACK")>
                <L [1]
                  <U1 "FCNID3">
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 44

    _dataFormat = [
        RSPACK,
        [   "ERRORS",    # name of the list
            [
                STRID,
                STRACK,
                [
                    "FCNIDS",    # name of the list
                    FCNID,
                ]
            ]
        ]
    ]

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False
