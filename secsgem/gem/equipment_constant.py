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
import typing

import secsgem.secs


class EquipmentConstant:  # pylint: disable=too-many-instance-attributes
    """Equipment constant definition."""

    def __init__(self,
                 ecid: typing.Union[int, str],
                 name: str,
                 min_value: typing.Union[int, float],
                 max_value: typing.Union[int, float],
                 default_value: typing.Union[int, float],
                 unit: str,
                 value_type: typing.Type[secsgem.secs.variables.Base],
                 use_callback: bool = True,
                 **kwargs):
        """
        Initialize an equipment constant.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Custom parameters can be set with the keyword arguments,
        they will be passed to the GemEquipmentHandlers callbacks
        :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_request`
        and :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_update` .

        If use_callbacks is disabled, you can set the value with the value property.

        :param ecid: ID of the equipment constant
        :type ecid: various
        :param name: long name
        :type name: string
        :param min_value: minimum value
        :type min_value: various
        :param max_value: maximum value
        :type max_value: various
        :param default_value: default value
        :type default_value: various
        :param unit: unit (see SEMI E5, Units of Measure)
        :type unit: string
        :param value_type: type of the status variable
        :type value_type: type of class inherited from :class:`secsgem.secs.variables.Base`
        :param use_callback: use the GemEquipmentHandler callbacks to get and set variable (True) or use internal value
        :type use_callback: boolean
        """
        self.ecid = ecid
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.unit = unit
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = default_value

        self.id_type: typing.Type[secsgem.secs.variables.Base]

        if isinstance(self.ecid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
