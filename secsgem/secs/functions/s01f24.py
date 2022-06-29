#####################################################################
# s01f24.py
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
"""Class for stream 01 function 24."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import CENAME


class SecsS01F24(SecsStreamFunction):
    """collection event name list response

    **Data Items**
    - :class:`CEID <secsgem.secs.dataitems.CEID>`
    - :class:`CENAME <secsgem.secs.dataitems.CENAME>`
    - :class:`VID <secsgem.secs.dataitems.VID>`

    **Structure**::
        >>> import secsgem
        >>> secsgem.secs.functions.SecsS01F24
        [
            {
                CEID: U1/U2/U4/U8/I1/I2/I4/I8/A
                CENAME: A
                VID: [
                    DATA: U1/U2/U4/U8/I1/I2/I4/I8/A
                    ...
                ]
            }
            ...
        ]
    
    **Example**::
        >>> import secsgem
        >>> secsgem.secs.functions.SecsS01F24([{"CEID": 1, "CENAME": "EquipmentOffline", "VID": []}, {"CEID": 100, "CENAME": "", "VID": []}])

        S1F24
          <L [2]
            <L [3]
              <U1 1 >
              <A "EquipmentOffline">
              <L>
            >
            <L [3]
              <U1 100 >
              <A>
              <L>
            >
          > .
     :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 1
    _function = 24
    _data_format = [
        [
            CEID,
            CENAME,
                [
                    VID
                ]
        ]
    ]
    _to_host = True
    _to_equipment = False
    _has_reply = False
    _is_reply_required = False
    _is_multi_block = True
