#####################################################################
# collection_event_link.py
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
"""Wrapper for GEM collection event link."""


class CollectionEventLink:
    """Representation for registered/linked collection event."""

    def __init__(self, ce, reports, **kwargs):
        """
        Initialize a collection event link.

        :param ce: ID of the collection event
        :type ce: :class:`gem.CollectionEvent`
        :param reports: list of the linked reports
        :type reports: list of :class:`gem.CollectionEventReport`
        """
        self.ce = ce
        self._reports = reports
        self.enabled = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def reports(self):
        """
        Get list of the data values.

        :returns: List of linked reports
        :rtype: list of :class:`gem.CollectionEventReport`
        """
        return self._reports
