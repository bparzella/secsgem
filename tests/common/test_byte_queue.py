#####################################################################
# test_byte_queue.py
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
"""Tests for the block_send_info module."""
from __future__ import annotations

import threading

from secsgem.common import ByteQueue


class TestByteQueue:
    """Tests for ByteQueue class."""

    def test_clear(self):
        """Test the clear method of a ByteQueue object."""
        queue = ByteQueue()

        assert len(queue) == 0

        queue.append(b"test")

        assert len(queue) == 4

        queue.clear()

        assert len(queue) == 0

    def test_pop(self):
        """Test the pop methods of a ByteQueue object."""
        queue = ByteQueue()
        queue.append(b"test")

        assert queue.pop() == b"t"
        assert queue.pop(2) == b"es"
        assert queue.pop_byte() == 116

        assert len(queue) == 0

    def test_peek(self):
        """Test the peek methods of a ByteQueue object."""
        queue = ByteQueue()
        queue.append(b"test")

        assert queue.peek() == b"t"
        assert queue.peek(2) == b"te"
        assert queue.peek_byte() == 116

        assert len(queue) == 4

    def test_wait_for_byte(self):
        """Test waiting for bytes using threading."""
        queue = ByteQueue()
        result = None

        def _wait_for_queue():
            nonlocal result
            result = queue.wait_for()

        thread = threading.Thread(target=_wait_for_queue, daemon=True)
        thread.start()

        queue.append(b"test")

        thread.join()

        assert result == b"t"
        assert len(queue) == 3

    def test_wait_for_bytes(self):
        """Test waiting for bytes using threading."""
        queue = ByteQueue()
        result = None

        def _wait_for_queue():
            nonlocal result
            result = queue.wait_for(2)

        thread = threading.Thread(target=_wait_for_queue, daemon=True)
        thread.start()

        queue.append(b"test")

        thread.join()

        assert result == b"te"
        assert len(queue) == 2
