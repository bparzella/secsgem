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
"""Handler for GEM commands. Used in combination with :class:`secsgem.hsms.HsmsConnectionManager`."""
import logging
import threading
import typing

import secsgem.common
import secsgem.secs


class GemHandler(secsgem.secs.SecsHandler):  # pylint: disable=too-many-instance-attributes
    """Baseclass for creating Host/Equipment models. This layer contains GEM functionality."""

    def __init__(self, settings: secsgem.common.Settings):
        """
        Initialize a gem handler.

        Inherit from this class and override required functions.

        :param connection: connection to use
        """
        super().__init__(settings)
        self._protocol.events.communicating += self._on_communicating

        self._mdln = "secsgem"  #: model number returned by S01E13/14
        self._softrev = "0.1.0"  #: software version returned by S01E13/14

        self._logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._is_host = True

        # not going to HOST_INITIATED_CONNECT because fysom doesn't support two states.
        # but there is a transistion to get out of EQUIPMENT_INITIATED_CONNECT when the HOST_INITIATED_CONNECT happens
        self._communication_state = secsgem.common.Fysom({
            'initial': 'DISABLED',  # 1
            'events': [
                {'name': 'enable', 'src': 'DISABLED', 'dst': 'ENABLED'},  # 2
                {'name': 'disable', 'src': ['ENABLED', 'NOT_COMMUNICATING', 'COMMUNICATING',
                                            'EQUIPMENT_INITIATED_CONNECT', 'WAIT_DELAY', 'WAIT_CRA',
                                            "HOST_INITIATED_CONNECT", "WAIT_CR_FROM_HOST"], 'dst': 'DISABLED'},  # 3
                {'name': 'select', 'src': 'NOT_COMMUNICATING', 'dst': 'EQUIPMENT_INITIATED_CONNECT'},  # 5
                {'name': 'communicationreqfail', 'src': 'WAIT_CRA', 'dst': 'WAIT_DELAY'},  # 6
                {'name': 'delayexpired', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 7
                {'name': 'messagereceived', 'src': 'WAIT_DELAY', 'dst': 'WAIT_CRA'},  # 8
                {'name': 's1f14received', 'src': 'WAIT_CRA', 'dst': 'COMMUNICATING'},  # 9
                {'name': 'communicationfail', 'src': 'COMMUNICATING', 'dst': 'NOT_COMMUNICATING'},  # 14
                # 15 (WAIT_CR_FROM_HOST is running in background - AND state -
                # so if s1f13 is received we go all communicating)
                {'name': 's1f13received', 'src': ['WAIT_CR_FROM_HOST', 'WAIT_DELAY', 'WAIT_CRA'],
                 'dst': 'COMMUNICATING'},
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

        self._wait_cra_timer = None
        self._comm_delay_timer = None
        self._establish_communication_timeout = 10

        self._report_id_counter = 1000

        self._wait_event_list: typing.List[threading.Event] = []

    def __repr__(self) -> str:
        """Generate textual representation for an object of this class."""
        return f"{self.__class__.__name__} {str(self.serialize_data())}"

    @property
    def communication_state(self) -> secsgem.common.Fysom:
        """Get the communication state model."""
        return self._communication_state

    def serialize_data(self) -> typing.Dict[str, typing.Any]:
        """
        Get serialized data.

        :returns: data to serialize for this object
        :rtype: dict
        """
        data = self.protocol.serialize_data()
        data.update({'communicationState': self._communication_state.current,
                     'commDelayTimeout': self._establish_communication_timeout,
                     'reportIDCounter': self._report_id_counter})
        return data

    def enable(self) -> None:
        """Enable the connection."""
        self._communication_state.enable()  # type: ignore
        self.protocol.enable()

        self._logger.info("Connection enabled")

    def disable(self) -> None:
        """Disable the connection."""
        self.protocol.disable()
        self._communication_state.disable()  # type: ignore

        self._logger.info("Connection disabled")

    def _on_message_received(self, data: typing.Dict[str, typing.Any]):
        """
        Message received from protocol layer.

        :param data: received event data
        """
        message = data["message"]
        if self._communication_state.isstate('WAIT_CRA'):
            if message.header.stream == 1 and message.header.function == 13:
                if self._is_host:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                                                    "MDLN": []}),
                                       message.header.system)
                else:
                    self.send_response(self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                                                    "MDLN": [self._mdln, self._softrev]}),
                                       message.header.system)

                self._communication_state.s1f13received()  # type: ignore
            elif message.header.stream == 1 and message.header.function == 14:
                self._communication_state.s1f14received()  # type: ignore
        elif self._communication_state.isstate('WAIT_DELAY'):
            pass
        elif self._communication_state.isstate('COMMUNICATING'):
            threading.Thread(target=self._handle_stream_function, args=(message, ),
                             name=f"secsgem_gemHandler_callback_S{message.header.stream}F{message.header.function}"
                             ).start()

    def _on_communicating(self, _):
        """Selected received from hsms layer."""
        self._communication_state.select()

    def _on_wait_cra_timeout(self):
        """Linktest time timed out, so send linktest request."""
        self._communication_state.communicationreqfail()

    def _on_wait_comm_delay_timeout(self):
        """Linktest time timed out, so send linktest request."""
        self._communication_state.delayexpired()

    def _on_state_wait_cra(self, _):
        """
        Connection state model changed to state WAIT_CRA.

        :param data: event attributes
        :type data: object
        """
        self._logger.debug("connectionState -> WAIT_CRA")

        self._wait_cra_timer = threading.Timer(self.protocol.timeouts.t3, self._on_wait_cra_timeout)
        self._wait_cra_timer.start()

        if self._is_host:
            self.send_stream_function(self.stream_function(1, 13)())
        else:
            self.send_stream_function(self.stream_function(1, 13)([self._mdln, self._softrev]))

    def _on_state_wait_delay(self, _):
        """
        Connection state model changed to state WAIT_DELAY.

        :param data: event attributes
        :type data: object
        """
        self._logger.debug("connectionState -> WAIT_DELAY")

        self._comm_delay_timer = threading.Timer(self._establish_communication_timeout,
                                                 self._on_wait_comm_delay_timeout)
        self._comm_delay_timer.start()

    def _on_state_leave_wait_cra(self, _):
        """
        Connection state model changed to state WAIT_CRA.

        :param data: event attributes
        :type data: object
        """
        if self._wait_cra_timer is not None:
            self._wait_cra_timer.cancel()

    def _on_state_leave_wait_delay(self, _):
        """
        Connection state model changed to state WAIT_DELAY.

        :param data: event attributes
        :type data: object
        """
        if self._comm_delay_timer is not None:
            self._comm_delay_timer.cancel()

    def _on_state_communicating(self, _):
        """
        Connection state model changed to state COMMUNICATING.

        :param data: event attributes
        :type data: object
        """
        self._logger.debug("connectionState -> COMMUNICATING")

        self.events.fire("handler_communicating", {'handler': self})

        for event in self._wait_event_list:
            event.set()

    def on_connection_closed(self, connection):
        """Handle connection was closed event."""
        self._logger.info("Connection was closed")

        # call parent handlers
        super().on_connection_closed(connection)

        if self._communication_state.current == "COMMUNICATING":
            # update communication state
            self._communication_state.communicationfail()

    def on_commack_requested(self) -> int:
        """
        Get the acknowledgement code for the connection request.

        override to accept or deny connection request

        :returns: 0 when connection is accepted, 1 when connection is denied
        :rtype: integer
        """
        return 0

    def send_process_program(self,
                             ppid: typing.Union[int, str],
                             ppbody: str):
        """
        Send a process program.

        :param ppid: Transferred process programs ID
        :type ppid: string
        :param ppbody: Content of process program
        :type ppbody: string
        """
        # send remote command
        self._logger.info("Send process program %s", ppid)

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(7, 3)(
            {"PPID": ppid, "PPBODY": ppbody}))).get()

    def request_process_program(self, 
                                ppid: typing.Union[int, str]) -> typing.Tuple[typing.Union[int, str], str]:
        """
        Request a process program.

        :param ppid: Transferred process programs ID
        :type ppid: string
        """
        self._logger.info("Request process program %s", ppid)

        # send remote command
        s7f6 = self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(7, 5)(ppid)))
        return s7f6.PPID.get(), s7f6.PPBODY.get()

    def waitfor_communicating(self, timeout: typing.Optional[float] = None) -> bool:
        """
        Wait until connection gets into communicating state. Returns immediately if state is communicating.

        :param timeout: seconds to wait before aborting
        :type timeout: float
        :returns: True if state is communicating, False if timed out
        :rtype: bool
        """
        event = threading.Event()
        self._wait_event_list.append(event)

        if self._communication_state.isstate("COMMUNICATING"):
            self._wait_event_list.remove(event)
            return True

        result = event.wait(timeout)

        self._wait_event_list.remove(event)

        return result

    def _on_s01f01(self, 
                   handler: secsgem.secs.SecsHandler, 
                   message: secsgem.common.Message) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 1, Are You There.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        if self._is_host:
            return self.stream_function(1, 2)()

        return self.stream_function(1, 2)([self._mdln, self._softrev])

    def _on_s01f13(self, 
                   handler: secsgem.secs.SecsHandler, 
                   message: secsgem.common.Message) -> typing.Optional[secsgem.secs.SecsStreamFunction]:
        """
        Handle Stream 1, Function 13, Establish Communication Request.

        Args:
            handler: handler the message was received on
            message: complete message received

        """
        del handler, message  # unused parameters

        if self._is_host:
            return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(), "MDLN": []})

        return self.stream_function(1, 14)({"COMMACK": self.on_commack_requested(),
                                            "MDLN": [self._mdln, self._softrev]})
