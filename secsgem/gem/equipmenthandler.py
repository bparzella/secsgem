#####################################################################
# equipmenthandler.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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
"""Handler for GEM equipment."""

from secsgem.gem.handler import GemHandler
from secsgem.secs.variables import SecsVarString, SecsVarU4, SecsVarArray

class StatusVariable:
    """Status variable definition

    You can manually set the secs-type of the id with the 'id_type' keyword argument.

    Custom parameters can be set with the keyword arguments,
    they will be passed to the GemEquipmentHandlers callback
    :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_sv_value_request`.

    If use_callbacks is disabled, you can set the value with the value property.

    :param svid: ID of the status variable
    :type svid: various
    :param name: long name of the status variable
    :type name: string
    :param unit: unit (see SEMI E5, Units of Measure)
    :type unit: string
    :param value_type: type of the status variable
    :type value_type: type of class inherited from :class:`secsgem.secs.variables.SecsVar`
    :param use_callback: use the GemEquipmentHandler callbacks to get variable (True) or use internal value
    :type use_callback: boolean
    """

    def __init__(self, svid, name, unit, value_type, use_callback=True, **kwargs):
        self.svid = svid
        self.name = name
        self.unit = unit
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = 0

        if isinstance(self.svid, int):
            self.id_type = SecsVarU4
        else:
            self.id_type = SecsVarString

        for key, value in kwargs.items():
            setattr(self, key, value)


class EquipmentConstant:
    """Equipment constant definition

    You can manually set the secs-type of the id with the 'id_type' keyword argument.

    Custom parameters can be set with the keyword arguments,
    they will be passed to the GemEquipmentHandlers callbacks
    :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_request`
    and :func:`secsgem.gem.equipmenthandler.GemEquipmentHandler.on_ec_value_update` .

    If use_callbacks is disabled, you can set the value with the value property.

    :param svid: ID of the equipment constant
    :type svid: various
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
    :type value_type: type of class inherited from :class:`secsgem.secs.variables.SecsVar`
    :param use_callback: use the GemEquipmentHandler callbacks to get and set variable (True) or use internal value
    :type use_callback: boolean
    """
    def __init__(self, ecid, name, min_value, max_value, default_value, unit, value_type, use_callback=True, **kwargs):
        self.ecid = ecid
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.unit = unit
        self.value_type = value_type
        self.use_callback = use_callback
        self.value = default_value

        if isinstance(self.ecid, int):
            self.id_type = SecsVarU4
        else:
            self.id_type = SecsVarString

        for key, value in kwargs.items():
            setattr(self, key, value)


class GemEquipmentHandler(GemHandler):
    """Baseclass for creating equipment models. Inherit from this class and override required functions.

    :param address: IP address of remote host
    :type address: string
    :param port: TCP port of remote host
    :type port: integer
    :param active: Is the connection active (*True*) or passive (*False*)
    :type active: boolean
    :param session_id: session / device ID to use for connection
    :type session_id: integer
    :param name: Name of the underlying configuration
    :type name: string
    :param event_handler: object for event handling
    :type event_handler: :class:`secsgem.common.EventHandler`
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port, active, session_id, name, event_handler=None, custom_connection_handler=None):
        GemHandler.__init__(self, address, port, active, session_id, name, event_handler, custom_connection_handler)

        self.isHost = False

        self.register_callback(1, 3, self.s01f03_handler)

        self.register_callback(1, 11, self.s01f11_handler)

        self.register_callback(2, 13, self.s02f13_handler)
        self.register_callback(2, 15, self.s02f15_handler)

        self.register_callback(2, 29, self.s02f29_handler)

        self.register_callback(2, 33, self.s02f33_handler)
        self.register_callback(2, 37, self.s02f37_handler)

        self._status_variables = {
            10: StatusVariable(10, "SV 10", "mm", SecsVarU4),
            "test": StatusVariable("test", "SV test", "deg", SecsVarString),
        }

        self._equipment_constants = {
            10: EquipmentConstant(10, "EC 10", 1, 100, 5, "mm", SecsVarU4),
            "test": EquipmentConstant("test", "EC test", "A", "Z", "DEF", "deg", SecsVarString),
        }

    def on_sv_value_request(self, svid, sv):
        """Get the status variable value depending on its configuation.

        Override in inherited class to provide custom status variable request handling.

        :param svid: Id of the status variable encoded in the corresponding type
        :type svid: :class:`secsgem.secs.variables.SecsVar`
        :param sv: The status variable requested
        :type sv: :class:`secsgem.gem.equipmenthandler.StatusVariable`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.SecsVar`
        """
        return sv.value_type(value=sv.value)

    def on_ec_value_request(self, ecid, ec):
        """Get the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant request handling.

        :param ecid: Id of the equipment constant encoded in the corresponding type
        :type ecid: :class:`secsgem.secs.variables.SecsVar`
        :param ec: The equipment constant requested
        :type ec: :class:`secsgem.gem.equipmenthandler.EquipmentConstant`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.SecsVar`
        """
        return ec.value_type(value=ec.value)

    def on_ec_value_update(self, ecid, ec, value):
        """Set the equipment constant value depending on its configuation.

        Override in inherited class to provide custom equipment constant update handling.

        :param ecid: Id of the equipment constant encoded in the corresponding type
        :type ecid: :class:`secsgem.secs.variables.SecsVar`
        :param ec: The equipment constant to be updated
        :type ec: :class:`secsgem.gem.equipmenthandler.EquipmentConstant`
        :param value: The value encoded in the corresponding type
        :type value: :class:`secsgem.secs.variables.SecsVar`
        """
        ec.value = value.get()

    def _get_sv_value(self, sv):
        """Get the status variable value depending on its configuation

        :param sv: The status variable requested
        :type sv: :class:`secsgem.gem.equipmenthandler.StatusVariable`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.SecsVar`
        """
        if sv.use_callback:
            return self.on_sv_value_request(sv.id_type(value=sv.svid), sv)
        else:
            return sv.value_type(value=sv.value)

    def _get_ec_value(self, ec):
        """Get the equipment constant value depending on its configuation

        :param ec: The equipment requested
        :type ec: :class:`secsgem.gem.equipmenthandler.EquipmentConstant`
        :returns: The value encoded in the corresponding type
        :rtype: :class:`secsgem.secs.variables.SecsVar`
        """
        if ec.use_callback:
            return self.on_ec_value_request(ec.id_type(value=ec.ecid), ec)
        else:
            return ec.value_type(value=ec.value)

    def _set_ec_value(self, ec, value):
        """Get the equipment constant value depending on its configuation

        :param ec: The equipment requested
        :type ec: :class:`secsgem.gem.equipmenthandler.EquipmentConstant`
        :param value: The value encoded in the corresponding type
        :type value: :class:`secsgem.secs.variables.SecsVar`
        """
        if ec.use_callback:
            self.on_ec_value_update(ec.id_type(value=ec.ecid), ec, value)
        else:
            ec.value = value.get()

    def s01f03_handler(self, handler, packet):
        """Callback handler for Stream 1, Function 3, Equipment status request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for svid in self._status_variables:
                sv = self._status_variables[svid]
                responses.append(self._get_sv_value(sv))
        else:
            for svid in message:
                if svid not in self._status_variables:
                    responses.append(SecsVarArray([]))
                else:
                    sv = self._status_variables[svid]
                    responses.append(self._get_sv_value(sv))

        handler.send_response(self.stream_function(1, 4)(responses), packet.header.system)

    def s01f11_handler(self, handler, packet):
        """Callback handler for Stream 1, Function 11, SV namelist request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for svid in self._status_variables:
                sv = self._status_variables[svid]
                responses.append({"SVID": sv.svid, "SVNAME": sv.name, "UNITS": sv.unit})
        else:
            for svid in message:
                if svid not in self._status_variables:
                    responses.append({"SVID": svid, "SVNAME": "", "UNITS": ""})
                else:
                    sv = self._status_variables[svid]
                    responses.append({"SVID": sv.svid, "SVNAME": sv.name, "UNITS": sv.unit})

        handler.send_response(self.stream_function(1, 12)(responses), packet.header.system)

    def s02f13_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 13, Equipment constant request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for ecid in self._equipment_constants:
                ec = self._equipment_constants[ecid]
                responses.append(self._get_ec_value(ec))
        else:
            for ecid in message:
                if ecid not in self._equipment_constants:
                    responses.append(SecsVarArray([]))
                else:
                    ec = self._equipment_constants[ecid]
                    responses.append(self._get_ec_value(ec))

        handler.send_response(self.stream_function(2, 14)(responses), packet.header.system)

    def s02f15_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 15, Equipment constant send

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        eac = 0

        for ec in message:
            if ec.ECID not in self._equipment_constants:
                eac = 1
            else:
                self._set_ec_value(ec.ECID, ec.ECV)

        handler.send_response(self.stream_function(2, 16)(eac), packet.header.system)

    def s02f29_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 29, EC namelist request

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        responses = []

        if len(message) == 0:
            for ecid in self._equipment_constants:
                ec = self._equipment_constants[ecid]
                responses.append({"ECID": ec.ecid, "ECNAME": ec.name, "ECMIN": ec.min_value, "ECMAX": ec.max_value, "ECDEF": ec.default_value, "UNITS": ec.unit})
        else:
            for ecid in message:
                if ecid not in self._equipment_constants:
                    responses.append({"ECID": ecid, "ECNAME": "", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""})
                else:
                    ec = self._equipment_constants[ecid]
                    responses.append({"ECID": ec.ecid, "ECNAME": ec.name, "ECMIN": ec.min_value, "ECMAX": ec.max_value, "ECDEF": ec.default_value, "UNITS": ec.unit})

        handler.send_response(self.stream_function(2, 30)(responses), packet.header.system)

    def s02f33_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 33, Define Report

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        handler.send_response(self.stream_function(2, 34)(0), packet.header.system)

    def s02f37_handler(self, handler, packet):
        """Callback handler for Stream 2, Function 37, En-/Disable Event Report

        .. seealso:: :func:`secsgem.common.StreamFunctionCallbackHandler.register_callback`

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        handler.send_response(self.stream_function(2, 38)(0), packet.header.system)
