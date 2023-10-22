#####################################################################
# settings.py
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
"""HSMS settings class."""
from __future__ import annotations

import enum
import typing

from secsgem.common.settings import Setting, Settings
from .active_connection import HsmsActiveConnection
from .passive_connection import HsmsPassiveConnection

if typing.TYPE_CHECKING:
    from secsgem.common.protocol import Protocol
    from secsgem.common.connection import Connection


class HsmsConnectMode(enum.Enum):
    """Hsms connect mode (active or passive)."""

    ACTIVE = 1
    PASSIVE = 2

    def __repr__(self) -> str:
        """String representation of object."""
        return "Active" if self == self.ACTIVE else "Passive"


class HsmsSettings(Settings):
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

    .. exec::
        import secsgem.hsms.settings

        secsgem.hsms.settings.HsmsSettings._attributes_help()

    """

    @classmethod
    def _attributes(cls) -> typing.List[Setting]:
        """Get the available settings for the class."""
        return super()._attributes() + [
            Setting("connect_mode", HsmsConnectMode.ACTIVE, "Hsms connect mode"),
            Setting("address", "127.0.0.1", "Remote (active) or local (passive) IP address"),
            Setting("port", 5000, "TCP port of remote host"),
        ]

    def create_protocol(self) -> Protocol:
        """Protocol class for this configuration."""
        from .protocol import HsmsProtocol  # pylint: disable=import-outside-toplevel

        return HsmsProtocol(self)

    def create_connection(self) -> Connection:
        """Connection class for this configuration."""
        if self.connect_mode == HsmsConnectMode.ACTIVE:
            return HsmsActiveConnection(self)
        return HsmsPassiveConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"

    @property
    def is_active(self) -> bool:
        """Check if connection is active."""
        return self.connect_mode == HsmsConnectMode.ACTIVE
