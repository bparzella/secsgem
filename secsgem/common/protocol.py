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
import typing

from .events import EventProducer
from .packet import Packet

if typing.TYPE_CHECKING:
    from ..secs.functions.base import SecsStreamFunction


class Protocol(abc.ABC):
    """Abstract base class for a protocol."""

    def __init__(self) -> None:
        """Initialize protocol base object."""
        super().__init__()

        self._event_producer = EventProducer()
        self._event_producer.targets += self

        self._secs_decode: typing.Optional[typing.Callable[[Packet], typing.Any]] = None

    @property
    def events(self):
        """Property for event handling."""
        return self._event_producer

    @property
    @abc.abstractmethod
    def timeouts(self):
        """Property for timeout."""
        raise NotImplementedError("Protocol.timeouts missing implementation")

    @property
    def secs_decode(self) -> typing.Optional[typing.Callable[[Packet], typing.Any]]:
        """Get secs decode."""
        return self._secs_decode

    @secs_decode.setter
    def secs_decode(self, value: typing.Optional[typing.Callable[[Packet], typing.Any]]):
        """Get secs decode."""
        self._secs_decode = value

    @abc.abstractmethod
    def serialize_data(self) -> typing.Dict[str, typing.Any]:
        """Get protocol serialized data for debugging."""
        raise NotImplementedError("Protocol.serialize_data missing implementation")

    @abc.abstractmethod
    def enable(self):
        """Enable the connection."""
        raise NotImplementedError("Protocol.enable missing implementation")

    @abc.abstractmethod
    def disable(self):
        """Disable the connection."""
        raise NotImplementedError("Protocol.disable missing implementation")

    @abc.abstractmethod
    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """
        Send the packet and wait for the response.

        :param function: packet to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        """
        raise NotImplementedError("Protocol.send_stream_function missing implementation")

    @abc.abstractmethod
    def send_and_waitfor_response(self, function: SecsStreamFunction) -> typing.Optional[Packet]:
        """
        Send the packet and wait for the response.

        :param function: packet to be sent
        :type function: :class:`secsgem.secs.functionbase.SecsStreamFunction`
        :returns: Packet that was received
        :rtype: :class:`secsgem.common.Packet`
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
