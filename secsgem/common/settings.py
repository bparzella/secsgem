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
"""settings base class."""
from __future__ import annotations

import abc
import enum
import typing
from typing import Any

from .timeouts import Timeouts

if typing.TYPE_CHECKING:
    from .connection import Connection
    from .protocol import Protocol


class DeviceType(enum.Enum):
    """Type of device (equipment or host)."""

    # This device is equipment
    EQUIPMENT = 0

    # This device is host
    HOST = 1


class Setting:
    """Setting descriptor."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 default_value: typing.Any,
                 help_text: str,
                 default_class: type | None = None,
                 writeable: bool = False) -> None:
        """Initialize setting descriptor.

        Args:
            name: name of the setting
            default_value: setting default value
            help_text: text to output in documentation
            default_class: if set, setting will be instanciated with this class and kwargs
            writeable: setting can be updated

        """
        self._name = name
        self._default_value = default_value
        self._help_text = help_text
        self._default_class = default_class
        self._writeable = writeable

    @property
    def name(self) -> str:
        """Setting name."""
        return self._name

    @property
    def default_value(self):
        """Default value."""
        return self._default_value

    @property
    def help_text(self) -> str:
        """Help text."""
        return self._help_text

    @property
    def default_class(self) -> type | None:
        """Class to initialize with kwargs as default."""
        return self._default_class

    @property
    def writeable(self) -> type | None:
        """Setting can be updated."""
        return self.writeable


class Settings(abc.ABC):
    r"""Settings base class.

    These attributes can be initialized in the constructor and accessed as property.

    .. exec::
        import secsgem.common.settings

        secsgem.common.settings.Settings._attributes_help()

    """

    @classmethod
    @abc.abstractmethod
    def _attributes(cls) -> list[Setting]:
        """Get the available settings for the class."""
        return [
            Setting("timeouts", None, "Communication timeout", Timeouts),
            Setting("device_type", DeviceType.HOST, "Device type"),
            Setting("streams_functions", None, "Container with streams/functions"),
            Setting("session_id", 0, "session / device ID to use for connection"),
            Setting("establish_communication_timeout", 10, "Time to wait between CA requests", writeable=True),
        ]

    @classmethod
    def _attributes_help(cls):
        """Print help for the attributes."""
        for attribute in cls._attributes():
            if attribute.default_class is not None:
                print(f".. attribute:: {attribute.name}\n\n"  # noqa: T201
                      f"   :type: {attribute.default_class.__name__}\n"
                      f"   {attribute.help_text}")
            else:
                print(f".. attribute:: {attribute.name}\n\n"  # noqa: T201
                      f"   :type: {attribute.default_value.__class__.__name__}\n"
                      f"   :value: {attribute.default_value}\n"
                      f"   {attribute.help_text}")

    def __init__(self, **kwargs) -> None:
        """Initialize settings.

        Pass parameter values as keyword arguments.

        """
        super().__setattr__("_data", {})

        for attribute in self._attributes():
            if attribute.default_class is not None:
                klass = attribute.default_class
                value = klass(**kwargs)
            else:
                value = kwargs.get(attribute.name, attribute.default_value)

            self._data[attribute.name] = value

        if self._data["streams_functions"] is None:
            from secsgem.secs.functions import StreamsFunctions  # pylint: disable=import-outside-toplevel,cyclic-import
            self._data["streams_functions"] = StreamsFunctions()

    @abc.abstractmethod
    def create_protocol(self) -> Protocol:
        """Protocol class for this configuration."""
        raise NotImplementedError(f"function 'create_protocol' is not implemented for '{self.__class__.__name__}'")

    @abc.abstractmethod
    def create_connection(self) -> Connection:
        """Connection class for this configuration."""
        raise NotImplementedError(f"function 'create_connection' is not implemented for '{self.__class__.__name__}'")

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of this configuration."""
        raise NotImplementedError(f"property 'name' is not implemented for '{self.__class__.__name__}'")

    @abc.abstractmethod
    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        raise NotImplementedError(f"function 'generate_thread_name' is not implemented for '{self.__class__.__name__}'")

    def __getattr__(self, name: str) -> typing.Any:
        """Get an attribute.

        Args:
            name: attribute name

        Returns:
            attribute value

        """
        if name not in self._data:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        return self._data[name]

    def __setattr__(self, name: str, value: Any) -> None:
        """Update an attribute.

        This can only be called if the attribute is writeable.

        Args:
            name: attribute name
            value: new attribute value

        """
        if name not in self._data:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        attribute = [attribute for attribute in self._attributes() if attribute.name == name]

        if len(attribute) < 1:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        if len(attribute) > 1:
            raise AttributeError(f"'{self.__class__.__name__}' object has attribute '{name}' multiple times")

        if not attribute[0].writeable:
            raise AttributeError(f"Attribute '{self.__class__.__name__}.{name}' is not writeable")

        self._data[name] = value


class ExistingProtocolSettings(Settings):
    """Settings for HSMS connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem.hsms
        >>>
        >>> settings = secsgem.hsms.HsmsSettings(device_type=secsgem.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>

    .. exec::
        import secsgem.hsms.settings

        secsgem.hsms.settings.HsmsSettings._attributes_help()

    """

    @classmethod
    def _attributes(cls) -> list[Setting]:
        """Get the available settings for the class."""
        return [
            *super()._attributes(),
            Setting("existing_protocol", None, "Existing protocol"),
        ]

    def create_protocol(self) -> Protocol:
        """Protocol class for this configuration."""
        return self.existing_protocol

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"
