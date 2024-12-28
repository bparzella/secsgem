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

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .collection_event import CollectionEvent


class CollectionEventLink:
    """Representation for registered/linked collection event."""

    def __init__(self, collection_event: CollectionEvent, reports: list[int | str], **kwargs):
        """Initialize a collection event link.

        Args:
            collection_event: collection event
            reports: list of the linked reports
            **kwargs: additional attributes for object

        """
        self._collection_event = collection_event
        self._reports = reports
        self.enabled = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def collection_event(self) -> CollectionEvent:
        """Get the associated collection event."""
        return self._collection_event

    @property
    def reports(self) -> list[int | str]:
        """Get list of the data values.

        Returns:
            List of linked reports

        """
        return self._reports
