#####################################################################
# mock_settings.py
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
"""Mock class for settings to simulate communication or protocol."""
from __future__ import annotations

import secsgem.common
import secsgem.hsms


class MockSettings(secsgem.common.Settings):
    """Mock settings class."""

    def __init__(
        self,
        protocol_class: type[secsgem.common.Protocol],
        connection_class: type[secsgem.common.Connection] | None = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.protocol = protocol_class(self)
        self.connection = None if connection_class is None else connection_class(self)

    @classmethod
    def _args(cls) -> list[str]:
        return super()._args()

    def create_protocol(self) -> secsgem.common.Protocol:
        """Protocol class for this configuration."""
        return self.protocol

    def create_connection(self) -> secsgem.common.Connection | None:  # type: ignore[override]
        """Connection class for this configuration."""
        return self.connection

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return "Mock"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_Mock_{functionality}"


class MockHsmsSettings(MockSettings):
    """Mock HSMS settings class."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(*args, **kwargs)

        self._connect_mode = kwargs.get("connect_mode", secsgem.hsms.HsmsConnectMode.ACTIVE)
        self._address = kwargs.get("address", "127.0.0.1")
        self._port = kwargs.get("port", 5000)

    @property
    def connect_mode(self) -> secsgem.hsms.HsmsConnectMode:
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

    @property
    def is_active(self) -> bool:
        """Check if connection is active."""
        return self.connect_mode == secsgem.hsms.HsmsConnectMode.ACTIVE
