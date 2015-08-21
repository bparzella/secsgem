#####################################################################
# functionbase.py
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

from variables import SecsVarList


class SecsStreamFunction(object):
    """Secs stream and function base class

    This class is inherited to create a stream/function class. To create a function specific content the class variables :attr:`_stream`, :attr:`_function` and :attr:`_formatDescriptor` must be overridden.

    **Example**::

        class SecsS02F30(SecsStreamFunction):
            _stream = 2
            _function = 30

            _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
                                ("ECID", SecsVarU4(1)),
                                ("ECNAME", SecsVarString()),
                                ("ECMIN", SecsVarDynamic([SecsVarString])),
                                ("ECMAX", SecsVarDynamic([SecsVarString])),
                                ("ECDEF", SecsVarDynamic([SecsVarString])),
                                ("UNITS", SecsVarString()),
                                )), 6))

    :param value: set the value of stream/function parameters
    :type value: various
    """

    _stream = 0
    _function = 0

    _formatDescriptor = None

    def __init__(self, value=None):
        self.__dict__["stream"] = self._stream
        self.__dict__["function"] = self._function

        if self._formatDescriptor is None:
            self.__dict__["format"] = None
        else:
            self.__dict__["format"] = self._formatDescriptor.clone()

        if value is not None and self.format is not None:
            self.format.set(value)

    def __repr__(self):
        function = "S{0}F{1}".format(self.stream, self.function)
        data = "{{ {} }}".format(self.format.__repr__())
        return "{} {}".format(function, data)

    def __getattr__(self, name):
        if not isinstance(self.format, SecsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        return self.format.__getattr__(name)

    def __setattr__(self, name, value):
        if not isinstance(self.format, SecsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        self.format.__setattr__(name, value)

    def __getitem__(self, key):
        return self.format[key]

    def __setitem__(self, key, item):
        self.format[key] = item

    def append(self, data):
        """Append data to list, if stream/function parameter is a list

        :param data: list item to add
        :type data: various
        """
        if hasattr(self.format, 'append') and callable(self.format.append):
            self.format.append(data)
        else:
            raise AttributeError("class {} has no attribute 'append'".format(self.__class__.__name__))

    def encode(self):
        """Generates the encoded hsms data of the stream/function parameter

        :returns: encoded data
        :rtype: string
        """
        if self.format is None:
            return ""

        return self.format.encode()

    def decode(self, data):
        """Updates stream/function parameter data from the passed data

        :param data: encoded data
        :type data: string
        """
        if self.format is not None:
            self.format.decode(data)

    def set(self, value):
        """Updates the value of the stream/function parameter

        :param value: new value for the parameter
        :type value: various
        """
        self.format.set(value)

    def get(self):
        """Gets the current value of the stream/function parameter

        :returns: current parameter value
        :rtype: various
        """
        return self.format.get()
