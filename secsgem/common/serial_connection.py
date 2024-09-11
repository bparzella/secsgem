#####################################################################
# serial_connection.py
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
"""Contains objects and functions to create and handle serial connections."""

from __future__ import annotations

import logging
import threading
import time
import typing

import serial

from .connection import Connection
from .helpers import format_hex

if typing.TYPE_CHECKING:
    from .settings import Settings


class SerialConnection(Connection):  # pylint: disable=too-many-instance-attributes
    """Connection class used for serial connections."""

    _receiver_timeout = 0.5

    def __init__(self, settings: Settings):
        """Initialize a serial connection.

        Args:
            settings: protocol and communication settings

        """
        super().__init__(settings)

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._bytestream_logger = logging.getLogger("bytestream")

        self.__port: serial.Serial | None = None

        self._enabled = False
        self._receiver_thread_running = False
        self._stop_receiver_thread = False
        self._receiver_thread: threading.Thread | None = None

    @property
    def _port(self) -> serial.Serial:
        if self.__port is None:
            raise ConnectionError(f"SecsI port is not connected: {self}")

        return self.__port

    def __str__(self):
        """Get the contents of this object as a string."""
        return (
            f"Serial connection to "
            f"{self._settings.port}@{self._settings.speed}"
            f" session_id={self._settings.session_id}"
        )

    def enable(self):
        """Enable the connection.

        Open port and start receiver thread.
        """
        # only start if not already enabled
        if self._enabled:
            return

        # mark connection as enabled
        self._enabled = True

        self.__port = serial.Serial(self._settings.port, self._settings.speed, timeout=self._receiver_timeout)

        # start data receiving thread
        self._receiver_thread = threading.Thread(
            target=self._receiver_thread_function,
            args=(),
            name=f"secsgem_secsIConnection_receiver_{self._settings.port}@{self._settings.speed}",
        )
        self._receiver_thread.daemon = True
        self._receiver_thread.start()

        try:
            self.on_connected({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_connected handler")

        # wait until thread is running
        while not self._receiver_thread_running:
            pass

    def disable(self):
        """Disable the connection.

        Close port and stop receiver thread.
        """
        # only stop if enabled
        if not self._enabled:
            return

        # mark connection as disabled
        self._enabled = False

        self._stop_receiver_thread = True

        # wait for connection thread to stop
        while self._stop_receiver_thread:
            time.sleep(0.2)

    def _receiver_thread_function(self):
        """Thread for receiving incoming data and sending it to the protocol handler."""
        self._receiver_thread_running = True

        try:
            self._receiver_loop()
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("exception")

        # notify listeners of disconnection
        try:
            self.on_disconnecting({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_disconnecting handler")

        # close the socket
        self._port.close()

        # notify listeners of disconnection
        try:
            self.on_disconnected({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_disconnected handler")

        # reset all flags
        self._connected = False
        self._receiver_thread_running = False
        self._stop_receiver_thread = False

    def _receiver_loop(self):
        # check if shutdown requested
        while not self._stop_receiver_thread:
            data = self._port.read(self._port.in_waiting) if self._port.in_waiting > 0 else self._port.read()

            if len(data) > 0:
                self._bytestream_logger.debug("< %s", format_hex(data))
                self.on_data({"source": self, "data": data})

    def send_data(self, data: bytes) -> bool:
        """Send data to the remote host.

        Args:
            data: encoded data.

        Returns:
            True if succeeded, False if failed

        """
        self._bytestream_logger.debug("> %s", format_hex(data))
        self._port.write(data)

        return True
