#####################################################################
# event.py
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
"""Contains helper functions"""

from future.utils import implements_iterator

class Event(object):
    """Class to handle the callbacks for a single event"""

    def __init__(self):
        """Initialize the event class"""
        self._callbacks = []

    def __iadd__(self, other):
        """Add a new callback to event"""
        self._callbacks.append(other)
        return self

    def __isub__(self, other):
        """Remove a callback from event"""
        self._callbacks.remove(other)
        return self

    def __call__(self, data):
        """Raise the event and call all callbacks"""
        for callback in self._callbacks:
            callback(data)

    def __len__(self):
        """Return the number of callbacks"""
        return len(self._callbacks)

    def __repr__(self):
        """Generate representation for an object"""
        return "{}: {}".format(self.__class__.__name__, self._callbacks)

class Targets(object):
    """Class to handle a list of objects as target for events"""

    def __init__(self):
        """Initialize the target class"""
        self._targets = []

    def __iadd__(self, other):
        """Add a targets"""
        self._targets.append(other)
        return self

    def __isub__(self, other):
        """Remove a target"""
        self._targets.remove(other)
        return self

    @implements_iterator
    class TargetsIter(object):
        def __init__(self, values):
            self._values = values
            self._counter = 0

        def __iter__(self):  # pragma: no cover
            """Return the iterator"""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list"""
            if self._counter < len(self._values):
                i = self._counter
                self._counter += 1
                return self._values[i]
            else:
                raise StopIteration()

    def __iter__(self):
        """Return the iterator"""
        return self.TargetsIter(self._targets)

class EventProducer(object):
    """Manages the consumers for the events and handles firing events"""
    
    def __init__(self):
        """Initialize the event producer class"""
        self._targets = Targets()
        self._events = {}
    
    def __getattr__(self, name):
        """Get an event as member of the EventProducer object"""
        if name not in self._events:
            self._events[name] = Event()

        return self._events[name]

    def __iadd__(self, other):
        """Add a the callbacks and targets of another EventProducer to this one"""
        for event_name in other._events:  # noqa
            if event_name not in self._events:
                self._events[event_name] = Event()
            
            for callback in other._events[event_name]._callbacks:  # noqa
                self._events[event_name] += callback
                
        for target in other._targets:  # noqa
            self._targets += target
        return self
    
    def fire(self, event, data):
        """Fire a event

        calls all the available handlers for a specific event

        :param event: name of the event
        :type event: string
        :param data: data connected to this event
        :type data: dict
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
    
    def __repr__(self):
        """Generate representation for an object"""
        return "{}: {}".format(self.__class__.__name__, self._events) 

    @implements_iterator
    class EventsIter(object):
        def __init__(self, keys):
            self._keys = list(keys)
            self._counter = 0

        def __iter__(self):  # pragma: no cover
            """Return the iterator"""
            return self

        def __next__(self):
            """Get the next item or raise StopIteration if at end of list"""
            if self._counter < len(self._keys):
                i = self._counter
                self._counter += 1
                return self._keys[i]
            else:
                raise StopIteration()

    def __iter__(self):
        """Return the iterator"""
        return self.EventsIter([event for event in self._events.keys() if len(self._events[event]) > 0])

    @property
    def targets(self):
        """Targets used as consumer for this producer"""
        return self._targets
    
    @targets.setter
    def targets(self, value):
        if self._targets != value:
            raise AttributeError("can't set attribute")