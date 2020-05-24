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
from transitions.extensions.nesting import NestedState
NestedState.separator = '_'

STATE_NOT_CONNECTED = "NOT-CONNECTED"
STATE_CONNECTED = "CONNECTED"
STATE_NOT_SELECTED = "NOT-SELECTED"
STATE_CONNECTED_NOT_SELECTED = "{}{}{}".format(STATE_CONNECTED, NestedState.separator, STATE_NOT_SELECTED)
STATE_SELECTED = "SELECTED"
STATE_CONNECTED_SELECTED = "{}{}{}".format(STATE_CONNECTED, NestedState.separator, STATE_SELECTED)


class ConnectionStateMachine:
    """HSMS Connection state machine."""

    def __init__(self, callbacks=None):
        """
        Initialize the hsms connection state machine.

        :param callbacks: callbacks for the state machine
        """
        self.callbacks = {}

        self.states = [STATE_NOT_CONNECTED,
                       {
                            'name': STATE_CONNECTED,
                            'on_enter': self._on_enter_CONNECTED,
                            'on_exit': self._on_exit_CONNECTED,
                            'children': [
                                STATE_NOT_SELECTED,
                                {
                                    'name': STATE_SELECTED,
                                    'on_enter': self._on_enter_CONNECTED_SELECTED
                                }
                            ]
                       }]

        # transition 1
        self.machine = Machine(model=self, states=self.states, initial=STATE_NOT_CONNECTED, auto_transitions=False)

        if callbacks:
            self.callbacks = callbacks

        self.machine.add_transition('connect', STATE_NOT_CONNECTED, STATE_CONNECTED_NOT_SELECTED)  # transition 2
        self.machine.add_transition('disconnect', STATE_CONNECTED, STATE_NOT_CONNECTED)  # transition 3
        self.machine.add_transition('select', STATE_CONNECTED_NOT_SELECTED, STATE_CONNECTED_SELECTED)  # transition 4
        self.machine.add_transition('deselect', STATE_CONNECTED_SELECTED, STATE_CONNECTED_NOT_SELECTED)  # transition 5
        self.machine.add_transition('timeoutT7', STATE_CONNECTED_NOT_SELECTED, STATE_NOT_CONNECTED)  # transition 6

    def _on_enter_CONNECTED(self):
        if "on_enter_CONNECTED" in self.callbacks:
            self.callbacks["on_enter_CONNECTED"]()

    def _on_exit_CONNECTED(self):
        if "on_exit_CONNECTED" in self.callbacks:
            self.callbacks["on_exit_CONNECTED"]()

    def _on_enter_CONNECTED_SELECTED(self):
        if "on_enter_CONNECTED_SELECTED" in self.callbacks:
            self.callbacks["on_enter_CONNECTED_SELECTED"]()
