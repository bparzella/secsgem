#####################################################################
# __init__.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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

import sys

import inspect
import logging
import string
import types
import threading


def format_hex(text):
    """Returns byte arrays (string) formated as hex numbers.

    **Example**::

        >>> import secsgem
        >>>
        >>> data = b"asdfg"
        >>> secsgem.common.format_hex(data)
        '61:73:64:66:67'


    :param text: byte array
    :type text: string
    :returns: Formated text
    :rtype: string
    """
    if sys.version_info < (3,):
        return ":".join("{0:02x}".format(ord(c)) for c in text)
    else:
        return ":".join("{0:02x}".format(c) for c in text)


def is_windows():
    """Returns True if running on windows

    :returns: Is windows system
    :rtype: bool
    """
    if sys.platform == "win32":  # pragma: no cover
        return True

    return False


def function_name(function):
    """Gets name of function or method

    :returns: function/method name
    :rtype: string
    """
    if isinstance(function, types.FunctionType):
        return function.__name__
    else:
        return function.__self__.__class__.__name__ + "." + function.__name__

def indent_line(line, spaces=2):
    """Indent line by a number of spaces

    :param line: input text
    :type line: string
    :param spaces: number of spaces to prepend
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    return (' ' * spaces) + line

def indent_block(block, spaces=2):
    """Indent a multiline string by a number of spaces

    :param block: input text
    :type block: string
    :param spaces: number of spaces to prepend to each line
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    lines = block.split('\n')
    lines = filter(None, lines)
    lines = map(lambda line, spc=spaces: indent_line(line, spc), lines)
    return '\n'.join(lines)


class StreamFunctionCallbackHandler(object):
    """Base class for all connection classes. Provides functionality for registering and unregistering callbacks for streams and functions."""
    def __init__(self):
        self.callbacks = {}

    def _generate_callback_name(self, stream, function):
        return "s" + str(stream) + "f" + str(function)

    def register_callback(self, stream, function, callback):
        """Register the function callback for stream and function. Multiple callbacks can be registered for one function.

        :param stream: stream to register callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to call when stream and functions is received
        :type callback: def callback(connection)
        """
        name = self._generate_callback_name(stream, function)

        if name not in self.callbacks:
            self.callbacks[name] = []

        self.callbacks[name].append(callback)

    def unregister_callback(self, stream, function, callback):
        """Unregister the function callback for stream and function. Multiple callbacks can be registered for one function, only the supplied callback will be removed.

        :param stream: stream to unregister callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to remove from callback list
        :type callback: def callback(connection)
        """
        name = self._generate_callback_name(stream, function)

        if callback in self.callbacks[name]:
            self.callbacks[name].remove(callback)


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

        stack = inspect.stack()
        calling_class = stack[2][0].f_locals["self"].__class__.__name__
        calling_method = stack[2][0].f_code.co_name

        if self.target:
            generic_handler = getattr(self.target, "_on_event", None)
            if callable(generic_handler):
                self.logger.debug("%s.%s: posting event %s to %s._on_event" % (calling_class, calling_method, event_name, self.target.__class__.__name__))
                if generic_handler(event_name, params) is not False:
                    handled = True

            specific_handler = getattr(self.target, "_on_event_" + event_name, None)
            if callable(specific_handler):
                self.logger.debug("%s.%s: posting event %s to %s._on_event_%s" % (calling_class, calling_method, event_name, self.target.__class__.__name__, event_name))
                if specific_handler(params):
                    handled = True

        if event_name in self.eventHandlers:
            for eventHandler in self.eventHandlers[event_name]:
                self.logger.debug("%s.%s: posting event %s to %s" % (calling_class, calling_method, event_name, function_name(eventHandler)))
                if eventHandler(event_name, params) is not False:
                    handled = True

        if self.genericHandler:
            self.logger.debug("%s.%s: posting event %s to %s" % (calling_class, calling_method, event_name, function_name(self.genericHandler)))
            if self.genericHandler(event_name, params) is not False:
                handled = True

        if not handled:
            self.logger.debug("%s.%s: unhandled event %s" % (calling_class, calling_method, event_name))

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
        self.parentEventHandler = event_handler

    def fire_event(self, event_name, data, async=False):
        """Fire an event

        :param event_name: event to fire
        :type event_name: string
        :param data: parameters for event
        :type data: dict
        """
        if self.parentEventHandler:
            if async:
                threading.Thread(target=self.parentEventHandler.fire_event, args=(event_name, data), name="EventProducer_fireEventAsync_{}".format(event_name)).start()
            else:
                self.parentEventHandler.fire_event(event_name, data)
