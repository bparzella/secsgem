#####################################################################
# protocol_state_machine.py
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
"""SECS-I protocol state machine."""
from __future__ import annotations

import transitions


class ProtocolStateMachine:
    """State machine for SECS I protocol states."""

    states = [
        "IDLE",
        "LINE_CONTROL_SEND",
        "LINE_CONTROL_RECEIVE",
        "SEND",
        "RECEIVE"
    ]

    def __init__(self) -> None:
        """Initialize state machine."""
        self.machine = transitions.Machine(model=self, states=self.states, initial='IDLE')

        self.machine.add_transition("SendRequest", "IDLE", "LINE_CONTROL_SEND")
        self.machine.add_transition("ENQReceived", "IDLE", "LINE_CONTROL_RECEIVE")
        self.machine.add_transition("Contention", "LINE_CONTROL_SEND", "LINE_CONTROL_RECEIVE")
        self.machine.add_transition("Receive", "LINE_CONTROL_RECEIVE", "RECEIVE")
        self.machine.add_transition("Send", "LINE_CONTROL_SEND", "SEND")
        self.machine.add_transition("ReceiveComplete", "RECEIVE", "IDLE")
        self.machine.add_transition("SendComplete", "SEND", "IDLE")
