#####################################################################
# secsVariables.py
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
"""SECS variable types"""

import struct

from collections import OrderedDict

DEBUG_DECODE = False
DEBUG_DECODE_DEPTH = 0

class secsVar(object):
    """Base class for SECS variables. Due to the python types, wrapper classes for variables are required. If constructor is called with secsVar or subclass only the value is copied."""
    formatCode = -1

    def __init__(self):
        self.value = None

    def encodeItemHeader(self, length):
        if (length > 0xFFFF):
            lengthBytes = 3
            formatByte = (self.formatCode << 2) | lengthBytes
            return chr(formatByte) + chr((length & 0xFF0000) >> 16) + chr((length & 0x00FF00) >> 8) + chr((length & 0x0000FF))
        elif (length > 0xFF):
            lengthBytes = 2
            formatByte = (self.formatCode << 2) | lengthBytes
            return chr(formatByte) + chr((length & 0x00FF00) >> 8) + chr((length & 0x0000FF))
        else:
            lengthBytes = 1
            formatByte = (self.formatCode << 2) | lengthBytes
            return chr(formatByte) + chr((length & 0x0000FF))

    def decodeItemHeader(self, data, textPos=0):
        if DEBUG_DECODE:
            print "{}--Decoded item header for {} starting at {}".format((" " * DEBUG_DECODE_DEPTH), self.__class__.__name__, textPos)
        
        if data == "":
            raise ValueError("Decoding for {} without any text".format(self.__class__.__name__))
        
        #parse format byte
        formatByte = ord(data[textPos])
        formatCode = (formatByte & 0b11111100) >> 2
        lengthBytes = (formatByte & 0b00000011)

        textPos += 1

        #read 1-3 length bytes
        length = 0
        for i in range(lengthBytes):
            length <<= 8
            length += ord(data[textPos])
            
            textPos += 1

        if self.formatCode >= 0 and formatCode != self.formatCode:
            raise ValueError("Decoding data for {} ({}) has invalid format {}".format(self.__class__.__name__, self.formatCode,  formatCode))

        if DEBUG_DECODE:
            print "{}Decoded item header with data @{} / format {} / length {}".format((" " * DEBUG_DECODE_DEPTH), textPos, formatCode, length)
        
        return (textPos, formatCode, length)

class secsVarDynamic(secsVar):
    def __init__(self, defaultType, length=-1, value=None):
        self.value = defaultType(length)

        self.defaultType = defaultType
        self.length = length

        if value:
            self.value.set(value)

    def __repr__(self):
        return self.value.__repr__()

    def __len__(self):
        return self.value.__len__()

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __setitem__(self, key, item):
        self.value.__setitem__(key, item)

    def set(self, value):
        if isinstance(value, secsVar):
            self.value = value
        else:
            self.value.set(value)

    def get(self):
        return self.value.get()

    def encode(self):
        return self.value.encode()

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        if formatCode == secsVarArray.formatCode:
            self.value = secsVarArray(secsVarDynamic(secsVarString))
        elif formatCode == secsVarBinary.formatCode:
            self.value = secsVarBinary()
        elif formatCode == secsVarBoolean.formatCode:
            self.value = secsVarBoolean()
        elif formatCode == secsVarString.formatCode:
            self.value = secsVarString()
        elif formatCode == secsVarI4.formatCode:
            self.value = secsVarI4()
        elif formatCode == secsVarU1.formatCode:
            self.value = secsVarU1()
        elif formatCode == secsVarU2.formatCode:
            self.value = secsVarU2()
        elif formatCode == secsVarU4.formatCode:
            self.value = secsVarU4()

        return self.value.decode(data, start)

    def clone(self):
        return secsVarDynamic(self.defaultType, self.length, self.value.get())

class secsVarList(secsVar):
    formatCode = 0

    def __init__(self, data, fieldCount=-1, value=None):
        self.__dict__["data"] = data
        self.__dict__["fieldCount"] = fieldCount

        #check if fieldCount parameter matches amount of fields in the list
        if self.fieldCount >= 0:
            if not len(data) == fieldCount:
                raise ValueError("Definition has invalid field count (expected: {}, actual: {})".format(self.fieldCount, len(data)))

        #set the value if passed
        if value:
            self.set(value)

    def __repr__(self):
        data = ""
        first = True

        for fieldName in self.data:
            if not first:
                data += ", "
            data += "{}: {}".format(fieldName, self.data[fieldName].__repr__())
            first = False

        return "[{}]".format(data)

    def __len__(self):
        return len(self.data)

    def set(self, value):
        if isinstance(value, dict):
            for fieldName in value:
                self.data[fieldName].set(value[fieldName])
        elif isinstance(value, list):
            if not len(value) == self.fieldCount:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.length, len(data)))
            counter = 0
            for fieldName in self.data:
                self.data[fieldName].set(value[counter])
                counter += 1
        else:
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

    def get(self):
        data = []
        for fieldName in self.data:
            data.append(self.data[fieldName].get())

        return data

    def encode(self):
        result = self.encodeItemHeader(len(self.data))
            
        for fieldName in self.data:
            result += self.data[fieldName].encode()

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        global DEBUG_DECODE_DEPTH

        #list
        for i in range(length):
            DEBUG_DECODE_DEPTH += 2
            fieldName = self.data.keys()[i]
            textPos = self.data[fieldName].decode(data, textPos)
            DEBUG_DECODE_DEPTH -= 2

        return textPos

    def __getattr__(self, name):
        if not name in self.data:
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        if isinstance(self.data[name], secsVarArray) or isinstance(self.data[name], secsVarList):
            return self.data[name]
        else:
            return self.data[name].get()

    def __setattr__(self, name, value):
        if not name in self.data:
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        self.data[name].set(value)

    def clone(self):
        newData = OrderedDict()
        for item in self.data:
            newData[item] = self.data[item].clone()

        return secsVarList(newData, self.fieldCount)

class secsVarArray(secsVar):
    formatCode = 0

    def __init__(self, data, fieldCount=-1, value=None):
        self.__dict__["itemDecriptor"] = data
        self.__dict__["fieldCount"] = fieldCount
        self.__dict__["data"] = []

        #set the value if passed
        if value:
            self.set(value)

    def __repr__(self):
        data = ""
        first = True

        for value in self.data:
            if not first:
                data += ", "
            data += "{}".format(value.__repr__())
            first = False

        return "[{}]".format(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self,key):
        if isinstance(self.data[key], secsVarArray) or isinstance(self.data[key], secsVarList):
            return self.data[key]
        else:
            return self.data[key].get()

    def __setitem__(self, key, item):
        self.data[key].set(item)

    def append(self, data):
        newObject = self.itemDecriptor.clone()
        newObject.set(data)
        self.data.append(newObject)

    def set(self, value):
        if not isinstance(value, list):
            raise ValueError("Invalid value type {} for {}".format(type(value).__name__, self.__class__.__name__))

        if self.fieldCount >= 0:
            if not len(value) == self.fieldCount:
                raise ValueError("Value has invalid field count (expected: {}, actual: {})".format(self.fieldCount, len(value)))

        self.__dict__["data"] = []

        for counter in range(len(value)):
            newObject = self.itemDecriptor.clone()
            newObject.set(value[counter])
            self.data.append(newObject)

    def get(self):
        data = []
        for item in self.data:
            data.append(item.get())

        return data

    def encode(self):
        result = self.encodeItemHeader(len(self.data))
            
        for item in self.data:
            result += item.encode()

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        global DEBUG_DECODE_DEPTH

        #list
        self.__dict__["data"] = []

        for counter in range(length):
            DEBUG_DECODE_DEPTH += 2
            newObject = self.itemDecriptor.clone()
            textPos = newObject.decode(data, textPos)
            self.data.append(newObject)
            DEBUG_DECODE_DEPTH -= 2

        return textPos

    def clone(self):
        itemDecriptor = self.itemDecriptor.clone()
        newData = []
        for item in self.data:
            newData.append(item.get())

        return secsVarArray(itemDecriptor, self.fieldCount, newData)

class secsVarBinary(secsVar):
    formatCode = 010
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        if len(self.value) == 1:
            return "B {}".format(self.get())
        else:
            return "B <{} bytes>".format(len(self.value))

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return ord(self.value[key])

    def __setitem__(self, key, item):
        self.value[key] = chr(item)

    def set(self, value):
        if value == None:
            return

        if not isinstance(value, str):
            value = chr(value)

        if self.length >= 0 and len(value) != self.length:
            raise ValueError("Value longer than {} chars".format(self.length))

        self.value = value

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return ord(self.value[0])
            else:
                return []

        return self.value

    def encode(self):
        if self.value == None:
            length = 0
        else:
            length = len(self.value)

        result = self.encodeItemHeader(length)

        if not self.value == None:
            result += self.value

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        #string
        result = None

        if length > 0:
            result = data[textPos:textPos+length]

            if DEBUG_DECODE:
                print "{}Decoded {} bytes".format((" " * DEBUG_DECODE_DEPTH), len(result))

        self.set(result)

        return textPos + length

    def clone(self):
        return secsVarBinary(self.length, self.value)

class secsVarBoolean(secsVar):
    formatCode = 011
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if not value == None:
            self.set(value)

    def __repr__(self):
        return "TF {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        if isinstance(value, list):
            if self.length >= 0 and len(value) > self.length:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [ bool(value) ]

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += chr(value)    

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        result = []

        for i in range(length):
            resultText = data[textPos]
            result.append(bool(struct.unpack(">b", resultText)[0]))

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            textPos += 1
                
        self.set(result)

        return textPos

    def clone(self):
        return secsVarBoolean(self.length, self.value)

class secsVarString(secsVar):
    formatCode = 020
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        return "A '{}'".format(self.value)

    def __len__(self):
        return len(self.value)

    def set(self, value):
        if not isinstance(value, str):
            value = str(value)

        if self.length >= 0 and len(value) > self.length:
            raise ValueError("Value longer than {} chars".format(self.length))

        self.value = value

    def get(self):
        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value))

        result += self.value

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)
        
        #string
        result = None

        if length > 0:
            result = data[textPos:textPos+length]

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result)

        self.set(result)

        return textPos + length

    def clone(self):
        return secsVarString(self.length, self.value)

class secsVarI4(secsVar):
    formatCode = 034
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        return "I4 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        if isinstance(value, list):
            if self.length >= 0 and len(value) > self.length:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [ int(value) ]

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value)*4)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">l", value)

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        result = []

        for i in range(length/4):
            resultText = data[textPos:textPos+4]
            result.append(struct.unpack(">l", resultText)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            textPos += 4
                
        self.set(result)

        return textPos

    def clone(self):
        return secsVarI4(self.length, self.value)

class secsVarU1(secsVar):
    formatCode = 051
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        return "U1 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        if isinstance(value, list):
            if self.length >= 0 and len(value) > self.length:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [ int(value) ]

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value))

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">B", value)

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        result = []

        for i in range(length):
            resultText = data[textPos]
            result.append(struct.unpack(">B", resultText)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            textPos += 1
                
        self.set(result)

        return textPos

    def clone(self):
        return secsVarU1(self.length, self.value)

class secsVarU2(secsVar):
    formatCode = 052
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        return "U2 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        if isinstance(value, list):
            if self.length >= 0 and len(value) > self.length:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [ int(value) ]

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value)*2)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">H", value)

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        result = []

        for i in range(length/2):
            resultText = data[textPos:textPos+2]
            result.append(struct.unpack(">H", resultText)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            textPos += 2
                
        self.set(result)

        return textPos

    def clone(self):
        return secsVarU2(self.length, self.value)

class secsVarU4(secsVar):
    formatCode = 054
    
    def __init__(self, length=-1, value=None):
        self.value = None
        self.length = length

        if value:
            self.set(value)

    def __repr__(self):
        return "U4 {}".format(self.get())

    def __len__(self):
        return len(self.value)

    def __getitem__(self,key):
        return self.value[key]

    def __setitem__(self, key, item):
        self.value[key] = item

    def set(self, value):
        if isinstance(value, list):
            if self.length >= 0 and len(value) > self.length:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = value
        else:
            if self.length >= 0 and self.length != 1:
                raise ValueError("Value longer than {} chars".format(self.length))

            self.value = [ int(value) ]

    def get(self):
        if len(self.value) == 1:
            if self.value:
                return self.value[0]
            else:
                return []

        return self.value

    def encode(self):
        result = self.encodeItemHeader(len(self.value)*4)

        for counter in range(len(self.value)):
            value = self.value[counter]
            result += struct.pack(">L", value)

        return result

    def decode(self, data, start = 0):
        (textPos, formatCode, length) = self.decodeItemHeader(data, start)

        result = []

        for i in range(length/4):
            resultText = data[textPos:textPos+4]
            result.append(struct.unpack(">L", resultText)[0])

            if DEBUG_DECODE:
                print "{}Decoded {}".format((" " * DEBUG_DECODE_DEPTH), result[i])

            textPos += 4
                
        self.set(result)

        return textPos

    def clone(self):
        return secsVarU4(self.length, self.value)
