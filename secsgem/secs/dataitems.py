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

class ACKC5(SecsVarBinary):
    """Acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+------------------------------------------------+
        | Value | Description       | Constant                                       |
        +=======+===================+================================================+
        | 0     | Accepted          | :const:`secsgem.secs.dataitems.ACKC5.ACCEPTED` |
        +-------+-------------------+------------------------------------------------+
        | 1-63  | Error             | :const:`secsgem.secs.dataitems.ACKC5.ERROR`    |
        +-------+-------------------+------------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F02 <secsgem.secs.functions.SecsS05F02>`
        - :class:`SecsS05F04 <secsgem.secs.functions.SecsS05F04>`

    """
    ACCEPTED = 0
    ERROR = 1

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class ACKC6(SecsVarBinary):
    """Acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+------------------------------------------------+
        | Value | Description       | Constant                                       |
        +=======+===================+================================================+
        | 0     | Accepted          | :const:`secsgem.secs.dataitems.ACKC6.ACCEPTED` |
        +-------+-------------------+------------------------------------------------+
        | 1-63  | Error             | :const:`secsgem.secs.dataitems.ACKC6.ERROR`    |
        +-------+-------------------+------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F02 <secsgem.secs.functions.SecsS06F02>`
        - :class:`SecsS06F04 <secsgem.secs.functions.SecsS06F04>`
        - :class:`SecsS06F10 <secsgem.secs.functions.SecsS06F10>`
        - :class:`SecsS06F12 <secsgem.secs.functions.SecsS06F12>`
        - :class:`SecsS06F14 <secsgem.secs.functions.SecsS06F14>`

    """
    ACCEPTED = 0
    ERROR = 1

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class ALCD(SecsVarBinary):
    """Alarm code byte

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------------+--------------------------------------------------------------+
        | Value | Description               | Constant                                                     |
        +=======+===========================+==============================================================+
        | 0     | Not used                  |                                                              |
        +-------+---------------------------+--------------------------------------------------------------+
        | 1     | Personal safety           | :const:`secsgem.secs.dataitems.ALCD.PERSONALSAFETY`          |
        +-------+---------------------------+--------------------------------------------------------------+
        | 2     | Equipment safety          | :const:`secsgem.secs.dataitems.ALCD.EQUIPMENTSAFETY`         |
        +-------+---------------------------+--------------------------------------------------------------+
        | 3     | Parameter control warning | :const:`secsgem.secs.dataitems.ALCD.PARAMETERCONTROLWARNING` |
        +-------+---------------------------+--------------------------------------------------------------+
        | 4     | Parameter control error   | :const:`secsgem.secs.dataitems.ALCD.PARAMETERCONTROLERROR`   |
        +-------+---------------------------+--------------------------------------------------------------+
        | 5     | Irrecoverable error       | :const:`secsgem.secs.dataitems.ALCD.IRRECOVERABLEERROR`      |
        +-------+---------------------------+--------------------------------------------------------------+
        | 6     | Equipment status warning  | :const:`secsgem.secs.dataitems.ALCD.EQUIPMENTSTATUSWARNING`  |
        +-------+---------------------------+--------------------------------------------------------------+
        | 7     | Attention flags           | :const:`secsgem.secs.dataitems.ALCD.ATTENTIONFLAGS`          |
        +-------+---------------------------+--------------------------------------------------------------+
        | 8     | Data integrity            | :const:`secsgem.secs.dataitems.ALCD.DATAINTEGRITY`           |
        +-------+---------------------------+--------------------------------------------------------------+
        | 2-63  | Other catogories          |                                                              |
        +-------+---------------------------+--------------------------------------------------------------+
        | 128   | Alarm set flag            | :const:`secsgem.secs.dataitems.ALCD.ALARMSET`                |
        +-------+---------------------------+--------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`

    """
    PERSONALSAFETY = 1
    EQUIPMENTSAFETY = 2
    PARAMETERCONTROLWARNING = 3
    PARAMETERCONTROLERROR = 4
    IRRECOVERABLEERROR = 5
    EQUIPMENTSTATUSWARNING = 6
    ATTENTIONFLAGS = 7
    DATAINTEGRITY = 8
    ALARMSET = 128

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class ALID(SecsVarDynamic):
    """Alarm ID

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F03 <secsgem.secs.functions.SecsS05F03>`
        - :class:`SecsS05F05 <secsgem.secs.functions.SecsS05F05>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class ALTX(SecsVarString):
    """Alarm ID

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(120)


class CEED(SecsVarBoolean):
    """Collection event or trace enable/disable code

       :Types: :class:`SecsVarBoolean <secsgem.secs.variables.SecsVarBoolean>`
       :Length: 1

    **Values**
        +-------+---------+
        | Value | State   |
        +=======+=========+
        | True  | Enable  |
        +-------+---------+
        | False | Disable |
        +-------+---------+

    **Used In Function**
        - :class:`SecsS02F37 <secsgem.secs.functions.SecsS02F37>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`

    """

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class CEID(SecsVarDynamic):
    """Collection event ID

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
        - :class:`SecsS02F35 <secsgem.secs.functions.SecsS02F35>`
        - :class:`SecsS02F37 <secsgem.secs.functions.SecsS02F37>`
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`
        - :class:`SecsS06F09 <secsgem.secs.functions.SecsS06F09>`
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F15 <secsgem.secs.functions.SecsS06F15>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F17 <secsgem.secs.functions.SecsS06F17>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`
        - :class:`SecsS17F09 <secsgem.secs.functions.SecsS17F09>`
        - :class:`SecsS17F10 <secsgem.secs.functions.SecsS17F10>`
        - :class:`SecsS17F11 <secsgem.secs.functions.SecsS17F11>`
        - :class:`SecsS17F12 <secsgem.secs.functions.SecsS17F12>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


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
    ACCEPTED = 0
    DENIED = 1

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class CPACK(SecsVarBinary):
    """Command parameter acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+------------------------+----------------------------------------------------------+
        | Value | Description            | Constant                                                 |
        +=======+========================+==========================================================+
        | 1     | Parameter name unknown | :const:`secsgem.secs.dataitems.CPACK.PARAMETERUNKNOWN`   |
        +-------+------------------------+----------------------------------------------------------+
        | 2     | CPVAL value illegal    | :const:`secsgem.secs.dataitems.CPACK.CPVALILLEGALVALUE`  |
        +-------+------------------------+----------------------------------------------------------+
        | 3     | CPVAL format illegal   | :const:`secsgem.secs.dataitems.CPACK.CPVALILLEGALFORMAT` |
        +-------+------------------------+----------------------------------------------------------+
        | 4-63  | Reserved               |                                                          |
        +-------+------------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
    """
    PARAMETERUNKNOWN = 1
    CPVALILLEGALVALUE = 2
    CPVALILLEGALFORMAT = 3

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class CPNAME(SecsVarDynamic):
    """Command parameter name

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
        - :class:`SecsS02F41 <secsgem.secs.functions.SecsS02F41>`
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS02F50 <secsgem.secs.functions.SecsS02F50>`
        - :class:`SecsS04F21 <secsgem.secs.functions.SecsS04F21>`
        - :class:`SecsS04F29 <secsgem.secs.functions.SecsS04F29>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F27 <secsgem.secs.functions.SecsS16F27>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class CPVAL(SecsVarDynamic):
    """Command parameter name

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       - :class:`SecsVarBoolean <secsgem.secs.variables.SecsVarBoolean>`
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
        - :class:`SecsS02F41 <secsgem.secs.functions.SecsS02F41>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS04F21 <secsgem.secs.functions.SecsS04F21>`
        - :class:`SecsS04F29 <secsgem.secs.functions.SecsS04F29>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F27 <secsgem.secs.functions.SecsS16F27>`
        - :class:`SecsS18F13 <secsgem.secs.functions.SecsS18F13>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarBinary, SecsVarBoolean, SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class DATAID(SecsVarDynamic):
    """Data ID

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
        - :class:`SecsS02F33 <secsgem.secs.functions.SecsS02F33>`
        - :class:`SecsS02F35 <secsgem.secs.functions.SecsS02F35>`
        - :class:`SecsS02F39 <secsgem.secs.functions.SecsS02F39>`
        - :class:`SecsS02F45 <secsgem.secs.functions.SecsS02F45>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS03F15 <secsgem.secs.functions.SecsS03F15>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS04F19 <secsgem.secs.functions.SecsS04F19>`
        - :class:`SecsS04F25 <secsgem.secs.functions.SecsS04F25>`
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F05 <secsgem.secs.functions.SecsS06F05>`
        - :class:`SecsS06F07 <secsgem.secs.functions.SecsS06F07>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`
        - :class:`SecsS06F09 <secsgem.secs.functions.SecsS06F09>`
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS06F27 <secsgem.secs.functions.SecsS06F27>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS13F13 <secsgem.secs.functions.SecsS13F13>`
        - :class:`SecsS13F15 <secsgem.secs.functions.SecsS13F15>`
        - :class:`SecsS14F19 <secsgem.secs.functions.SecsS14F19>`
        - :class:`SecsS14F21 <secsgem.secs.functions.SecsS14F21>`
        - :class:`SecsS14F23 <secsgem.secs.functions.SecsS14F23>`
        - :class:`SecsS15F27 <secsgem.secs.functions.SecsS15F27>`
        - :class:`SecsS15F29 <secsgem.secs.functions.SecsS15F29>`
        - :class:`SecsS15F33 <secsgem.secs.functions.SecsS15F33>`
        - :class:`SecsS15F35 <secsgem.secs.functions.SecsS15F35>`
        - :class:`SecsS15F37 <secsgem.secs.functions.SecsS15F37>`
        - :class:`SecsS15F39 <secsgem.secs.functions.SecsS15F39>`
        - :class:`SecsS15F41 <secsgem.secs.functions.SecsS15F41>`
        - :class:`SecsS15F43 <secsgem.secs.functions.SecsS15F43>`
        - :class:`SecsS15F45 <secsgem.secs.functions.SecsS15F45>`
        - :class:`SecsS15F47 <secsgem.secs.functions.SecsS15F47>`
        - :class:`SecsS15F49 <secsgem.secs.functions.SecsS15F49>`
        - :class:`SecsS16F01 <secsgem.secs.functions.SecsS16F01>`
        - :class:`SecsS16F03 <secsgem.secs.functions.SecsS16F03>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F11 <secsgem.secs.functions.SecsS16F11>`
        - :class:`SecsS16F13 <secsgem.secs.functions.SecsS16F13>`
        - :class:`SecsS17F01 <secsgem.secs.functions.SecsS17F01>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`
        - :class:`SecsS17F09 <secsgem.secs.functions.SecsS17F09>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class DATALENGTH(SecsVarDynamic):
    """Length of data to be sent

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS02F39 <secsgem.secs.functions.SecsS02F39>`
        - :class:`SecsS03F15 <secsgem.secs.functions.SecsS03F15>`
        - :class:`SecsS03F29 <secsgem.secs.functions.SecsS03F29>`
        - :class:`SecsS03F31 <secsgem.secs.functions.SecsS03F31>`
        - :class:`SecsS04F25 <secsgem.secs.functions.SecsS04F25>`
        - :class:`SecsS06F05 <secsgem.secs.functions.SecsS06F05>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS14F23 <secsgem.secs.functions.SecsS14F23>`
        - :class:`SecsS16F01 <secsgem.secs.functions.SecsS16F01>`
        - :class:`SecsS16F11 <secsgem.secs.functions.SecsS16F11>`
        - :class:`SecsS18F05 <secsgem.secs.functions.SecsS18F05>`
        - :class:`SecsS18F07 <secsgem.secs.functions.SecsS18F07>`
        - :class:`SecsS19F19 <secsgem.secs.functions.SecsS19F19>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class DRACK(SecsVarBinary):
    """Define report acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------------------+---------------------------------------------------------+
        | Value | Description                   | Constant                                                |
        +=======+===============================+=========================================================+
        | 0     | Acknowledge                   | :const:`secsgem.secs.dataitems.DRACK.ACK`               |
        +-------+-------------------------------+---------------------------------------------------------+
        | 1     | Denied, insufficient space    | :const:`secsgem.secs.dataitems.DRACK.INSUFFICIENTSPACE` |
        +-------+-------------------------------+---------------------------------------------------------+
        | 2     | Denied, invalid format        | :const:`secsgem.secs.dataitems.DRACK.INVALIDFORMAT`     |
        +-------+-------------------------------+---------------------------------------------------------+
        | 3     | Denied, RPTID already defined | :const:`secsgem.secs.dataitems.DRACK.RPTIDREDEFINED`    |
        +-------+-------------------------------+---------------------------------------------------------+
        | 4     | Denied, VID doesn't exist     | :const:`secsgem.secs.dataitems.DRACK.VIDUNKNOWN`        |
        +-------+-------------------------------+---------------------------------------------------------+
        | 5-63  | Reserved, other errors        |                                                         |
        +-------+-------------------------------+---------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F34 <secsgem.secs.functions.SecsS02F34>`
    """
    ACK = 0
    INSUFFICIENTSPACE = 1
    INVALIDFORMAT = 2
    RPTIDREDEFINED = 3
    VIDUNKNOWN = 4

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class DSID(SecsVarDynamic):
    """Data set ID

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
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`
        - :class:`SecsS06F09 <secsgem.secs.functions.SecsS06F09>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class DVNAME(SecsVarDynamic):
    """Data value name

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
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class DVVAL(SecsVarDynamic):
    """Data value

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
        - :class:`SecsS06F03 <secsgem.secs.functions.SecsS06F03>`
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`
        - :class:`SecsS06F09 <secsgem.secs.functions.SecsS06F09>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([])


class EAC(SecsVarBinary):
    """Equipment acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------------------+-----------------------------------------------------+
        | Value | Description                     | Constant                                            |
        +=======+=================================+=====================================================+
        | 0     | Acknowledge                     | :const:`secsgem.secs.dataitems.EAC.ACK`             |
        +-------+---------------------------------+-----------------------------------------------------+
        | 1     | Denied, not all constants exist | :const:`secsgem.secs.dataitems.EAC.INVALIDCONSTANT` |
        +-------+---------------------------------+-----------------------------------------------------+
        | 2     | Denied, busy                    | :const:`secsgem.secs.dataitems.EAC.BUSY`            |
        +-------+---------------------------------+-----------------------------------------------------+
        | 3     | Denied, constant out of range   | :const:`secsgem.secs.dataitems.EAC.OUTOFRANGE`      |
        +-------+---------------------------------+-----------------------------------------------------+
        | 4-63  | Reserved, equipment specific    |                                                     |
        +-------+---------------------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F16 <secsgem.secs.functions.SecsS02F16>`
    """
    ACK = 0
    INVALIDCONSTANT = 1
    BUSY = 2
    OUTOFRANGE = 3

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class ECDEF(SecsVarDynamic):
    """Equipment constant default value

    :Types:
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
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarBinary, SecsVarBoolean, SecsVarString, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4])


class ECID(SecsVarDynamic):
    """Equipment constant ID

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
        - :class:`SecsS02F13 <secsgem.secs.functions.SecsS02F13>`
        - :class:`SecsS02F15 <secsgem.secs.functions.SecsS02F15>`
        - :class:`SecsS02F29 <secsgem.secs.functions.SecsS02F29>`
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class ECMAX(SecsVarDynamic):
    """Equipment constant maximum value

    :Types:
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
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarBinary, SecsVarBoolean, SecsVarString, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4])


class ECMIN(SecsVarDynamic):
    """Equipment constant minimum value

    :Types:
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
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarBinary, SecsVarBoolean, SecsVarString, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4])


class ECNAME(SecsVarString):
    """Equipment constant name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__()


class ECV(SecsVarDynamic):
    """Equipment constant value

    :Types:
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
        - :class:`SecsS02F14 <secsgem.secs.functions.SecsS02F14>`
        - :class:`SecsS02F15 <secsgem.secs.functions.SecsS02F15>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarBinary, SecsVarBoolean, SecsVarString, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4])


class ERACK(SecsVarBinary):
    """Enable/disable event report acknowledge

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+----------------------------+---------------------------------------------------+
        | Value | Description                | Constant                                          |
        +=======+============================+===================================================+
        | 0     | Accepted                   | :const:`secsgem.secs.dataitems.ERACK.ACCEPTED`    |
        +-------+----------------------------+---------------------------------------------------+
        | 1     | Denied, CEID doesn't exist | :const:`secsgem.secs.dataitems.ERACK.CEIDUNKNOWN` |
        +-------+----------------------------+---------------------------------------------------+
        | 2-63  | Reserved                   |                                                   |
        +-------+----------------------------+---------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F38 <secsgem.secs.functions.SecsS02F38>`

    """
    ACCEPTED = 0
    CEIDUNKNOWN = 1

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class GRANT6(SecsVarBinary):
    """Permission to send

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+----------------+------------------------------------------------------+
        | Value | Description    | Constant                                             |
        +=======+================+======================================================+
        | 0     | Granted        | :const:`secsgem.secs.dataitems.GRANT6.GRANTED`       |
        +-------+----------------+------------------------------------------------------+
        | 1     | Busy           | :const:`secsgem.secs.dataitems.GRANT6.BUSY`          |
        +-------+----------------+------------------------------------------------------+
        | 2     | Not interested | :const:`secsgem.secs.dataitems.GRANT6.NOTINTERESTED` |
        +-------+----------------+------------------------------------------------------+
        | 3-63  | Other error    |                                                      |
        +-------+----------------+------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F06 <secsgem.secs.functions.SecsS06F06>`
    """
    GRANTED = 0
    BUSY = 1
    NOTINTERESTED = 2

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class HCACK(SecsVarBinary):
    """Host command parameter acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+--------------------------------+----------------------------------------------------------+
        | Value | Description                    | Constant                                                 |
        +=======+================================+==========================================================+
        | 0     | Acknowledge                    | :const:`secsgem.secs.dataitems.HCACK.ACK`                |
        +-------+--------------------------------+----------------------------------------------------------+
        | 1     | Denied, invalid command        | :const:`secsgem.secs.dataitems.HCACK.INVALIDCOMMAND`     |
        +-------+--------------------------------+----------------------------------------------------------+
        | 2     | Denied, cannot perform now     | :const:`secsgem.secs.dataitems.HCACK.CANTPERFORMNOW`     |
        +-------+--------------------------------+----------------------------------------------------------+
        | 3     | Denied, parameter invalid      | :const:`secsgem.secs.dataitems.HCACK.PARAMETERINVALID`   |
        +-------+--------------------------------+----------------------------------------------------------+
        | 4     | Acknowledge, will finish later | :const:`secsgem.secs.dataitems.HCACK.ACKFINISHLATER`     |
        +-------+--------------------------------+----------------------------------------------------------+
        | 5     | Rejected, already in condition | :const:`secsgem.secs.dataitems.HCACK.ALREADYINCONDITION` |
        +-------+--------------------------------+----------------------------------------------------------+
        | 6     | No such object                 | :const:`secsgem.secs.dataitems.HCACK.NOOBJECT`           |
        +-------+--------------------------------+----------------------------------------------------------+
        | 7-63  | Reserved                       |                                                          |
        +-------+--------------------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
        - :class:`SecsS02F50 <secsgem.secs.functions.SecsS02F50>`

    """
    ACK = 0
    INVALIDCOMMAND = 1
    CANTPERFORMNOW = 2
    PARAMETERINVALID = 3
    ACKFINISHLATER = 4
    ALREADYINCONDITION = 5
    NOOBJECT = 6

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class LRACK(SecsVarBinary):
    """Link report acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-----------------------------+---------------------------------------------------------+
        | Value | Description                 | Constant                                                |
        +=======+=============================+=========================================================+
        | 0     | Acknowledge                 | :const:`secsgem.secs.dataitems.LRACK.ACK`               |
        +-------+-----------------------------+---------------------------------------------------------+
        | 1     | Denied, insufficient space  | :const:`secsgem.secs.dataitems.LRACK.INSUFFICIENTSPACE` |
        +-------+-----------------------------+---------------------------------------------------------+
        | 2     | Denied, invalid format      | :const:`secsgem.secs.dataitems.LRACK.INVALIDFORMAT`     |
        +-------+-----------------------------+---------------------------------------------------------+
        | 3     | Denied, CEID already linked | :const:`secsgem.secs.dataitems.LRACK.CEIDLINKED`        |
        +-------+-----------------------------+---------------------------------------------------------+
        | 4     | Denied, CEID doesn't exist  | :const:`secsgem.secs.dataitems.LRACK.CEIDUNKNOWN`       |
        +-------+-----------------------------+---------------------------------------------------------+
        | 5     | Denied, RPTID doesn't exist | :const:`secsgem.secs.dataitems.LRACK.RPTIDUNKNOWN`      |
        +-------+-----------------------------+---------------------------------------------------------+
        | 6-63  | Reserved, other errors      |                                                         |
        +-------+-----------------------------+---------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F36 <secsgem.secs.functions.SecsS02F36>`
    """
    ACK = 0
    INSUFFICIENTSPACE = 1
    INVALIDFORMAT = 2
    CEIDLINKED = 3
    CEIDUNKNOWN = 4
    RPTIDUNKNOWN = 5

    def __init__(self):
        self.name = self.__class__.__name__

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
    ACK = 0

    def __init__(self):
        self.name = self.__class__.__name__

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
    ACCEPTED = 0
    NOTALLOWED = 1
    ALREADYON = 2

    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(1)


class RCMD(SecsVarDynamic):
    """Remote command

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS02F21 <secsgem.secs.functions.SecsS02F21>`
        - :class:`SecsS02F41 <secsgem.secs.functions.SecsS02F41>`
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarI1])


class RPTID(SecsVarDynamic):
    """Report ID

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
        - :class:`SecsS02F33 <secsgem.secs.functions.SecsS02F33>`
        - :class:`SecsS02F35 <secsgem.secs.functions.SecsS02F35>`
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS06F19 <secsgem.secs.functions.SecsS06F19>`
        - :class:`SecsS06F21 <secsgem.secs.functions.SecsS06F21>`
        - :class:`SecsS06F27 <secsgem.secs.functions.SecsS06F27>`
        - :class:`SecsS06F30 <secsgem.secs.functions.SecsS06F30>`
        - :class:`SecsS17F01 <secsgem.secs.functions.SecsS17F01>`
        - :class:`SecsS17F02 <secsgem.secs.functions.SecsS17F02>`
        - :class:`SecsS17F03 <secsgem.secs.functions.SecsS17F03>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F05 <secsgem.secs.functions.SecsS17F05>`
        - :class:`SecsS17F09 <secsgem.secs.functions.SecsS17F09>`
        - :class:`SecsS17F11 <secsgem.secs.functions.SecsS17F11>`
        - :class:`SecsS17F12 <secsgem.secs.functions.SecsS17F12>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


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
    def __init__(self):
        self.name = self.__class__.__name__

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
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


class SVNAME(SecsVarString):
    """Status variable name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__()


class TIME(SecsVarString):
    """Time of day

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F18 <secsgem.secs.functions.SecsS02F18>`
        - :class:`SecsS02F31 <secsgem.secs.functions.SecsS02F31>`
    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__(32)


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
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__()

class V(SecsVarDynamic):
    """Variable data

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
        - :class:`SecsS06F11 <secsgem.secs.functions.SecsS06F11>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F16 <secsgem.secs.functions.SecsS06F16>`
        - :class:`SecsS06F20 <secsgem.secs.functions.SecsS06F20>`
        - :class:`SecsS06F22 <secsgem.secs.functions.SecsS06F22>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([])


class VID(SecsVarDynamic):
    """Variable ID

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
        - :class:`SecsS02F33 <secsgem.secs.functions.SecsS02F33>`
        - :class:`SecsS02F45 <secsgem.secs.functions.SecsS02F45>`
        - :class:`SecsS02F46 <secsgem.secs.functions.SecsS02F46>`
        - :class:`SecsS02F47 <secsgem.secs.functions.SecsS02F47>`
        - :class:`SecsS02F48 <secsgem.secs.functions.SecsS02F48>`
        - :class:`SecsS06F13 <secsgem.secs.functions.SecsS06F13>`
        - :class:`SecsS06F18 <secsgem.secs.functions.SecsS06F18>`
        - :class:`SecsS06F22 <secsgem.secs.functions.SecsS06F22>`
        - :class:`SecsS17F01 <secsgem.secs.functions.SecsS17F01>`

    """
    def __init__(self):
        self.name = self.__class__.__name__

        super(self.__class__, self).__init__([SecsVarString, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8])


