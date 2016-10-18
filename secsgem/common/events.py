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

import logging
import threading

class EventHandler(object):
    """Class for event handling. Provides functionality for managing events.

    :param target: receiver object for event callbacks
    :type target: object
    :params events: dictionary of event names with handlers
    :type events: dict
    :param generic_handler: receiver function for all events
    :type generic_handler: def handler(eventName, data)
    """
    def __init__(self, target=None, events=None, generic_handler=None):
        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.eventHandlers = {}
        self.target = target
        self.genericHandler = generic_handler

        if not events:
            events = {}

        for event in events:
            self.add_event_handler(event, events[event])

    def fire_event(self, event_name, params):
        """Fire an event

        :param event_name: event to fire
        :type event_name: string
        :param params: parameters for event
        :type params: dict
        """
        handled = False

        if self.target:
            generic_handler = getattr(self.target, "_on_event", None)
            if callable(generic_handler):
                if generic_handler(event_name, params) is not False:
                    handled = True

            specific_handler = getattr(self.target, "_on_event_" + event_name, None)
            if callable(specific_handler):
                if specific_handler(params):
                    handled = True

        if event_name in self.eventHandlers:
            for eventHandler in self.eventHandlers[event_name]:
                if eventHandler(event_name, params) is not False:
                    handled = True

        if self.genericHandler:
            if self.genericHandler(event_name, params) is not False:
                handled = True

        return handled

    def add_event_handler(self, event_name, handler):
        """Register handler for an event. Multiple handlers can be registered for one event.

        :param event_name: event to register handler for
        :type event_name: string
        :param handler: method to call when event is received
        :type handler: def handler(event_name, handler)
        """
        if event_name not in self.eventHandlers:
            self.eventHandlers[event_name] = []

        self.eventHandlers[event_name].append(handler)

    def remove_event_handler(self, event_name, handler):
        """Unregister handler for an event.

        :param event_name: event to unregister handler for
        :type event_name: string
        :param handler: method to unregister
        :type handler: def handler(event_name, handler)
        """
        if event_name not in self.eventHandlers:
            return

        self.eventHandlers[event_name].remove(handler)


class EventProducer(object):
    """Class for event production. Provides functionality for sending events.

    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, event_handler):
        self._eventHandler = event_handler

    def fire_event(self, event_name, data, async=True):
        """Fire an event

        :param event_name: event to fire
        :type event_name: string
        :param data: parameters for event
        :type data: dict
        """
        if self._eventHandler:
            if async:
                threading.Thread(target=self._eventHandler.fire_event, args=(event_name, data), \
                    name="EventProducer_fireEventAsync_{}".format(event_name)).start()
            else:
                self._eventHandler.fire_event(event_name, data)
