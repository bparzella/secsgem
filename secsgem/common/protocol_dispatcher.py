#####################################################################
# protocol_dispatcher.py
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
"""Thread that can be triggered and call a callback."""

from __future__ import annotations

import logging
import queue
import threading
import typing

if typing.TYPE_CHECKING:
    from .message import Block
    from .settings import Settings


class ProtocolDispatcher:  # pylint: disable=too-many-instance-attributes
    """Thread that calls a target function when a trigger was raised."""

    def __init__(
        self,
        receiver_target: typing.Callable,
        dispatcher_target: typing.Callable,
        settings: Settings,
    ) -> None:
        """Initialize thread object.

        Args:
            receiver_target: function to call when receiver triggered
            dispatcher_target: function to call when message available for dispatch
            settings: communication/protocol settings

        """
        self._receiver_target = receiver_target
        self._dispatcher_target = dispatcher_target
        self._settings = settings

        self._receiver_thread: threading.Thread | None = None
        self._dispatcher_thread: threading.Thread | None = None

        self._receiver_thread_trigger = threading.Event()
        self._dispatcher_thread_trigger = threading.Event()

        self._dispatch_queue: queue.Queue[tuple[object, Block]] = queue.Queue()

        self._stop_receiver_thread = False
        self._stop_dispatcher_thread = False

    def start(self):
        """Start the thread."""
        self._stop_receiver_thread = False
        self._stop_dispatcher_thread = False

        self._receiver_thread = threading.Thread(
            target=self._receiver_thread_function,
            args=(),
            name=self._settings.generate_thread_name("protocol_receiver"),
            daemon=True,
        )

        self._dispatcher_thread = threading.Thread(
            target=self._dispatcher_thread_function,
            args=(),
            name=self._settings.generate_thread_name("protocol_dispatcher"),
            daemon=True,
        )

        self._receiver_thread.start()
        self._dispatcher_thread.start()

    def stop(self):
        """Stop the thread."""
        if not self._receiver_thread.is_alive():
            return

        self._stop_receiver_thread = True
        self._receiver_thread_trigger.set()

        self._receiver_thread.join()

    def trigger_receiver(self):
        """Trigger the thread to call target function."""
        self._receiver_thread_trigger.set()

    def queue_block(self, source: object, block: Block):
        """Add a block to the dispatch queue and trigger dispatch thread.

        Args:
            source: source of the block
            block: new block

        """
        self._dispatch_queue.put((source, block))
        self._dispatcher_thread_trigger.set()

    def _receiver_thread_function(self):
        while not self._stop_receiver_thread:
            self._receiver_thread_trigger.wait()
            self._receiver_thread_trigger.clear()

            if self._stop_receiver_thread:
                continue

            try:
                self._receiver_target()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                logging.warning("Exception in receiver callback, ignoring", exc_info=exc)

        self._stop_receiver_thread = False

    def _dispatcher_thread_function(self):
        while not self._stop_dispatcher_thread:
            self._dispatcher_thread_trigger.wait()
            self._dispatcher_thread_trigger.clear()

            if self._stop_dispatcher_thread:
                continue

            while self._dispatch_queue.qsize() > 0:
                data = self._dispatch_queue.get()

                try:
                    self._dispatcher_target(*data)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    logging.warning("Exception in dispatcher callback, ignoring", exc_info=exc)

        self._stop_dispatcher_thread = False
