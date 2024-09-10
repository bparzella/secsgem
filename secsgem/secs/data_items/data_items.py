#####################################################################
# data_items.py
#
# (c) Copyright 2024, Benjamin Parzella. All rights reserved.
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
"""Container class for data items."""

from __future__ import annotations

import typing

from ._all import secs_data_items

if typing.TYPE_CHECKING:
    from .base import DataItemBase


class DataItems:
    """Container for data items classes."""

    def __init__(
        self,
        data_items: list[type[DataItemBase]] | None = None,
    ) -> None:
        """Initialize data items container."""
        if data_items is None:
            data_items = secs_data_items.copy()

        self._data_items = data_items

    def item(self, name: str) -> type[DataItemBase] | None:
        """Get a specific data item.

        Args:
            name: name of the data item

        Returns:
            data item class

        """
        for data_item in self._data_items:
            if data_item.name == name:
                return data_item

        return None

    def __getattr__(self, name: str) -> type[DataItemBase]:
        """Get a specific data item.

        Args:
            name: name of the data item

        Returns:
            data item class

        """
        item = self.item(name)

        if item is None:
            raise AttributeError(f"Data item {name} not found")

        return item

    def update(self, data_item: type[DataItemBase]) -> None:
        """Update data items container.

        Args:
            data_item: data item class

        """
        data_items = [
            item for item in self._data_items if item.name == data_item.name
        ]

        if data_items:
            for item in data_items:
                self._data_items.remove(item)

        self._data_items.append(data_item)
