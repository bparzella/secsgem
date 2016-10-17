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
"""Contains callback handling routines"""

class CallbackHandler(object):
    def __init__(self, delegate=None):
        self._callbacks = {}
        self.delegate = delegate

    def register(self, callback, function):
        self._callbacks[callback] = function

    def unregister(self, callback):
        if callback not in self._callbacks:
            return False

        del self._callbacks[callback]
        return True

    def has(self, callback):
        if callback in self._callbacks:
            return True

        delegate_handler = getattr(self.delegate, "_on_" + callback, None)
        if callable(delegate_handler):
            return True
        
        return False


    def call(self, callback, sender, data):
        if callback in self._callbacks:
            return self._callbacks[callback](sender, data)

        delegate_handler = getattr(self.delegate, "_on_" + callback, None)
        if callable(delegate_handler):
            return delegate_handler(sender, data)

        return None
