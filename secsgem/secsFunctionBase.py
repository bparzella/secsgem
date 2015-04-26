#####################################################################
# secsFunctionBase.py
#
# (c) Copyright 2015, Benjamin Parzella. All rights reserved.
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
"""Base class for for SECS stream and functions"""

from secsVariables import secsVarList, secsVarArray

class secsStreamFunction(object):
    stream = 0
    function = 0

    def __init__(self, value=None):
        if self.formatDescriptor == None:
            self.__dict__["format"] = None
        else:
            self.__dict__["format"] = self.formatDescriptor.clone()

        if not value == None and not self.format == None:
            self.format.set(value)

    def __repr__(self):
        function = "S{0}F{1}".format(self.stream, self.function)
        data = "{{ {} }}".format(self.format.__repr__())
        return "{} {}".format(function, data)

    def __getattr__(self, name):
        if not isinstance(self.format, secsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        return self.format.__getattr__(name)

    def __setattr__(self, name, value):
        if not isinstance(self.format, secsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        self.format.__setattr__(name, value)

    def __getitem__(self,key):
        return self.format[key]

    def __setitem__(self, key, item):
        self.format[key] = item

    def append(self, data):
        if hasattr(self.format, 'append') and callable(self.format.append):
            self.format.append(data)
        else:
            raise AttributeError("class {} has no attribute 'append'".format(self.__class__.__name__))

    def encode(self):
        if self.format == None:
            return ""

        return self.format.encode()

    def decode(self, data):
        if not self.format == None:
            self.format.decode(data)

    def set(self, value):
        self.format.set(value)

    def get(self):
        return self.format.get()
