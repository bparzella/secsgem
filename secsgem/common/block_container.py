#####################################################################
# block_container.py
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
"""Container to collect blocks for messages."""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .message import Message, Block

MessageT = typing.TypeVar("MessageT", bound="Message")
BlockT = typing.TypeVar("BlockT", bound="Block")


class BlockContainer(typing.Generic[MessageT, BlockT]):
    """Container for message blocks."""

    message_type: typing.Type[Message]

    def __init__(self) -> None:
        """Initialize container."""
        self._messages: typing.Dict[int, MessageT] = {}

    def add_block(self, block: BlockT) -> typing.Optional[MessageT]:
        """Add a block, and get completed message if available.

        Args:
            block: block to add

        Returns:
            completed message or None if paket not complete

        """
        if block.header.system not in self._messages:
            self._messages[block.header.system] = self.message_type.from_block(block)
        else:
            self._messages[block.header.system].blocks.append(block)

        message = self._messages[block.header.system]

        if not message.complete:
            return None

        del self._messages[block.header.system]
        return message
