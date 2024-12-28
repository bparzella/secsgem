#####################################################################
# handler.py
#
# (c) Copyright 2013-2024, Benjamin Parzella. All rights reserved.
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
"""Handler for SECS commands."""

from __future__ import annotations

import logging
import typing

import secsgem.common
import secsgem.hsms

if typing.TYPE_CHECKING:
    from .data_items.data_items import DataItems
    from .functions.base import SecsStreamFunction


class SecsHandler:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Baseclass for creating Host/Equipment models. This layer contains the SECS functionality.

    Inherit from this class and override required functions.
    """

    def __init__(self, settings: secsgem.common.Settings):
        """Initialize a secs handler.

        Args:
            settings: settings defining protocol and connection

        """
        self._settings = settings

        self._protocol = settings.create_protocol()
        self._protocol.events.message_received += self._on_message_received

        self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)

        self._callback_handler = secsgem.common.CallbackHandler()
        self._callback_handler.target = self

    @property
    def settings(self) -> secsgem.common.Settings:
        """Get the setting object."""
        return self._settings

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

    def send_response(self, function: SecsStreamFunction, system: int) -> bool:
        """Wrapper for connections send_response function."""
        return self.protocol.send_response(function, system)

    def send_and_waitfor_response(self, function: SecsStreamFunction) -> secsgem.common.Message | None:
        """Wrapper for connections send_and_waitfor_response function."""
        return self.protocol.send_and_waitfor_response(function)

    def send_stream_function(self, function: SecsStreamFunction) -> bool:
        """Wrapper for connections send_stream_function function."""
        return self.protocol.send_stream_function(function)

    @property
    def events(self) -> secsgem.common.EventProducer:
        """Wrapper for connections events."""
        return self.protocol.events

    @property
    def callbacks(self) -> secsgem.common.CallbackHandler:
        """Property for callback handling."""
        return self._callback_handler

    def register_stream_function(self, stream: int, function: int, callback: typing.Callable):
        """Register the function callback for stream and function.

        Args:
            stream: stream to register callback for
            function: function to register callback for
            callback: method to call when stream and functions is received

        """
        name = self._generate_sf_callback_name(stream, function)
        setattr(self._callback_handler, name, callback)

    def unregister_stream_function(self, stream: int, function: int):
        """Unregister the function callback for stream and function.

        Args:
            stream: stream to unregister callback for
            function: function to register callback for

        """
        name = self._generate_sf_callback_name(stream, function)
        setattr(self._callback_handler, name, None)

    def _handle_unknown_functions(self, message: secsgem.common.Message):
        self.logger.warning(
            "unexpected function received S%02dF%02d\n%s",
            message.header.stream,
            message.header.function,
            message.header,
        )

        # reply S09F05 if no callback present
        if message.header.require_response:
            self.send_response(self.stream_function(9, 5)(message.header.encode()), message.header.system)

    def _handle_stream_function(self, message: secsgem.common.Message):
        sf_callback_index = self._generate_sf_callback_name(message.header.stream, message.header.function)

        if sf_callback_index not in self._callback_handler:
            self._handle_unknown_functions(message)
            return

        try:
            callback = getattr(self._callback_handler, sf_callback_index)
            result = callback(self, message)
            if result is not None:
                self.send_response(result, message.header.system)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Callback aborted because of exception, abort sent")
            self.send_response(self.stream_function(message.header.stream, 0)(), message.header.system)

    def _on_message_received(self, data: dict[str, typing.Any]):
        """Message received from protocol layer.

        Args:
            data: received data

        """
        message = data["message"]

        # check if callbacks available for this stream and function
        self._handle_stream_function(message)

    def disable_ceids(self) -> secsgem.common.Message | None:
        """Disable all Collection Events."""
        self.logger.info("Disable all collection events")

        return self.send_and_waitfor_response(self.stream_function(2, 37)({"CEED": False, "CEID": []}))

    def disable_ceid_reports(self) -> secsgem.common.Message | None:
        """Disable all Collection Event Reports."""
        self.logger.info("Disable all collection event reports")

        return self.send_and_waitfor_response(self.stream_function(2, 33)({"DATAID": 0, "DATA": []}))

    def list_svs(self, svs: list[str | int] | None = None) -> SecsStreamFunction | None:
        """Get list of available Status Variables.

        Args:
            svs: Status Variables to list

        Returns:
            available Status Variables

        """
        self.logger.info("Get list of status variables")

        if svs is None:
            svs = []

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(1, 11)(svs)))

    def request_svs(self, svs: list[str | int]) -> SecsStreamFunction | None:
        """Request contents of supplied Status Variables.

        Args:
            svs: Status Variables to request

        Returns:
            values of requested Status Variables

        """
        self.logger.info("Get value of status variables %s", svs)

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(1, 3)(svs)))

    def request_sv(self, sv_id: int | str) -> int | str | None:
        """Request contents of one Status Variable.

        Args:
            sv_id: id of Status Variable

        Returns:
            value of requested Status Variable

        """
        self.logger.info("Get value of status variable %s", sv_id)

        result = self.request_svs([sv_id])

        if result is None:
            return None

        return result[0]

    def list_ecs(self, ecs: list[str | int] | None = None) -> SecsStreamFunction | None:
        """Get list of available Equipment Constants.

        Args:
            ecs: Equipment Constants to list

        Returns:
            available Equipment Constants

        """
        self.logger.info("Get list of equipment constants")

        if ecs is None:
            ecs = []

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(2, 29)(ecs)))

    def request_ecs(self, ecs: list[int | str]) -> SecsStreamFunction | None:
        """Request contents of supplied Equipment Constants.

        Args:
            ecs: Equipment Constants to request

        Returns:
            values of requested Equipment Constants

        """
        self.logger.info("Get value of equipment constants %s", ecs)

        return self.settings.streams_functions.decode(self.send_and_waitfor_response(self.stream_function(2, 13)(ecs)))

    def request_ec(self, ec_id: int | str) -> SecsStreamFunction | None:
        """Request contents of one Equipment Constant.

        Args:
            ec_id: id of Equipment Constant

        Returns:
            value of requested Equipment Constant

        """
        self.logger.info("Get value of equipment constant %s", ec_id)

        return self.request_ecs([ec_id])

    def set_ecs(self, ecs: list[list[str | int | float]]) -> int | str | float | bytes | None:
        """Set contents of supplied Equipment Constants.

        Args:
            ecs: list containing list of id / value pairs

        """
        self.logger.info("Set value of equipment constants %s", ecs)

        return self.settings.streams_functions.decode(
            self.send_and_waitfor_response(self.stream_function(2, 15)(ecs)),
        ).get()

    def set_ec(self, ec_id: int | str, value: int | str | float) -> int | str | float | bytes | None:
        """Set contents of one Equipment Constant.

        Args:
            ec_id: id of Equipment Constant
            value: new content of Equipment Constant

        """
        self.logger.info("Set value of equipment constant %s to %s", ec_id, value)

        return self.set_ecs([[ec_id, value]])

    def send_equipment_terminal(self, terminal_id: int, text: str) -> secsgem.common.Message | None:
        """Set text to equipment terminal.

        Args:
            terminal_id: ID of terminal
            text: text to send

        """
        self.logger.info("Send text to terminal %s", terminal_id)

        return self.send_and_waitfor_response(self.stream_function(10, 3)({"TID": terminal_id, "TEXT": text}))

    def are_you_there(self) -> secsgem.common.Message | None:
        """Check if remote is still replying."""
        self.logger.info("Requesting 'are you there'")

        return self.send_and_waitfor_response(self.stream_function(1, 1)())

    def stream_function(self, stream: int, function: int) -> type[SecsStreamFunction]:
        """Get class for stream and function.

        Args:
            stream: stream to get class for
            function: function to get class for

        Returns:
            class for function

        """
        klass = self.settings.streams_functions.function(stream, function)

        if klass is None:
            raise KeyError(f"Undefined function requested: S{stream:02d}F{function:02d}")

        return klass

    @property
    def data_items(self) -> DataItems:
        """Get data item container.

        Returns:
            data item container

        """
        return self.settings.streams_functions.data_items
