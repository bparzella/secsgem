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
"""SECS-I settings class."""
from __future__ import annotations

import typing

from secsgem.common.settings import Setting, Settings
from .connection import SecsIConnection

if typing.TYPE_CHECKING:
    from secsgem.common.protocol import Protocol
    from secsgem.common.connection import Connection


class SecsISettings(Settings):
    """Settings for SECS-I connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.secsi
        >>>
        >>> settings = secsgem.secsi.SecsISettings(port="COM1")
        >>> settings.port
        'COM1"
        >>> settings.speed
        9600

    .. exec::
        import secsgem.hsms.settings

        secsgem.hsms.settings.HsmsSettings._attributes_help()

    """

    @classmethod
    def _attributes(cls) -> typing.List[Setting]:
        """Get the available settings for the class."""
        return super()._attributes() + [
            Setting("port", None, "Serial port"),
            Setting("speed", 9600, "Serial port baud rate"),
        ]

    def create_protocol(self) -> Protocol:
        """Protocol class for this configuration."""
        from .protocol import SecsIProtocol  # pylint: disable=import-outside-toplevel

        return SecsIProtocol(self)

    def create_connection(self) -> Connection:
        """Connection class for this configuration."""
        return SecsIConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"SECSI-{self.port}"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_SecsI_{functionality}_{self.port}@{self.speed}"
