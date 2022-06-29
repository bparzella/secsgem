#####################################################################
# s02f23.py
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
"""Class for stream 02 function 23."""

from secsgem.secs.functions.base import SecsStreamFunction
from secsgem.secs.data_items import TRID, DSPER, TOTSMP, REPGSZ, SVID             


class SecsS02F23(SecsStreamFunction):
    """Trace Initialize Send

    **Data Items**

    - :class:`TRID <secsgem.secs.dataitems.TRID>` Trace Request ID
    - :class:`DSPER <secsgem.secs.dataitems.DSPER>` Data Sample Period hhmmss
    - :class:`TOTSMP <secsgem.secs.dataitems.TOTSMP)>`  total samples to be made (even multiple of REPGSZ )
    - :class:`REPGSZ <secsgem.secs.dataitems.REPGSZ)>` reporting group size
    
    **Structure**::

    **Example**::

        >>> import secsgem
        >>> secsgem.secs.functions.SecsS02F23([{"TRID":1 ,"DSPER":'000010',"TOTSMP":secsgem.secs.variables.U4(10),"REPGSZ":secsgem.secs.variables.U4(1),"SVID":[1002004,400210]}])
        S2F23 W          
            <L [5]
              <A "1">
              <A "000010">
              <U4 10 >
              <U4 1 >
              <L [2]
                <U4 1002004 >
                <U4 400210 >
              >            
          > .

    :param value: parameters for this function (see example)
    :type value:
    """

    _stream = 2
    _function = 23

    _data_format = [
        
           TRID,
           DSPER,
           TOTSMP,
           REPGSZ,
           [SVID]             
                 
    ]
    

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
