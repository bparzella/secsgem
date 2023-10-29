#####################################################################
# protocol.py
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
"""protocol base class."""
from __future__ import annotations

import abc
import logging
import random
import typing

from .connection import Connection
from .events import EventProducer
from .message import Message
from .timeouts import Timeouts

if typing.TYPE_CHECKING:
    from .settings import Settings
    from ..secs.functions.base import SecsStreamFunction


class Protocol(abc.ABC):
    """Abstract base class for a protocol."""

    def __init__(self, settings: Settings) -> None:
        """Initialize protocol base object."""
        super().__init__()

        self._settings = settings

        self._event_producer = EventProducer()
        self._event_producer.targets += self

        self._system_counter = random.randint(0, (2 ** 32) - 1)

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._communication_logger = logging.getLogger("communication")

        self.__connection: typing.Optional[Connection] = None

    @property
    def _connection(self) -> Connection:
        if self.__connection is None:
            self.__connection = self._settings.create_connection()
            self.__connection.on_connected.register(self._on_connected)
            self.__connection.on_data.register(self._on_connection_data_received)
            self.__connection.on_disconnecting.register(self._on_disconnecting)
            self.__connection.on_disconnected.register(self._on_disconnected)

        return self.__connection

    @abc.abstractmethod
    def _on_connected(self, _: typing.Dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_connected missing implementation")

    @abc.abstractmethod
    def _on_connection_data_received(self, _: typing.Dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_connection_data_received missing implementation")

    @abc.abstractmethod
    def _on_disconnecting(self, _: typing.Dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_disconnecting missing implementation")

    @abc.abstractmethod
    def _on_disconnected(self, _: typing.Dict[str, typing.Any]):
        raise NotImplementedError("Protocol._on_disconnected missing implementation")

    @property
    def events(self):
        """Property for event handling."""
        return self._event_producer

    def get_next_system_counter(self):
        """
        Return the next System.

        :returns: System for the next command
        :rtype: integer
        """
        self._system_counter += 1

        if self._system_counter > ((2 ** 32) - 1):
            self._system_counter = 0

        return self._system_counter

    def enable(self):
        """Enable the connection."""
        self._connection.enable()

    def disable(self):
        """Disable the connection."""
        self._connection.disable()

    @property
    def timeouts(self) -> Timeouts:
        """Property for timeout."""
        return self._settings.timeouts

    @abc.abstractmethod
    def serialize_data(self) -> typing.Dict[str, typing.Any]:
        """Get protocol serialized data for debugging."""
        raise NotImplementedError("Protocol.serialize_data missing implementation")

    @abc.abstractmethod
    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            True if sent successful

        """
        raise NotImplementedError("Protocol.send_stream_function missing implementation")

    @abc.abstractmethod
    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[Message]:
        """
        Send the message and wait for the response.

        Args:
            function: message to be sent

        Returns:
            message that was received

        """
        raise NotImplementedError("Protocol.send_and_waitfor_response missing implementation")

    @abc.abstractmethod
    def send_response(self, function: SecsStreamFunction, system: int) -> bool:
        """
        Send response function for system.

        :param function: function to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :param system: system to reply to
        :type system: int
        """
        raise NotImplementedError("Protocol.send_response missing implementation")
