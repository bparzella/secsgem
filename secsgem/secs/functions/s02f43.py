#####################################################################
# s02f43.py
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
"""Class for stream 02 function 43."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import STRID, FCNID


class SecsS02F43(SecsStreamFunction):
    """
    reset spooling streams and functions - send.

    **Data Items**

    - :class:`STRID <secsgem.secs.dataitems.STRID>`
    - :class:`FCNID <secsgem.secs.dataitems.FCNID>`

    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS02F43
        [
            {
                STRID: U1
                FCNIDS: [
                    FCNID: U1
                    ...
                ]
            }
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F43([{"STRID": "STRID1", "FCNIDS": ["FCNID1", "FCNID2"]}, {"STRID": "STRID2", "FCNIDS": ["FCNID3", "FCNID4"]})
        S2F43 W
          <L [2]
            <L [2]
              <U1 "STRID1">
              <L [2]
                <U1 "FCNID1">
                <U1 "FCNID2">
              >
            >
            <L [2]
              <U1 "STRID2">
              <L [2]
                <U1 "FCNID3">
                <U1 "FCNID4">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """

    _stream = 2
    _function = 43

    _dataFormat = [
        [
            STRID,
            [
                "FCNIDS",   # name of the list
                FCNID
            ]
        ]
    ]

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False
