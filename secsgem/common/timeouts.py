#####################################################################
# timeouts.py
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
"""Timeout class."""
from __future__ import annotations


class _Timeout:
    def __init__(self, name: str, default: float, help_text: str) -> None:
        self._name = name
        self._default = default
        self._help = help_text

    @property
    def name(self) -> str:
        """Get the timeout name."""
        return self._name

    @property
    def default(self) -> float:
        """Get the default timeout value."""
        return self._default

    @property
    def help(self) -> str:
        """Get the help text for the timeout."""
        return self._help


class Timeouts:
    r"""Timeouts.

    Example:
        >>> import secsgem.common
        >>> timeouts = secsgem.common.Timeouts(t3=60.0)
        >>> timeouts.t3
        60.0
        >>> timeouts.t4
        10.0

    .. exec::
        import secsgem.common.timeouts

        for timeout in secsgem.common.timeouts.Timeouts.timeouts():
            print(f".. attribute:: {timeout.name}\n\n"
                    f"   :type: {timeout.default.__class__.__name__}\n"
                    f"   :value: {timeout.default}\n\n"
                    f"   {timeout.help}")

    """

    @classmethod
    def timeouts(cls) -> list[_Timeout]:
        """Get a list of default timeouts."""
        return [
            _Timeout("t1", 5.0, "Inter-Character Timeout"),
            _Timeout("t2", 100.0, "Protocol Timeout"),
            _Timeout("t3", 45.0, "Reply Timeout"),
            _Timeout("t4", 10.0, "Inter-Block Timeout"),
            _Timeout("t5", 10.0, "Connect Separation Time"),
            _Timeout("t6", 5.0, "Control Transaction Timeout"),
            _Timeout("t7", 8.0, "Not Selected Timeout"),
            _Timeout("t8", 5.0, "Network Intercharacter Timeout"),
        ]

    @classmethod
    def args(cls) -> list[str]:
        """Get a list of available arguments."""
        return [timeout.name for timeout in cls.timeouts()]

    def __init__(self, **kwargs) -> None:
        """Timout initializer.

        All arguments are optional.
        The default value will be used, when an argument is omitted.

        Args:
            **kwargs: keyword arguments, see below

        Keyword Args:
            t1: Inter-Character Timeout
            t2: Protocol Timeout
            t3: Reply Timeout
            t4: Inter-Block Timeout
            t5: Connect Separation Time
            t6: Control Transaction Timeout
            t7: Not Selected Timeout
            t8: Network Intercharacter Timeout

        """
        self._data = {}

        for timeout in self.timeouts():
            self._data[timeout.name] = kwargs.get(timeout.name, timeout.default)

    def __getattr__(self, name: str):
        """Get an attribute.

        Args:
            name: attribute name

        Returns:
            attribute value

        """
        if name not in self._data:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        return self._data[name]
