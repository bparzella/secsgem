#####################################################################
# collection_event_report.py
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
"""Wrapper for GEM collection event report."""

from __future__ import annotations

import secsgem.secs


class CollectionEventReport:  # pylint: disable=too-few-public-methods
    """Report definition for registered collection events."""

    def __init__(self, rptid: int | str, variables: list[int | str], **kwargs):
        """Initialize a collection event report.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Args:
            rptid: ID of the report
            variables: long name of the collection event
            **kwargs: additional attributes for object

        """
        self.rptid = rptid
        self.vars = variables

        self.id_type: type[secsgem.secs.variables.Base]

        if isinstance(self.rptid, int):
            self.id_type = secsgem.secs.variables.U4
        else:
            self.id_type = secsgem.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
