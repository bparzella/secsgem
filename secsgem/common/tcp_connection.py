#####################################################################
# tcp_connection.py
#
# (c) Copyright 2013-2023, Benjamin Parzella. All rights reserved.
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
"""Contains objects and functions to create and handle tcp connection."""

from __future__ import annotations

import logging
import select
import threading
import time
import typing

from .connection import Connection
from .helpers import format_hex, is_errorcode_ewouldblock

if typing.TYPE_CHECKING:
    import socket

    from .settings import Settings


class TcpConnection(Connection):
    """Base connection class used for TCP connection types."""

    select_timeout = 0.5
    """Timeout for select calls ."""

    def __init__(self, settings: Settings):
        """Initialize a TCP connection.

        Args:
            settings: protocol and communication settings

        """
        super().__init__(settings)

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        self._bytestream_logger = logging.getLogger("bytestream")

        # connection socket
        self._sock: socket.socket | None = None

        # receiving thread flags
        self._thread_running = False
        self._stop_thread = False

    @property
    def _socket(self) -> socket.socket:
        if self._sock is None:
            raise ConnectionError(f"TCP socket is not connected: {self}")

        return self._sock

    def _serialize_data(self):
        """Return data for serialization.

        Returns:
            data to serialize for this object

        """
        return {
            "connect_mode": self._settings.connect_mode,
            "remoteAddress": self._settings.address,
            "remotePort": self._settings.port,
            "session_id": self._settings.session_id,
            "connected": self._connected,
        }

    def __str__(self):
        """Get the contents of this object as a string."""
        return (
            f"{self._settings.connect_mode} connection to "
            f"{self._settings.address}:{self._settings.port}"
            f" session_id={self._settings.session_id}"
        )

    def _start_receiver(self):
        """Start the thread for receiving and handling incoming messages.

        Will also do the initial Select and Linktest requests.
        """
        # start data receiving thread
        threading.Thread(
            target=self.__receiver_thread,
            args=(),
            name=f"secsgem_tcpConnection_receiver_{self._settings.address}:{self._settings.port}",
        ).start()

        # wait until thread is running
        while not self._thread_running:
            pass

    def disconnect(self):
        """Close connection."""
        # return if thread isn't running
        if not self._thread_running:
            return

        # set disconnecting flag to avoid another select
        self._disconnecting = True

        # set flag to stop the thread
        self._stop_thread = True

        # wait until thread stopped
        while self._thread_running:
            pass

        # clear disconnecting flag, no selects coming any more
        self._disconnecting = False

    def send_data(self, data: bytes) -> bool:
        """Send data to the remote host.

        Args:
            data: encoded data.

        Returns:
            True if succeeded, False if failed

        """
        retry = True

        # not sent yet, retry
        while retry:
            # wait until socket is writable
            while not select.select([], [self._socket], [], self.select_timeout)[1]:
                pass

            try:
                # send message
                self._socket.send(data)

                # retry will be cleared if send succeeded
                retry = False
            except OSError as exc:
                if not is_errorcode_ewouldblock(exc.errno):
                    # raise if not EWOULDBLOCK
                    return False
                # it is EWOULDBLOCK, so retry sending

            self._bytestream_logger.debug("> %s", format_hex(data))

        return True

    def __receiver_thread_read_data(self):
        # check if shutdown requested
        while not self._stop_thread:
            # check if data available
            select_result = select.select([self._socket], [], [self._socket], self.select_timeout)

            # check if disconnection was started
            if self._disconnecting:
                time.sleep(0.2)
                continue

            if select_result[0]:
                try:
                    # get data from socket
                    recv_data = self._socket.recv(1024)

                    # check if socket was closed
                    if len(recv_data) == 0:
                        self._connected = False
                        self._stop_thread = True
                        continue

                    self._bytestream_logger.debug("< %s", format_hex(recv_data))

                    # add received data to input buffer
                    self.on_data({"source": self, "data": recv_data})
                except OSError as exc:
                    if not is_errorcode_ewouldblock(exc.errno):
                        raise exc

    def __receiver_thread(self):
        """Thread for receiving incoming data and adding it to the receive buffer."""
        self._thread_running = True

        try:
            self.__receiver_thread_read_data()
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("exception")

        # notify listeners of disconnection
        try:
            self.on_disconnecting({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_connection_before_closed handler")

        # close the socket
        self._socket.close()

        # notify listeners of disconnection
        try:
            self.on_disconnected({"source": self})
        except Exception:  # pylint: disable=broad-except
            self._logger.exception("ignoring exception for on_connection_closed handler")

        # reset all flags
        self._connected = False
        self._thread_running = False
        self._stop_thread = False
