#####################################################################
# alarm.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
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
"""Wrapper for GEM alarm."""

from __future__ import annotations

import secsgem.secs


class Alarm:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Alarm definition."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        alid: str | int,
        name: str,
        text: str,
        code: int,
        ce_on: str | int,
        ce_off: str | int,
        **kwargs,
    ):
        """Initialize an alarm.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Args:
            alid: ID of the alarm
            name: long name of the alarm
            text: alarm text
            code: alarm code
            ce_on: collection event for alarm set
            ce_off: collection event for alarm cleared
            **kwargs: additional attributes for object

        """
        self.alid = alid
        self.name = name
        self.text = text
        self.code = code
        self.ce_on = ce_on
        self.ce_off = ce_off
        self.enabled = False
        self.set = False

        self.id_type: type[secsgem.secs.variables.Base]

        if isinstance(self.alid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
