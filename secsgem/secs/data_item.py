#####################################################################
# data_item.py
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
"""Data item classes."""

from __future__ import annotations

import dataclasses
import json
import pathlib
import re
import typing

import jsonschema
import yaml

descriptor_value_range_regex = re.compile("^(\\d+)-?(\\d*)$")

_script_path = pathlib.Path(__file__).resolve().absolute().parent
default_yaml_path = _script_path / "data_items.yaml"
schema_path = _script_path / "data_items.schema.json"


class _DataItemSchema:  # pylint: disable=too-few-public-methods
    __schema = None

    @classmethod
    def get(cls) -> dict[str, typing.Any]:
        """Get the schema for the data_items.yaml file."""
        if cls.__schema is None:
            cls.__schema = json.loads(schema_path.read_text(encoding="utf8"))

        return cls.__schema


@dataclasses.dataclass
class DataItemDescriptorValue:
    """Data item descriptor values class."""

    range_start: int
    range_end: int | None

    description: str
    constant: str | None = None

    @staticmethod
    def parse_range(value: str) -> tuple[int, int | None]:
        """Parse range value.

        Args:
            value: range value.

        Returns:
            tuple with start and end of the range. if no end is provided, None is returned.

        """
        match = descriptor_value_range_regex.match(value)
        if not match:
            raise ValueError(f"Invalid data item descriptor value range: {value}")
        return int(match.group(1)), int(match.group(2)) if match.group(2) else None

    @classmethod
    def from_yaml_item(cls, value_range: str, data: dict[str, typing.Any]) -> DataItemDescriptorValue:
        """Load data item descriptor from yaml structure.

        Args:
            value_range: Name of the data item.
            data: Data item descriptor data.

        Returns:
            DataItemDescriptorValue object for the provided yaml data

        """
        dataset = data.copy()

        dataset["range_start"], dataset["range_end"] = cls.parse_range(value_range)

        return cls(**dataset)


@dataclasses.dataclass
class DataItemDescriptor:
    """Data item descriptor class."""

    name: str

    description: str
    type: str | list[str]
    length: int | None = None
    values: list[DataItemDescriptorValue] = dataclasses.field(default_factory=list)
    linter_message: str | None = None
    help: str | None = None

    def __getattr__(self, key: str) -> int:
        """Get data item descriptor value by key.

        Args:
            key: item descriptor value name.

        Returns:
            Value of the descriptor item value.

        """
        for value in self.values:
            if value.constant == key:
                return value.range_start

        raise AttributeError(f"Data item descriptor value {key} not found")

    def value_description(self, key: int | str) -> str:
        """Get data item descriptor value description by key.

        Args:
            key: item descriptor value name.

        Returns:
            Description of the descriptor item value.

        """
        if isinstance(key, int):
            for value in self.values:
                if value.range_end:
                    if value.range_start <= key <= value.range_end:
                        return value.description
                else:
                    if value.range_start == key:
                        return value.description
        else:
            for value in self.values:
                if value.constant == key:
                    return value.description

        raise AttributeError(f"Data item descriptor value {key} not found")

    def value_constant(self, key: int) -> str | None:
        """Get data item descriptor value constant by value.

        Args:
            key: item descriptor value.

        Returns:
            constant name of the descriptor item value.

        """
        for value in self.values:
            if value.range_end:
                if value.range_start <= key <= value.range_end:
                    return value.constant
            else:
                if value.range_start == key:
                    return value.constant

        return None

    @classmethod
    def from_yaml_item(cls, name: str, data: dict[str, typing.Any]) -> DataItemDescriptor:
        """Load data item descriptor from yaml structure.

        Args:
            name: Name of the data item.
            data: Data item descriptor data.

        Returns:
            DataItemDescriptor object for the provided data

        """
        dataset = data.copy()

        dataset["name"] = name
        if "values" in dataset:
            dataset["values"] = [
                DataItemDescriptorValue.from_yaml_item(key, value) for key, value in dataset["values"].items()
            ]
        return cls(**dataset)


@dataclasses.dataclass
class DataItemDescriptors:
    """Data item descriptors class."""

    __descriptors: dict[str, DataItemDescriptor]

    def __getitem__(self, key: str) -> DataItemDescriptor:
        """Get data item descriptor by name.

        Args:
            key: name of the data item.

        Returns:
            DataItemDescriptor object for the requested data item.

        """
        return self.__descriptors[key]

    def __getattr__(self, key: str) -> DataItemDescriptor:
        """Get data item descriptor by name.

        Args:
            key: name of the data item.

        Returns:
            DataItemDescriptor object for the requested data item.

        """
        return self.__descriptors[key]

    @classmethod
    def from_yaml(cls, path: pathlib.Path) -> DataItemDescriptors:
        """Load data item descriptor list from yaml file.

        Args:
            path: Path to yaml file.

        Returns:
            DataItemDescriptors object for all data items in the yaml file.

        """
        data = path.read_text(encoding="utf8")
        yaml_data = yaml.safe_load(data)
        jsonschema.validate(instance=yaml_data, schema=_DataItemSchema.get())
        return cls(
            {
                data_item: DataItemDescriptor.from_yaml_item(data_item, data_item_data)
                for data_item, data_item_data in yaml_data.items()
            },
        )
