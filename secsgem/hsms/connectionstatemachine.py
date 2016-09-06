#####################################################################
# connectionstatemachine.py
#
# (c) Copyright 2013-2016, Benjamin Parzella. All rights reserved.
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
"""Contains the state machine for the connection state."""

from transitions.extensions import HierarchicalMachine as Machine

class ConnectionStateMachine(object):
    states = ["NOT_CONNECTED", {'name': 'CONNECTED', 'children': ['NOT_SELECTED', 'SELECTED']}]

    def __init__(self, callbacks=None):
        self.machine = Machine(model=self, states=ConnectionStateMachine.states, initial='NOT_CONNECTED', auto_transitions=False, queued=True)  # transition 1

        if callbacks is None:
            self.callbacks = {}
        else:
            self.callbacks = callbacks

        self.machine.add_transition('connect', 'NOT_CONNECTED', 'CONNECTED_NOT_SELECTED')  # transition 2
        self.machine.add_transition('disconnect', 'CONNECTED', 'NOT_CONNECTED')  # transition 3
        self.machine.add_transition('select', 'CONNECTED_NOT_SELECTED', 'CONNECTED_SELECTED')  # transition 4
        self.machine.add_transition('deselect', 'CONNECTED_SELECTED', 'CONNECTED_NOT_SELECTED')  # transition 5
        self.machine.add_transition('timeoutT7', 'CONNECTED_NOT_SELECTED', 'NOT_CONNECTED')  # transition 6

    def on_enter_CONNECTED(self):
        if "on_enter_CONNECTED" in self.callbacks:
            self.callbacks["on_enter_CONNECTED"]()

    def on_exit_CONNECTED(self):
        if "on_exit_CONNECTED" in self.callbacks:
            self.callbacks["on_exit_CONNECTED"]()

    def on_enter_CONNECTED_SELECTED(self):
        if "on_enter_CONNECTED_SELECTED" in self.callbacks:
            self.callbacks["on_enter_CONNECTED_SELECTED"]()
