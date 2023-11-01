#####################################################################
# collection_event.py
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
"""Wrapper for GEM collection event."""
import typing

import secsgem.secs.variables


class CollectionEvent:
    """Collection event definition."""

    def __init__(self,
                 ceid: typing.Union[int, str],
                 name: str,
                 data_values: typing.List[typing.Union[int, str]],
                 **kwargs):
        """Initialize a collection event.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Custom parameters can be set with the keyword arguments,
        they will be passed to the GemEquipmentHandlers callback
        :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_dv_value_request`.

        If use_callbacks is disabled, you can set the value with the value property.

        Args:
            ceid: ID of the collection event
            name: long name of the collection event
            data_values: data values available for this event

        """
        self.ceid = ceid
        self.name = name
        self.data_values = data_values

        self.id_type: typing.Type[secsgem.secs.variables.Base]

        if isinstance(self.ceid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
