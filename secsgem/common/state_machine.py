#####################################################################
# state_machine.py
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
"""State machine for connection state."""

from __future__ import annotations

import logging
import typing
from typing import Any

from .events import EventProducer

if typing.TYPE_CHECKING:
    import enum


class UnknownTransitionError(Exception):
    """Exception for unknown transition."""

    def __init__(self, transition: str) -> None:
        """Initialize unknown transition exception.

        Args:
            transition: name of the transition

        """
        super().__init__(f"Invalid transition: {transition}")


class WrongSourceStateError(Exception):
    """Exception for wrong source state for transition."""

    def __init__(self, transition: str, expected: str, actual: str) -> None:
        """Initialize wrong source state exception.

        Args:
            transition: name of the transition
            expected: expected source state
            actual: actual source state

        """
        super().__init__(f"Invalid source state for transition '{transition}': {actual} (expected {expected})")


class State:
    """State machine state class."""

    def __init__(
        self,
        state: enum.Enum,
        name: str,
        parent: State | None = None,
        initial: bool = False,
    ) -> None:
        """Initialize state object.

        Args:
            state: state
            name: state name
            parent: parent state
            initial: is initial state

        """
        self._state = state
        self._name = name
        self._parent = parent
        self._active = initial

        self._event_producer = EventProducer()

    @property
    def state(self) -> enum.Enum:
        """Get the connection state for this state."""
        return self._state

    @property
    def name(self) -> str:
        """Get the name for this state."""
        return self._name

    @property
    def events(self) -> EventProducer:
        """Property for event handling."""
        return self._event_producer

    @property
    def parent(self) -> State | None:
        """Get parent state if available."""
        return self._parent

    @property
    def active(self) -> bool:
        """Get if the state is active."""
        return self._active

    def enter(self, source: State | None):
        """Enter the state.

        Args:
            source: state to enter from.

        """
        self.events.fire("enter", {})

        self._active = True

        if self.parent is not None and (source is None or source.parent != self.parent):
            self.parent.enter(source.parent if source is not None else None)

    def leave(self, destination: State | None):
        """Leave the state.

        Args:
            destination: state to enter from.

        """
        self.events.fire("leave", {})

        self._active = False

        if self.parent is not None and (destination is None or destination.parent != self.parent):
            self.parent.leave(destination.parent if destination is not None else None)


class Transition:
    """State machine transition class."""

    def __init__(
        self,
        name: str,
        sources: State | list[State],
        destination: State,
    ) -> None:
        """Initialize transition object.

        Args:
            name: name of the transition
            sources: source states allowed for transition
            destination: destination state for transition

        """
        self._name = name
        self._sources = sources if isinstance(sources, list) else [sources]
        self._destination = destination

        self._event_producer = EventProducer()

    @property
    def name(self) -> str:
        """Get transition name."""
        return self._name

    @property
    def events(self) -> EventProducer:
        """Property for event handling."""
        return self._event_producer

    @property
    def sources(self) -> list[State]:
        """Get the allowed source states for the transition."""
        return self._sources

    @property
    def destination(self) -> State:
        """Get the destination state for the transition."""
        return self._destination

    def __call__(self) -> Any:
        """Call the transition."""
        self.events.fire("called", {})


class StateMachine:
    """Base state machine."""

    def __init__(self) -> None:
        """Initialize state machine."""
        self._current_state: State
        self._transitions: list[Transition]
        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

    @property
    def current(self) -> enum.Enum:
        """Get the current state enum."""
        return self._current_state.state

    @property
    def current_state(self) -> State:
        """Get the current state."""
        return self._current_state

    def transition(self, name: str) -> Transition:
        """Get the object for a specific transition.

        Args:
            name: transition name

        """
        value = next((transition for transition in self._transitions if transition.name == name), None)

        if value is None:
            raise UnknownTransitionError(name)

        return value

    def _perform_transition(self, name: str) -> None:
        """Perform a transition.

        Args:
            name: transition name

        """
        transition = self.transition(name)

        if self._current_state not in transition.sources:
            raise WrongSourceStateError(
                name,
                "/".join([state.name for state in transition.sources]),
                self._current_state.name,
            )

        self._logger.debug("State change: %s >> %s", self._current_state.name, transition.destination.name)
        self._current_state.leave(transition.destination)

        old_state = self._current_state
        self._current_state = transition.destination

        transition.destination.enter(old_state)

        transition()
