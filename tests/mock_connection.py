#####################################################################
# mock_connection.py
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
"""Mock class for connection."""
from __future__ import annotations

import datetime

import secsgem.common
import secsgem.hsms


class MockHsmsConnection(secsgem.common.Connection):
    """Hsms connection mock class."""

    def __init__(self, settings: secsgem.common.Settings) -> None:
        super().__init__(settings)

        self._packets = []
        self._fail_send = False


    def enable(self):
        """Enable the connection.

        Open port and start receiver thread.
        """

    def disable(self):
        """Disable the connection.

        Close port and stop receiver thread.
        """

    def simulate_connect(self):
        """Simulate connection established."""
        self.on_connected({"source": self})

    def expect_block(self, system_id=None, s_type=None, stream=None, function=None, timeout=5):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            for packet in self._packets:
                match = False
                if system_id is not None and packet.header.system == system_id:
                    match = True

                if s_type is not None and packet.header.s_type.value == s_type:
                    match = True

                if stream is not None and packet.header.stream == stream:
                    match = True

                if function is not None and packet.header.function == function:
                    match = True

                if match:
                    self._packets.remove(packet)
                    return packet

                if datetime.datetime.now() > end_time:
                    return None

    def send_data(self, data: bytes) -> bool:
        """Send data to the remote host.

        Args:
            data: encoded data.

        Returns:
            True if succeeded, False if failed

        """
        if self._fail_send:
            self._fail_send = False

            return False

        self._packets.append(secsgem.hsms.HsmsBlock.decode(data))

    def fail_next_send(self):
        self._fail_send = True

    def simulate_message(self, message: secsgem.hsms.HsmsMessage):
        """Simulate incoming block."""
        for block in message.blocks:
            self.on_data({"source": self, "data": block.encode()})
