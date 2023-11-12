#####################################################################
# test_block_send_info.py
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

from secsgem.common import BlockSendInfo


class TestBlockSendInfo:
    """Tests for BlockSendInfo class."""

    def test_data(self) -> None:
        """Test BlockSendInfo with a failure as result."""
        test_data = b"abcd"

        block_send_info = BlockSendInfo(test_data)
        assert block_send_info.data == test_data

    def test_failure_result(self) -> None:
        """Test BlockSendInfo with a failure as result."""
        test_data = b"abcd"

        block_send_info = BlockSendInfo(test_data)

        block_send_info.resolve(False)
        assert block_send_info.wait() is False

    def test_success_result(self) -> None:
        """Test BlockSendInfo with success as result."""
        test_data = b"abcd"

        block_send_info = BlockSendInfo(test_data)

        block_send_info.resolve(True)
        assert block_send_info.wait() is True
