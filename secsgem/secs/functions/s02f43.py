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
    """configure spooling - when none disable spooling

    **Data Items**

    - :class:`STRID <secsgem.secs.data_items.STRID>`
    - :class:`FCNID <secsgem.secs.data_items.FCNID>`
    
    **Structure**::

        >>> import secsgem
        >>> secsgem.SecsS02F43 ([{"STRID": secsgem.secs.variables.U1(11), "FCNID": [secsgem.secs.variables.U1(11)]}])
        S2F43 W
              <L [1]
                <L [2]
                  <U1 11 >
                  <L [1]
                    <U1 11 >
                  >
                >
              > .    

       

    :param value: parameters for this function (see example)
    :type value: 
    """

    _stream = 2
    _function = 43

    _data_format = [
        [            
            STRID,
            [
                FCNID
            ]
        ]
    ]

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
