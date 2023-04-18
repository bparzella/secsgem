#####################################################################
# timeouts.py
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
"""timout class."""


class Timeouts:
    """Timeouts."""

    T3 = 45.0
    T5 = 10.0
    T6 = 5.0

    def __init__(self) -> None:
        """Timout initializer."""
        # Reply Timeout
        self.t3 = self.T3  # pylint: disable=invalid-name

        # Connect Separation Time
        self.t5 = self.T5  # pylint: disable=invalid-name

        # Control Transaction Timeout
        self.t6 = self.T6  # pylint: disable=invalid-name
