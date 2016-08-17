#####################################################################
# dataitems.py
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
"""Data items for functions"""

from variables import SecsVarList, SecsVarArray, SecsVarString, SecsVarBinary, SecsVarI1, SecsVarI2, SecsVarI4,\
    SecsVarI8, SecsVarF4, SecsVarF8, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarBoolean, SecsVarDynamic

class COMMACK(SecsVarBinary):
    """Establish communications acknowledge

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+--------------------------------------------------+
        | Value | Description       | Constant                                         |
        +=======+===================+==================================================+
        | 0     | Accepted          | :const:`secsgem.secs.dataitems.COMMACK.ACCEPTED` |
        +-------+-------------------+--------------------------------------------------+
        | 1     | Denied, Try Again | :const:`secsgem.secs.dataitems.COMMACK.DENIED`   |
        +-------+-------------------+--------------------------------------------------+
        | 2-63  | Reserved          |                                                  |
        +-------+-------------------+--------------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F14 <secsgem.secs.functions.SecsS01F14>`
    """
    name = "COMMACK"

    ACCEPTED = 0
    DENIED = 1

    def __init__(self):
        super(self.__class__, self).__init__(1)

class OFLACK(SecsVarBinary):
    """Acknowledge code for OFFLINE request

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------+--------------------------------------------+
        | Value | Description         | Constant                                   |
        +=======+=====================+============================================+
        | 0     | OFFLINE Acknowledge | :const:`secsgem.secs.dataitems.OFLACK.ACK` |
        +-------+---------------------+--------------------------------------------+
        | 1-63  | Reserved            |                                            |
        +-------+---------------------+--------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F16 <secsgem.secs.functions.SecsS01F16>`
    """
    name = "OFLACK"

    ACK = 0

    def __init__(self):
        super(self.__class__, self).__init__(1)

class ONLACK(SecsVarBinary):
    """Acknowledge code for ONLINE request

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+--------------------+---------------------------------------------------+
        | Value | Description        | Constant                                          |
        +=======+====================+===================================================+
        | 0     | ONLINE Accepted    | :const:`secsgem.secs.dataitems.ONLACK.ACCEPTED`   |
        +-------+--------------------+---------------------------------------------------+
        | 1     | ONLINE Not allowed | :const:`secsgem.secs.dataitems.ONLACK.NOTALLOWED` |
        +-------+--------------------+---------------------------------------------------+
        | 2     | Already ONLINE     | :const:`secsgem.secs.dataitems.ONLACK.ALREADYON`  |
        +-------+--------------------+---------------------------------------------------+
        | 3-63  | Reserved           |                                                   |
        +-------+--------------------+---------------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F18 <secsgem.secs.functions.SecsS01F18>`
    """
    name = "ONLACK"

    ACCEPTED = 0
    NOTALLOWED = 1
    ALREADYON = 2

    def __init__(self):
        super(self.__class__, self).__init__(1)

class SV(SecsVarDynamic):
    """Status variable value

    :Types:
       - :class:`SecsVarArray <secsgem.secs.variables.SecsVarArray>`
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       - :class:`SecsVarBoolean <secsgem.secs.variables.SecsVarBoolean>`
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`
       - :class:`SecsVarF8 <secsgem.secs.variables.SecsVarF8>`
       - :class:`SecsVarF4 <secsgem.secs.variables.SecsVarF4>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS01F04 <secsgem.secs.functions.SecsS01F04>`
        - :class:`SecsS06F01 <secsgem.secs.functions.SecsS06F01>`
    """
    name = "SV"

    def __init__(self):
        super(self.__class__, self).__init__([])

class SVID(SecsVarDynamic):
    """Status variable ID

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS01F03 <secsgem.secs.functions.SecsS01F03>`
        - :class:`SecsS01F11 <secsgem.secs.functions.SecsS01F11>`
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
        - :class:`SecsS02F23 <secsgem.secs.functions.SecsS02F23>`
    """
    name = "SVID"

    def __init__(self):
        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8], 1)

class SVNAME(SecsVarString):
    """Status variable name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
    """
    name = "SVNAME"

    def __init__(self):
        super(self.__class__, self).__init__()

class UNITS(SecsVarString):
    """Status variable name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
        - :class:`SecsS02F48 <secsgem.secs.functions.SecsS02F48>`
        - :class:`SecsS07F22 <secsgem.secs.functions.SecsS07F22>`
    """
    name = "UNITS"

    def __init__(self):
        super(self.__class__, self).__init__()
