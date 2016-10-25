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
"""Handler for GEM commands. Used in combination with :class:`secsgem.HsmsHandler.HsmsConnectionManager`"""

import logging
import threading

from ..common.fysom import Fysom
from ..secs.handler import SecsHandler

class GemHandler(SecsHandler):
    """Baseclass for creating Host/Equipment models. This layer contains GEM functionality. Inherit from this class and override required functions.

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
        SecsHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

        self.MDLN = "secsgem"  #: model number returned by S01E13/14
        self.SOFTREV = "0.0.6"  #: software version returned by S01E13/14

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self.isHost = True

        # not going to HOST_INITIATED_CONNECT because fysom doesn't support two states. 
        # but there is a transistion to get out of EQUIPMENT_INITIATED_CONNECT when the HOST_INITIATED_CONNECT happens
        self.communicationState = Fysom({
            'initial': 'DISABLED',  # 1
            'events': [
                {'name': 'enable', 'src': 'DISABLED', 'dst': 'ENABLED'},  # 2
                {'name': 'disable', 'src': ['ENABLED', 'NOT_COMMUNICATING', 'COMMUNICATING', 'EQUIPMENT_INITIATED_CONNECT', 'WAIT_DELAY', 'WAIT_CRA', \
                    "HOST_INITIATED_CONNECT", "WAIT_CR_FROM_HOST"], 'dst': 'DISABLED'},  # 3
                {'name': 'select', 'src': 'NOT_COMMUNICATING', 'dst': 'EQUIPMENT_INITIATED_CONNECT'},  # 5
                {'name': 'communicationreqfail', 'src': 'WAIT_CRA', 'dst': 'WAIT_DELAY'},  # 6
                {'name': 'delayexpired', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 7
                {'name': 'messagereceived', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 8
                {'name': 's1f14received', 'src': 'WAIT_CRA', 'dst': 'COMMUNICATING'},  # 9
                {'name': 'communicationfail', 'src': 'COMMUNICATING', 'dst': 'NOT_COMMUNICATING'},  # 14
                # 15 (WAIT_CR_FROM_HOST is running in background - AND state - so if s1f13 is received we go all communicating)
                {'name': 's1f13received', 'src': ['WAIT_CR_FROM_HOST', 'WAIT_DELAY', 'WAIT_CRA'], 'dst': 'COMMUNICATING'},  
            ],
            'callbacks': {
                'onWAIT_CRA': self._on_state_wait_cra,
                'onWAIT_DELAY': self._on_state_wait_delay,
                'onleaveWAIT_CRA': self._on_state_leave_wait_cra,
                'onleaveWAIT_DELAY': self._on_state_leave_wait_delay,
                'onCOMMUNICATING': self._on_state_communicating,
                # 'onselect': self.onStateSelect,
            },
            'autoforward': [
                {'src': 'ENABLED', 'dst': 'NOT_COMMUNICATING'},  # 4
                {'src': 'EQUIPMENT_INITIATED_CONNECT', 'dst': 'WAIT_CRA'},  # 5
                {'src': 'HOST_INITIATED_CONNECT', 'dst': 'WAIT_CR_FROM_HOST'},  # 10
            ]
        })

        self.waitCRATimer = None
        self.commDelayTimer = None
        self.establishCommunicationTimeout = 10

        self.reportIDCounter = 1000

        self.waitEventList = []

    def __repr__(self):
        """Generate textual representation for an object of this class"""
        return "{} {}".format(self.__class__.__name__, str(self._serialize_data()))

    def _serialize_data(self):
        """Returns data for serialization

        :returns: data to serialize for this object
        :rtype: dict
        """
        data = SecsHandler._serialize_data(self)
        data.update({'communicationState': self.communicationState.current, 'commDelayTimeout': self.establishCommunicationTimeout, \
            'reportIDCounter': self.reportIDCounter})
        return data

    def enable(self):
        """Enables the connection"""
        self.connection.enable()
        self.communicationState.enable()

        self.logger.info("Connection enabled")

    def disable(self):
        """Disables the connection"""
        self.connection.disable()
        self.communicationState.disable()

        self.logger.info("Connection disabled")

    def _on_hsms_packet_received(self, packet):
        """Packet received from hsms layer

        :param packet: received data packet
        :type packet: :class:`secsgem.HsmsPacket`
        """
        if self.communicationState.isstate('WAIT_CRA'):
            if packet.header.stream == 1 and packet.header.function == 13:
                if self.isHost:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": []}), packet.header.system)
                else:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": [self.MDLN, self.SOFTREV]}), \
                        packet.header.system)

                self.communicationState.s1f13received()
            elif packet.header.stream == 1 and packet.header.function == 14:
                self.communicationState.s1f14received()
        elif self.communicationState.isstate('WAIT_DELAY'):
            pass
        elif self.communicationState.isstate('COMMUNICATING'):
            threading.Thread(target=self._handle_stream_function, args=(packet, ), \
                name="secsgem_gemHandler_callback_S{}F{}".format(packet.header.stream, packet.header.function)).start()

    def _on_hsms_select(self):
        """Selected received from hsms layer"""
        self.communicationState.select()

    def _on_wait_cra_timeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.communicationreqfail()

    def _on_wait_comm_delay_timeout(self):
        """Linktest time timed out, so send linktest request"""
        self.communicationState.delayexpired()

    def _on_state_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_CRA")

        self.waitCRATimer = threading.Timer(self.connection.T3, self._on_wait_cra_timeout)
        self.waitCRATimer.start()

        if self.isHost:
            self.send_stream_function(self.stream_function(1, 13)())
        else:
            self.send_stream_function(self.stream_function(1, 13)([self.MDLN, self.SOFTREV]))

    def _on_state_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> WAIT_DELAY")

        self.commDelayTimer = threading.Timer(self.establishCommunicationTimeout, self._on_wait_comm_delay_timeout)
        self.commDelayTimer.start()

    def _on_state_leave_wait_cra(self, _):
        """Connection state model changed to state WAIT_CRA

        :param data: event attributes
        :type data: object
        """
        if self.waitCRATimer is not None:
            self.waitCRATimer.cancel()

    def _on_state_leave_wait_delay(self, _):
        """Connection state model changed to state WAIT_DELAY

        :param data: event attributes
        :type data: object
        """
        if self.commDelayTimer is not None:
            self.commDelayTimer.cancel()

    def _on_state_communicating(self, _):
        """Connection state model changed to state COMMUNICATING

        :param data: event attributes
        :type data: object
        """
        self.logger.debug("connectionState -> COMMUNICATING")

        self.events.fire("handler_communicating", {'handler': self})

        for event in self.waitEventList:
            event.set()

    def on_connection_closed(self, connection):
        """Connection was closed"""
        self.logger.info("Connection was closed")

        # call parent handlers
        SecsHandler.on_connection_closed(self, connection)

        if self.communicationState.current == "COMMUNICATING":
            # update communication state
            self.communicationState.communicationfail()

    def on_commack_requested(self):
        """Get the acknowledgement code for the connection request

        override to accept or deny connection request

        :returns: 0 when connection is accepted, 1 when connection is denied
        :rtype: integer
        """
        return 0

    def send_process_program(self, ppid, ppbody):
        """Send a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        :param ppbody: Content of process program
        :type ppbody: string
        """
        # send remote command
        self.logger.info("Send process program %s", ppid)

        return self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 3)({"PPID": ppid, "PPBODY": ppbody}))).get()

    def request_process_program(self, ppid):
        """Request a process program

        :param ppid: Transferred process programs ID
        :type ppid: string
        """
        self.logger.info("Request process program %s", ppid)

        # send remote command
        s7f6 = self.secs_decode(self.send_and_waitfor_response(self.stream_function(7, 5)(ppid)))
        return s7f6.PPID.get(), s7f6.PPBODY.get()

    def waitfor_communicating(self, timeout=None):
        """Wait until connection gets into communicating state. Returns immediately if state is communicating

        :param timeout: seconds to wait before aborting
        :type timeout: float
        :returns: True if state is communicating, False if timed out
        :rtype: bool
        """
        event = threading.Event()
        self.waitEventList.append(event)

        if self.communicationState.isstate("COMMUNICATING"):
            self.waitEventList.remove(event)
            return True

        result = event.wait(timeout)

        self.waitEventList.remove(event)

        return result

    def _on_s01f01(self, handler, packet):
        """Callback handler for Stream 1, Function 1, Are You There

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        del handler, packet  # unused parameters

        if self.isHost:
            return self.stream_function(1, 2)()
        else:
            return self.stream_function(1, 2)([self.MDLN, self.SOFTREV])

    def _on_s01f13(self, handler, packet):
        """Callback handler for Stream 1, Function 13, Establish Communication Request

        :param handler: handler the message was received on
        :type handler: :class:`secsgem.hsms.handler.HsmsHandler`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsms.packets.HsmsPacket`
        """
        del handler, packet  # unused parameters

        if self.isHost:
            return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": []})
        else:
            return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": [self.MDLN, self.SOFTREV]})
