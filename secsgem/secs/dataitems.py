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
# pylint: disable=I0011, W0233
"""Data items for functions"""

from __future__ import absolute_import
from future.utils import with_metaclass

from .variables import SecsVarArray, SecsVarString, SecsVarBinary, \
    SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarF4, SecsVarF8, SecsVarU1, \
    SecsVarU2, SecsVarU4, SecsVarU8, SecsVarBoolean, SecsVarDynamic

# DataItemMeta adds __type__ member as base class
class DataItemMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name != "DataItemBase":
            bases += (attrs["__type__"], )
        return type.__new__(mcs, name, bases, attrs)

# DataItemBase initializes __type__ member as base class and provides get_format
class DataItemBase(with_metaclass(DataItemMeta)):
    __type__ = None
    __allowedtypes__ = None
    __count__ = -1

    def __init__(self, value=None):
        self.name = self.__class__.__name__

        if self.__type__ is SecsVarDynamic:
            self.__type__.__init__(self, self.__allowedtypes__, value, self.__count__)
        else:
            self.__type__.__init__(self, value, self.__count__)

    @classmethod
    def get_format(cls, showname=True):
        if showname:
            clsname = format(cls.__name__)
        else:
            clsname = "DATA"

        if cls.__type__ is SecsVarDynamic:
            if cls.__count__ > 0:
                return "{}: {}[{}]".format(clsname, "/".join([x.textCode for x in cls.__allowedtypes__]), cls.__count__)
            else:
                return "{}: {}".format(clsname, "/".join([x.textCode for x in cls.__allowedtypes__]))
        else:
            if cls.__count__ > 0:
                return "{}: {}[{}]".format(clsname, cls.textCode, cls.__count__)
            else:
                return "{}: {}".format(clsname, cls.textCode)


class ACKC5(DataItemBase):
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

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    ERROR = 1


class ACKC6(DataItemBase):
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

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    ERROR = 1


class ACKC7(DataItemBase):
    """Acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+------------------------+--------------------------------------------------------+
        | Value | Description            | Constant                                               |
        +=======+========================+========================================================+
        | 0     | Accepted               | :const:`secsgem.secs.dataitems.ACKC7.ACCEPTED`         |
        +-------+------------------------+--------------------------------------------------------+
        | 1     | Permission not granted | :const:`secsgem.secs.dataitems.ACKC7.NO_PERMISSION`    |
        +-------+------------------------+--------------------------------------------------------+
        | 2     | Length error           | :const:`secsgem.secs.dataitems.ACKC7.LENGTH_ERROR`     |
        +-------+------------------------+--------------------------------------------------------+
        | 3     | Matrix overflow        | :const:`secsgem.secs.dataitems.ACKC7.MATRIX_OVERFLOW`  |
        +-------+------------------------+--------------------------------------------------------+
        | 4     | PPID not found         | :const:`secsgem.secs.dataitems.ACKC7.PPID_NOT_FOUND`   |
        +-------+------------------------+--------------------------------------------------------+
        | 5     | Mode unsupported       | :const:`secsgem.secs.dataitems.ACKC7.MODE_UNSUPPORTED` |
        +-------+------------------------+--------------------------------------------------------+
        | 6     | Performed later        | :const:`secsgem.secs.dataitems.ACKC7.PERFORMED_LATER`  |
        +-------+------------------------+--------------------------------------------------------+
        | 7-63  | Reserved               |                                                        |
        +-------+------------------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS07F04 <secsgem.secs.functions.SecsS07F04>`
        - :class:`SecsS07F12 <secsgem.secs.functions.SecsS07F12>`
        - :class:`SecsS07F14 <secsgem.secs.functions.SecsS07F14>`
        - :class:`SecsS07F16 <secsgem.secs.functions.SecsS07F16>`
        - :class:`SecsS07F18 <secsgem.secs.functions.SecsS07F18>`
        - :class:`SecsS07F24 <secsgem.secs.functions.SecsS07F24>`
        - :class:`SecsS07F32 <secsgem.secs.functions.SecsS07F32>`
        - :class:`SecsS07F38 <secsgem.secs.functions.SecsS07F38>`
        - :class:`SecsS07F40 <secsgem.secs.functions.SecsS07F40>`
        - :class:`SecsS07F42 <secsgem.secs.functions.SecsS07F42>`
        - :class:`SecsS07F44 <secsgem.secs.functions.SecsS07F44>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    NO_PERMISSION = 1
    LENGTH_ERROR = 2
    MATRIX_OVERFLOW = 3
    PPID_NOT_FOUND = 4
    MODE_UNSUPPORTED = 5
    PERFORMED_LATER = 6


class ACKC10(DataItemBase):
    """Acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+------------------------+---------------------------------------------------------------+
        | Value | Description            | Constant                                                      |
        +=======+========================+===============================================================+
        | 0     | Accepted               | :const:`secsgem.secs.dataitems.ACKC10.ACCEPTED`               |
        +-------+------------------------+---------------------------------------------------------------+
        | 1     | Will not be displayed  | :const:`secsgem.secs.dataitems.ACKC10.NOT_DISPLAYED`          |
        +-------+------------------------+---------------------------------------------------------------+
        | 2     | Terminal not available | :const:`secsgem.secs.dataitems.ACKC10.TERMINAL_NOT_AVAILABLE` |
        +-------+------------------------+---------------------------------------------------------------+
        | 3-63  | Other error            |                                                               |
        +-------+------------------------+---------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS10F02 <secsgem.secs.functions.SecsS10F02>`
        - :class:`SecsS10F04 <secsgem.secs.functions.SecsS10F04>`
        - :class:`SecsS10F06 <secsgem.secs.functions.SecsS10F06>`
        - :class:`SecsS10F10 <secsgem.secs.functions.SecsS10F10>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    NOT_DISPLAYED = 1
    TERMINAL_NOT_AVAILABLE = 2


class ACKA(DataItemBase):
    """Request success

       :Types: :class:`SecsVarBoolean <secsgem.secs.variables.SecsVarBoolean>`
       :Length: 1

    **Values**
        +-------+---------+
        | Value |         |
        +=======+=========+
        | True  | Success |
        +-------+---------+
        | False | Failed  |
        +-------+---------+

    **Used In Function**
        - :class:`SecsS05F14 <secsgem.secs.functions.SecsS05F14>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS05F18 <secsgem.secs.functions.SecsS05F18>`
        - :class:`SecsS16F02 <secsgem.secs.functions.SecsS16F02>`
        - :class:`SecsS16F04 <secsgem.secs.functions.SecsS16F04>`
        - :class:`SecsS16F06 <secsgem.secs.functions.SecsS16F06>`
        - :class:`SecsS16F12 <secsgem.secs.functions.SecsS16F12>`
        - :class:`SecsS16F14 <secsgem.secs.functions.SecsS16F14>`
        - :class:`SecsS16F16 <secsgem.secs.functions.SecsS16F16>`
        - :class:`SecsS16F18 <secsgem.secs.functions.SecsS16F18>`
        - :class:`SecsS16F24 <secsgem.secs.functions.SecsS16F24>`
        - :class:`SecsS16F26 <secsgem.secs.functions.SecsS16F26>`
        - :class:`SecsS16F28 <secsgem.secs.functions.SecsS16F28>`
        - :class:`SecsS16F30 <secsgem.secs.functions.SecsS16F30>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F08 <secsgem.secs.functions.SecsS17F08>`
        - :class:`SecsS17F14 <secsgem.secs.functions.SecsS17F14>`

    """

    __type__ = SecsVarBoolean
    __count__ = 1


class ALCD(DataItemBase):
    """Alarm code byte

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------------+----------------------------------------------------------------+
        | Value | Description               | Constant                                                       |
        +=======+===========================+================================================================+
        | 0     | Not used                  |                                                                |
        +-------+---------------------------+----------------------------------------------------------------+
        | 1     | Personal safety           | :const:`secsgem.secs.dataitems.ALCD.PERSONAL_SAFETY`           |
        +-------+---------------------------+----------------------------------------------------------------+
        | 2     | Equipment safety          | :const:`secsgem.secs.dataitems.ALCD.EQUIPMENT_SAFETY`          |
        +-------+---------------------------+----------------------------------------------------------------+
        | 3     | Parameter control warning | :const:`secsgem.secs.dataitems.ALCD.PARAMETER_CONTROL_WARNING` |
        +-------+---------------------------+----------------------------------------------------------------+
        | 4     | Parameter control error   | :const:`secsgem.secs.dataitems.ALCD.PARAMETER_CONTROL_ERROR`   |
        +-------+---------------------------+----------------------------------------------------------------+
        | 5     | Irrecoverable error       | :const:`secsgem.secs.dataitems.ALCD.IRRECOVERABLE_ERROR`       |
        +-------+---------------------------+----------------------------------------------------------------+
        | 6     | Equipment status warning  | :const:`secsgem.secs.dataitems.ALCD.EQUIPMENT_STATUS_WARNING`  |
        +-------+---------------------------+----------------------------------------------------------------+
        | 7     | Attention flags           | :const:`secsgem.secs.dataitems.ALCD.ATTENTION_FLAGS`           |
        +-------+---------------------------+----------------------------------------------------------------+
        | 8     | Data integrity            | :const:`secsgem.secs.dataitems.ALCD.DATA_INTEGRITY`            |
        +-------+---------------------------+----------------------------------------------------------------+
        | 9-63  | Other catogories          |                                                                |
        +-------+---------------------------+----------------------------------------------------------------+
        | 128   | Alarm set flag            | :const:`secsgem.secs.dataitems.ALCD.ALARM_SET`                 |
        +-------+---------------------------+----------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    PERSONAL_SAFETY = 1
    EQUIPMENT_SAFETY = 2
    PARAMETER_CONTROL_WARNING = 3
    PARAMETER_CONTROL_ERROR = 4
    IRRECOVERABLE_ERROR = 5
    EQUIPMENT_STATUS_WARNING = 6
    ATTENTION_FLAGS = 7
    DATA_INTEGRITY = 8
    ALARM_SET = 128


class ALED(DataItemBase):
    """Alarm en-/disable code byte

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +---------+-------------+----------------------------------------------+
        | Value   | Description | Constant                                     |
        +=========+=============+==============================================+
        | 0       | Disable     | :const:`secsgem.secs.dataitems.ALED.DISABLE` |
        +---------+-------------+----------------------------------------------+
        | 1-127   | Not used    |                                              |
        +---------+-------------+----------------------------------------------+
        | 128     | Enable      | :const:`secsgem.secs.dataitems.ALED.ENABLE`  |
        +---------+-------------+----------------------------------------------+
        | 129-255 | Not used    |                                              |
        +---------+-------------+----------------------------------------------+

    **Used In Function**
        - :class:`SecsS05F03 <secsgem.secs.functions.SecsS05F03>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    DISABLE = 0
    ENABLE = 128


class ALID(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]


class ALTX(DataItemBase):
    """Alarm ID

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F01 <secsgem.secs.functions.SecsS05F01>`
        - :class:`SecsS05F06 <secsgem.secs.functions.SecsS05F06>`

    """

    __type__ = SecsVarString
    __count__ = 120


class ATTRDATA(DataItemBase):
    """Object attribute value

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
        - :class:`SecsS01F20 <secsgem.secs.functions.SecsS01F20>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS03F18 <secsgem.secs.functions.SecsS03F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F09 <secsgem.secs.functions.SecsS14F09>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F11 <secsgem.secs.functions.SecsS14F11>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F13 <secsgem.secs.functions.SecsS14F13>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F15 <secsgem.secs.functions.SecsS14F15>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F17 <secsgem.secs.functions.SecsS14F17>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS18F02 <secsgem.secs.functions.SecsS18F02>`
        - :class:`SecsS18F03 <secsgem.secs.functions.SecsS18F03>`

    """

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]


class ATTRID(DataItemBase):
    """Object attribute identifier

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS01F19 <secsgem.secs.functions.SecsS01F19>`
        - :class:`SecsS03F17 <secsgem.secs.functions.SecsS03F17>`
        - :class:`SecsS03F18 <secsgem.secs.functions.SecsS03F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F09 <secsgem.secs.functions.SecsS14F09>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F11 <secsgem.secs.functions.SecsS14F11>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F13 <secsgem.secs.functions.SecsS14F13>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F15 <secsgem.secs.functions.SecsS14F15>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F17 <secsgem.secs.functions.SecsS14F17>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS18F01 <secsgem.secs.functions.SecsS18F01>`
        - :class:`SecsS18F03 <secsgem.secs.functions.SecsS18F03>`

    """

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarString]


class ATTRRELN(DataItemBase):
    """Attribute relation to attribute of object

       :Types: :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Values**
        +-------+-----------------------+-----------------------------------------------------+
        | Value | Description           | Constant                                            |
        +=======+=======================+=====================================================+
        | 0     | Equal to              | :const:`secsgem.secs.dataitems.ATTRRELN.EQUAL`      |
        +-------+-----------------------+-----------------------------------------------------+
        | 1     | Not equal to          | :const:`secsgem.secs.dataitems.ATTRRELN.NOT_EQUAL`  |
        +-------+-----------------------+-----------------------------------------------------+
        | 2     | Less than             | :const:`secsgem.secs.dataitems.ATTRRELN.LESS`       |
        +-------+-----------------------+-----------------------------------------------------+
        | 3     | Less than or equal to | :const:`secsgem.secs.dataitems.ATTRRELN.LESS_EQUAL` |
        +-------+-----------------------+-----------------------------------------------------+
        | 4     | More than             | :const:`secsgem.secs.dataitems.ATTRRELN.MORE`       |
        +-------+-----------------------+-----------------------------------------------------+
        | 5     | More than or equal to | :const:`secsgem.secs.dataitems.ATTRRELN.MORE_EQUAL` |
        +-------+-----------------------+-----------------------------------------------------+
        | 6     | Value present         | :const:`secsgem.secs.dataitems.ATTRRELN.PRESENT`    |
        +-------+-----------------------+-----------------------------------------------------+
        | 7     | Value absent          | :const:`secsgem.secs.dataitems.ATTRRELN.ABSENT`     |
        +-------+-----------------------+-----------------------------------------------------+
        | 8-63  | Error                 |                                                     |
        +-------+-----------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`

    """

    __type__ = SecsVarU1

    EQUAL = 0
    NOT_EQUAL = 1
    LESS = 2
    LESS_EQUAL = 3
    MORE = 4
    MORE_EQUAL = 5
    PRESENT = 6
    ABSENT = 7


class BCEQU(DataItemBase):
    """Bin code equivalents

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarString]


class BINLT(DataItemBase):
    """Bin list

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS12F07 <secsgem.secs.functions.SecsS12F07>`
        - :class:`SecsS12F09 <secsgem.secs.functions.SecsS12F09>`
        - :class:`SecsS12F11 <secsgem.secs.functions.SecsS12F11>`
        - :class:`SecsS12F14 <secsgem.secs.functions.SecsS12F14>`
        - :class:`SecsS12F16 <secsgem.secs.functions.SecsS12F16>`
        - :class:`SecsS12F18 <secsgem.secs.functions.SecsS12F18>`

    """

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarString]


class CEED(DataItemBase):
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

    __type__ = SecsVarBoolean
    __count__ = 1


class CEID(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class COLCT(DataItemBase):
    """Column count in dies

    :Types:
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8]


class COMMACK(DataItemBase):
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

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    DENIED = 1


class CPACK(DataItemBase):
    """Command parameter acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+------------------------+------------------------------------------------------------+
        | Value | Description            | Constant                                                   |
        +=======+========================+============================================================+
        | 1     | Parameter name unknown | :const:`secsgem.secs.dataitems.CPACK.PARAMETER_UNKNOWN`    |
        +-------+------------------------+------------------------------------------------------------+
        | 2     | CPVAL value illegal    | :const:`secsgem.secs.dataitems.CPACK.CPVAL_ILLEGAL_VALUE`  |
        +-------+------------------------+------------------------------------------------------------+
        | 3     | CPVAL format illegal   | :const:`secsgem.secs.dataitems.CPACK.CPVAL_ILLEGAL_FORMAT` |
        +-------+------------------------+------------------------------------------------------------+
        | 4-63  | Reserved               |                                                            |
        +-------+------------------------+------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    PARAMETER_UNKNOWN = 1
    CPVAL_ILLEGAL_VALUE = 2
    CPVAL_ILLEGAL_FORMAT = 3


class CPNAME(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class CPVAL(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString, SecsVarBinary]


class DATAID(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class DATALENGTH(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]


class DATLC(DataItemBase):
    """Data location

       :Types: :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS12F19 <secsgem.secs.functions.SecsS12F19>`

    """

    __type__ = SecsVarU1        


class DRACK(DataItemBase):
    """Define report acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------------------+----------------------------------------------------------+
        | Value | Description                   | Constant                                                 |
        +=======+===============================+==========================================================+
        | 0     | Acknowledge                   | :const:`secsgem.secs.dataitems.DRACK.ACK`                |
        +-------+-------------------------------+----------------------------------------------------------+
        | 1     | Denied, insufficient space    | :const:`secsgem.secs.dataitems.DRACK.INSUFFICIENT_SPACE` |
        +-------+-------------------------------+----------------------------------------------------------+
        | 2     | Denied, invalid format        | :const:`secsgem.secs.dataitems.DRACK.INVALID_FORMAT`     |
        +-------+-------------------------------+----------------------------------------------------------+
        | 3     | Denied, RPTID already defined | :const:`secsgem.secs.dataitems.DRACK.RPTID_REDEFINED`    |
        +-------+-------------------------------+----------------------------------------------------------+
        | 4     | Denied, VID doesn't exist     | :const:`secsgem.secs.dataitems.DRACK.VID_UNKNOWN`        |
        +-------+-------------------------------+----------------------------------------------------------+
        | 5-63  | Reserved, other errors        |                                                          |
        +-------+-------------------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F34 <secsgem.secs.functions.SecsS02F34>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0
    INSUFFICIENT_SPACE = 1
    INVALID_FORMAT = 2
    RPTID_REDEFINED = 3
    VID_UNKNOWN = 4


class DSID(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class DUTMS(DataItemBase):
    """Die units of measure

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarString


class DVNAME(DataItemBase):
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

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class DVVAL(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]


class EAC(DataItemBase):
    """Equipment acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------------------+-------------------------------------------------------+
        | Value | Description                     | Constant                                              |
        +=======+=================================+=======================================================+
        | 0     | Acknowledge                     | :const:`secsgem.secs.dataitems.EAC.ACK`               |
        +-------+---------------------------------+-------------------------------------------------------+
        | 1     | Denied, not all constants exist | :const:`secsgem.secs.dataitems.EAC.INVALID_CONSTANT`  |
        +-------+---------------------------------+-------------------------------------------------------+
        | 2     | Denied, busy                    | :const:`secsgem.secs.dataitems.EAC.BUSY`              |
        +-------+---------------------------------+-------------------------------------------------------+
        | 3     | Denied, constant out of range   | :const:`secsgem.secs.dataitems.EAC.OUT_OF_RANGE`      |
        +-------+---------------------------------+-------------------------------------------------------+
        | 4-63  | Reserved, equipment specific    |                                                       |
        +-------+---------------------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F16 <secsgem.secs.functions.SecsS02F16>`
    """

    __type__ = SecsVarBinary    
    __count__ = 1

    ACK = 0
    INVALID_CONSTANT = 1
    BUSY = 2
    OUT_OF_RANGE = 3


class ECDEF(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarBoolean, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4, \
        SecsVarString, SecsVarBinary]


class ECID(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class ECMAX(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarBoolean, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4, \
        SecsVarString, SecsVarBinary]


class ECMIN(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarBoolean, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4, \
        SecsVarString, SecsVarBinary]


class ECNAME(DataItemBase):
    """Equipment constant name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
    """

    __type__ = SecsVarString


class ECV(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarI8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarF8, SecsVarF4, \
        SecsVarU8, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarString, SecsVarBinary]


class EDID(DataItemBase):
    """Expected data identification

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
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
        - :class:`SecsS09F13 <secsgem.secs.functions.SecsS09F13>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString, SecsVarBinary]


class ERACK(DataItemBase):
    """Enable/disable event report acknowledge

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+----------------------------+----------------------------------------------------+
        | Value | Description                | Constant                                           |
        +=======+============================+====================================================+
        | 0     | Accepted                   | :const:`secsgem.secs.dataitems.ERACK.ACCEPTED`     |
        +-------+----------------------------+----------------------------------------------------+
        | 1     | Denied, CEID doesn't exist | :const:`secsgem.secs.dataitems.ERACK.CEID_UNKNOWN` |
        +-------+----------------------------+----------------------------------------------------+
        | 2-63  | Reserved                   |                                                    |
        +-------+----------------------------+----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F38 <secsgem.secs.functions.SecsS02F38>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    CEID_UNKNOWN = 1


class ERRCODE(DataItemBase):
    """Reference point

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`

    **Used In Function**
        - :class:`SecsS01F03 <secsgem.secs.functions.SecsS01F03>`
        - :class:`SecsS01F20 <secsgem.secs.functions.SecsS01F20>`
        - :class:`SecsS03F16 <secsgem.secs.functions.SecsS03F16>`
        - :class:`SecsS03F30 <secsgem.secs.functions.SecsS03F30>`
        - :class:`SecsS03F32 <secsgem.secs.functions.SecsS03F32>`
        - :class:`SecsS04F20 <secsgem.secs.functions.SecsS04F20>`
        - :class:`SecsS04F22 <secsgem.secs.functions.SecsS04F22>`
        - :class:`SecsS04F23 <secsgem.secs.functions.SecsS04F23>`
        - :class:`SecsS04F33 <secsgem.secs.functions.SecsS04F33>`
        - :class:`SecsS04F35 <secsgem.secs.functions.SecsS04F35>`
        - :class:`SecsS05F14 <secsgem.secs.functions.SecsS05F14>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS05F18 <secsgem.secs.functions.SecsS05F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F28 <secsgem.secs.functions.SecsS14F28>`
        - :class:`SecsS15F18 <secsgem.secs.functions.SecsS15F18>`
        - :class:`SecsS15F20 <secsgem.secs.functions.SecsS15F20>`
        - :class:`SecsS15F22 <secsgem.secs.functions.SecsS15F22>`
        - :class:`SecsS15F24 <secsgem.secs.functions.SecsS15F24>`
        - :class:`SecsS15F26 <secsgem.secs.functions.SecsS15F26>`
        - :class:`SecsS15F28 <secsgem.secs.functions.SecsS15F28>`
        - :class:`SecsS15F30 <secsgem.secs.functions.SecsS15F30>`
        - :class:`SecsS15F32 <secsgem.secs.functions.SecsS15F32>`
        - :class:`SecsS15F34 <secsgem.secs.functions.SecsS15F34>`
        - :class:`SecsS15F36 <secsgem.secs.functions.SecsS15F36>`
        - :class:`SecsS15F38 <secsgem.secs.functions.SecsS15F38>`
        - :class:`SecsS15F40 <secsgem.secs.functions.SecsS15F40>`
        - :class:`SecsS15F42 <secsgem.secs.functions.SecsS15F42>`
        - :class:`SecsS15F44 <secsgem.secs.functions.SecsS15F44>`
        - :class:`SecsS15F48 <secsgem.secs.functions.SecsS15F48>`
        - :class:`SecsS15F53 <secsgem.secs.functions.SecsS15F53>`
        - :class:`SecsS16F12 <secsgem.secs.functions.SecsS16F12>`
        - :class:`SecsS16F14 <secsgem.secs.functions.SecsS16F14>`
        - :class:`SecsS16F16 <secsgem.secs.functions.SecsS16F16>`
        - :class:`SecsS16F18 <secsgem.secs.functions.SecsS16F18>`
        - :class:`SecsS16F24 <secsgem.secs.functions.SecsS16F24>`
        - :class:`SecsS16F26 <secsgem.secs.functions.SecsS16F26>`
        - :class:`SecsS16F28 <secsgem.secs.functions.SecsS16F28>`
        - :class:`SecsS17F02 <secsgem.secs.functions.SecsS17F02>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F06 <secsgem.secs.functions.SecsS17F06>`
        - :class:`SecsS17F08 <secsgem.secs.functions.SecsS17F08>`
        - :class:`SecsS17F10 <secsgem.secs.functions.SecsS17F10>`
        - :class:`SecsS17F12 <secsgem.secs.functions.SecsS17F12>`
        - :class:`SecsS17F14 <secsgem.secs.functions.SecsS17F14>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]


class ERRTEXT(DataItemBase):
    """Error description for error code

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F20 <secsgem.secs.functions.SecsS01F20>`
        - :class:`SecsS03F16 <secsgem.secs.functions.SecsS03F16>`
        - :class:`SecsS03F18 <secsgem.secs.functions.SecsS03F18>`
        - :class:`SecsS03F20 <secsgem.secs.functions.SecsS03F20>`
        - :class:`SecsS03F22 <secsgem.secs.functions.SecsS03F22>`
        - :class:`SecsS03F24 <secsgem.secs.functions.SecsS03F24>`
        - :class:`SecsS03F26 <secsgem.secs.functions.SecsS03F26>`
        - :class:`SecsS03F30 <secsgem.secs.functions.SecsS03F30>`
        - :class:`SecsS03F32 <secsgem.secs.functions.SecsS03F32>`
        - :class:`SecsS04F20 <secsgem.secs.functions.SecsS04F20>`
        - :class:`SecsS04F22 <secsgem.secs.functions.SecsS04F22>`
        - :class:`SecsS04F23 <secsgem.secs.functions.SecsS04F23>`
        - :class:`SecsS04F33 <secsgem.secs.functions.SecsS04F33>`
        - :class:`SecsS04F35 <secsgem.secs.functions.SecsS04F35>`
        - :class:`SecsS05F14 <secsgem.secs.functions.SecsS05F14>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS05F18 <secsgem.secs.functions.SecsS05F18>`
        - :class:`SecsS13F14 <secsgem.secs.functions.SecsS13F14>`
        - :class:`SecsS13F16 <secsgem.secs.functions.SecsS13F16>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F28 <secsgem.secs.functions.SecsS14F28>`
        - :class:`SecsS15F28 <secsgem.secs.functions.SecsS15F28>`
        - :class:`SecsS15F30 <secsgem.secs.functions.SecsS15F30>`
        - :class:`SecsS15F32 <secsgem.secs.functions.SecsS15F32>`
        - :class:`SecsS15F34 <secsgem.secs.functions.SecsS15F34>`
        - :class:`SecsS15F36 <secsgem.secs.functions.SecsS15F36>`
        - :class:`SecsS15F38 <secsgem.secs.functions.SecsS15F38>`
        - :class:`SecsS15F40 <secsgem.secs.functions.SecsS15F40>`
        - :class:`SecsS15F42 <secsgem.secs.functions.SecsS15F42>`
        - :class:`SecsS15F44 <secsgem.secs.functions.SecsS15F44>`
        - :class:`SecsS15F48 <secsgem.secs.functions.SecsS15F48>`
        - :class:`SecsS15F53 <secsgem.secs.functions.SecsS15F53>`
        - :class:`SecsS16F12 <secsgem.secs.functions.SecsS16F12>`
        - :class:`SecsS16F14 <secsgem.secs.functions.SecsS16F14>`
        - :class:`SecsS16F16 <secsgem.secs.functions.SecsS16F16>`
        - :class:`SecsS16F18 <secsgem.secs.functions.SecsS16F18>`
        - :class:`SecsS16F24 <secsgem.secs.functions.SecsS16F24>`
        - :class:`SecsS16F26 <secsgem.secs.functions.SecsS16F26>`
        - :class:`SecsS16F28 <secsgem.secs.functions.SecsS16F28>`
        - :class:`SecsS17F04 <secsgem.secs.functions.SecsS17F04>`
        - :class:`SecsS17F08 <secsgem.secs.functions.SecsS17F08>`
        - :class:`SecsS17F14 <secsgem.secs.functions.SecsS17F14>`

    """

    __type__ = SecsVarString
    __count__ = 120


class EXID(DataItemBase):
    """Exception identifier

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem.secs.functions.SecsS05F11>`
        - :class:`SecsS05F13 <secsgem.secs.functions.SecsS05F13>`
        - :class:`SecsS05F14 <secsgem.secs.functions.SecsS05F14>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS05F17 <secsgem.secs.functions.SecsS05F17>`
        - :class:`SecsS05F18 <secsgem.secs.functions.SecsS05F18>`
    """

    __type__ = SecsVarString
    __count__ = 20


class EXMESSAGE(DataItemBase):
    """Exception message

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem.secs.functions.SecsS05F11>`
    """

    __type__ = SecsVarString


class EXRECVRA(DataItemBase):
    """Exception recovery action

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F13 <secsgem.secs.functions.SecsS05F13>`
    """

    __type__ = SecsVarString
    __count__ = 40


class EXTYPE(DataItemBase):
    """Exception type

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem.secs.functions.SecsS05F11>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
    """

    __type__ = SecsVarString


class FFROT(DataItemBase):
    """Film frame rotation

    In degrees from the bottom CW. (Bottom equals zero degrees.) Zero length indicates not used.

       :Types: :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`

    """

    __type__ = SecsVarU2


class FNLOC(DataItemBase):
    """Flat/notch location

    In degrees from the bottom CW. (Bottom equals zero degrees.) Zero length indicates not used.

       :Types: :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarU2


class GRANT6(DataItemBase):
    """Permission to send

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+----------------+-------------------------------------------------------+
        | Value | Description    | Constant                                              |
        +=======+================+=======================================================+
        | 0     | Granted        | :const:`secsgem.secs.dataitems.GRANT6.GRANTED`        |
        +-------+----------------+-------------------------------------------------------+
        | 1     | Busy           | :const:`secsgem.secs.dataitems.GRANT6.BUSY`           |
        +-------+----------------+-------------------------------------------------------+
        | 2     | Not interested | :const:`secsgem.secs.dataitems.GRANT6.NOT_INTERESTED` |
        +-------+----------------+-------------------------------------------------------+
        | 3-63  | Other error    |                                                       |
        +-------+----------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS06F06 <secsgem.secs.functions.SecsS06F06>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    GRANTED = 0
    BUSY = 1
    NOT_INTERESTED = 2


class GRNT1(DataItemBase):
    """Grant code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-----------------------+----------------------------------------------------------+
        | Value | Description           | Constant                                                 |
        +=======+=======================+==========================================================+
        | 0     | Acknowledge           | :const:`secsgem.secs.dataitems.GRNT1.ACK`                |
        +-------+-----------------------+----------------------------------------------------------+
        | 1     | Busy, try again       | :const:`secsgem.secs.dataitems.GRNT1.BUSY`               |
        +-------+-----------------------+----------------------------------------------------------+
        | 2     | No space              | :const:`secsgem.secs.dataitems.GRNT1.NO_SPACE`           |
        +-------+-----------------------+----------------------------------------------------------+
        | 3     | Map too large         | :const:`secsgem.secs.dataitems.GRNT1.MAP_TOO_LARGE`      |
        +-------+-----------------------+----------------------------------------------------------+
        | 4     | Duplicate ID          | :const:`secsgem.secs.dataitems.GRNT1.DUPLICATE_ID`       |
        +-------+-----------------------+----------------------------------------------------------+
        | 5     | Material ID not found | :const:`secsgem.secs.dataitems.GRNT1.MATERIALID_UNKNOWN` |
        +-------+-----------------------+----------------------------------------------------------+
        | 6     | Unknown map format    | :const:`secsgem.secs.dataitems.GRNT1.UNKNOWN_MAP_FORMAT` |
        +-------+-----------------------+----------------------------------------------------------+
        | 7-63  | Reserved, error       |                                                          |
        +-------+-----------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F06 <secsgem.secs.functions.SecsS12F06>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0
    BUSY = 1
    NO_SPACE = 2
    MAP_TOO_LARGE = 3
    DUPLICATE_ID = 4
    MATERIALID_UNKNOWN = 5
    UNKNOWN_MAP_FORMAT = 6


class HCACK(DataItemBase):
    """Host command parameter acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+--------------------------------+------------------------------------------------------------+
        | Value | Description                    | Constant                                                   |
        +=======+================================+============================================================+
        | 0     | Acknowledge                    | :const:`secsgem.secs.dataitems.HCACK.ACK`                  |
        +-------+--------------------------------+------------------------------------------------------------+
        | 1     | Denied, invalid command        | :const:`secsgem.secs.dataitems.HCACK.INVALID_COMMAND`      |
        +-------+--------------------------------+------------------------------------------------------------+
        | 2     | Denied, cannot perform now     | :const:`secsgem.secs.dataitems.HCACK.CANT_PERFORM_NOW`     |
        +-------+--------------------------------+------------------------------------------------------------+
        | 3     | Denied, parameter invalid      | :const:`secsgem.secs.dataitems.HCACK.PARAMETER_INVALID`    |
        +-------+--------------------------------+------------------------------------------------------------+
        | 4     | Acknowledge, will finish later | :const:`secsgem.secs.dataitems.HCACK.ACK_FINISH_LATER`     |
        +-------+--------------------------------+------------------------------------------------------------+
        | 5     | Rejected, already in condition | :const:`secsgem.secs.dataitems.HCACK.ALREADY_IN_CONDITION` |
        +-------+--------------------------------+------------------------------------------------------------+
        | 6     | No such object                 | :const:`secsgem.secs.dataitems.HCACK.NO_OBJECT`            |
        +-------+--------------------------------+------------------------------------------------------------+
        | 7-63  | Reserved                       |                                                            |
        +-------+--------------------------------+------------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F42 <secsgem.secs.functions.SecsS02F42>`
        - :class:`SecsS02F50 <secsgem.secs.functions.SecsS02F50>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0
    INVALID_COMMAND = 1
    CANT_PERFORM_NOW = 2
    PARAMETER_INVALID = 3
    ACK_FINISH_LATER = 4
    ALREADY_IN_CONDITION = 5
    NO_OBJECT = 6


class IDTYP(DataItemBase):
    """ID type

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+------------------------------------------------------+
        | Value | Description       | Constant                                             |
        +=======+===================+======================================================+
        | 0     | Wafer ID          | :const:`secsgem.secs.dataitems.IDTYP.WAFER`          |
        +-------+-------------------+------------------------------------------------------+
        | 1     | Wafer cassette ID | :const:`secsgem.secs.dataitems.IDTYP.WAFER_CASSETTE` |
        +-------+-------------------+------------------------------------------------------+
        | 2     | Film frame ID     | :const:`secsgem.secs.dataitems.IDTYP.FILM_FRAME`     |
        +-------+-------------------+------------------------------------------------------+
        | 3-63  | Reserved, error   |                                                      |
        +-------+-------------------+------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F06>`
        - :class:`SecsS12F07 <secsgem.secs.functions.SecsS12F07>`
        - :class:`SecsS12F09 <secsgem.secs.functions.SecsS12F09>`
        - :class:`SecsS12F11 <secsgem.secs.functions.SecsS12F11>`
        - :class:`SecsS12F13 <secsgem.secs.functions.SecsS12F13>`
        - :class:`SecsS12F14 <secsgem.secs.functions.SecsS12F14>`
        - :class:`SecsS12F15 <secsgem.secs.functions.SecsS12F15>`
        - :class:`SecsS12F16 <secsgem.secs.functions.SecsS12F16>`
        - :class:`SecsS12F17 <secsgem.secs.functions.SecsS12F17>`
        - :class:`SecsS12F18 <secsgem.secs.functions.SecsS12F18>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    WAFER = 0
    WAFER_CASSETTE = 1
    FILM_FRAME = 2


class LENGTH(DataItemBase):
    """Service/process program length

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
        - :class:`SecsS02F01 <secsgem.secs.functions.SecsS02F01>`
        - :class:`SecsS07F01 <secsgem.secs.functions.SecsS07F01>`
        - :class:`SecsS07F29 <secsgem.secs.functions.SecsS07F29>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]


class LRACK(DataItemBase):
    """Link report acknowledge code

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-----------------------------+----------------------------------------------------------+
        | Value | Description                 | Constant                                                 |
        +=======+=============================+==========================================================+
        | 0     | Acknowledge                 | :const:`secsgem.secs.dataitems.LRACK.ACK`                |
        +-------+-----------------------------+----------------------------------------------------------+
        | 1     | Denied, insufficient space  | :const:`secsgem.secs.dataitems.LRACK.INSUFFICIENT_SPACE` |
        +-------+-----------------------------+----------------------------------------------------------+
        | 2     | Denied, invalid format      | :const:`secsgem.secs.dataitems.LRACK.INVALID_FORMAT`     |
        +-------+-----------------------------+----------------------------------------------------------+
        | 3     | Denied, CEID already linked | :const:`secsgem.secs.dataitems.LRACK.CEID_LINKED`        |
        +-------+-----------------------------+----------------------------------------------------------+
        | 4     | Denied, CEID doesn't exist  | :const:`secsgem.secs.dataitems.LRACK.CEID_UNKNOWN`       |
        +-------+-----------------------------+----------------------------------------------------------+
        | 5     | Denied, RPTID doesn't exist | :const:`secsgem.secs.dataitems.LRACK.RPTID_UNKNOWN`      |
        +-------+-----------------------------+----------------------------------------------------------+
        | 6-63  | Reserved, other errors      |                                                          |
        +-------+-----------------------------+----------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F36 <secsgem.secs.functions.SecsS02F36>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0
    INSUFFICIENT_SPACE = 1
    INVALID_FORMAT = 2
    CEID_LINKED = 3
    CEID_UNKNOWN = 4
    RPTID_UNKNOWN = 5


class MAPER(DataItemBase):
    """Map error

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------+----------------------------------------------------+
        | Value | Description   | Constant                                           |
        +=======+===============+====================================================+
        | 0     | ID not found  | :const:`secsgem.secs.dataitems.MAPER.ID_UNKNOWN`   |
        +-------+---------------+----------------------------------------------------+
        | 1     | Invalid data  | :const:`secsgem.secs.dataitems.MAPER.INVALID_DATA` |
        +-------+---------------+----------------------------------------------------+
        | 2     | Format error  | :const:`secsgem.secs.dataitems.MAPER.FORMAT_ERROR` |
        +-------+---------------+----------------------------------------------------+
        | 3-63  | Invalid error |                                                    |
        +-------+---------------+----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F19 <secsgem.secs.functions.SecsS12F19>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    ID_UNKNOWN = 0
    INVALID_DATA = 1
    FORMAT_ERROR = 2


class MAPFT(DataItemBase):
    """Map data format

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+--------------------------------------------------+
        | Value | Description       | Constant                                         |
        +=======+===================+==================================================+
        | 0     | Row format        | :const:`secsgem.secs.dataitems.MAPFT.ROW`        |
        +-------+-------------------+--------------------------------------------------+
        | 1     | Array format      | :const:`secsgem.secs.dataitems.MAPFT.ARRAY`      |
        +-------+-------------------+--------------------------------------------------+
        | 2     | Coordinate format | :const:`secsgem.secs.dataitems.MAPFT.COORDINATE` |
        +-------+-------------------+--------------------------------------------------+
        | 3-63  | Error             |                                                  |
        +-------+-------------------+--------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F05>`
        
    """

    __type__ = SecsVarBinary
    __count__ = 1

    ROW = 0
    ARRAY = 1
    COORDINATE = 2


class MDACK(DataItemBase):
    """Map data acknowledge

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+-------------------+----------------------------------------------------+
        | Value | Description       | Constant                                           |
        +=======+===================+====================================================+
        | 0     | Map received      | :const:`secsgem.secs.dataitems.MDACK.ACK`          |
        +-------+-------------------+----------------------------------------------------+
        | 1     | Format error      | :const:`secsgem.secs.dataitems.MDACK.FORMAT_ERROR` |
        +-------+-------------------+----------------------------------------------------+
        | 2     | No ID match       | :const:`secsgem.secs.dataitems.MDACK.UNKNOWN_ID`   |
        +-------+-------------------+----------------------------------------------------+
        | 3     | Abort/discard map | :const:`secsgem.secs.dataitems.MDACK.ABORT_MAP`    |
        +-------+-------------------+----------------------------------------------------+
        | 4-63  | Reserved, error   |                                                    |
        +-------+-------------------+----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F08 <secsgem.secs.functions.SecsS12F08>`
        - :class:`SecsS12F10 <secsgem.secs.functions.SecsS12F10>`
        - :class:`SecsS12F12 <secsgem.secs.functions.SecsS12F12>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0
    FORMAT_ERROR = 1
    UNKNOWN_ID = 2
    ABORT_MAP = 3


class MDLN(DataItemBase):
    """Equipment model type 

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F02 <secsgem.secs.functions.SecsS01F02>`
        - :class:`SecsS01F13 <secsgem.secs.functions.SecsS01F13>`
        - :class:`SecsS01F14 <secsgem.secs.functions.SecsS01F14>`
        - :class:`SecsS07F22 <secsgem.secs.functions.SecsS07F22>`
        - :class:`SecsS07F23 <secsgem.secs.functions.SecsS07F23>`
        - :class:`SecsS07F26 <secsgem.secs.functions.SecsS07F26>`
        - :class:`SecsS07F31 <secsgem.secs.functions.SecsS07F31>`
        - :class:`SecsS07F39 <secsgem.secs.functions.SecsS07F39>`
        - :class:`SecsS07F43 <secsgem.secs.functions.SecsS07F43>`

    """

    __type__ = SecsVarString
    __count__ = 20


class MEXP(DataItemBase):
    """Message expected

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS09F13 <secsgem.secs.functions.SecsS09F13>`
    """

    __type__ = SecsVarString
    __count__ = 6


class MHEAD(DataItemBase):
    """SECS message header

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 10

    **Used In Function**
        - :class:`SecsS09F01 <secsgem.secs.functions.SecsS09F01>`
        - :class:`SecsS09F03 <secsgem.secs.functions.SecsS09F03>`
        - :class:`SecsS09F05 <secsgem.secs.functions.SecsS09F05>`
        - :class:`SecsS09F07 <secsgem.secs.functions.SecsS09F07>`
        - :class:`SecsS09F11 <secsgem.secs.functions.SecsS09F11>`

    """

    __type__ = SecsVarBinary
    __count__ = 10


class MID(DataItemBase):
    """Material ID

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F27 <secsgem.secs.functions.SecsS02F27>`
        - :class:`SecsS03F02 <secsgem.secs.functions.SecsS03F02>`
        - :class:`SecsS03F04 <secsgem.secs.functions.SecsS03F04>`
        - :class:`SecsS03F07 <secsgem.secs.functions.SecsS03F07>`
        - :class:`SecsS03F09 <secsgem.secs.functions.SecsS03F09>`
        - :class:`SecsS03F12 <secsgem.secs.functions.SecsS03F12>`
        - :class:`SecsS03F13 <secsgem.secs.functions.SecsS03F13>`
        - :class:`SecsS04F01 <secsgem.secs.functions.SecsS04F01>`
        - :class:`SecsS04F03 <secsgem.secs.functions.SecsS04F03>`
        - :class:`SecsS04F05 <secsgem.secs.functions.SecsS04F05>`
        - :class:`SecsS04F07 <secsgem.secs.functions.SecsS04F07>`
        - :class:`SecsS04F09 <secsgem.secs.functions.SecsS04F09>`
        - :class:`SecsS04F11 <secsgem.secs.functions.SecsS04F11>`
        - :class:`SecsS04F13 <secsgem.secs.functions.SecsS04F13>`
        - :class:`SecsS04F15 <secsgem.secs.functions.SecsS04F15>`
        - :class:`SecsS04F17 <secsgem.secs.functions.SecsS04F17>`
        - :class:`SecsS07F07 <secsgem.secs.functions.SecsS07F07>`
        - :class:`SecsS07F08 <secsgem.secs.functions.SecsS07F08>`
        - :class:`SecsS07F10 <secsgem.secs.functions.SecsS07F10>`
        - :class:`SecsS07F11 <secsgem.secs.functions.SecsS07F11>`
        - :class:`SecsS07F13 <secsgem.secs.functions.SecsS07F13>`
        - :class:`SecsS07F35 <secsgem.secs.functions.SecsS07F35>`
        - :class:`SecsS07F36 <secsgem.secs.functions.SecsS07F36>`
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F05>`
        - :class:`SecsS12F07 <secsgem.secs.functions.SecsS12F07>`
        - :class:`SecsS12F09 <secsgem.secs.functions.SecsS12F09>`
        - :class:`SecsS12F11 <secsgem.secs.functions.SecsS12F11>`
        - :class:`SecsS12F13 <secsgem.secs.functions.SecsS12F13>`
        - :class:`SecsS12F14 <secsgem.secs.functions.SecsS12F14>`
        - :class:`SecsS12F15 <secsgem.secs.functions.SecsS12F15>`
        - :class:`SecsS12F16 <secsgem.secs.functions.SecsS12F16>`
        - :class:`SecsS12F17 <secsgem.secs.functions.SecsS12F17>`
        - :class:`SecsS12F18 <secsgem.secs.functions.SecsS12F18>`
        - :class:`SecsS16F11 <secsgem.secs.functions.SecsS16F11>`
        - :class:`SecsS16F13 <secsgem.secs.functions.SecsS16F13>`
        - :class:`SecsS16F15 <secsgem.secs.functions.SecsS16F15>`
        - :class:`SecsS18F10 <secsgem.secs.functions.SecsS18F10>`
        - :class:`SecsS18F11 <secsgem.secs.functions.SecsS18F11>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarString, SecsVarBinary]
    __count__ = 80


class MLCL(DataItemBase):
    """Message length

    :Types:
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`
        - :class:`SecsS12F05 <secsgem.secs.functions.SecsS12F05>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8]


class NULBC(DataItemBase):
    """Column count in dies

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarString]


class OBJACK(DataItemBase):
    """Object acknowledgement code

       :Types: :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       :Length: 1

    **Values**
        +-------+-------------+---------------------------------------------------+
        | Value | Description | Constant                                          |
        +=======+=============+===================================================+
        | 0     | Successful  | :const:`secsgem.secs.dataitems.OBJACK.SUCCESSFUL` |
        +-------+-------------+---------------------------------------------------+
        | 1     | Error       | :const:`secsgem.secs.dataitems.OBJACK.ERROR`      |
        +-------+-------------+---------------------------------------------------+
        | 2-63  | Reserved    |                                                   |
        +-------+-------------+---------------------------------------------------+

    **Used In Function**
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F12 <secsgem.secs.functions.SecsS14F12>`
        - :class:`SecsS14F14 <secsgem.secs.functions.SecsS14F14>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F18 <secsgem.secs.functions.SecsS14F18>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F28 <secsgem.secs.functions.SecsS14F28>`

    """

    __type__ = SecsVarU1
    __count__ = 1

    SUCCESSFUL = 0
    ERROR = 1


class OBJID(DataItemBase):
    """Object identifier

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS01F19 <secsgem.secs.functions.SecsS01F19>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F02 <secsgem.secs.functions.SecsS14F02>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F04 <secsgem.secs.functions.SecsS14F04>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarString]


class OBJSPEC(DataItemBase):
    """Specific object instance

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F49 <secsgem.secs.functions.SecsS02F49>`
        - :class:`SecsS13F11 <secsgem.secs.functions.SecsS13F11>`
        - :class:`SecsS13F13 <secsgem.secs.functions.SecsS13F13>`
        - :class:`SecsS13F15 <secsgem.secs.functions.SecsS13F15>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F05 <secsgem.secs.functions.SecsS14F05>`
        - :class:`SecsS14F07 <secsgem.secs.functions.SecsS14F07>`
        - :class:`SecsS14F09 <secsgem.secs.functions.SecsS14F09>`
        - :class:`SecsS14F10 <secsgem.secs.functions.SecsS14F10>`
        - :class:`SecsS14F11 <secsgem.secs.functions.SecsS14F11>`
        - :class:`SecsS14F13 <secsgem.secs.functions.SecsS14F13>`
        - :class:`SecsS14F15 <secsgem.secs.functions.SecsS14F15>`
        - :class:`SecsS14F16 <secsgem.secs.functions.SecsS14F16>`
        - :class:`SecsS14F17 <secsgem.secs.functions.SecsS14F17>`
        - :class:`SecsS14F19 <secsgem.secs.functions.SecsS14F19>`
        - :class:`SecsS14F25 <secsgem.secs.functions.SecsS14F25>`
        - :class:`SecsS14F27 <secsgem.secs.functions.SecsS14F27>`
        - :class:`SecsS15F43 <secsgem.secs.functions.SecsS15F43>`
        - :class:`SecsS15F47 <secsgem.secs.functions.SecsS15F47>`

    """

    __type__ = SecsVarString


class OBJTYPE(DataItemBase):
    """Class of object identifier

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS01F19 <secsgem.secs.functions.SecsS01F19>`
        - :class:`SecsS14F01 <secsgem.secs.functions.SecsS14F01>`
        - :class:`SecsS14F03 <secsgem.secs.functions.SecsS14F03>`
        - :class:`SecsS14F06 <secsgem.secs.functions.SecsS14F06>`
        - :class:`SecsS14F07 <secsgem.secs.functions.SecsS14F07>`
        - :class:`SecsS14F08 <secsgem.secs.functions.SecsS14F08>`
        - :class:`SecsS14F25 <secsgem.secs.functions.SecsS14F25>`
        - :class:`SecsS14F26 <secsgem.secs.functions.SecsS14F26>`
        - :class:`SecsS14F27 <secsgem.secs.functions.SecsS14F27>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarString]


class OFLACK(DataItemBase):
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

    __type__ = SecsVarBinary
    __count__ = 1

    ACK = 0


class ONLACK(DataItemBase):
    """Acknowledge code for ONLINE request

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+--------------------+----------------------------------------------------+
        | Value | Description        | Constant                                           |
        +=======+====================+====================================================+
        | 0     | ONLINE Accepted    | :const:`secsgem.secs.dataitems.ONLACK.ACCEPTED`    |
        +-------+--------------------+----------------------------------------------------+
        | 1     | ONLINE Not allowed | :const:`secsgem.secs.dataitems.ONLACK.NOT_ALLOWED` |
        +-------+--------------------+----------------------------------------------------+
        | 2     | Already ONLINE     | :const:`secsgem.secs.dataitems.ONLACK.ALREADY_ON`  |
        +-------+--------------------+----------------------------------------------------+
        | 3-63  | Reserved           |                                                    |
        +-------+--------------------+----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS01F18 <secsgem.secs.functions.SecsS01F18>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    ACCEPTED = 0
    NOT_ALLOWED = 1
    ALREADY_ON = 2


class ORLOC(DataItemBase):
    """Origin location 

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------+---------------------------------------------------+
        | Value | Description         | Constant                                          |
        +=======+=====================+===================================================+
        | 0     | Center die of wafer | :const:`secsgem.secs.dataitems.ORLOC.CENTER_DIE`  |
        +-------+---------------------+---------------------------------------------------+
        | 1     | Upper right         | :const:`secsgem.secs.dataitems.ORLOC.UPPER_RIGHT` |
        +-------+---------------------+---------------------------------------------------+
        | 2     | Upper left          | :const:`secsgem.secs.dataitems.ORLOC.UPPER_LEFT`  |
        +-------+---------------------+---------------------------------------------------+
        | 3     | Lower left          | :const:`secsgem.secs.dataitems.ORLOC.LOWER_LEFT`  |
        +-------+---------------------+---------------------------------------------------+
        | 4     | Lower right         | :const:`secsgem.secs.dataitems.ORLOC.LOWER_RIGHT` |
        +-------+---------------------+---------------------------------------------------+
        | 5-63  | Reserved, error     |                                                   |
        +-------+---------------------+---------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarBinary

    CENTER_DIE = 0
    UPPER_RIGHT = 1
    UPPER_LEFT = 2
    LOWER_LEFT = 3
    LOWER_RIGHT = 3


class PPBODY(DataItemBase):
    """Status variable ID

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
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
        - :class:`SecsS07F03 <secsgem.secs.functions.SecsS07F03>`
        - :class:`SecsS07F06 <secsgem.secs.functions.SecsS07F06>`
        - :class:`SecsS07F36 <secsgem.secs.functions.SecsS07F36>`
        - :class:`SecsS07F37 <secsgem.secs.functions.SecsS07F37>`
        - :class:`SecsS07F41 <secsgem.secs.functions.SecsS07F41>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString, SecsVarBinary]


class PPGNT(DataItemBase):
    """Process program grant status

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+------------------------+-------------------------------------------------------+
        | Value | Description            | Constant                                              |
        +=======+========================+=======================================================+
        | 0     | OK                     | :const:`secsgem.secs.dataitems.PPGNT.OK`              |
        +-------+------------------------+-------------------------------------------------------+
        | 1     | Already have           | :const:`secsgem.secs.dataitems.PPGNT.ALREADY_HAVE`    |
        +-------+------------------------+-------------------------------------------------------+
        | 2     | No space               | :const:`secsgem.secs.dataitems.PPGNT.NO_SPACE`        |
        +-------+------------------------+-------------------------------------------------------+
        | 3     | Invalid PPID           | :const:`secsgem.secs.dataitems.PPGNT.INVALID_PPID`    |
        +-------+------------------------+-------------------------------------------------------+
        | 4     | Busy, try later        | :const:`secsgem.secs.dataitems.PPGNT.BUSY`            |
        +-------+------------------------+-------------------------------------------------------+
        | 5     | Will not accept        | :const:`secsgem.secs.dataitems.PPGNT.WILL_NOT_ACCEPT` |
        +-------+------------------------+-------------------------------------------------------+
        | 6-63  | Reserved, other errors |                                                       |
        +-------+------------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS07F02 <secsgem.secs.functions.SecsS07F02>`
        - :class:`SecsS07F30 <secsgem.secs.functions.SecsS07F30>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    OK = 0
    ALREADY_HAVE = 1
    NO_SPACE = 2
    INVALID_PPID = 3
    BUSY = 4
    WILL_NOT_ACCEPT = 5


class PPID(DataItemBase):
    """Process program ID

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F27 <secsgem.secs.functions.SecsS02F27>`
        - :class:`SecsS07F01 <secsgem.secs.functions.SecsS07F01>`
        - :class:`SecsS07F03 <secsgem.secs.functions.SecsS07F03>`
        - :class:`SecsS07F05 <secsgem.secs.functions.SecsS07F05>`
        - :class:`SecsS07F06 <secsgem.secs.functions.SecsS07F06>`
        - :class:`SecsS07F08 <secsgem.secs.functions.SecsS07F08>`
        - :class:`SecsS07F10 <secsgem.secs.functions.SecsS07F10>`
        - :class:`SecsS07F11 <secsgem.secs.functions.SecsS07F11>`
        - :class:`SecsS07F13 <secsgem.secs.functions.SecsS07F13>`
        - :class:`SecsS07F17 <secsgem.secs.functions.SecsS07F17>`
        - :class:`SecsS07F20 <secsgem.secs.functions.SecsS07F20>`
        - :class:`SecsS07F23 <secsgem.secs.functions.SecsS07F23>`
        - :class:`SecsS07F25 <secsgem.secs.functions.SecsS07F25>`
        - :class:`SecsS07F26 <secsgem.secs.functions.SecsS07F26>`
        - :class:`SecsS07F27 <secsgem.secs.functions.SecsS07F27>`
        - :class:`SecsS07F31 <secsgem.secs.functions.SecsS07F31>`
        - :class:`SecsS07F33 <secsgem.secs.functions.SecsS07F33>`
        - :class:`SecsS07F34 <secsgem.secs.functions.SecsS07F34>`
        - :class:`SecsS07F36 <secsgem.secs.functions.SecsS07F36>`
        - :class:`SecsS07F53 <secsgem.secs.functions.SecsS07F53>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarString, SecsVarBinary]
    __count__ = 120


class PRAXI(DataItemBase):
    """Process axis

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+----------------------------+-------------------------------------------------------+
        | Value | Description                | Constant                                              |
        +=======+============================+=======================================================+
        | 0     | Rows, top, increasing      | :const:`secsgem.secs.dataitems.PRAXI.ROWS_TOP_INCR`   |
        +-------+----------------------------+-------------------------------------------------------+
        | 1     | Rows, top, decreasing      | :const:`secsgem.secs.dataitems.PRAXI.ROWS_TOP_DECR`   |
        +-------+----------------------------+-------------------------------------------------------+
        | 2     | Rows, bottom, increasing   | :const:`secsgem.secs.dataitems.PRAXI.ROWS_BOT_INCR`   |
        +-------+----------------------------+-------------------------------------------------------+
        | 3     | Rows, bottom, decreasing   | :const:`secsgem.secs.dataitems.PRAXI.ROWS_BOT_DECR`   |
        +-------+----------------------------+-------------------------------------------------------+
        | 4     | Columns, left, increasing  | :const:`secsgem.secs.dataitems.PRAXI.COLS_LEFT_INCR`  |
        +-------+----------------------------+-------------------------------------------------------+
        | 5     | Columns, left, decreasing  | :const:`secsgem.secs.dataitems.PRAXI.COLS_LEFT_DECR`  |
        +-------+----------------------------+-------------------------------------------------------+
        | 6     | Columns, right, increasing | :const:`secsgem.secs.dataitems.PRAXI.COLS_RIGHT_INCR` |
        +-------+----------------------------+-------------------------------------------------------+
        | 7     | Columns, right, decreasing | :const:`secsgem.secs.dataitems.PRAXI.COLS_RIGHT_DECR` |
        +-------+----------------------------+-------------------------------------------------------+
        | 8-63  | Error                      |                                                       |
        +-------+----------------------------+-------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarBinary
    __count__ = 1

    ROWS_TOP_INCR = 0
    ROWS_TOP_DECR = 1
    ROWS_BOT_INCR = 2
    ROWS_BOT_DECR = 3
    COLS_LEFT_INCR = 4
    COLS_LEFT_DECR = 5
    COLS_RIGHT_INCR = 6
    COLS_RIGHT_DECR = 7


class PRDCT(DataItemBase):
    """Process die count

    :Types:
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8]


class RCMD(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarI1, SecsVarString]


class REFP(DataItemBase):
    """Reference point

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`

    **Used In Function**
        - :class:`SecsS01F03 <secsgem.secs.functions.SecsS01F03>`
        - :class:`SecsS01F11 <secsgem.secs.functions.SecsS01F11>`
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
        - :class:`SecsS02F23 <secsgem.secs.functions.SecsS02F23>`
    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]


class ROWCT(DataItemBase):
    """Row count in dies

    :Types:
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8]


class RPSEL(DataItemBase):
    """Reference point select 

       :Types: :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarU1


class RPTID(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class RSINF(DataItemBase):
    """Starting location

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`

    **Used In Function**
        - :class:`SecsS12F07 <secsgem.secs.functions.SecsS12F07>`
        - :class:`SecsS12F14 <secsgem.secs.functions.SecsS12F14>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]
    __count__ = 3


class SDACK(DataItemBase):
    """Map setup acknowledge

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------+-------------------------------------------+
        | Value | Description   | Constant                                  |
        +=======+===============+===========================================+
        | 0     | Received Data | :const:`secsgem.secs.dataitems.SDACK.ACK` |
        +-------+---------------+-------------------------------------------+
        | 1-63  | Error         |                                           |
        +-------+---------------+-------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F02 <secsgem.secs.functions.SecsS12F02>`

    """

    __type__ = SecsVarBinary
    __count__ = 1
    
    ACK = 0


class SDBIN(DataItemBase):
    """Send bin information

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Values**
        +-------+---------------------------+-------------------------------------------------+
        | Value | Description               | Constant                                        |
        +=======+===========================+=================================================+
        | 0     | Send bin information      | :const:`secsgem.secs.dataitems.SDBIN.SEND`      |
        +-------+---------------------------+-------------------------------------------------+
        | 1     | Don't send bin infomation | :const:`secsgem.secs.dataitems.SDBIN.DONT_SEND` |
        +-------+---------------------------+-------------------------------------------------+
        | 2-63  | Reserved                  |                                                 |
        +-------+---------------------------+-------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F17 <secsgem.secs.functions.SecsS12F17>`
    """

    __type__ = SecsVarBinary
    __count__ = 1

    SEND = 0
    DONT_SEND = 1


class SHEAD(DataItemBase):
    """SECS message header

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 10

    **Used In Function**
        - :class:`SecsS09F09 <secsgem.secs.functions.SecsS09F09>`

    """

    __type__ = SecsVarBinary
    __count__ = 10


class SOFTREV(DataItemBase):
    """Software revision 

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F02 <secsgem.secs.functions.SecsS01F02>`
        - :class:`SecsS01F13 <secsgem.secs.functions.SecsS01F13>`
        - :class:`SecsS01F14 <secsgem.secs.functions.SecsS01F14>`
        - :class:`SecsS07F22 <secsgem.secs.functions.SecsS07F22>`
        - :class:`SecsS07F23 <secsgem.secs.functions.SecsS07F23>`
        - :class:`SecsS07F26 <secsgem.secs.functions.SecsS07F26>`
        - :class:`SecsS07F31 <secsgem.secs.functions.SecsS07F31>`
        - :class:`SecsS07F39 <secsgem.secs.functions.SecsS07F39>`
        - :class:`SecsS07F43 <secsgem.secs.functions.SecsS07F43>`

    """

    __type__ = SecsVarString
    __count__ = 20


class STRP(DataItemBase):
    """Starting position

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`

    **Used In Function**
        - :class:`SecsS12F09 <secsgem.secs.functions.SecsS12F09>`
        - :class:`SecsS12F16 <secsgem.secs.functions.SecsS12F16>`
    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]
    __count__ = 2


class SV(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]


class SVID(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class SVNAME(DataItemBase):
    """Status variable name

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
    """

    __type__ = SecsVarString


class TEXT(DataItemBase):
    """Line of characters

    :Types:
       - :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
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
        - :class:`SecsS10F01 <secsgem.secs.functions.SecsS10F01>`
        - :class:`SecsS10F03 <secsgem.secs.functions.SecsS10F03>`
        - :class:`SecsS10F05 <secsgem.secs.functions.SecsS10F05>`
        - :class:`SecsS10F09 <secsgem.secs.functions.SecsS10F09>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString, SecsVarBinary]


class TID(DataItemBase):
    """Terminal ID

       :Types: :class:`SecsVarBinary <secsgem.secs.variables.SecsVarBinary>`
       :Length: 1

    **Used In Function**
        - :class:`SecsS10F01 <secsgem.secs.functions.SecsS10F01>`
        - :class:`SecsS10F03 <secsgem.secs.functions.SecsS10F03>`
        - :class:`SecsS10F05 <secsgem.secs.functions.SecsS10F05>`
        - :class:`SecsS10F07 <secsgem.secs.functions.SecsS10F07>`

    """

    __type__ = SecsVarBinary
    __count__ = 1


class TIME(DataItemBase):
    """Time of day

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS02F18 <secsgem.secs.functions.SecsS02F18>`
        - :class:`SecsS02F31 <secsgem.secs.functions.SecsS02F31>`
    """

    __type__ = SecsVarString
    __count__ = 32

class TIMESTAMP(DataItemBase):
    """Timestamp

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS05F09 <secsgem.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem.secs.functions.SecsS05F11>`
        - :class:`SecsS05F15 <secsgem.secs.functions.SecsS05F15>`
        - :class:`SecsS15F41 <secsgem.secs.functions.SecsS15F41>`
        - :class:`SecsS15F44 <secsgem.secs.functions.SecsS15F44>`
        - :class:`SecsS16F05 <secsgem.secs.functions.SecsS16F05>`
        - :class:`SecsS16F07 <secsgem.secs.functions.SecsS16F07>`
        - :class:`SecsS16F09 <secsgem.secs.functions.SecsS16F09>`
    """

    __type__ = SecsVarString
    __count__ = 32


class UNITS(DataItemBase):
    """Units identifier

    :Types:
       - :class:`SecsVarString <secsgem.secs.variables.SecsVarString>`

    **Used In Function**
        - :class:`SecsS01F12 <secsgem.secs.functions.SecsS01F12>`
        - :class:`SecsS02F30 <secsgem.secs.functions.SecsS02F30>`
        - :class:`SecsS02F48 <secsgem.secs.functions.SecsS02F48>`
        - :class:`SecsS07F22 <secsgem.secs.functions.SecsS07F22>`
    """

    __type__ = SecsVarString


class V(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]


class VID(DataItemBase):
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

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, SecsVarString]


class XDIES(DataItemBase):
    """Die size/index X-axis

    :Types:
       - :class:`SecsVarF4 <secsgem.secs.variables.SecsVarF4>`
       - :class:`SecsVarF8 <secsgem.secs.variables.SecsVarF8>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarF4, SecsVarF8]


class XYPOS(DataItemBase):
    """X/Y coordinate position

    :Types:
       - :class:`SecsVarI8 <secsgem.secs.variables.SecsVarI8>`
       - :class:`SecsVarI1 <secsgem.secs.variables.SecsVarI1>`
       - :class:`SecsVarI2 <secsgem.secs.variables.SecsVarI2>`
       - :class:`SecsVarI4 <secsgem.secs.variables.SecsVarI4>`

    **Used In Function**
        - :class:`SecsS12F11 <secsgem.secs.functions.SecsS12F11>`
        - :class:`SecsS12F18 <secsgem.secs.functions.SecsS12F18>`
    """

    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8]
    __count__ = 2


class YDIES(DataItemBase):
    """Die size/index Y-axis

    :Types:
       - :class:`SecsVarF4 <secsgem.secs.variables.SecsVarF4>`
       - :class:`SecsVarF8 <secsgem.secs.variables.SecsVarF8>`
       - :class:`SecsVarU8 <secsgem.secs.variables.SecsVarU8>`
       - :class:`SecsVarU1 <secsgem.secs.variables.SecsVarU1>`
       - :class:`SecsVarU2 <secsgem.secs.variables.SecsVarU2>`
       - :class:`SecsVarU4 <secsgem.secs.variables.SecsVarU4>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem.secs.functions.SecsS12F04>`

    """
    
    __type__ = SecsVarDynamic    
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarF4, SecsVarF8]

