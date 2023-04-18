#####################################################################
# header.py
#
# (c) Copyright 2023, Benjamin Parzella. All rights reserved.
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
"""header base class."""
import abc


class Header(abc.ABC):
    """Abstract base class for a packet header."""

    def __init__(self, system: int, session_id: int, stream: int, function: int):
        """
        Initialize a hsms header.

        :param system: message ID
        :type system: integer
        :param session_id: device / session ID
        :type session_id: integer
        :param stream: stream
        :type stream: integer
        :param function: function
        :type function: integer
        """
        self._session_id = session_id
        self._stream = stream
        self._function = function
        self._system = system

    @property
    def session_id(self) -> int:
        """Get session id."""
        return self._session_id

    @property
    def stream(self) -> int:
        """Get stream."""
        return self._stream

    @property
    def function(self) -> int:
        """Get function."""
        return self._function

    @property
    def system(self) -> int:
        """Get system."""
        return self._system
