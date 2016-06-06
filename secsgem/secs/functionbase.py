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
from ..common import indent_block


class SecsStreamFunction(object):
    """Secs stream and function base class

    This class is inherited to create a stream/function class. To create a function specific content the class variables :attr:`_stream`, :attr:`_function` and :attr:`_formatDescriptor` must be overridden.

    **Example**::

        class SecsS02F30(SecsStreamFunction):
            _stream = 2
            _function = 30

            _toHost = True
            _toEquipment = False

            _hasReply = False
            _isReplyRequired = False

            _isMultiBlock = True

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

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False

    def __init__(self, value=None):
        self.__dict__["stream"] = self._stream
        self.__dict__["function"] = self._function

        if self._formatDescriptor is None:
            self.__dict__["data"] = None
        else:
            self.__dict__["data"] = self._formatDescriptor.clone()

        self.__dict__["toHost"] = self._toHost
        self.__dict__["toEquipment"] = self._toEquipment

        self.__dict__["hasReply"] = self._hasReply
        self.__dict__["isReplyRequired"] = self._isReplyRequired

        self.__dict__["isMultiBlock"] = self._isMultiBlock

        if value is not None and self.data is not None:
            self.data.set(value)

    def __repr__(self):
        function = "S{0}F{1}".format(self.stream, self.function)
        if self.data is None:
            return "{} {} .".format(function, "W" if self._isReplyRequired else "")
        data = "{}".format(self.data.__repr__())
        return "{} {} \n{} .".format(function, "W" if self._isReplyRequired else "", indent_block(data))

    def __getattr__(self, name):
        if not isinstance(self.data, SecsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        return self.data.__getattr__(name)

    def __setattr__(self, name, value):
        if not isinstance(self.data, SecsVarList):
            raise AttributeError("class {} has no attribute '{}'".format(self.__class__.__name__, name))

        self.data.__setattr__(name, value)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        self.format[key] = item

    def __len__(self):
        return len(self.data)

    def append(self, data):
        """Append data to list, if stream/function parameter is a list

        :param data: list item to add
        :type data: various
        """
        if hasattr(self.data, 'append') and callable(self.data.append):
            self.data.append(data)
        else:
            raise AttributeError("class {} has no attribute 'append'".format(self.__class__.__name__))

    def encode(self):
        """Generates the encoded hsms data of the stream/function parameter

        :returns: encoded data
        :rtype: string
        """
        if self.data is None:
            return ""

        return self.data.encode()

    def decode(self, data):
        """Updates stream/function parameter data from the passed data

        :param data: encoded data
        :type data: string
        """
        if self.data is not None:
            self.data.decode(data)

    def set(self, value):
        """Updates the value of the stream/function parameter

        :param value: new value for the parameter
        :type value: various
        """
        self.data.set(value)

    def get(self):
        """Gets the current value of the stream/function parameter

        :returns: current parameter value
        :rtype: various
        """
        return self.data.get()
