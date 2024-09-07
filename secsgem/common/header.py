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

from __future__ import annotations

import abc
import typing

HeaderT = typing.TypeVar("HeaderT", bound="Header")


class Header(abc.ABC):
    """Abstract base class for a message header."""

    length = -1

    def __init__(  # pylint: disable=too-many-arguments
        self,
        system: int,
        session_id: int,
        stream: int,
        function: int,
        require_response: bool,
    ):
        """Initialize a hsms header.

        Args:
            system: message ID
            session_id: device / session ID
            stream: stream
            function: function
            require_response: True when a response is required

        """
        self._session_id = session_id
        self._stream = stream
        self._function = function
        self._system = system
        self._require_response = require_response

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

    @property
    def require_response(self) -> bool:
        """Get require response flag."""
        return self._require_response

    @abc.abstractmethod
    def encode(self) -> bytes:
        """Encode header to message.

        Returns:
            encoded header

        """
        raise NotImplementedError("Header.encode missing implementation")

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: bytes) -> Header:
        """Decode byte array header to Header object.

        Args:
            data: byte-encode header data

        Returns:
            Header object

        """
        raise NotImplementedError("Header.decode missing implementation")

    @property
    @abc.abstractmethod
    def _as_dictionary(self) -> dict[str, typing.Any]:
        """Get the data as dictionary.

        Returns:
            Header data as dictionary.

        """
        raise NotImplementedError("Header._as_dictionary missing implementation")

    def updated_with(self: HeaderT, **kwargs) -> HeaderT:
        """Get a new header with updated fields.

        Args:
            kwargs: parameter name will update constructor field

        Returns:
            new header with modified data

        """
        data = self._as_dictionary

        data.update(kwargs)

        return self.__class__(**data)
