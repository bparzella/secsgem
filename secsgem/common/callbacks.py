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


class _CallbackCallWrapper:
    def __init__(self, handler, name):
        self.name = name
        self.handler = handler

    def __call__(self, *args, **kwargs):
        return self.handler._call(self.name, *args, **kwargs)  # noqa


class CallbackHandler:
    """
    Handler for callbacks for HSMS/SECS/GEM events.

    This handler manages callbacks for events that can happen on a handler for a connection.
    """

    def __init__(self):
        """Initialize the handler."""
        self._callbacks = {}
        self.target = None
        self._object_intitialized = True

    def __setattr__(self, name, value):
        """
        Set an item as object member.

        :param name: Name of the callback
        :param value: Callback
        """
        if '_object_intitialized' not in self.__dict__ or name in self.__dict__:
            dict.__setattr__(self, name, value)
            return

        if value is None:
            if name in self._callbacks:
                del self._callbacks[name]
        else:
            self._callbacks[name] = value

    def __getattr__(self, name):
        """
        Get a callable function for an event.

        :param name: Name of the event
        :return: Callable representation of the callback
        """
        return _CallbackCallWrapper(self, name)

    class _CallbacksIter:
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):  # pragma: no cover
            return self

        def __next__(self):
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]

            raise StopIteration()

    def __iter__(self):
        """
        Get an iterator for the callbacks.

        :return: Callback iterator.
        """
        return self._CallbacksIter(self._callbacks.keys())

    def __contains__(self, callback):
        """
        Check if a callback is present.

        :param callback: Name of the event
        :return: True if callback present
        """
        if callback in self._callbacks:
            return True

        delegate_handler = getattr(self.target, "_on_" + callback, None)
        if callable(delegate_handler):
            return True

        return False

    def _call(self, callback, *args, **kwargs):
        if callback in self._callbacks:
            return self._callbacks[callback](*args, **kwargs)

        delegate_handler = getattr(self.target, "_on_" + callback, None)
        if callable(delegate_handler):
            return delegate_handler(*args, **kwargs)

        return None
