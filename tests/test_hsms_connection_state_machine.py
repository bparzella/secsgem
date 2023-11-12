#####################################################################
# test_hsms_connection_state_machine.py
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
"""Tests for HSMS connection state machine"""
from __future__ import annotations

import pytest

import secsgem.common
import secsgem.hsms.connection_state_machine


class TestHsmsConnectionStateMachine:
    """Tests for HSMS connection state machine."""

    def test_initial_state(self):
        """Test the initial state is NOT_CONNECTED"""
        csm = secsgem.hsms.connection_state_machine.ConnectionStateMachine()

        assert csm.current == secsgem.hsms.connection_state_machine.ConnectionState.NOT_CONNECTED

    def test_invalid_transition_name(self):
        """Test the exception and exception message for invalid transition name."""
        csm = secsgem.hsms.connection_state_machine.ConnectionStateMachine()

        with pytest.raises(secsgem.common.UnknownTransitionError) as exc:
            csm._perform_transition("invalid")  # pylint: disable=protected-access

        assert str(exc.value) == "Invalid transition: invalid"

    @pytest.mark.parametrize(
        "transition, source, expected_destination, will_except, exception_text",
        [
            ("connect", "not_connected", "connected_not_selected", False, ""),
            (
                "connect",
                "connected_not_selected",
                "",
                True,
                "Invalid source state for transition 'connect': CONNECTED_NOT_SELECTED (expected NOT_CONNECTED)"
            ),
            (
                "connect",
                "connected_selected",
                "",
                True,
                "Invalid source state for transition 'connect': CONNECTED_SELECTED (expected NOT_CONNECTED)"
            ),
            (
                "disconnect",
                "not_connected",
                "",
                True,
                (
                    "Invalid source state for transition 'disconnect': "
                    "NOT_CONNECTED (expected CONNECTED_NOT_SELECTED/CONNECTED_SELECTED)"
                )
            ),
            ("disconnect", "connected_not_selected", "not_connected", False, ""),
            ("disconnect", "connected_selected", "not_connected", False, ""),
            (
                "select",
                "not_connected",
                "",
                True,
                "Invalid source state for transition 'select': NOT_CONNECTED (expected CONNECTED_NOT_SELECTED)"
            ),
            ("select", "connected_not_selected", "connected_selected", False, ""),
            (
                "select",
                "connected_selected",
                "",
                True,
                "Invalid source state for transition 'select': CONNECTED_SELECTED (expected CONNECTED_NOT_SELECTED)"
            ),
            (
                "deselect",
                "not_connected",
                "",
                True,
                "Invalid source state for transition 'deselect': NOT_CONNECTED (expected CONNECTED_SELECTED)"
            ),
            (
                "deselect",
                "connected_not_selected",
                "",
                True,
                "Invalid source state for transition 'deselect': CONNECTED_NOT_SELECTED (expected CONNECTED_SELECTED)"
            ),
            ("deselect", "connected_selected", "connected_not_selected", False, ""),
        ]
    )
    def test_state_transitions(  # pylint: disable=too-many-arguments
        self,
        transition: str,
        source: str,
        expected_destination: str,
        will_except: bool,
        exception_text: str
    ):
        """Test the exception and exception message for invalid transition name."""
        csm = secsgem.hsms.connection_state_machine.ConnectionStateMachine()

        current_state_attribute = getattr(csm, source)
        transition_function = getattr(csm, transition)

        csm._current_state = current_state_attribute  # pylint: disable=protected-access

        if will_except:
            with pytest.raises(secsgem.common.WrongSourceStateError) as exc:
                transition_function()

            assert str(exc.value) == exception_text
        else:
            destination_attribute = getattr(csm, expected_destination)

            transition_function()

            assert csm.current_state == destination_attribute  # pylint: disable=protected-access
            assert csm.current_state.active  # pylint: disable=protected-access
