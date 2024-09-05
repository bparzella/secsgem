#####################################################################
# settings.py
#
# (c) Copyright 2023-2024, Benjamin Parzella. All rights reserved.
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
"""HSMS settings class."""
from __future__ import annotations

import enum

import secsgem.common


class HsmsConnectMode(enum.Enum):
    """Hsms connect mode (active or passive)."""

    ACTIVE = 1
    PASSIVE = 2

    def __repr__(self) -> str:
        """String representation of object."""
        return "Active" if self == self.ACTIVE else "Passive"


class HsmsSettings(secsgem.common.Settings):
    """Settings for HSMS connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.hsms
        >>>
        >>> settings = secsgem.hsms.HsmsSettings(device_type=secsgem.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>
        >>> settings.address
        '127.0.0.1'

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._connect_mode = kwargs.get("connect_mode", HsmsConnectMode.ACTIVE)
        self._address = kwargs.get("address", "127.0.0.1")
        self._port = kwargs.get("port", 5000)

        self._validate_args(kwargs)

    @classmethod
    def _args(cls) -> list[str]:
        return [*super()._args(), "connect_mode", "address", "port"]

    @property
    def connect_mode(self) -> HsmsConnectMode:
        """Hsms connect mode.

        Default: HsmsConnectMode.ACTIVE
        """
        return self._connect_mode

    @property
    def address(self) -> str:
        """Remote (active) or local (passive) IP address.

        Default: "127.0.0.1"
        """
        return self._address

    @property
    def port(self) -> int:
        """TCP port of remote host.

        Default: 5000
        """
        return self._port

    def create_protocol(self) -> secsgem.common.Protocol:
        """Protocol class for this configuration."""
        from .protocol import HsmsProtocol  # pylint: disable=import-outside-toplevel

        return HsmsProtocol(self)

    def create_connection(self) -> secsgem.common.Connection:
        """Connection class for this configuration."""
        if self.connect_mode == HsmsConnectMode.ACTIVE:
            return secsgem.common.TcpClientConnection(self)
        return secsgem.common.TcpServerConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"

    @property
    def is_active(self) -> bool:
        """Check if connection is active."""
        return self.connect_mode == HsmsConnectMode.ACTIVE

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_HSMS_{functionality}_{self.connect_mode}_{self.address}:{self.port}"


class ExistingProtocolSettings(HsmsSettings):
    """Settings for existing HSMS connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.hsms
        >>>
        >>> settings = secsgem.hsms.HsmsSettings(device_type=secsgem.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._existing_protocol = kwargs.get("existing_protocol", None)

    @property
    def existing_protocol(self) -> secsgem.common.Protocol:
        """Existing protocol.

        Default: None
        """
        return self._existing_protocol

    def create_protocol(self) -> secsgem.common.Protocol:
        """Protocol class for this configuration."""
        return self.existing_protocol

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"
