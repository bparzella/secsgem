#####################################################################
# byte_queue.py
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
"""Queue for bytes."""

from __future__ import annotations

import threading


class ByteQueue:
    """FIFO class for queuing and retrieving bytes."""

    def __init__(self) -> None:
        """Initialize the queue."""
        self._buffer = bytearray()
        self._buffer_lock = threading.Condition()

    def append(self, data: bytes):
        """Add bytes to the end of the queue.

        Args:
            data: bytes to add

        """
        with self._buffer_lock:
            self._buffer.extend(data)
            self._buffer_lock.notify_all()

    def pop(self, size: int = 1) -> bytes:
        """Remove and return bytes from the beginning of queue.

        Args:
            size: number of bytes to remove

        Returns:
            removed bytes

        """
        with self._buffer_lock:
            data = self._buffer[:size]
            del self._buffer[:size]
            return data

    def pop_byte(self) -> int:
        """Remove and return single byte from the beginning of queue.

        Returns:
            removed byte

        """
        with self._buffer_lock:
            data = self._buffer[0]
            del self._buffer[0]
            return data

    def peek(self, size: int = 1) -> bytes:
        """Get bytes from beginning of the queue without removing them.

        Args:
            size: number of bytes to peek

        Returns:
            peek bytes

        """
        return self._buffer[:size]

    def peek_byte(self, position: int = 0) -> int:
        """Get single byte in the buffer without removing.

        Args:
            position: byte position to peek at

        Returns:
            peek bytes

        """
        return self._buffer[position]

    def clear(self):
        """Clear the bytes in the queue."""
        with self._buffer_lock:
            self._buffer.clear()

    def __len__(self) -> int:
        """Get the length of the queue.

        Returns:
            queue length

        """
        return len(self._buffer)

    def wait_for(self, size: int = 1, peek: bool = False) -> bytes:
        """Wait until the requested number of bytes is available in the receive queue.

        Args:
            size: number of bytes
            peek: only look, don't remove the item from the queue.

        Returns:
            Found bytes

        """

        def min_size() -> bool:
            return len(self._buffer) >= size

        if len(self._buffer) < size:
            with self._buffer_lock:
                self._buffer_lock.wait_for(min_size)

        if peek:
            return self.peek(size)

        return self.pop(size)

    def wait_for_byte(self, peek: bool = False) -> int:
        """Wait until one byte is available in the receive queue.

        Args:
            peek: only look, don't remove the item from the queue.

        Returns:
            Found byte

        """
        return self.wait_for(peek=peek)[0]
