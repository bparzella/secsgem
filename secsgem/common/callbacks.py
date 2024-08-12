#####################################################################
# callback.py
#
# (c) Copyright 2016, Benjamin Parzella. All rights reserved.
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
"""Contains callback handling routines."""
from __future__ import annotations

import typing


class _CallbackCallWrapper:
    def __init__(self, handler: CallbackHandler, name: str):
        self._name = name
        self._handler = handler

    def __call__(self, *args: tuple, **kwargs: dict) -> typing.Any:
        return self.handler._call(self.name, *args, **kwargs)  # noqa: SLF001

    @property
    def name(self) -> str:
        """Get the callback name."""
        return self._name

    @property
    def handler(self) -> CallbackHandler:
        """Get the handler for the callback."""
        return self._handler


class CallbackHandler:
    """Handler for callbacks for HSMS/SECS/GEM events.

    This handler manages callbacks for events that can happen on a handler for a connection.
    """

    def __init__(self) -> None:
        """Initialize the handler."""
        self._callbacks: dict[str, typing.Callable] = {}
        self.target: object = None
        self._object_intitialized = True

    def __setattr__(self, name: str, value: typing.Callable):
        """Set an item as object member.

        Args:
            name: name of the callback
            value: callback function

        """
        if "_object_intitialized" not in self.__dict__ or name in self.__dict__:
            dict.__setattr__(self, name, value)
            return

        if value is None:
            if name in self._callbacks:
                del self._callbacks[name]
        else:
            self._callbacks[name] = value

    def __getattr__(self, name: str) -> typing.Callable:
        """Get a callable function for an event.

        Args:
            name: name of the event

        """
        return _CallbackCallWrapper(self, name)

    class _CallbacksIter:
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]

            raise StopIteration

    def __iter__(self) -> _CallbacksIter:
        """Get an iterator for the callbacks.

        Returns:
            callback iterator

        """
        return self._CallbacksIter(self._callbacks.keys())

    def __contains__(self, callback: str) -> bool:
        """Check if a callback is present.

        Args:
            callback: name of the event

        Returns:
            True if callback present

        """
        if callback in self._callbacks:
            return True

        delegate_handler = getattr(self.target, "_on_" + callback, None)
        return bool(callable(delegate_handler))

    def _call(self, callback: str, *args, **kwargs) -> typing.Any:
        if callback in self._callbacks:
            return self._callbacks[callback](*args, **kwargs)

        delegate_handler = getattr(self.target, "_on_" + callback, None)
        if callable(delegate_handler):
            return delegate_handler(*args, **kwargs)

        return None
