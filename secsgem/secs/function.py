#####################################################################
# function.py
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
"""Function classes."""

from __future__ import annotations

import dataclasses
import json
import pathlib
import re
import typing

import jsonschema
import yaml

stream_function_regex = re.compile("^S(\\d+)F(\\d+$)")

_script_path = pathlib.Path(__file__).resolve().absolute().parent
default_yaml_path = _script_path / "functions.yaml"
schema_path = _script_path / "functions.schema.json"


class _FunctionSchema:  # pylint: disable=too-few-public-methods
    __schema = None

    @classmethod
    def get(cls) -> dict[str, typing.Any]:
        """Get the schema for the functions.yaml file."""
        if cls.__schema is None:
            cls.__schema = json.loads(schema_path.read_text(encoding="utf8"))

        return cls.__schema


def parse_stream_function(value: str) -> tuple[int, int]:
    """Parse stream function value.

    Args:
        value: stream function value.

    Returns:
        Tuple of stream and function values.

    """
    match = stream_function_regex.match(value)
    if match is None:
        raise ValueError(f"Invalid stream function value: {value}")

    return int(match.group(1)), int(match.group(2))


@dataclasses.dataclass(frozen=True)
class FunctionDescriptor:  # pylint: disable=too-many-instance-attributes
    """Function descriptor class."""

    stream: int
    function: int

    name: str
    mnemonic: str
    to_host: bool
    to_equipment: bool
    reply: bool
    reply_required: bool
    multi_block: bool
    structure: str | list[str] | None = None
    sample_data: str | list[str] | None = None
    extra_help: str | None = None

    @classmethod
    def from_yaml_item(cls, index: tuple[int, int], data: dict[str, typing.Any]) -> FunctionDescriptor:
        """Load function descriptor from yaml structure.

        Args:
            index: Tuple of stream and function.
            data: function descriptor data.

        Returns:
            FunctionDescriptor object for the provided data

        """
        dataset = data.copy()

        stream, function = index

        return cls(stream=stream, function=function, **dataset)


@dataclasses.dataclass(frozen=True)
class FunctionDescriptors:
    """Function descriptors class."""

    __descriptors: dict[tuple[int, int], FunctionDescriptor]

    def __getitem__(self, key: str | tuple[int, int]) -> FunctionDescriptor:
        """Get function descriptor by name.

        When using a string as key, it is formated as `S{stream}F{function}`.

        Args:
            key: name of the function or tuple of stream and function.

        Returns:
            FunctionDescriptor object for the requested function.

        """
        if isinstance(key, str):
            return self.__descriptors[parse_stream_function(key)]

        return self.__descriptors[key]

    def __getattr__(self, key: str) -> FunctionDescriptor:
        """Get function descriptor by name.

        This is formated as `S{stream}F{function}`.

        Args:
            key: name of the function.

        Returns:
            DataItemDescriptor object for the requested function.

        """
        return self.__descriptors[parse_stream_function(key)]

    @classmethod
    def from_yaml(cls, path: pathlib.Path) -> FunctionDescriptors:
        """Load function descriptor list from yaml file.

        Args:
            path: Path to yaml file.

        Returns:
            FunctionDescriptors object for all functions in the yaml file.

        """
        data = path.read_text(encoding="utf8")
        yaml_data = yaml.safe_load(data)
        jsonschema.validate(instance=yaml_data, schema=_FunctionSchema.get())
        return cls(
            {
                parse_stream_function(function): FunctionDescriptor.from_yaml_item(
                    parse_stream_function(function),
                    function_data,
                )
                for function, function_data in yaml_data.items()
            },
        )
