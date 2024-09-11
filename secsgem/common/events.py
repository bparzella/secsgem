#####################################################################
# event.py
#
# (c) Copyright 2016-2023, Benjamin Parzella. All rights reserved.
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
"""Contains helper functions."""

from __future__ import annotations

import typing


class Event:
    """Class to handle the callbacks for a single event."""

    def __init__(self) -> None:
        """Initialize the event class."""
        self._callbacks: list[typing.Callable[[dict[str, typing.Any]], None]] = []

    def register(self, callback: typing.Callable[[dict[str, typing.Any]], None]) -> None:
        """Add a new callback to event.

        Args:
            callback: function to register as callback

        """
        self._callbacks.append(callback)

    def __iadd__(self, other: typing.Callable[[dict[str, typing.Any]], None]) -> Event:
        """Add a new callback to event.

        Args:
            other: function to register as callback

        Returns:
            updated instance

        """
        self.register(other)
        return self

    def unregister(self, callback: typing.Callable[[dict[str, typing.Any]], None]) -> None:
        """Remove a callback from the event.

        Args:
            callback: function to unregister

        """
        self._callbacks.remove(callback)

    def __isub__(self, other: typing.Callable[[dict[str, typing.Any]], None]) -> Event:
        """Remove a callback from event.

        Args:
            other: function to unregister

        Returns:
            updated instance

        """
        self.unregister(other)
        return self

    def __call__(self, data: dict[str, typing.Any]):
        """Raise the event and call all callbacks."""
        for callback in self._callbacks:
            callback(data)

    def __len__(self) -> int:
        """Return the number of callbacks."""
        return len(self._callbacks)

    def __repr__(self) -> str:
        """Generate representation for an object."""
        return f"{self.__class__.__name__}: {self._callbacks}"


class Targets:
    """Class to handle a list of objects as target for events."""

    def __init__(self) -> None:
        """Initialize the target class."""
        self._targets: list[object] = []

    def __iadd__(self, other: object) -> Targets:
        """Add a targets."""
        self._targets.append(other)
        return self

    def __isub__(self, other: object) -> Targets:
        """Remove a target."""
        self._targets.remove(other)
        return self

    class _TargetsIter:
        def __init__(self, values):
            self._values = values
            self._counter = 0

        def __iter__(self):
            """Return the iterator."""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list."""
            if self._counter < len(self._values):
                i = self._counter
                self._counter += 1
                return self._values[i]

            raise StopIteration

    def __iter__(self) -> _TargetsIter:
        """Return the iterator."""
        return self._TargetsIter(self._targets)


class EventProducer:
    """Manages the consumers for the events and handles firing events."""

    def __init__(self) -> None:
        """Initialize the event producer class."""
        self._targets = Targets()
        self._events: dict[str, Event] = {}

    def __getattr__(self, name: str) -> Event:
        """Get an event as member of the EventProducer object."""
        if name not in self._events:
            self._events[name] = Event()

        return self._events[name]

    def __iadd__(self, other) -> EventProducer:
        """Add a the callbacks and targets of another EventProducer to this one."""
        for event_name in other._events:
            if event_name not in self._events:
                self._events[event_name] = Event()

            for callback in other._events[event_name]._callbacks:
                self._events[event_name] += callback

        for target in other._targets:
            self._targets += target
        return self

    def fire(self, event: str, data: dict[str, typing.Any]):
        """Fire a event.

        calls all the available handlers for a specific event

        Args:
            event: name of the event
            data: data connected to this event

        """
        for target in self._targets:
            generic_handler = getattr(target, "_on_event", None)
            if callable(generic_handler):
                generic_handler(event, data)

            specific_handler = getattr(target, "_on_event_" + event, None)
            if callable(specific_handler):
                specific_handler(data)

        if event in self._events:
            self._events[event](data)

    def __repr__(self) -> str:
        """Generate representation for an object."""
        return f"{self.__class__.__name__}: {self._events}"

    class _EventsIter:
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):
            """Return the iterator."""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list."""
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]

            raise StopIteration

    def __iter__(self) -> _EventsIter:
        """Return the iterator."""
        return self._EventsIter([event for event, event_value in self._events.items() if len(event_value) > 0])

    @property
    def targets(self) -> Targets:
        """Targets used as consumer for this producer."""
        return self._targets

    @targets.setter
    def targets(self, value: Targets):
        if self._targets != value:
            raise AttributeError("can't set attribute")
