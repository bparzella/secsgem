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
import struct
import typing

from .header import Header

BlockHeaderT = typing.TypeVar("BlockHeaderT", bound="Header")
BlockT = typing.TypeVar("BlockT", bound="Block")

MessageT = typing.TypeVar("MessageT", bound="Message")


class Block(abc.ABC, typing.Generic[BlockHeaderT]):
    """Base class for data block."""

    header_type: typing.Type[BlockHeaderT]

    def __init__(self, header: BlockHeaderT, data: bytes):
        """
        Initialize a block header.

        Args:
            header: block header
            data: block data

        """
        self._header = header
        self._data = data

    @property
    def header(self) -> BlockHeaderT:
        """Get the header."""
        return self._header

    @property
    def data(self) -> bytes:
        """Get the data."""
        return self._data

    def encode(self) -> bytes:
        """Encode block data.

        Returns:
            byte-encoded block

        """
        headerdata = self.header.encode()

        length = len(headerdata) + len(self.data)

        return struct.pack(">L", length) + headerdata + self.data

    @classmethod
    def decode(cls: typing.Type[BlockT], data: bytes) -> BlockT:
        """Decode byte array hsms packet to HsmsPacket object.

        Args:
            data: byte-encode packet data

        Returns:
            received packet object

        """
        data_length = len(data) - cls.header_type.length

        header = cls.header_type.decode(data[:cls.header_type.length])
        res = struct.unpack(f">{data_length}s", data[cls.header_type.length:])

        return cls(header, res[0])


class Message(abc.ABC, typing.Generic[BlockT]):
    """Abstract base class for a message."""

    block_size = -1
    block_type: typing.Type[BlockT]

    def __init__(self, header: BlockHeaderT, data: bytes):
        """
        Initialize a Message object.

        Args:
            header: header used for this message
            data: data part used for streams and functions (SType 0)

        """
        self._blocks: typing.List[BlockT] = self._split_blocks(data, header)

    @classmethod
    def _split_blocks(cls, data: bytes, header: BlockHeaderT) -> typing.List[BlockT]:
        if cls.block_size == -1:
            return cls.block_type(header, data)

        data_blocks = [data[i: i + cls.block_size] for i in range(0, len(data), cls.block_size)]

        blocks = []
        for index, block_data in enumerate(data_blocks):
            header_data = {
                "block": index + 1,
                "last_block": (index + 1) == len(data_blocks)
            }
            block_header = header.updated_with(**header_data)
            blocks.append(cls.block_type(block_header, block_data))

        return blocks

    @classmethod
    def from_block(cls: typing.Type[MessageT], block: Block) -> MessageT:
        """Initialize Message object from Block object.

        Args:
            block to initialize from

        Returns:
            Message object

        """
        return cls(block.header, block.data)

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

    @property
    @abc.abstractmethod
    def complete(self) -> bool:
        """Check if the message is complete."""
        raise NotImplementedError("Message.complete missing implementation")

    @property
    def blocks(self) -> typing.List[BlockT]:
        """Get the blocks."""
        return self._blocks

    def __str__(self) -> str:
        """Generate string representation for an object of this class."""
        return f"'header': {self.header} "

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__}" \
               f"({{'header': {self.header.__repr__()}, 'data': '{self.data.decode('utf-8')}'}})"
