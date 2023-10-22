#####################################################################
# handler.py
#
# (c) Copyright 2013-2021, Benjamin Parzella. All rights reserved.
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
"""Handler for SECS commands. Used in combination with :class:`secsgem.hsms.HsmsConnectionManager`."""
import logging
import threading
import typing

import secsgem.common
import secsgem.hsms

if typing.TYPE_CHECKING:
    from ..gem.collection_event import CollectionEvent
    from ..gem.data_value import DataValue
    from ..gem.alarm import Alarm
    from ..gem.remote_command import RemoteCommand


class SecsHandler:  # pylint: disable=too-many-instance-attributes
    """
    Baseclass for creating Host/Equipment models. This layer contains the SECS functionality.

    Inherit from this class and override required functions.
    """

    def __init__(self, settings: secsgem.common.Settings):
        """
        Initialize a secs handler.

        Args:
            settings: settings defining protocol and connection

        """
        self.settings = settings

        self._protocol = settings.create_protocol()
        self._protocol.events.packet_received += self._on_packet_received

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._collection_events: typing.Dict[typing.Union[int, str], CollectionEvent] = {}
        self._data_values: typing.Dict[typing.Union[int, str], DataValue] = {}
        self._alarms: typing.Dict[typing.Union[int, str], Alarm] = {}
        self._remote_commands: typing.Dict[typing.Union[int, str], RemoteCommand] = {}

        self._callback_handler = secsgem.common.CallbackHandler()
        self._callback_handler.target = self

    @staticmethod
    def _generate_sf_callback_name(stream: int, function: int) -> str:
        return f"s{stream:02d}f{function:02d}"

    @property
    def protocol(self) -> secsgem.common.Protocol:
        """Get the connection for the handler."""
        return self._protocol

    def enable(self):
        """Enable the connection."""
        self.protocol.enable()

    def disable(self):
        """Disable the connection."""
        self.protocol.disable()

    def send_response(self, *args, **kwargs):
        """Wrapper for connections send_response function."""
        return self.protocol.send_response(*args, **kwargs)

    def send_and_waitfor_response(self, *args, **kwargs):
        """Wrapper for connections send_and_waitfor_response function."""
        return self.protocol.send_and_waitfor_response(*args, **kwargs)

    def send_stream_function(self, *args, **kwargs):
        """Wrapper for connections send_stream_function function."""
        return self.protocol.send_stream_function(*args, **kwargs)

    @property
    def events(self):
        """Wrapper for connections events."""
        return self.protocol.events

    @property
    def callbacks(self):
        """Property for callback handling."""
        return self._callback_handler

    def register_stream_function(self, stream: int, function: int, callback):
        """
        Register the function callback for stream and function.

        :param stream: stream to register callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        :param callback: method to call when stream and functions is received
        :type callback: def callback(connection)
        """
        name = self._generate_sf_callback_name(stream, function)
        setattr(self._callback_handler, name, callback)

    def unregister_stream_function(self, stream, function):
        """
        Unregister the function callback for stream and function.

        :param stream: stream to unregister callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        """
        name = self._generate_sf_callback_name(stream, function)
        setattr(self._callback_handler, name, None)

    @property
    def collection_events(self):
        """
        Get available collection events.

        *Example*::

            >>> settings = secsgem.hsms.HsmsSettings(address="127.0.0.1", port=5000, name="test")
            >>> handler = SecsHandler(settings)
            >>> handler.collection_events[123] = {'name': 'collectionEventName', 'dvids': [1, 5] }

        **Key**

        Id of the collection event (integer)

        **Data**

        Dictionary with the following fields

            name
                Name of the collection event (string)

            dvids
                Data values for the collection event (list of integers)

        """
        return self._collection_events

    @property
    def data_values(self):
        """
        Get available data values.

        *Example*::

            >>> settings = secsgem.hsms.HsmsSettings(address="127.0.0.1", port=5000, name="test")
            >>> handler = SecsHandler(settings)
            >>> handler.data_values[5] = {'name': 'dataValueName', 'ceid': 123 }

        **Key**

        Id of the data value (integer)

        **Data**

        Dictionary with the following fields

            name
                Name of the data value (string)

            ceid
                Collection event the data value is used for (integer)

        """
        return self._data_values

    @property
    def alarms(self):
        """
        Get available alarms.

        *Example*::

            >>> settings = secsgem.hsms.HsmsSettings(address="127.0.0.1", port=5000, name="test")
            >>> handler = SecsHandler(settings)
            >>> handler.alarms[137] = {'ceidon': 1371, 'ceidoff': 1372}

        **Key**

        Id of the alarm (integer)

        **Data**

        Dictionary with the following fields

            ceidon
                Collection event id for alarm on (integer)

            ceidoff
                Collection event id for alarm off (integer)

        """
        return self._alarms

    @property
    def remote_commands(self):
        """
        Get available remote commands.

        *Example*::

            >>> settings = secsgem.hsms.HsmsSettings(address="127.0.0.1", port=5000, name="test")
            >>> handler = SecsHandler(settings)
            >>> handler.remote_commands["PP_SELECT"] = {'params': [{'name': 'PROGRAM', 'format': 'A'}], \
'ceids': [200, 343]}

        **Key**

        Name of the remote command (string)

        **Data**

        Dictionary with the following fields

            params
                Parameters for the remote command (list of dictionaries)

                *Parameters*

                    The dictionaries have the following fields

                    name
                        name of the parameter (string)

                    format
                        format character of the parameter (string)

            ceids
                Collection events ids the remote command might return (list of integers)

        """
        return self._remote_commands

    def _handle_stream_function(self, packet):
        sf_callback_index = self._generate_sf_callback_name(packet.header.stream, packet.header.function)

        # return S09F05 if no callback present
        if sf_callback_index not in self._callback_handler:
            self.logger.warning("unexpected function received %s\n%s", sf_callback_index, packet.header)
            if packet.header.require_response:
                self.send_response(self.stream_function(9, 5)(packet.header.encode()), packet.header.system)

            return

        try:
            callback = getattr(self._callback_handler, sf_callback_index)
            result = callback(self, packet)
            if result is not None:
                self.send_response(result, packet.header.system)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception('Callback aborted because of exception, abort sent')
            self.send_response(self.stream_function(packet.header.stream, 0)(), packet.header.system)

    def _on_packet_received(self, data: secsgem.common.Packet):
        """Packet received from protocol layer.

        Args:
            data: received data

        """
        packet = data["packet"]

        # check if callbacks available for this stream and function
        threading.Thread(
            target=self._handle_stream_function, args=(packet, ),
            name=f"secsgem_secsHandler_callback_S{packet.header.stream}F{packet.header.function}").start()

    def disable_ceids(self):
        """Disable all Collection Events."""
        self.logger.info("Disable all collection events")

        return self.send_and_waitfor_response(self.stream_function(2, 37)({"CEED": False, "CEID": []}))

    def disable_ceid_reports(self):
        """Disable all Collection Event Reports."""
        self.logger.info("Disable all collection event reports")

        return self.send_and_waitfor_response(self.stream_function(2, 33)({"DATAID": 0, "DATA": []}))

    def list_svs(self, svs=None):
        """
        Get list of available Service Variables.

        :returns: available Service Variables
        :rtype: list
        """
        self.logger.info("Get list of service variables")

        if svs is None:
            svs = []

        packet = self.send_and_waitfor_response(self.stream_function(1, 11)(svs))

        return self.settings.streams_functions.decode(packet)

    def request_svs(self, svs):
        """
        Request contents of supplied Service Variables.

        :param svs: Service Variables to request
        :type svs: list
        :returns: values of requested Service Variables
        :rtype: list
        """
        self.logger.info("Get value of service variables %s", svs)

        packet = self.send_and_waitfor_response(self.stream_function(1, 3)(svs))

        return self.settings.streams_functions.decode(packet)

    def request_sv(self, sv_id):
        """
        Request contents of one Service Variable.

        :param sv_id: id of Service Variable
        :type sv_id: int
        :returns: value of requested Service Variable
        :rtype: various
        """
        self.logger.info("Get value of service variable %s", sv_id)

        return self.request_svs([sv_id])[0]

    def list_ecs(self, ecs=None):
        """
        Get list of available Equipment Constants.

        :returns: available Equipment Constants
        :rtype: list
        """
        self.logger.info("Get list of equipment constants")

        if ecs is None:
            ecs = []
        packet = self.send_and_waitfor_response(self.stream_function(2, 29)(ecs))

        return self.settings.streams_functions.decode(packet)

    def request_ecs(self, ecs):
        """
        Request contents of supplied Equipment Constants.

        :param ecs: Equipment Constants to request
        :type ecs: list
        :returns: values of requested Equipment Constants
        :rtype: list
        """
        self.logger.info("Get value of equipment constants %s", ecs)

        packet = self.send_and_waitfor_response(self.stream_function(2, 13)(ecs))

        return self.settings.streams_functions.decode(packet)

    def request_ec(self, ec_id):
        """
        Request contents of one Equipment Constant.

        :param ec_id: id of Equipment Constant
        :type ec_id: int
        :returns: value of requested Equipment Constant
        :rtype: various
        """
        self.logger.info("Get value of equipment constant %s", ec_id)

        return self.request_ecs([ec_id])

    def set_ecs(self, ecs):
        """
        Set contents of supplied Equipment Constants.

        :param ecs: list containing list of id / value pairs
        :type ecs: list
        """
        self.logger.info("Set value of equipment constants %s", ecs)

        packet = self.send_and_waitfor_response(self.stream_function(2, 15)(ecs))

        return self.secs_decode(packet).get()

    def set_ec(self, ec_id, value):
        """
        Set contents of one Equipment Constant.

        :param ec_id: id of Equipment Constant
        :type ec_id: int
        :param value: new content of Equipment Constant
        :type value: various
        """
        self.logger.info("Set value of equipment constant %s to %s", ec_id, value)

        return self.set_ecs([[ec_id, value]])

    def send_equipment_terminal(self, terminal_id, text):
        """
        Set text to equipment terminal.

        :param terminal_id: ID of terminal
        :type terminal_id: int
        :param text: text to send
        :type text: string
        """
        self.logger.info("Send text to terminal %s", terminal_id)

        return self.send_and_waitfor_response(self.stream_function(10, 3)({"TID": terminal_id, "TEXT": text}))

    def get_ceid_name(self, ceid):
        """
        Get the name of a collection event.

        :param ceid: ID of collection event
        :type ceid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if ceid in self._collection_events:
            if "name" in self._collection_events[ceid]:
                return self._collection_events[ceid]["name"]

        return ""

    def get_dvid_name(self, dvid):
        """
        Get the name of a data value.

        :param dvid: ID of data value
        :type dvid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if dvid in self._data_values:
            if "name" in self._data_values[dvid]:
                return self._data_values[dvid]["name"]

        return ""

    def are_you_there(self):
        """Check if remote is still replying."""
        self.logger.info("Requesting 'are you there'")

        return self.send_and_waitfor_response(self.stream_function(1, 1)())

    def stream_function(self, stream, function):
        """
        Get class for stream and function.

        :param stream: stream to get function for
        :type stream: int
        :param function: function to get
        :type function: int
        :return: matching stream and function class
        :rtype: secsSxFx class
        """
        return self.settings.streams_functions.function(stream, function)
