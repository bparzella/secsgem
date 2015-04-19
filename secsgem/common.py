#####################################################################
# common.py
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
import types

def formatHex(text):
    """Returns byte arrays (string) formated as hex numbers.

    **Example**::

        >>> data = "asdfg"
        >>> secsgem.common.formatHex(data)
        '61:73:64:66:67'


    :param text: byte array
    :type text: string
    :returns: Formated text
    :rtype: string
    """
    return ":".join("{0:02x}".format(ord(c)) for c in text)

def isWindows():
    """Returns True if running on windows

    :returns: Is windows system
    :rtype: bool
    """
    if sys.platform == "win32":
        return True

    return False

def functionName(function):
    """Gets name of function or method

    :returns: function/method name
    :rtype: string
    """
    if isinstance(function, types.FunctionType):
        return function.__name__
    else:
        return function.__self__.__class__.__name__ + "." + function.__name__

class StreamFunctionCallbackHandler:
    """Base class for all connection classes. Provides functionality for registering and unregistering callbacks for streams and functions."""
    def __init__(self):
        self.callbacks = {}

    def registerCallback(self, stream, function, callback):
        """Register the function callback for stream and function. Multiple callbacks can be registered for one function.

        :param stream: stream to register callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to call when stream and functions is received
        :type callback: def callback(connection)
        """
        name = "s"+str(stream)+"f"+str(function)

        if not name in self.callbacks:
            self.callbacks[name] = []

        self.callbacks[name].append(callback)

    def unregisterCallback(self, stream, function, callback):
        """Unregister the function callback for stream and function. Multiple callbacks can be registered for one function, only the supplied callback will be removed.

        :param stream: stream to unregister callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to remove from callback list
        :type callback: def callback(connection)
        """
        name = "s"+str(stream)+"f"+str(function)

        if callback in self.callbacks[name]:
            self.callbacks[name].remove(callback)

class EventHandler:
    """Class for event handling. Provides functionality for managing events.

    :param target: receiver object for event callbacks
    :type target: object
    :params events: dictionary of event names with handlers
    :type events: dict
    :param genericHandler: receiver function for all events
    :type genericHandler: def handler(eventName, data)
    """
    def __init__(self, target=None, events={}, genericHandler=None):
        self.eventHandlers = {}
        self.target = target
        self.genericHandler = genericHandler

        for event in events:
            self.addEventHandler(event, events[event])

    def fireEvent(self, eventName, params):
        """Fire an event

        :param eventName: event to fire
        :type eventName: string
        :param params: parameters for event
        :type params: dict
        """
        handled = False

        stack = inspect.stack()
        callingClass = stack[2][0].f_locals["self"].__class__.__name__ #.split('.')[-1]
        callingMethod = stack[2][0].f_code.co_name

        if self.target:
            genericHandler = getattr(self.target, "_onEvent", None)
            if callable(genericHandler):
                logging.debug("%s.%s: posting event %s to %s._onEvent" % (callingClass, callingMethod, eventName, self.target.__class__.__name__))
                genericHandler(eventName, params)
                handled = True

            specificHandler = getattr(self.target, "_onEvent" + eventName, None)
            if callable(specificHandler):
                logging.debug("%s.%s: posting event %s to %s._onEvent%s" % (callingClass, callingMethod, eventName, self.target.__class__.__name__, eventName))
                specificHandler(params)
                handled = True

        if eventName in self.eventHandlers:
            for eventHandler in self.eventHandlers[eventName]:
                logging.debug("%s.%s: posting event %s to %s" % (callingClass, callingMethod, eventName, functionName(eventHandler)))
                eventHandler(eventName, params)
                handled = True

        if self.genericHandler:
            logging.debug("%s.%s: posting event %s to %s" % (callingClass, callingMethod, eventName, functionName(self.genericHandler)))
            self.genericHandler(eventName, params)
            handled = True

        if not handled:
            logging.debug("%s.%s: unhandled event %s" % (callingClass, callingMethod, eventName))


    def addEventHandler(self, eventName, handler):
        """Register handler for an event. Multiple handlers can be registered for one event.

        :param eventName: event to register handler for
        :type eventName: string
        :param handler: method to call when event is received
        :type handler: def handler(eventName, handler)
        """
        if not eventName in self.eventHandlers:
            self.eventHandlers[eventName] = []

        self.eventHandlers[eventName].append(handler)

    def removeEventHandler(self, eventName, handler):
        """Unregister handler for an event.

        :param eventName: event to unregister handler for
        :type eventName: string
        :param handler: method to unregister
        :type handler: def handler(eventName, handler)
        """
        if not eventName in self.eventHandlers:
            return

        self.eventHandlers[eventName].remove(handler)

class EventProducer:
    """Class for event production. Provides functionality for sending events.

    :param eventHandler: object for event handling
    :type eventHandler: :class:`secsgem.common.EventHandler`
    """
    def __init__(self, eventHandler):
        self.parentEventHandler = eventHandler

    def fireEvent(self, eventName, data):
        """Fire an event

        :param eventName: event to fire
        :type eventName: string
        :param data: parameters for event
        :type data: dict
        """
        if self.parentEventHandler:
            self.parentEventHandler.fireEvent(eventName, data)
