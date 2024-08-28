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

if typing.TYPE_CHECKING:
    from .header import Header

BlockHeaderT = typing.TypeVar("BlockHeaderT", bound="Header")
BlockT = typing.TypeVar("BlockT", bound="Block")

MessageT = typing.TypeVar("MessageT", bound="Message")


class Block(abc.ABC, typing.Generic[BlockHeaderT]):
    """Base class for data block."""

    header_type: type[BlockHeaderT]
    length_format: str
    checksum_format: str

    def __init__(self, header: BlockHeaderT, data: bytes):
        """Initialize a block header.

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

    @property
    def checksum(self) -> int:
        """Get the checksum."""
        if self.checksum_format == "":
            return 0

        calculated_checksum = 0

        for data_byte in self.header.encode() + self.data:
            calculated_checksum += data_byte

        return calculated_checksum

    def encode(self) -> bytes:
        """Encode block data.

        Returns:
            byte-encoded block

        """
        data_length = len(self.data)

        struct_args: tuple = (
            self.header.length + data_length,
            self.header.encode(),
            self.data,
        )

        if self.checksum_format != "":
            struct_args += (self.checksum, )

        return struct.pack(
            f">{self.length_format}{self.header.length}s{data_length}s{self.checksum_format}",
            *struct_args,
        )

    @classmethod
    def decode(cls: type[BlockT], data: bytes) -> BlockT | None:
        """Decode a byte array to Block object.

        Args:
            data: byte-encode packet data

        Returns:
            received packet object

        """
        data_length = struct.unpack_from(f">{cls.length_format}", data)[0] - cls.header_type.length

        data_fields = struct.unpack(
            f">{cls.length_format}{cls.header_type.length}s{data_length}s{cls.checksum_format}",
            data,
        )

        header = cls.header_type.decode(data_fields[1])

        obj = cls(header, data_fields[2])

        if cls.checksum_format != "" and obj.checksum != data_fields[3]:
            return None

        return obj


class Message(abc.ABC, typing.Generic[BlockT]):
    """Abstract base class for a message."""

    block_size = -1
    block_type: type[BlockT]

    def __init__(self, header: BlockHeaderT, data: bytes, complete: bool = True):
        """Initialize a Message object.

        Args:
            header: header used for this message
            data: data part used for streams and functions (SType 0)
            complete: data contains all blocks, False if more blocks coming

        """
        self._blocks: list[BlockT] = self._split_blocks(data, header, complete)

    @classmethod
    def _split_blocks(cls, data: bytes, header: BlockHeaderT, complete: bool = True) -> list[BlockT]:
        if cls.block_size == -1:
            return [cls.block_type(header, data)]

        if len(data) == 0:
            data_blocks = [data]
        else:
            data_blocks = [data[i: i + cls.block_size] for i in range(0, len(data), cls.block_size)]

        blocks = []
        for index, block_data in enumerate(data_blocks):
            last_block = (index + 1) == len(data_blocks)

            if not complete and hasattr(header, "last_block"):
                last_block = header.last_block

            header_data = {
                "block": index + 1,
                "last_block": last_block,
            }
            block_header = header.updated_with(**header_data)
            blocks.append(cls.block_type(block_header, block_data))

        return blocks

    @classmethod
    def from_block(cls: type[MessageT], block: Block) -> MessageT:
        """Initialize Message object from Block object.

        Args:
            block: block to initialize from

        Returns:
            Message object

        """
        return cls(block.header, block.data, complete=False)

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
    def blocks(self) -> list[BlockT]:
        """Get the blocks."""
        return self._blocks

    def __str__(self) -> str:
        """Generate string representation for an object of this class."""
        return f"'header': {self.header} "

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return (
            f"{self.__class__.__name__}"
            f"({{'header': {self.header.__repr__()}, 'data': '{self.data.decode('utf-8')}'}})"
        )
