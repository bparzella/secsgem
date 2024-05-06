#####################################################################
# equipment_constants_capability.py
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
"""Equipment Constants capability."""
from __future__ import annotations

import secsgem.secs

from .capability import Capability
from .equipment_constant import EquipmentConstant, EquipmentConstantId
from .handler import GemHandler


class EquipmentConstantsCapability(GemHandler, Capability):
    """Equipment Contstants capability on GEM equipment."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize capability."""
        super().__init__(*args, **kwargs)

        self._equipment_constants: dict[int | str | EquipmentConstantId, EquipmentConstant] = {
            EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value: EquipmentConstant(
                EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT,
                "EstablishCommunicationsTimeout",
                10,
                120,
                10,
                "sec",
                secsgem.secs.variables.I2),
            EquipmentConstantId.TIME_FORMAT.value: EquipmentConstant(
                EquipmentConstantId.TIME_FORMAT,
                "TimeFormat",
                0,
                2,
                1,
                "",
                secsgem.secs.variables.I4),
        }

    @property
    def equipment_constants(self) -> dict[int | str | EquipmentConstantId, EquipmentConstant]:
        """The list of the equipments contstants.

        Returns:
            Equipment constant list

        """
        return self._equipment_constants

    def on_ec_value_request(self,
                            equipment_constant_id: secsgem.secs.variables.Base,
                            equipment_constant: EquipmentConstant) -> secsgem.secs.variables.Base:
        """Get the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant request handling.

        Args:
            equipment_constant_id: Id of the equipment constant encoded in the corresponding type
            equipment_constant: The equipment constant requested

        Returns:
            The value encoded in the corresponding type

        """
        del equipment_constant_id  # unused variable

        return equipment_constant.value_type(equipment_constant.value)

    def on_ec_value_update(self,
                           equipment_constant_id: secsgem.secs.variables.Base,
                           equipment_constant: EquipmentConstant,
                           value: int | float):
        """Set the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant update handling.

        Args:
            equipment_constant_id: Id of the equipment constant encoded in the corresponding type
            equipment_constant: The equipment constant to be updated
            value: The value encoded in the corresponding type

        """
        del equipment_constant_id  # unused variable

        equipment_constant.value = value

    def _get_ec_value(self, equipment_constant: EquipmentConstant) -> secsgem.secs.variables.Base:
        """Get the equipment constant value depending on its configuation.

        Args:
            equipment_constant: The equipment requested

        Returns:
            The value encoded in the corresponding type

        """
        if equipment_constant.ecid == EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value:
            return equipment_constant.value_type(self.settings.establish_communication_timeout)
        if equipment_constant.ecid == EquipmentConstantId.TIME_FORMAT.value:
            return equipment_constant.value_type(self._time_format)

        if equipment_constant.use_callback:
            return self.on_ec_value_request(equipment_constant.id_type(equipment_constant.ecid), equipment_constant)
        return equipment_constant.value_type(equipment_constant.value)

    def _set_ec_value(self, equipment_constant: EquipmentConstant, value: int | float):
        """Get the equipment constant value depending on its configuation.

        Args:
            equipment_constant: The equipment requested
            value: The value encoded in the corresponding type

        """
        if equipment_constant.ecid == EquipmentConstantId.ESTABLISH_COMMUNICATIONS_TIMEOUT.value:
            self.settings.establish_communication_timeout = int(value)
        if equipment_constant.ecid == EquipmentConstantId.TIME_FORMAT.value:
            self._time_format = int(value)

        if equipment_constant.use_callback:
            self.on_ec_value_update(equipment_constant.id_type(equipment_constant.ecid), equipment_constant, value)
        else:
            equipment_constant.value = value

    def _on_s02f13(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 2, Function 13, Equipment constant request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        responses = []

        if len(function) == 0:
            responses = [self._get_ec_value(equipment_constant)
                         for equipment_constant in self._equipment_constants.values()]
        else:
            for equipment_constant_id in function:  # type: ignore[attr-defined]
                if equipment_constant_id not in self._equipment_constants:
                    responses.append(secsgem.secs.variables.Array(secsgem.secs.data_items.ECV, []))
                else:
                    equipment_constant = self._equipment_constants[equipment_constant_id]
                    responses.append(self._get_ec_value(equipment_constant))

        return self.stream_function(2, 14)(responses)

    def _on_s02f15(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 2, Function 15, Equipment constant send.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        eac = 0

        for equipment_constant in function:  # type: ignore[attr-defined]
            if equipment_constant.ECID not in self._equipment_constants:
                eac = 1
            else:
                constant = self.equipment_constants[equipment_constant.ECID.get()]

                if constant.min_value is not None and equipment_constant.ECV.get() < constant.min_value:
                    eac = 3

                if constant.max_value is not None and equipment_constant.ECV.get() > constant.max_value:
                    eac = 3

        if eac == 0:
            for equipment_constant in function:  # type: ignore[attr-defined]
                self._set_ec_value(self._equipment_constants[equipment_constant.ECID], equipment_constant.ECV.get())

        return self.stream_function(2, 16)(eac)

    def _on_s02f29(self,
                   handler: secsgem.secs.SecsHandler,
                   message: secsgem.common.Message) -> secsgem.secs.SecsStreamFunction | None:
        """Handle Stream 2, Function 29, EC namelist request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler  # unused parameters

        function = self.settings.streams_functions.decode(message)

        responses = []

        if len(function) == 0:
            responses = [{
                "ECID": eq_constant.ecid,
                "ECNAME": eq_constant.name,
                "ECMIN": eq_constant.min_value if eq_constant.min_value is not None else "",
                "ECMAX": eq_constant.max_value if eq_constant.max_value is not None else "",
                "ECDEF": eq_constant.default_value,
                "UNITS": eq_constant.unit,
            } for eq_constant in self._equipment_constants.values()]
        else:
            for ecid in function:  # type: ignore[attr-defined]
                if ecid not in self._equipment_constants:
                    responses.append({"ECID": ecid, "ECNAME": "", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""})
                else:
                    eq_constant = self._equipment_constants[ecid]
                    responses.append({"ECID": eq_constant.ecid, "ECNAME": eq_constant.name,
                                      "ECMIN": eq_constant.min_value if eq_constant.min_value is not None else "",
                                      "ECMAX": eq_constant.max_value if eq_constant.max_value is not None else "",
                                      "ECDEF": eq_constant.default_value, "UNITS": eq_constant.unit})

        return self.stream_function(2, 30)(responses)
