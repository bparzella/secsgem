#####################################################################
# streams_functions.py
#
# (c) Copyright 2023-2024, Benjamin Parzella. All rights reserved.
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
"""Container class for streams and functions."""

from __future__ import annotations

import typing

from ._all import secs_streams_functions
from .base import SecsStreamFunction

if typing.TYPE_CHECKING:
    import secsgem.common


class StreamsFunctions:
    """Container for functions classes."""

    def __init__(
        self,
        functions: list[type[SecsStreamFunction]] | None = None,
    ) -> None:
        """Initialize streams functions container."""
        if functions is None:
            functions = secs_streams_functions.copy()

        self._functions = functions

    def stream(self, stream: int) -> list[type[SecsStreamFunction]]:
        """Get all functions for a stream.

        Args:
            stream: number of the stream.

        Returns:
            list of function classes for this stream

        """
        return [function for function in self._functions if function.stream == stream]

    def function(self, stream: int, function: int) -> type[SecsStreamFunction] | None:
        """Get a specific function.

        Args:
            stream: number of the stream
            function: number of the function

        Returns:
            function class

        """
        functions = [func for func in self._functions if func.stream == stream and func.function == function]

        if len(functions) == 0:
            return None
        if len(functions) > 1:
            raise ValueError(f"More than one function found for S{stream:02}F{function:02}: {functions}")

        return functions[0]

    def decode(self, message: secsgem.common.Message) -> SecsStreamFunction:
        """Get object of decoded stream and function class, or None if no class is available.

        Args:
            message: message to get object for

        Returns:
            matching stream and function object

        """
        if message is None:
            raise ValueError("Decoding failed, missing message")

        func = self.function(message.header.stream, message.header.function)
        if func is None:
            raise ValueError("Decoding failed, invalid message")

        if isinstance(message.data, SecsStreamFunction):
            return message.data

        function = func()
        function.decode(message.data)

        return function

    def update(self, function: type[SecsStreamFunction]):
        """Add or update a function descriptor."""
        functions = [
            func for func in self._functions if func.stream == function.stream and func.function == function.function
        ]

        if functions:
            for func in functions:
                self._functions.remove(func)

        self._functions.append(function)
