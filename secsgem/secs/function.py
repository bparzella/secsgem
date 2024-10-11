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

from secsgem.secs.item_l import ItemL

from .data_item import DataItemDescriptor
from .functions.sfdl_tokenizer import SFDLTokenizer, SFDLTokens, SFDLTokenType

if typing.TYPE_CHECKING:
    from secsgem.secs.item import Item

    from .data_item import DataItemDescriptors

stream_function_regex = re.compile("^S(\\d+)F(\\d+$)")

_script_path = pathlib.Path(__file__).resolve().absolute().parent
default_yaml_path = _script_path / "functions.yaml"
schema_path = _script_path / "functions.schema.json"


class DataStructure:  # pylint: disable=too-few-public-methods
    """Represents a data structure for a function."""

    def __init__(self, structure: str, descriptors: DataItemDescriptors):
        """Initialize the data structure.

        Args:
            structure: string representationo of the data.
            descriptors: list of data item descriptors to use for this data structure.

        """
        self.text = structure
        self.descriptors = descriptors

        self.struct = self._parse(structure)

    def _parse(self, structure: str) -> list | dict | DataItemDescriptor:
        """Parse the structure string.

        Args:
            structure: string representation of the data.

        Returns:
            Parsed data structure.

        """
        tokens = SFDLTokenizer(structure).tokens
        result = self._process_tokens(tokens)

        if isinstance(result, tuple):
            return result[1]

        return result

    def _process_tokens(
        self,
        tokens: SFDLTokens,
    ) -> tuple[str, list | dict | DataItemDescriptor]:
        """Process tokens for the function.

        Args:
            tokens: tokens to process.
            descriptors: list of data item descriptors to use for this function.

        Returns:
            structure of data items for the function.

        """
        if not tokens.available:
            raise ValueError("Expected opening tag, got end of tokens")

        token = tokens.next()

        if token.type != SFDLTokenType.OPEN_TAG:
            raise ValueError(f"Expected opening tag, got: {token}")

        token = tokens.next()

        if token.type == SFDLTokenType.DATA_ITEM:
            close_token = tokens.next()

            if close_token.type != SFDLTokenType.CLOSE_TAG:
                raise close_token.exception(f"Expected closing tag, got: {close_token}")

            return token.value, self.descriptors[token.value]

        if token.type != SFDLTokenType.LIST:
            raise ValueError(f"Expected list or data item, got: {token}")

        name = "DATA"
        data = {}
        if tokens.peek().type == SFDLTokenType.LIST_NAME:
            name = tokens.next().value

        while tokens.peek().type != SFDLTokenType.CLOSE_TAG:
            result = self._process_tokens(tokens)
            data.update({result[0]: result[1]})

        close_token = tokens.next()

        if len(data) == 1:
            return name, [next(iter(data.values()))]

        return name, data

    def _generate(
        self,
        struct: list | dict | DataItemDescriptor,
        value: dict | list | str | int | float | None,
    ) -> Item:
        if isinstance(struct, list):
            return self._generate_list(struct, value)
        if isinstance(struct, dict):
            return self._generate_dict(struct, value)
        if isinstance(struct, DataItemDescriptor):
            return self._generate_descriptor(struct, value)

        raise ValueError(f"Invalid data structure: {struct} ({type(struct)})")

    def _generate_list(
        self,
        struct: list,
        value: dict | list | str | int | float | None,
    ) -> Item:
        if value is None:
            return ItemL([])

        if not isinstance(value, list):
            raise ValueError(f"Expected list, got: {type(value)} ({value})")

        if len(struct) != 1:
            raise ValueError(f"Expected list of length 1, got {len(struct)}")

        list_data = [self._generate(struct[0], value[i]) for i in range(len(value))]

        return ItemL(list_data)

    def _generate_dict(
        self,
        struct: dict,
        value: dict | list | str | int | float | None,
    ) -> Item:
        if isinstance(value, list) and len(value) == len(struct):
            dict_data = {key: self._generate(struct[key], value[index]) for index, key in enumerate(struct.keys())}
            return ItemL(dict_data)

        if not isinstance(value, dict):
            raise ValueError(f"Expected dict, got: {type(value)} ({value})")

        dict_data = {
            key: self._generate(struct[key], value[key]) if key in value else self._generate(struct[key], None)
            for key in struct
        }

        return ItemL(dict_data)

    def _generate_descriptor(
        self,
        struct: DataItemDescriptor,
        value: dict | list | str | int | float | None,
    ) -> Item:
        if isinstance(value, dict):
            raise ValueError(f"Expected value, got dict: {value}")

        if value is None:
            raise ValueError("Expected value, got None")

        return struct.generate(value)

    def generate(self, value: dict | list | str | int | float) -> Item:
        """Generate the value of the data structure.

        Args:
            value: value to generate.

        Returns:
            Value of the data structure.

        """
        if isinstance(self.struct, str):
            if isinstance(value, dict):
                raise ValueError("Item can't be initialized from dict.")

            return self.descriptors[self.struct].generate(value)

        return self._generate(self.struct, value)


class _FunctionSchema:  # pylint: disable=too-few-public-methods
    __schema: dict[str, typing.Any] | None = None

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

    data_items: DataItemDescriptors

    name: str
    mnemonic: str
    to_host: bool
    to_equipment: bool
    reply: bool
    reply_required: bool
    multi_block: bool
    structure: str | list[str] | None = None
    sample_data: str | list[str] | list[dict] | None = None
    extra_help: str | None = None

    _data_structures: list[DataStructure] | None = None

    @classmethod
    def from_yaml_item(
        cls,
        index: tuple[int, int],
        data: dict[str, typing.Any],
        data_items: DataItemDescriptors,
    ) -> FunctionDescriptor:
        """Load function descriptor from yaml structure.

        Args:
            index: Tuple of stream and function.
            data: function descriptor data.
            data_items: data item descriptors to use for this function descriptors.

        Returns:
            FunctionDescriptor object for the provided data

        """
        dataset = data.copy()

        stream, function = index

        return cls(stream=stream, function=function, data_items=data_items, **dataset)

    @property
    def data_structures(self) -> list[DataStructure]:
        """Get data structures for the function.

        Returns:
            Data item structures for this function.

        """
        if self.structure is None:
            return []

        if self._data_structures is not None:
            return self._data_structures

        structures = self.structure
        if isinstance(structures, str):
            structures = [structures]

        datastructures = [DataStructure(structure, self.data_items) for structure in structures]

        object.__setattr__(self, "_data_structures", datastructures)

        if self._data_structures is None:
            raise ValueError(f"Data structures invalid for function: {self.name}")

        return self._data_structures

    def generate(self, data: dict | list | str | int | float) -> Item | None:
        """Generate the data for the function.

        Args:
            data: data to generate.

        Returns:
            generated item structure or None if not generated

        """
        last_exception = Exception("Invalid data structures")

        for structure in self.data_structures:
            try:
                return structure.generate(data)
            except Exception as exc:  # noqa: PERF203 # pylint: disable=broad-exception-caught
                last_exception = exc

        raise last_exception


@dataclasses.dataclass(frozen=True)
class FunctionDescriptors:
    """Function descriptors class."""

    __descriptors: dict[tuple[int, int], FunctionDescriptor]

    data_items: DataItemDescriptors

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
    def from_yaml(cls, path: pathlib.Path, data_items: DataItemDescriptors) -> FunctionDescriptors:
        """Load function descriptor list from yaml file.

        Args:
            path: Path to yaml file.
            data_items: data item descriptors to use for this function descriptors.

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
                    data_items,
                )
                for function, function_data in yaml_data.items()
            },
            data_items,
        )

    @property
    def streams(self) -> list[int]:
        """Get all available streams.

        Returns:
            list of functions for the stream

        """
        return sorted({descriptor_key[0] for descriptor_key in self.__descriptors})

    def functions(self, stream: int) -> list[int]:
        """Get all available functions for stream.

        Args:
            stream: stream index number

        Returns:
            list of functions for the stream

        """
        return sorted({descriptor_key[1] for descriptor_key in self.__descriptors if descriptor_key[0] == stream})
