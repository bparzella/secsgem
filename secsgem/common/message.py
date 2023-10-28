#####################################################################
# message.py
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
"""Message base class."""
from __future__ import annotations

import abc

from .header import Header


class Message(abc.ABC):
    """Abstract base class for a message."""

    @property
    @abc.abstractmethod
    def header(self) -> Header:
        """Get the header."""
        raise NotImplementedError("Message.header missing implementation")

    @property
    @abc.abstractmethod
    def data(self) -> bytes:
        """Get the header."""
        raise NotImplementedError("Message.data missing implementation")

    @abc.abstractmethod
    def encode(self) -> bytes:
        """
        Encode message object to transmittable bytes.

        Returns:
            byte-encoded message

        """
        raise NotImplementedError("Message.encode missing implementation")

    @staticmethod
    @abc.abstractmethod
    def decode(data: bytes) -> Message:
        """Decode byte array Message to Message object.

        Args:
            data: byte-encode message data

        Returns
            received message object

        """
        raise NotImplementedError("Message.decode missing implementation")
