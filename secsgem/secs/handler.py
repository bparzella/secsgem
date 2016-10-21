#####################################################################
# handler.py
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
"""Handler for SECS commands. Used in combination with :class:`secsgem.HsmsHandler.HsmsConnectionManager`"""

from __future__ import absolute_import

import logging
import threading
import copy

from ..hsms.handler import HsmsHandler
from . import functions


class SecsHandler(HsmsHandler):
    """Baseclass for creating Host/Equipment models. This layer contains the SECS functionality. Inherit from this class and override required functions.

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
    :param custom_connection_handler: object for connection handling (ie multi server)
    :type custom_connection_handler: :class:`secsgem.hsms.connections.HsmsMultiPassiveServer`
    """

    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        HsmsHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._collectionEvents = {}
        self._dataValues = {}
        self._alarms = {}
        self._remoteCommands = {}

        self.secsStreamsFunctions = copy.deepcopy(functions.secsStreamsFunctions)

    def _generate_sf_callback_name(self, stream, function):
        return "s{stream:02d}f{function:02d}".format(stream=stream, function=function)

    def register_stream_function(self, stream, function, callback):
        """Register the function callback for stream and function.

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
        """Unregister the function callback for stream and function. 

        :param stream: stream to unregister callback for
        :type stream: integer
        :param function: function to register callback for
        :type function: integer
        """
        name = self._generate_sf_callback_name(stream, function)
        setattr(self._callback_handler, name, None)

    @property
    def collection_events(self):
        """Dictionary of available collection events

        *Example*::

            >>> handler = SecsHandler("127.0.0.1", 5000, False, 0, "test")
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
        return self._collectionEvents

    @property
    def data_values(self):
        """Dictionary of available data values

        *Example*::

            >>> handler = SecsHandler("127.0.0.1", 5000, False, 0, "test")
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
        return self._dataValues

    @property
    def alarms(self):
        """Dictionary of available alarms

        *Example*::

            >>> handler = SecsHandler("127.0.0.1", 5000, True, 0, "test")
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
        """Dictionary of available remote commands

        *Example*::

            >>> handler = SecsHandler("127.0.0.1", 5000, True, 0, "test")
            >>> handler.remote_commands["PP_SELECT"] = {'params': [{'name': 'PROGRAM', 'format': 'A'}], 'ceids': [200, 343]}

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
        return self._remoteCommands

    def _handle_stream_function(self, packet):
        sf_callback_index = self._generate_sf_callback_name(packet.header.stream, packet.header.function)

        # return S09F05 if no callback present
        if sf_callback_index not in self._callback_handler:
            self.logger.warning("unexpected function received %s\n%s", sf_callback_index, packet.header)
            if packet.header.requireResponse:
                self.send_response(self.stream_function(9, 5)(packet.header.encode()), packet.header.system)
            
            return

        try:
            callback = getattr(self._callback_handler, sf_callback_index)
            result = callback(self, packet)
            if result is not None:
                self.send_response(result, packet.header.system)
        except Exception:
            self.logger.exception('Callback aborted because of exception, abort sent')
            self.send_response(self.stream_function(packet.header.stream, 0)(), packet.header.system)

    def _on_hsms_packet_received(self, packet):
        """Packet received from hsms layer

        :param packet: received data packet
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        # check if callbacks available for this stream and function
        threading.Thread(target=self._handle_stream_function, args=(packet, ), \
            name="secsgem_secsHandler_callback_S{}F{}".format(packet.header.stream, packet.header.function)).start()

    def disable_ceids(self):
        """Disable all Collection Events."""
        self.logger.info("Disable all collection events")

        return self.send_and_waitfor_response(self.stream_function(2, 37)({"CEED": False, "CEID": []}))

    def disable_ceid_reports(self):
        """Disable all Collection Event Reports."""
        self.logger.info("Disable all collection event reports")

        return self.send_and_waitfor_response(self.stream_function(2, 33)({"DATAID": 0, "DATA": []}))

    def list_svs(self, svs=None):
        """Get list of available Service Variables.

        :returns: available Service Variables
        :rtype: list
        """
        self.logger.info("Get list of service variables")

        if svs is None:
            svs = []

        packet = self.send_and_waitfor_response(self.stream_function(1, 11)(svs))

        return self.secs_decode(packet)

    def request_svs(self, svs):
        """Request contents of supplied Service Variables.

        :param svs: Service Variables to request
        :type svs: list
        :returns: values of requested Service Variables
        :rtype: list
        """
        self.logger.info("Get value of service variables %s", svs)

        packet = self.send_and_waitfor_response(self.stream_function(1, 3)(svs))

        return self.secs_decode(packet)

    def request_sv(self, sv):
        """Request contents of one Service Variable.

        :param sv: id of Service Variable
        :type sv: int
        :returns: value of requested Service Variable
        :rtype: various
        """
        self.logger.info("Get value of service variable %s", sv)

        return self.request_svs([sv])[0]

    def list_ecs(self, ecs=None):
        """Get list of available Equipment Constants.

        :returns: available Equipment Constants
        :rtype: list
        """
        self.logger.info("Get list of equipment constants")

        if ecs is None:
            ecs = []
        packet = self.send_and_waitfor_response(self.stream_function(2, 29)(ecs))

        return self.secs_decode(packet)

    def request_ecs(self, ecs):
        """Request contents of supplied Equipment Constants.

        :param ecs: Equipment Constants to request
        :type ecs: list
        :returns: values of requested Equipment Constants
        :rtype: list
        """
        self.logger.info("Get value of equipment constants %s", ecs)

        packet = self.send_and_waitfor_response(self.stream_function(2, 13)(ecs))

        return self.secs_decode(packet)

    def request_ec(self, ec):
        """Request contents of one Equipment Constant.

        :param ec: id of Equipment Constant
        :type ec: int
        :returns: value of requested Equipment Constant
        :rtype: various
        """
        self.logger.info("Get value of equipment constant %s", ec)

        return self.request_ecs([ec])

    def set_ecs(self, ecs):
        """Set contents of supplied Equipment Constants.

        :param ecs: list containing list of id / value pairs
        :type ecs: list
        """
        self.logger.info("Set value of equipment constants %s", ecs)

        packet = self.send_and_waitfor_response(self.stream_function(2, 15)(ecs))

        return self.secs_decode(packet).get()

    def set_ec(self, ec, value):
        """Set contents of one Equipment Constant.

        :param ec: id of Equipment Constant
        :type ec: int
        :param value: new content of Equipment Constant
        :type value: various
        """
        self.logger.info("Set value of equipment constant %s to %s", ec, value)

        return self.set_ecs([[ec, value]])

    def send_equipment_terminal(self, terminal_id, text):
        """Set text to equipment terminal

        :param terminal_id: ID of terminal
        :type terminal_id: int
        :param text: text to send
        :type text: string
        """
        self.logger.info("Send text to terminal %s", terminal_id)

        return self.send_and_waitfor_response(self.stream_function(10, 3)({"TID": terminal_id, "TEXT": text}))

    def get_ceid_name(self, ceid):
        """Get the name of a collection event

        :param ceid: ID of collection event
        :type ceid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if ceid in self._collectionEvents:
            if "name" in self._collectionEvents[ceid]:
                return self._collectionEvents[ceid]["name"]

        return ""

    def get_dvid_name(self, dvid):
        """Get the name of a data value

        :param dvid: ID of data value
        :type dvid: integer
        :returns: Name of the event or empty string if not found
        :rtype: string
        """
        if dvid in self._dataValues:
            if "name" in self._dataValues[dvid]:
                return self._dataValues[dvid]["name"]

        return ""

    def are_you_there(self):
        """Check if remote is still replying"""
        self.logger.info("Requesting 'are you there'")

        return self.send_and_waitfor_response(self.stream_function(1, 1)())

    def stream_function(self, stream, function):
        """Get class for stream and function

        :param stream: stream to get function for
        :type stream: int
        :param function: function to get
        :type function: int
        :return: matching stream and function class
        :rtype: secsSxFx class
        """
        if stream not in self.secsStreamsFunctions:
            self.logger.warning("unknown function S%02dF%02d", stream, function)
            return None
        else:
            if function not in self.secsStreamsFunctions[stream]:
                self.logger.warning("unknown function S%02dF%02d", stream, function)
                return None
            else:
                return self.secsStreamsFunctions[stream][function]

    def secs_decode(self, packet):
        """Get object of decoded stream and function class, or None if no class is available.

        :param packet: packet to get object for
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        :return: matching stream and function object
        :rtype: secsSxFx object
        """
        if packet is None:
            return None

        if packet.header.stream not in self.secsStreamsFunctions:
            self.logger.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None

        if packet.header.function not in self.secsStreamsFunctions[packet.header.stream]:
            self.logger.warning("unknown function S%02dF%02d", packet.header.stream, packet.header.function)
            return None

        function = self.secsStreamsFunctions[packet.header.stream][packet.header.function]()
        function.decode(packet.data)

        return function
