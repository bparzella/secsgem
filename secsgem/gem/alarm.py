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

import secsgem.secs


class Alarm:
    """Alarm definition."""

    def __init__(self, alid, name, text, code, ce_on, ce_off, **kwargs):
        """
        Initialize an alarm.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        :param alid: ID of the alarm
        :type alid: various
        :param name: long name of the alarm
        :type name: string
        :param text: alarm text
        :type text: string
        :param ce_on: collection event for alarm set
        :type ce_on: types supported by data item CEID
        :param ce_off: collection event for alarm cleared
        :type ce_off: types supported by data item CEID
        """
        self.alid = alid
        self.name = name
        self.text = text
        self.code = code
        self.ce_on = ce_on
        self.ce_off = ce_off
        self.enabled = False
        self.set = False

        if isinstance(self.alid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
