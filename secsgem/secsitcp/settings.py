#####################################################################
# settings.py
#
# (c) Copyright 2024, Benjamin Parzella. All rights reserved.
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
"""Secs I over TCP settings class."""
from __future__ import annotations

import enum

import secsgem.common
import secsgem.secsi


class SecsITcpConnectMode(enum.Enum):
    """Secs I over TCP connect mode (client or server)."""

    CLIENT = 1
    SERVER = 2

    def __repr__(self) -> str:
        """String representation of object."""
        return "Client" if self == self.CLIENT else "Server"


class SecsITcpSettings(secsgem.secsi.SecsISettings):
    """Settings for Secs I over TCP connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.secsitcp
        >>>
        >>> settings = secsgem.secsitcp.SecsITcpSettings(device_type=secsgem.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>
        >>> settings.address
        '127.0.0.1'

    .. exec::
        import secsgem.secsitcp.settings

        secsgem.secsitcp.settings.SecsITcpSettings._attributes_help()

    """

    @classmethod
    def _attributes(cls) -> list[secsgem.common.Setting]:
        """Get the available settings for the class."""
        return [
            *super()._attributes(),
            secsgem.common.Setting("connect_mode", SecsITcpConnectMode.CLIENT, "Secs I over TCP connect mode"),
            secsgem.common.Setting("address", "127.0.0.1", "Remote (client) or local (server) IP address"),
            secsgem.common.Setting("port", 5000, "TCP port of remote host"),
        ]

    def create_protocol(self) -> secsgem.common.Protocol:
        """Protocol class for this configuration."""
        from ..secsi.protocol import SecsIProtocol  # pylint: disable=import-outside-toplevel

        return SecsIProtocol(self)

    def create_connection(self) -> secsgem.common.Connection:
        """Connection class for this configuration."""
        if self.connect_mode == SecsITcpConnectMode.CLIENT:
            return secsgem.common.TcpClientConnection(self)
        return secsgem.common.TcpServerConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_SECSITCP_{functionality}_{self.connect_mode}_{self.address}:{self.port}"
