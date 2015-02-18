#####################################################################
# secsFunctions.py
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
"""Wrappers for SECS stream and functions"""

import logging

from secsVariables import *

class secsS0F0:
    """Class for hsms low level functions (like Select, Linktest). All data is contained in the header.

    **Example**::

        >>> secsgem.secsS0F0()
        LL

    """
    def __init__(self):
        self.stream = 0
        self.function = 0
        
    def __repr__(self):
        return "LL"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s0f0 = secsgem.secsS0F0()
            >>> secsgem.formatHex(s0f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS0F0`

        **Example**::

            >>> secsgem.secsS0F0.decode(s0f0.encode())
            LL

        """
        return secsS0F0()

class secsS1F0:
    """Class for stream 1 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS1F0()
        S1F0 {}

    """
    def __init__(self):
        self.stream = 1
        self.function = 0
        
    def __repr__(self):
        return "S1F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f0 = secsgem.secsS1F0()
            >>> secsgem.formatHex(s1f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F0`

        **Example**::

            >>> secsgem.secsS1F0.decode(s1f0.encode())
            S1F0 {}

        """
        return secsS1F0()

class secsS1F1:
    """Class for stream 1 function 1, Are You There - Request.

    **Example**::

        >>> secsgem.secsS1F1()
        S1F1 {}

    """
    def __init__(self):
        self.stream = 1
        self.function = 1
        
    def __repr__(self):
        return "S1F1 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f1 = secsgem.secsS1F1()
            >>> secsgem.formatHex(s1f1.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F1`

        **Example**::

            >>> secsgem.secsS1F1.decode(s1f1.encode())
            S1F1 {}

        """
        return secsS1F1()

class secsS1F2:
    """Class for stream 1 function 2, Online Data Response , response to Are You There - Request.

    :param MDLN: model name
    :type MDLN: string
    :param SOFTREV: software revision
    :type SOFTREV: string

    **Example**::

        >>> secsgem.secsS1F2("secsgem", "0.0.3")
        S1F2 {MDLN: 'secsgem', SOFTREV: '0.0.3'}

    """
    def __init__(self, MDLN, SOFTREV):
        self.stream = 1
        self.function = 2

        self.MDLN = secsVarString(MDLN)
        self.SOFTREV = secsVarString(SOFTREV)
        
    def __repr__(self):
        return "S1F2 {MDLN: '%s', SOFTREV: '%s'}" % (self.MDLN.value, self.SOFTREV.value)
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f2 = secsgem.secsS1F2("secsgem", "0.0.3")
            >>> secsgem.formatHex(s1f2.encode())
            '01:02:41:07:73:65:63:73:67:65:6d:41:05:30:2e:30:2e:33'

        """
        return secsCoder.encode([self.MDLN, self.SOFTREV])
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F2`

        **Example**::

            >>> secsgem.secsS1F2.decode(s1f2.encode())
            S1F2 {MDLN: 'secsgem', SOFTREV: '0.0.3'}

        """
        data = secsCoder.decode(text)
        
        return secsS1F2(data[0], data[1])

class secsS1F3:
    """Class for stream 1 function 3, Selected Equipment Status - Request.

    :param SVIDs: list of UINT4, Status Variables to request
    :type SVIDs: list

    **Example**::

        >>> secsgem.secsS1F3([1000, 50000])
        S1F3 {SVID: '[U4 1000, U4 50000]'}

    """
    def __init__(self, SVIDs):
        self.stream = 1
        self.function = 3

        self.SVID = []
        for SVID in SVIDs:
            self.SVID.append(secsVarUINT4(SVID))

    def __repr__(self):
        return "S1F3 {SVID: '%s'}" % (self.SVID)

    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f3 = secsgem.secsS1F3([1000, 50000])
            >>> secsgem.formatHex(s1f3.encode())
            '01:02:b1:04:00:00:03:e8:b1:04:00:00:c3:50'

        """
        return secsCoder.encode(self.SVID)

    @staticmethod
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F3`

        **Example**::

            >>> secsgem.secsS1F3.decode(s1f3.encode())
            S1F3 {SVID: '[U4 1000, U4 50000]'}

        """
        data = secsCoder.decode(text)

        return secsS1F3(data)

class secsS1F4:
    """Class for stream 1 function 4, Selected Equipment Status - Response.

    Because of the dynamic type of the values, the types must be specified in the list.

    :param SV: list, Status Variables values of various types
    :type SV: list

    **Example**::

        >>> secsgem.secsS1F4([secsgem.secsVarString("ASDFG"), secsgem.secsVarUINT4(10)])
        S1F4 {SV: '[A ASDFG, U4 10]'}

    """
    def __init__(self, SV):
        self.stream = 1
        self.function = 4

        self.SV = SV

    def __repr__(self):
        return "S1F4 {SV: '%s'}" % (self.SV)

    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f4 = secsgem.secsS1F4([secsgem.secsVarString("ASDFG"), secsgem.secsVarUINT4(10)])
            >>> secsgem.formatHex(s1f4.encode())
            '01:02:41:05:41:53:44:46:47:b1:04:00:00:00:0a'

        """
        return secsCoder.encode(self.SV)

    @staticmethod
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F4`

        **Example**::

            >>> secsgem.secsS1F4.decode(s1f4.encode())
            S1F4 {SV: '[A ASDFG, U4 10]'}

        """
        data = secsCoder.decode(text)

        return secsS1F4(data)
        
class secsS1F11:
    """Class for stream 1 function 11, Status Variable List - Request.

    :param SVIDs: ids of Status Variables to list, all if empty
    :type SVIDs: list

    **Example**::

        >>> secsgem.secsS1F11([1000, 50000])
        S1F11 {SVID: '[U4 1000, U4 50000]'}

    """
    def __init__(self, SVIDs):
        self.stream = 1
        self.function = 11

        self.SVID = []
        for SVID in SVIDs:
            self.SVID.append(secsVarUINT4(SVID))

    def __repr__(self):
        return "S1F11 {SVID: '%s'}" % (self.SVID)

    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f11 = secsgem.secsS1F11([1000, 50000])
            >>> secsgem.formatHex(s1f11.encode())
            '01:02:b1:04:00:00:03:e8:b1:04:00:00:c3:50'

        """
        return secsCoder.encode(self.SVID)

    @staticmethod
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F11`

        **Example**::

            >>> secsgem.secsS1F11.decode(s1f11.encode())
            S1F11 {SVID: '[U4 1000, U4 50000]'}

        """
        data = secsCoder.decode(text)

        return secsS1F11(data)

class secsS1F12:
    """Class for stream 1 function 12, Status Variable List - Response.

    :param data: list with list of Status Variable ID, Name and Unit
    :type data: list

    **Example**::

        >>> secsgem.secsS1F12([[1000, "Variable1", ""], [50000, "Variable2", ""]])
        S1F12 {data: [[SVID: 'U4 1000', SVNAME: 'A Variable1',  UNIT: 'A '][SVID: 'U4 50000', SVNAME: 'A Variable2',  UNIT: 'A ']]}

    """
    def __init__(self, data):
        self.stream = 1
        self.function = 12

        self.data = []
        for item in data:
            self.data.append([secsVarUINT4(item[0]), secsVarString(item[1]), secsVarString(item[2])])

    def __repr__(self):
        data = "["
        for item in self.data:
            data += "[SVID: '%s', SVNAME: '%s',  UNIT: '%s']" % (item[0], item[1], item[2])
        data += "]"

        return "S1F12 {data: %s}" % (data)

    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f12 = secsgem.secsS1F12([[1000, "Variable1", ""], [50000, "Variable2", ""]])
            >>> secsgem.formatHex(s1f12.encode())
            '01:02:01:03:b1:04:00:00:03:e8:41:09:56:61:72:69:61:62:6c:65:31:41:00:01:03:b1:04:00:00:c3:50:41:09:56:61:72:69:61:62:6c:65:32:41:00'

        """
        return secsCoder.encode(self.data)

    @staticmethod
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F12`

        **Example**::

            >>> secsgem.secsS1F12.decode(s1f12.encode())
            S1F12 {data: [[SVID: 'U4 1000', SVNAME: 'A Variable1',  UNIT: 'A None'][SVID: 'U4 50000', SVNAME: 'A Variable2',  UNIT: 'A None']]}

        """
        data = secsCoder.decode(text)

        return secsS1F12(data)

class secsS1F13:
    """Class for stream 1 function 13, Establish Communication - Request.

    :param MDLN: model name
    :type MDLN: string
    :param SOFTREV: software revision
    :type SOFTREV: string

    **Example**::

        >>> secsgem.secsS1F13("secsgem", "0.0.3")
        S1F13 {MDLN: 'secsgem', SOFTREV: '0.0.3'}

    """
    def __init__(self, MDLN, SOFTREV):
        self.stream = 1
        self.function = 13

        self.MDLN = secsVarString(MDLN)
        self.SOFTREV = secsVarString(SOFTREV)
        
    def __repr__(self):
        return "S1F13 {MDLN: '%s', SOFTREV: '%s'}" % (self.MDLN.value, self.SOFTREV.value)
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f13 = secsgem.secsS1F13("secsgem", "0.0.3")
            >>> secsgem.formatHex(s1f13.encode())
            '01:02:41:07:73:65:63:73:67:65:6d:41:05:30:2e:30:2e:33'

        """
        return secsCoder.encode([self.MDLN, self.SOFTREV])
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F13`

        **Example**::

            >>> secsgem.secsS1F13.decode(s1f13.encode())
            S1F13 {MDLN: 'secsgem', SOFTREV: '0.0.3'}

        """
        data = secsCoder.decode(text)
        
        return secsS1F13(data[0], data[1])


class secsS1F14:
    """Class for stream 1 function 14, Establish Communication - Response.

    :param COMMACK: acknowledgement code, binary, 0=ok / 1=denied
    :type COMMACK: string
    :param MDLN: model name
    :type MDLN: string
    :param SOFTREV: software revision
    :type SOFTREV: string

    **Example**::

        >>> secsgem.secsS1F14("\\0", "secsgem", "0.0.3")
        S1F14 {COMMACK: '', {MDLN: 'secsgem', SOFTREV: '0.0.3'}}

    """
    def __init__(self, COMMACK, MDLN, SOFTREV):
        self.stream = 1
        self.function = 14

        self.COMMACK = secsVarBinary(COMMACK)
        self.MDLN = secsVarString(MDLN)
        self.SOFTREV = secsVarString(SOFTREV)
        
    def __repr__(self):
        return "S1F14 {COMMACK: '%s', {MDLN: '%s', SOFTREV: '%s'}}" % (self.COMMACK.value, self.MDLN.value, self.SOFTREV.value)
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s1f14 = secsgem.secsS1F14("\\0", "secsgem", "0.0.3")
            >>> secsgem.formatHex(s1f14.encode())
            '01:02:21:01:00:01:02:41:07:73:65:63:73:67:65:6d:41:05:30:2e:30:2e:33'

        """
        return secsCoder.encode([self.COMMACK, [self.MDLN, self.SOFTREV]])
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS1F14`

        **Example**::

            >>> secsgem.secsS1F14.decode(s1f14.encode())
            S1F14 {COMMACK: '', {MDLN: 'secsgem', SOFTREV: '0.0.3'}}

        """
        data = secsCoder.decode(text)
        
        return secsS1F14(data[0], data[1][0], data[1][1])

class secsS2F0:
    """Class for stream 2 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS2F0()
        S2F0 {}

    """
    def __init__(self):
        self.stream = 2
        self.function = 0
        
    def __repr__(self):
        return "S2F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s2f0 = secsgem.secsS2F0()
            >>> secsgem.formatHex(s2f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS2F0`

        **Example**::

            >>> secsgem.secsS2F0.decode(s2f0.encode())
            S2F0 {}

        """
        return secsS2F0()

class secsS2F13:
    def __init__(self, ECIDs):
        self.stream = 2
        self.function = 13

        self.ECID = []
        for ECID in ECIDs:
            self.ECID.append(secsVarUINT4(ECID))

    def __repr__(self):
        return "S2F13 {ECID: '%s'}" % (self.ECID)

    def encode(self):
        return secsCoder.encode(self.ECID)

    @staticmethod
    def decode(text):
        data = secsCoder.decode(text)

        return secsS2F13(data)

class secsS2F14:
    def __init__(self, EC):
        self.stream = 2
        self.function = 14

        self.EC = EC

    def __repr__(self):
        return "S2F14 {EC: '%s'}" % (self.EC)

    def encode(self):
        return secsCoder.encode(self.EC)

    @staticmethod
    def decode(text):
        data = secsCoder.decode(text)

        logging.debug("  %s", secsS2F14(data))
        return secsS2F14(data)

class secsS2F15:
    def __init__(self, ECIDs):
        self.stream = 2
        self.function = 15

        self.ECID = []
        for ECID in ECIDs:
            self.ECID.append([secsVarUINT4(ECID[0]), secsConvertVarIfRequired(secsVarString,ECID[1])])

    def __repr__(self):
        return "S2F15 {ECID: '%s'}" % (self.ECID)

    def encode(self):
        logging.debug(" %s", self)
        return secsCoder.encode(self.ECID)

    @staticmethod
    def decode(text):
        data = secsCoder.decode(text)

        return secsS2F15(data)

class secsS2F16:
    def __init__(self, EAC):
        self.stream = 2
        self.function = 16

        self.EAC = secsVarBinary(EAC)

    def __repr__(self):
        return "2F16 {EAC: %s}" % (self.EAC)

    def encode(self):
        return secsCoder.encode(self.EAC)

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)

        logging.debug("  %s", secsS2F16(data))
        return secsS2F16(data)

class secsS2F29:
    def __init__(self, ECIDs):
        self.stream = 2
        self.function = 29

        self.ECID = []
        for ECID in ECIDs:
            self.ECID.append(secsVarUINT4(ECID))

    def __repr__(self):
        return "S2F29 {ECID: '%s'}" % (self.ECID)

    def encode(self):
        return secsCoder.encode(self.ECID)

    @staticmethod
    def decode(text):
        data = secsCoder.decode(text)

        return secsS2F29(data)

class secsS2F30:
    def __init__(self, data):
        self.stream = 2
        self.function = 30

        self.data = []
        for item in data:
            self.data.append([secsVarUINT4(item[0]), secsVarString(item[1]), secsVarString(item[2]), secsVarString(item[3]), secsVarString(item[4]), secsVarString(item[5])])

    def __repr__(self):
        data = "["
        for item in self.data:
            data += "[ECID: '%s', ECNAME: '%s',  ECMIN: '%s',  ECMAX: '%s',  ECDEF: '%s',  UNITS: '%s']" % (item[0], item[1], item[2], item[3], item[4], item[5])
        data += "]"

        return "S2F30 {data: %s}" % (data)

    def encode(self):
        return secsCoder.encode(self.data)

    @staticmethod
    def decode(text):
        data = secsCoder.decode(text)

        return secsS2F30(data)

class secsS2F33:
    def __init__(self, DATAID, reports):
        self.stream = 2
        self.function = 33

        self.DATAID = secsVarUINT4(DATAID)
        self.reports = []
        for report in reports:
            CEIDs = []

            for CEID in report[1]:
                CEIDs.append(secsVarUINT4(CEID))

            self.reports.append([secsVarUINT4(report[0]), CEIDs])

    def __repr__(self):
        reports = "["
        for report in self.reports:
            CEIDs = "["
            for CEID in report[1]:
                CEIDs += "VID = %d," % (CEID.value)

            CEIDs += "]"

            reports += "[RPTID: '%d', %s]" % (report[0].value, CEIDs)
        reports += "]"
        return "2F33 {DATAID: '%s', %s}" % (self.DATAID.value, reports)

    def encode(self):
        return secsCoder.encode([self.DATAID, self.reports])

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS2F33(data[0], data[1][0], data[1][1])

class secsS2F34:
    def __init__(self, DRACK):
        self.stream = 2
        self.function = 34

        self.DRACK = secsVarBinary(DRACK)

    def __repr__(self):
        return "2F34 {DRACK: '%d'}" % (ord(self.DRACK.value[0]))

    def encode(self):
        return secsCoder.encode(self.DRACK)

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        return secsS2F34(data[0])

class secsS2F35:
    def __init__(self, DATAID, CEIDs):
        self.stream = 2
        self.function = 35

        self.DATAID = secsVarUINT4(DATAID)
        self.CEIDs = []
        for CEID in CEIDs:
            RPTIDs = []

            for RPTID in CEID[1]:
                RPTIDs.append(secsVarUINT4(RPTID))

            self.CEIDs.append([secsVarUINT4(CEID[0]), RPTIDs])

    def __repr__(self):
        CEIDs = "["
        for CEID in self.CEIDs:
            RPTIDs = "["
            for RPTID in CEID[1]:
                RPTIDs += "RPTID = %d," % (RPTID.value)

            RPTIDs += "]"

            CEIDs += "[CEID: '%d', %s]" % (CEID[0].value, RPTIDs)
        CEIDs += "]"
        return "2F35 {DATAID: '%s', %s}" % (self.DATAID.value, CEIDs)

    def encode(self):
        return secsCoder.encode([self.DATAID, self.CEIDs])

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS2F35(data[0], data[1][0], data[1][1])

class secsS2F36:
    def __init__(self, LRACK):
        self.stream = 2
        self.function = 36

        self.LRACK = secsVarBinary(LRACK)

    def __repr__(self):
        return "2F36 {LRACK: '%d'}" % (ord(self.LRACK.value[0]))

    def encode(self):
        return secsCoder.encode(self.LRACK)

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        return secsS2F36(data[0])

class secsS2F37:
    def __init__(self, CEED, CEIDs):
        self.stream = 2
        self.function = 37

        self.CEED = secsVarBoolean(CEED)
        self.CEIDs = []
        for CEID in CEIDs:
            self.CEIDs.append(secsVarUINT4(CEID))

    def __repr__(self):
        CEIDs = "["
        for CEID in self.CEIDs:
            CEIDs += "CEID = %d," % (CEID.value)

        CEIDs += "]"

        return "2F37 {CEED: '%s', %s}" % (self.CEED.value, CEIDs)

    def encode(self):
        return secsCoder.encode([self.CEED, self.CEIDs])

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS2F37(data[0], data[1])

class secsS2F38:
    def __init__(self, ERACK):
        self.stream = 2
        self.function = 38

        self.ERACK = secsVarBinary(ERACK)

    def __repr__(self):
        return "2F38 {ERACK: '%d'}" % (ord(self.ERACK.value[0]))

    def encode(self):
        return secsCoder.encode(self.ERACK)

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        return secsS2F38(data[0])

class secsS2F41:
    def __init__(self, RCMD, parameters):
        self.stream = 2
        self.function = 41

        self.RCMD = secsVarString(RCMD)
        self.parameters = []
        for parameter in parameters:
            self.parameters.append([secsVarString(parameter[0]), secsVarString(parameter[1])])

    def __repr__(self):
        parameters = "["
        for parameter in self.parameters:
            parameters += "[RPTID: '%s', CPVAL: '%s']" % (parameter[0].value, parameter[1].value)
        parameters += "]"
        return "2F41 {RCMD: '%s', %s}" % (self.RCMD.value, parameters)

    def encode(self):
        return secsCoder.encode([self.RCMD, self.parameters])

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS2F41(data[0], data[1][0], data[1][1])

class secsS2F42:
    def __init__(self, parameters):
        self.stream = 2
        self.function = 42

        self.parameters = parameters

    def __repr__(self):
        return "2F42 {%s}" % (parameters)

    def encode(self):
        return secsCoder.encode(self.parameters)

    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        return secsS2F42_generic(data)

class secsS5F0:
    """Class for stream 5 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS5F0()
        S5F0 {}

    """
    def __init__(self):
        self.stream = 5
        self.function = 0
        
    def __repr__(self):
        return "S5F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s5f0 = secsgem.secsS5F0()
            >>> secsgem.formatHex(s5f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS5F0`

        **Example**::

            >>> secsgem.secsS5F0.decode(s5f0.encode())
            S5F0 {}

        """
        return secsS5F0()

class secsS5F1:
    def __init__(self, ALCD, ALID, ALTX):
        self.stream = 5
        self.function = 1

        self.ALCD = secsVarBinary(ALCD)
        self.ALID = secsVarUINT4(ALID)
        self.ALTX = secsVarString(ALTX)
        
    def __repr__(self):
        return "S5F1 {ALCD: '%s', ALID: %d, ALTX: '%s'}" % (self.ALCD.value, self.ALID.value, self.ALTX.value)
        
    def encode(self):
        return secsCoder.encode([self.ALCD, self.ALID, self.ALTX])
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS5F1(data[0], data[1], data[2])

class secsS5F2:
    def __init__(self, ACKC5):
        self.stream = 5
        self.function = 2

        self.ACKC5 = secsVarBinary(ACKC5)
        
    def __repr__(self):
        return "S5F2 {ACKC5: '%s'}" % (self.ACKC5.value)
        
    def encode(self):
        return secsCoder.encode(self.ACKC5)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS5F2(data[0])

class secsS6F0:
    """Class for stream 6 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS6F0()
        S6F0 {}

    """
    def __init__(self):
        self.stream = 6
        self.function = 0
        
    def __repr__(self):
        return "S6F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s6f0 = secsgem.secsS6F0()
            >>> secsgem.formatHex(s6f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS6F0`

        **Example**::

            >>> secsgem.secsS6F0.decode(s6f0.encode())
            S6F0 {}

        """
        return secsS6F0()

class secsS6F11:
    def __init__(self, DATAID, CEID, reports = []):
        self.stream = 6
        self.function = 11

        self.DATAID = secsVarUINT4(DATAID)
        self.CEID = secsVarUINT4(CEID)

        self.reports = reports
        
    def __repr__(self):
        return "S6F11 {DATAID: %d, CEID: %d, %s}" % (self.DATAID.value, self.CEID.value, self.reports)
            
    def encode(self):
        return secsCoder.encode([self.DATAID.value, self.CEID.value, self.reports])
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS6F11(data[0], data[1], data[2])
        
class secsS6F12:
    def __init__(self, ACKC6):
        self.stream = 6
        self.function = 12

        self.ACKC6 = secsVarBinary(ACKC6)
        
    def __repr__(self):
        return "S6F12 {ACKC6: '%s'}" % (self.ACKC6.value)
        
    def encode(self):
        return secsCoder.encode(self.ACKC6)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS6F12(data[0])

class secsS9F0:
    """Class for stream 9 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS9F0()
        S9F0 {}

    """
    def __init__(self):
        self.stream = 9
        self.function = 0
        
    def __repr__(self):
        return "S9F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s9f0 = secsgem.secsS9F0()
            >>> secsgem.formatHex(s9f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS9F0`

        **Example**::

            >>> secsgem.secsS9F0.decode(s9f0.encode())
            S9F0 {}

        """
        return secsS9F0()

class secsS9F1:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 1

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F1 ERROR: Unrecognized Device ID {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F1(data[0])

class secsS9F3:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 3

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F3 ERROR: Unrecognized Stream Type {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F3(data[0])

class secsS9F5:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 5

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F5 ERROR: Unrecognized Function Type {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F5(data[0])

class secsS9F7:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 7

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F7 ERROR: Illegal Data {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F7(data[0])

class secsS9F9:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 9

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F9 ERROR: Transaction Timer Time-out {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F9(data[0])

class secsS9F11:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 11

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F11 ERROR: Data Too Long {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F11(data[0])

class secsS9F13:
    def __init__(self, MHEAD):
        self.stream = 9
        self.function = 13

        self.MHEAD = secsVarBinary(MHEAD)
        
    def __repr__(self):
        return "S9F13 ERROR: Inter Block Time-out {MHEAD: '%s'}" % (self.MHEAD.value)
        
    def encode(self):
        return secsCoder.encode(self.MHEAD)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS9F13(data[0])

class secsS10F0:
    """Class for stream 10 function 0, Transaction Abort

    **Example**::

        >>> secsgem.secsS10F0()
        S10F0 {}

    """
    def __init__(self):
        self.stream = 10
        self.function = 0
        
    def __repr__(self):
        return "S10F0 {}"
        
    def encode(self):
        """Encode the class data to byte array.

        :returns: data byte array
        :rtype: string

        **Example**::

            >>> s10f0 = secsgem.secsS10F0()
            >>> secsgem.formatHex(s10f0.encode())
            ''

        """
        return secsCoder.encode(None)
    
    @staticmethod    
    def decode(text):
        """Create object from byte array

        :param text: data byte array
        :type text: string
        :returns: stream and function object
        :rtype: :class:`secsgem.secsFunctions.secsS10F0`

        **Example**::

            >>> secsgem.secsS10F0.decode(s10f0.encode())
            S10F0 {}

        """
        return secsS10F0()

class secsS10F1:
    def __init__(self, TID, TEXT):
        self.stream = 10
        self.function = 1

        self.TID = secsVarBinary(TID)
        self.TEXT = secsVarString(TEXT)
        
    def __repr__(self):
        return "S10F1 {TID: %d, TEXT: '%s'}" % (ord(self.TID.value[0]), self.TEXT.value)
        
    def encode(self):
        return secsCoder.encode([self.TID, self.TEXT])
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS10F1(data[0], data[1])

class secsS10F2:
    def __init__(self, ACKC10):
        self.stream = 10
        self.function = 2

        self.ACKC10 = secsVarBinary(ACKC10)
        
    def __repr__(self):
        return "S10F2 {ACKC10: '%s'}" % (self.ACKC10.value)
        
    def encode(self):
        return secsCoder.encode(self.ACKC10)
    
    @staticmethod    
    def decode(text):
        data = secsCoder.decode(text)
        
        return secsS10F2(data[0])

secsStreamsFunctions = {
     0:     {
         0: secsS0F0,
        },
     1:     {
         0: secsS1F0,
         1: secsS1F1,
         2: secsS1F2,
         3: secsS1F3,
         4: secsS1F4,
        11: secsS1F11,
        12: secsS1F12,
        13: secsS1F13,
        14: secsS1F14,
        },
     2:     {
         0: secsS2F0,
        13: secsS2F13,
        14: secsS2F14,
        15: secsS2F15,
        16: secsS2F16,
        29: secsS2F29,
        30: secsS2F30,
        33: secsS2F33,
        34: secsS2F34,
        35: secsS2F35,
        36: secsS2F36,
        37: secsS2F37,
        38: secsS2F38,
        41: secsS2F41,
        42: secsS2F42,
        },
     5:    {
         0: secsS5F0,
         1: secsS5F1,
         2: secsS5F2,
        },
     6:    {
         0: secsS6F0,
        11: secsS6F11,
        12: secsS6F12,
        },
     9:    {
         0: secsS9F0,
         1: secsS9F1,
         3: secsS9F3,
         5: secsS9F5,
         7: secsS9F7,
         9: secsS9F9,
        11: secsS9F11,
        13: secsS9F13,
        },
    10:    {
         0: secsS10F0,
         1: secsS10F1,
         2: secsS10F2,
        },
}

def secsDecode(packet):
    """Get object of decoded stream and function class, or None if no class is available.

    :param packet: packet to get object for
    :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
    :return: matching stream and function object
    :rtype: secsSxFx object
    """
    if not packet.header.stream in secsStreamsFunctions:
        logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
        return None
    else:
        if not packet.header.function in secsStreamsFunctions[packet.header.stream]:
            logging.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None
        else:
            return secsStreamsFunctions[packet.header.stream][packet.header.function].decode(packet.data)

