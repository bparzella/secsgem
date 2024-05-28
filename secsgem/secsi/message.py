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
"""Contains SECS I message class."""
from __future__ import annotations

import secsgem.common

from .header import SecsIHeader


class SecsIBlock(secsgem.common.Block[SecsIHeader]):
    """Data block for SECS I."""

    header_type = SecsIHeader
    length_format = "B"
    checksum_format = "H"


class SecsIMessage(secsgem.common.Message[SecsIBlock]):
    """Class for SECS I message.

    Contains all required data and functions.
    """

    block_size = 244
    block_type = SecsIBlock

    @property
    def header(self) -> SecsIHeader:
        """Get the header."""
        return self._blocks[-1].header

    @property
    def data(self) -> bytes:
        """Get the data."""
        return b"".join(block.data for block in self._blocks)

    @property
    def complete(self) -> bool:
        """Check if the message is complete."""
        return self.blocks[-1].header.last_block

    @classmethod
    def from_block(cls: type[MessageT], block: Block):
        setattr(block.header, "_from_block", True)
        return super().from_block(block)

    @classmethod
    def _split_blocks(cls, data: bytes, header: BlockHeaderT):
        from_block = getattr(header, "_from_block", False)

        if cls.block_size == -1:
            return [cls.block_type(header, data)]

        if len(data) < cls.block_size:
            data_blocks = [data, ]
        else:
            data_blocks = [data[i: i + cls.block_size] for i in range(0, len(data), cls.block_size)]

        blocks = []
        for index, block_data in enumerate(data_blocks):
            block_header = header.updated_with()
            if not from_block:
                header_data = {
                    "block": index + 1,
                    "last_block": (index + 1) == len(data_blocks),
                }
                block_header = header.updated_with(**header_data)

            blocks.append(cls.block_type(block_header, block_data))

        return blocks
