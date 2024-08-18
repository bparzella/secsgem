#####################################################################
# status_variable.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
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
"""Wrapper for GEM status variable."""
from __future__ import annotations

import enum

import secsgem.secs


class StatusVariableId(enum.Enum):
    """Default IDs for status variables."""
    CLOCK = 1001
    CONTROL_STATE = 1002
    EVENTS_ENABLED = 1003
    ALARMS_ENABLED = 1004
    ALARMS_SET = 1005


class StatusVariable:  # pylint: disable=too-few-public-methods
    """Status variable definition."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        svid: int | str | StatusVariableId,
        name: str,
        unit: str,
        value_type: type[secsgem.secs.variables.Base],
        use_callback: bool = True,
        **kwargs,
    ):
        """Initialize a status variable.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Custom parameters can be set with the keyword arguments,
        they will be passed to the GemEquipmentHandlers callback
        :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_sv_value_request`.

        If use_callbacks is disabled, you can set the value with the value property.

        Args:
            svid: ID of the status variable
            name: long name of the status variable
            unit: unit (see SEMI E5, Units of Measure)
            value_type: type of the status variable
            use_callback: use the GemEquipmentHandler callbacks to get variable (True) or use internal value
            kwargs: extra class attributes

        """
        self.svid = svid if not isinstance(svid, StatusVariableId) else svid.value
        self.name = name
        self.unit = unit
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = 0

        self.id_type: type[secsgem.secs.variables.Base]

        if isinstance(self.svid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
