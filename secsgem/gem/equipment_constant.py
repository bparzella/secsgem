#####################################################################
# equipment_constant.py
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
"""Wrapper for GEM equipment constant."""

from __future__ import annotations

import enum

import secsgem.secs


class EquipmentConstantId(enum.Enum):
    """Default IDs for equipment constants."""

    ESTABLISH_COMMUNICATIONS_TIMEOUT = 1
    TIME_FORMAT = 2


class EquipmentConstant:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Equipment constant definition."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        ecid: int | str | EquipmentConstantId,
        name: str,
        min_value: int | float,
        max_value: int | float,
        default_value: int | float,
        unit: str,
        value_type: type[secsgem.secs.variables.Base],
        use_callback: bool = True,
        **kwargs,
    ):
        """Initialize an equipment constant.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Custom parameters can be set with the keyword arguments,
        they will be passed to the GemEquipmentHandlers callbacks
        :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_request`
        and :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_update` .

        If use_callbacks is disabled, you can set the value with the value property.

        Args:
            ecid: ID of the equipment constant
            name: long name
            min_value: minimum value
            max_value: maximum value
            default_value: default value
            unit: unit (see SEMI E5, Units of Measure)
            value_type: type of the status variable
            use_callback: use the GemEquipmentHandler callbacks to get and set variable (True) or use internal value
            **kwargs: additional attributes for object

        """
        self.ecid = ecid if not isinstance(ecid, EquipmentConstantId) else ecid.value
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.unit = unit
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = default_value

        self.id_type: type[secsgem.secs.variables.Base]

        if isinstance(self.ecid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
