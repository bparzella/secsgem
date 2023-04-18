#####################################################################
# data_value.py
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
"""Wrapper for GEM data value."""
import typing

import secsgem.secs


class DataValue:
    """Data value definition."""

    def __init__(self,
                 dvid: typing.Union[int, str],
                 name: str,
                 value_type: typing.Type[secsgem.secs.variables.Base],
                 use_callback: bool = True,
                 **kwargs):
        """
        Initialize a data value.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Custom parameters can be set with the keyword arguments,
        they will be passed to the GemEquipmentHandlers callback
        :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_dv_value_request`.

        If use_callbacks is disabled, you can set the value with the value property.

        :param dvid: ID of the data value
        :type dvid: various
        :param name: long name of the data value
        :type name: string
        :param value_type: type of the data value
        :type value_type: type of class inherited from :class:`secsgem.secs.variables.Base`
        :param use_callback: use the GemEquipmentHandler callbacks to get variable (True) or use internal value
        :type use_callback: boolean
        """
        self.dvid = dvid
        self.name = name
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = 0

        self.id_type: typing.Type[secsgem.secs.variables.Base]

        if isinstance(self.dvid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
