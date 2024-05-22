#####################################################################
# data_item.py
#
# (c) Copyright 2023-2024, Benjamin Parzella. All rights reserved.
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
"""Classes for data item."""
from __future__ import annotations

import abc
import collections.abc
import dataclasses
import pathlib
import re
import typing

import yaml

import secsgem.common
import secsgem.secs

from .item import Item
from .item_l import ItemL


def _update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class DataItems:
    """Container for data items."""

    def __init__(
        self, extra_yaml: pathlib.Path | list[pathlib.Path] | None = None, skip_defaults: bool = False
    ) -> None:
        """Initialize data items container.

        Args:
            extra_yaml: extra file(s) to load, None to not load any extras
            skip_defaults: don't load default data items

        """
        self._extra_yaml = [extra_yaml] if isinstance(extra_yaml, pathlib.Path) else extra_yaml
        self._skip_defaults = skip_defaults

        self._data = self._generate_data()

    def _generate_data(self) -> dict[str, DataItemDefinition]:
        data = {}

        if not self._skip_defaults:
            self._default_file_path = pathlib.Path(__file__).resolve().parent / "data" / "data_items.yaml"

            yaml_data = self._default_file_path.read_text(encoding="utf8")
            data = yaml.safe_load(yaml_data)

        if self._extra_yaml is not None:
            for extra_path in self._extra_yaml:
                yaml_data = extra_path.read_text(encoding="utf8")
                extra_data = yaml.safe_load(yaml_data)
                _update_dict(data, extra_data)

        return {key: DataItemDefinition(key, value) for key, value in data.items()}

    def get(self, key: str) -> DataItem:
        """Get a specific data item using index notation.

        Args:
            key: name of the data_item

        Returns:
            DataItem object for the selected data item

        """
        return DataItem(key, self._data[key])

    def __getitem__(self, key: str) -> DataItem:
        """Get a specific data item using index notation.

        Args:
            key: name of the data_item

        Returns:
            DataItem object for the selected data item

        """
        return self.get(key)

    def __getattr__(self, key: str) -> DataItem:
        """Get a specific data item using attribute notation.

        Args:
            key: name of the data_item

        Returns:
            DataItem object for the selected data item

        """
        return self.get(key)


class DataItemDefinition:
    """Data item definition class."""

    def __init__(self, name: str, definition_data: dict[str, typing.Any]) -> None:
        """Intialiize data item definition object.

        Args:
            name: name of the data item
            definition_data: item definition (from the yaml)

        """
        self._name = name
        self._data = definition_data

    @property
    def supported_types(self) -> list[type[Item]]:
        """Get the supported types for the data item.

        Returns:
            list of supported secs types

        """
        type_names = self._data["type"] if isinstance(self._data["type"], list) else [self._data["type"]]

        return [Item.by_yaml_type(type_name) for type_name in type_names]

    @property
    def length(self) -> int | None:
        """Get the allowed length for the data item.

        Returns:
            allowed length

        """
        if "length" not in self._data:
            return None

        return int(self._data["length"])

    @property
    def constants(self) -> dict[str, typing.Any]:
        """Get the defined constants for the data item or an empty dict if no constants are defined."""
        if "values" not in self._data:
            return {}

        return {value["constant"]: key for key, value in self._data["values"].items() if "constant" in value}


class DataItem:
    """Data Item."""

    def __init__(self, name: str, definition: DataItemDefinition) -> None:
        """Initialize data_item object.

        Args:
            name: data item name
            definition: structural definition of the item

        """
        self._name = name
        self._definition = definition

    @property
    def supported_types(self) -> list[type[Item]]:
        """Get the supported types for the data item.

        Returns:
            list of supported secs types

        """
        return self._definition.supported_types

    @property
    def length(self) -> int | None:
        """Get the allowed length for the data item.

        Returns:
            allowed length

        """
        return self._definition.length

    def constant(self, name: str) -> typing.Any:
        """Get a constant for the data item.

        Args:
            name: data item constant name

        Returns:
            data item value

        """
        constants = self._definition.constants

        if name not in constants:
            raise ValueError(f"Missing constant {name} for data item {self._name}")

        return constants[name]

    def __getattr__(self, key: str) -> typing.Any:
        """Get a constant using attribute notation.

        Args:
            key: name of the constant

        Returns:
            Constant value

        """
        return self.constant(key)


class StreamFunctionStructureItem(abc.ABC):
    """Base object for stream function definition items."""

    def __repr__(self) -> str:
        """Generate readable output."""
        return self.format_debug()

    def format_debug(self, _indent: int = 2) -> str:
        """Generate readable debug output.

        Args:
            _indent: indention level

        Returns:
            debug string

        """
        return ""

    @abc.abstractmethod
    def generate(self, data: typing.Any) -> Item:
        """Generate item structure from data.

        Args:
            data: python data

        Returns:
            Item structure

        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Get item name."""
        raise NotImplementedError

    @abc.abstractmethod
    def generate_dict(self, value: typing.Any) -> typing.Any:
        """Generate a dict using the structure.

        Args:
            value: value to generate the dict

        Returns:
            generated dict

        """
        raise NotImplementedError


class StreamFunctionStructureList(StreamFunctionStructureItem):
    """List structure object for stream function definition."""

    REGEX = re.compile(r"^<\s*L([+?]*)\s*([A-Za-z0-9_]*)\s*")

    def __init__(
        self,
        children: list[StreamFunctionStructureItem],
        data_items: DataItems,
        name: str = "",
        repeating: bool = False,
        optional: bool = False,
    ) -> None:
        """Initialize list structure object."""
        self._data_items = data_items
        self._name = name
        self._repeating = repeating
        self._optional = optional
        self._children = children

    @classmethod
    def from_match(cls, children: list[StreamFunctionStructureItem], match: re.Match, data_items: DataItems):
        """Extract object information from regex.

        Args:
            children: list contents
            match: regex match results
            data_items: data items to match

        Returns:
            new object

        """
        options = match.group(1)
        name = match.group(2)

        return cls(children, data_items, name, repeating="+" in options, optional="?" in options)

    @property
    def name(self) -> str:
        """Get item name."""
        return self._name

    @property
    def children(self) -> list[StreamFunctionStructureItem]:
        """Get the list children."""
        return self._children

    def format_debug(self, indent: int = 2) -> str:
        """Generate readable debug output.

        Args:
            indent: indention level

        Returns:
            debug string

        """
        indent_str = indent * " "
        sub_items = [item.format_debug(indent + 2) for item in self._children]
        sub_items_str = "\n".join(sub_items)
        return (
            f"{indent_str}L {len(self._children)} {self._name} repeating={self._repeating} optional={self._optional}\n"
            f"{sub_items_str}"
        )

    def generate(self, data: typing.Any) -> Item:
        """Generate item structure from data.

        Args:
            data: python data

        Returns:
            Item structure

        """
        if isinstance(data, list):
            return self._generate_list(data)

        if isinstance(data, dict):
            return self._generate_dict(data)

        if isinstance(data, ItemL):
            return self._generate_item_l(data)

        if data is None:
            return self._generate_none()

        raise StreamFunctionStructureValidationError(
            f"Unexpected data type {data.__class__.__name__} ({data}) for list item"
        )

    def _generate_list(self, data: typing.Any) -> Item:
        if (len(data) == 0 or data == [None]) and self._optional:
            return Item.from_value([])

        if self._repeating:
            result = [child.generate(item) for child, item in zip(self._children * len(data), data)]

            return Item.from_value(result)

        if len(data) != len(self._children):
            raise StreamFunctionStructureValidationError(
                f"List length for '{data}' ({len(data)}) doesn't match expected {len(self._children)}"
            )

        result = [child.generate(item) for child, item in zip(self._children, data)]

        return Item.from_value(result)

    def _generate_dict(self, data: typing.Any) -> Item:
        if len(data) == 0 and self._optional:
            return Item.from_value([])

        if len(data) != len(self._children):
            raise StreamFunctionStructureValidationError(
                f"Dict length for '{data}' ({len(data)}) doesn't match expected {len(self._children)}"
            )

        result = [child.generate(data[child.name]) for child in self._children]

        return Item.from_value(result)

    def _generate_item_l(self, data: typing.Any) -> Item:
        data = data.value
        if (len(data) == 0 or data == [None]) and self._optional:
            return Item.from_value([])

        if self._repeating:
            result = [child.generate(item) for child, item in zip(self._children * len(data), data)]

            return Item.from_value(result)

        if len(data) != len(self._children):
            raise StreamFunctionStructureValidationError(
                f"List length for '{data}' ({len(data)}) doesn't match expected {len(self._children)}"
            )

        result = [child.generate(item) for child, item in zip(self._children, data)]

        return Item.from_value(result)

    def _generate_none(self) -> Item:
        if not self._optional:
            raise StreamFunctionStructureValidationError("Expected value but got an empty Array")

        return Item.from_value([])

    def generate_dict(self, value: typing.Any) -> typing.Any:
        """Generate a dict using the structure.

        Args:
            value: value to generate the dict

        Returns:
            generated dict

        """
        if self._repeating:
            result = []

            if isinstance(self._children[0], StreamFunctionStructureDataItem):
                result = [
                    child.generate_dict(item) for child, item in zip(self._children * len(value), value)
                ]

            if isinstance(self.children[0], StreamFunctionStructureList):
                result = [child.generate_dict(item) for child, item in zip(self._children * len(value), value)]

            return result

        results = {}
        for value_item, structure_item in zip(value, self.children):
            if isinstance(structure_item, StreamFunctionStructureDataItem):
                results.update({structure_item.name: value_item})

            if isinstance(structure_item, StreamFunctionStructureList):
                results.update({structure_item.name: structure_item.generate_dict(value_item)})

        return results


class StreamFunctionStructureDataItem(StreamFunctionStructureItem):
    """Data item structure object for stream function definition."""

    REGEX = re.compile(r"^<\s*([A-Za-z0-9_]+)\s*>")

    def __init__(self, structure: str, data_items: DataItems) -> None:
        """Initialize list structure object."""
        self._structure = structure
        self._name = structure
        self._data_item = data_items[structure]
        self._types = self._data_item.supported_types

    @classmethod
    def from_match(cls, match: re.Match, data_items: DataItems):
        """Extract object information from regex.

        Args:
            match: regex match results
            data_items: data items to match

        Returns:
            new object

        """
        name = match.group(1)
        return cls(name, data_items)

    @property
    def name(self) -> str:
        """Get item name."""
        return self._name

    def format_debug(self, indent: int = 2) -> str:
        """Generate readable debug output.

        Args:
            indent: indention level

        Returns:
            debug string

        """
        indent_str = " " * indent
        types_str = ",".join([typ.__name__ for typ in self._types])
        return f"{indent_str}I {self._name} types={types_str}"

    def generate(self, data: typing.Any) -> Item:
        """Generate item structure from data.

        Args:
            data: python data

        Returns:
            Item structure

        """
        if type(data) in self._types:
            return data

        for typ in self._types:
            try:
                return typ(data)
            except (TypeError, ValueError):  # noqa: PERF203
                continue

        raise StreamFunctionStructureValidationError(
            f"Unknown type '{data.__class__.__name__}' ({data}) for Item {self.name}"
        )

    def generate_dict(self, value: typing.Any) -> typing.Any:
        """Generate a dict using the structure.

        Args:
            value: value to generate the dict

        Returns:
            generated dict

        """
        if isinstance(value, (list, bytes)) and len(value) == 1 and self._data_item.length == 1:
            return value[0]

        return value


class StreamFunctionStructureParserError(Exception):
    """Parser error for stream function definition."""


class StreamFunctionStructureValidationError(Exception):
    """Error in data validation."""

    def __init__(self, message: str) -> None:
        """Initialize data validation error object."""
        super().__init__(message)
        self.message = message


class StreamFunctionStructureParser:
    """Parser for stream function definition."""

    def __init__(self, structure: str, data_items: DataItems) -> None:
        """Initialize structure parser object.

        Args:
            structure: structure definition
            data_items: available data items for this function

        """
        self._structure = structure.replace("\n", "").replace("\r", "").strip()
        self._data_items = data_items

    @property
    def item(self) -> StreamFunctionStructureItem:
        """Get al the items from the structure."""
        parsing_structure = self._structure
        items: list[tuple[str, re.Match | None, int]] = []
        level = 0
        while len(parsing_structure) > 0:
            parsing_structure = parsing_structure.strip()

            match_item = StreamFunctionStructureDataItem.REGEX.match(parsing_structure)
            if match_item is not None:
                items.append(("ITEM", match_item, level))
                parsing_structure = parsing_structure[match_item.end() :].strip()
                continue

            match_list = StreamFunctionStructureList.REGEX.match(parsing_structure)
            if match_list is not None:
                items.append(("LIST_START", match_list, level))
                level += 1
                parsing_structure = parsing_structure[match_list.end() :].strip()
                continue

            if parsing_structure.startswith(">"):
                level -= 1
                items.append(("LIST_END", None, level))
                parsing_structure = parsing_structure[1:].strip()
                continue

            raise StreamFunctionStructureParserError(f"Can't parse structure: {parsing_structure}")
        return self._process_items(items)

    def _process_items(self, items: list[tuple[str, re.Match | None, int]]) -> StreamFunctionStructureItem:
        item = items.pop(0)

        if item[0] == "LIST_START":
            results: list[StreamFunctionStructureItem] = []
            list_start = item
            level = item[2]

            if list_start[1] is None:
                raise StreamFunctionStructureParserError(f"Missing match in LIST_START {list_start}")

            while items:
                if items[0][0] == "LIST_END" and items[0][2] == level:
                    items.pop(0)
                    return StreamFunctionStructureList.from_match(results, list_start[1], self._data_items)

                results.append(self._process_items(items))

        elif item[0] == "ITEM":
            if item[1] is None:
                raise StreamFunctionStructureParserError(f"Missing match in ITEM {item}")

            return StreamFunctionStructureDataItem.from_match(item[1], self._data_items)

        raise StreamFunctionStructureParserError(f"Unexpected item in parser list: {item}")


class StreamFunctionStructure:
    """Structure object for stream function definition."""

    def __init__(self, structure: str, data_items: DataItems) -> None:
        """Initialize structure object.

        Args:
            structure: structure definition
            data_items: available data items for this function

        """
        self._data_items = data_items
        self._item_data = structure

        self.item = StreamFunctionStructureParser(structure, data_items).item

    def __repr__(self) -> str:
        """Get readable interpretation of object."""
        return repr(self.item)

    def generate(self, data: typing.Any) -> Item:
        """Generate item structure of data according to structure.

        Args:
            data: data to validate

        Returns:
            item structure

        """
        return self.item.generate(data)

    def generate_dict(self, value: typing.Any) -> typing.Any:
        """Generate a dict using the structure.

        Args:
            value: value to generate the dict based structure

        Returns:
            generated dict based structure

        """
        return self.item.generate_dict(value)


class StreamFunctionDefinition:
    """Stream function definition class.

    Contains the definition of a stream function as defined in the functions.yaml.
    """

    def __init__(self, name: str, definition_data: dict[str, typing.Any], data_items: DataItems) -> None:
        """Intialiize stream function definition object.

        Args:
            name: name of the stream/function
            definition_data: item definition (from the yaml)
            data_items: data items defined for function list

        """
        self._name = name
        self._data = definition_data
        self._stream, self._function = self._parse_stream_function()
        self._data_items = data_items

    def _parse_stream_function(self) -> tuple[int, int]:
        stream_function = self._name.strip("S").split("F")
        return int(stream_function[0]), int(stream_function[1])

    @property
    def stream(self) -> int:
        """Get the stream."""
        return self._stream

    @property
    def function(self) -> int:
        """Get the function."""
        return self._function

    @property
    def require_response(self) -> bool:
        """Check if function requires response."""
        return self._data["reply_required"]

    @property
    def structures(self) -> list[StreamFunctionStructure]:
        """Get the defined structures."""
        if "definitions" not in self._data:
            return []

        return [
            StreamFunctionStructure(definition["structure"], self._data_items)
            for definition in self._data["definitions"]
        ]

    def create(self, value: typing.Any = None) -> StreamFunction:
        """Create a function from the definition.

        Args:
            value: initial value for the function

        Returns:
            created function

        """
        return StreamFunction(self, value)

    @property
    def sml(self) -> str:
        """Get SML text representation for function definition.

        Returns:
            SML text

        """
        # TODO(BP): implement
        raise NotImplementedError


class _StreamFunctionDataObject:
    def __init__(self, data: typing.Any) -> None:
        self._data = dict(data)
        for key, val in data.items():
            if isinstance(val, (list, tuple)):
                self._data[key] = [_StreamFunctionDataObject(x) if isinstance(x, dict) else x for x in val]
            else:
                self._data[key] = _StreamFunctionDataObject(val) if isinstance(val, dict) else val

            setattr(self, key, self._data[key])

    def __repr__(self) -> str:
        return f"({', '.join([f'{key}={value}' for key, value in self._data.items()])})"

class _StreamFunctionUndefinedValue:
    """Undefined value for stream function."""

    def encode(self) -> bytes:
        return b""

class StreamFunction:
    """Function class."""

    undefined_value = _StreamFunctionUndefinedValue()

    def __init__(self, definition: StreamFunctionDefinition, value: typing.Any = undefined_value) -> None:
        """Initialize function object.

        Args:
            definition: definition of the function
            value: data for the function.

        """
        self._definition = definition
        self._value: Item | self.undefined_value = self.undefined_value
        self.structure: StreamFunctionStructure | None

        self.value = value

    def generate_header(self, system: int, session_id: int) -> secsgem.common.HeaderData:
        """Generate a generic header for this function.

        Args:
            system: message system
            session_id: message device id

        Returns:
            generated header

        """
        return secsgem.common.HeaderData(
            system, session_id, self._definition.stream, self._definition.function, self._definition.require_response
        )

    @property
    def to_list(self) -> list[typing.Any]:
        """Get the function payload in python list based format."""
        return self._value.to_list

    @property
    def to_dict(self) -> dict[str, typing.Any]:
        """Get the function payload in python dict based format.

        If the value can't be converted into a dict based format, an exception will be raised.
        """
        if self._structure is None:
            raise ValueError(
                f"Can't generate dict, no structure in S{self._definition.stream}F{self._definition.function}"
            )

        return self._structure.generate_dict(self.to_list)

    @property
    def to_object(self) -> typing.Any:
        """Get the function payload data as dataclass instance."""
        data = self.to_dict

        if isinstance(data, list):
            return [_StreamFunctionDataObject(x) if isinstance(x, dict) else x for x in data]

        if isinstance(data, dict):
            return _StreamFunctionDataObject(self.to_dict)

        return self.to_dict

    @property
    def data(self) -> Item:
        """Get the data value of the function in Item type.

        Returns:
            stream function data

        """
        return self._value

    @property
    def value(self) -> typing.Any:
        """Get the data value of the function in python type.

        Returns:
            stream function data

        """
        return self.to_object

    @value.setter
    def value(self, value: typing.Any):
        """Set the data value of the function.

        Args:
            value: data either in python or in Item type.

        """
        if value == self.undefined_value:
            self._value = self.undefined_value
            return

        self._value = self._generate_value(value)

    def get(self) -> typing.Any:
        """Get the value.

        This is a function for backward compatibility.

        """
        return self.value

    def _generate_value(self, data: typing.Any) -> Item:
        errors: list[str] = []

        for structure in self._definition.structures:
            try:
                import pprint

                print(
                    f"--------------------------------------------------------------------------------------------\n"
                    f"generating s{self._definition.stream}f{self._definition.function}\n"
                    f"{structure}\nwith\n"
                    f"{pprint.pformat(data, sort_dicts=False)}\n"
                )

                result = structure.generate(data)

                print(f"generated s{self._definition.stream}f{self._definition.function}\n" f"{result}")

                self._structure = structure
                return result
            except StreamFunctionStructureValidationError as exc:  # noqa: PERF203
                errors.append(exc.message)

        raise StreamFunctionStructureValidationError(
            f"{'/'.join(errors)} in S{self._definition.stream}F{self._definition.function}"
        )

    @property
    def sml(self) -> str:
        """Get SML text representation for function.

        Returns:
            SML text

        """
        # TODO(BP): implement
        raise NotImplementedError


class StreamsFunctions:
    """Container for streams/functions."""

    def __init__(
        self,
        extra_yaml: pathlib.Path | list[pathlib.Path] | None = None,
        data_items_extra_yaml: pathlib.Path | list[pathlib.Path] | None = None,
        skip_defaults: bool = False,
    ) -> None:
        """Initialize stream/function container.

        Args:
            extra_yaml: extra file(s) to load, None to not load any extras
            data_items_extra_yaml: extra file(s) to load for the data items, None to not load any extras
            skip_defaults: don't load default streams/function and data items

        """
        self._extra_yaml = [extra_yaml] if isinstance(extra_yaml, pathlib.Path) else extra_yaml
        self._skip_defaults = skip_defaults

        self._data_items = DataItems(
            data_items_extra_yaml, skip_defaults if data_items_extra_yaml is not None else False
        )

        self._data = self._generate_data()

    def _generate_data(self) -> dict[str, StreamFunctionDefinition]:
        data = {}

        if not self._skip_defaults:
            self._default_file_path = pathlib.Path(__file__).resolve().parent / "data" / "functions.yaml"

            file_contents = self._default_file_path.read_text(encoding="utf8")
            data = yaml.safe_load(file_contents)

        if self._extra_yaml is not None:
            for extra_path in self._extra_yaml:
                file_contents = extra_path.read_text(encoding="utf8")
                extra_data = yaml.safe_load(file_contents)
                _update_dict(data, extra_data)

                data.update(extra_data)

        return {key: StreamFunctionDefinition(key, value, self._data_items) for key, value in data.items()}

    @property
    def data_items(self) -> DataItems:
        """Get data items container."""
        return self._data_items

    def definition(self, stream: int, function: int) -> StreamFunctionDefinition:
        """Get a specific stream/function object.

        Args:
            stream: number for stream
            function: number for function

        Returns:
            definition object for stream/function

        """
        index = f"S{stream:02}F{function:02}"

        return self._data[index] if index in self._data else StreamFunctionDefinition(index, {}, self._data_items)

    def function(
        self, stream: int, function: int, value: typing.Any = StreamFunction.undefined_value
    ) -> StreamFunction:
        """Get a specific stream/function object.

        Args:
            stream: number for stream
            function: number for function
            value: initial value

        Returns:
            object for stream/function

        """
        return self.definition(stream, function).create(value)

    def __call__(
        self, stream: int, function: int, value: typing.Any = StreamFunction.undefined_value
    ) -> StreamFunction:
        """Get a specific stream/function object by calling the object.

        Args:
            stream: number for stream
            function: number for function
            value: initial value

        Returns:
            object for stream/function

        """
        return self.function(stream, function, value)

    def from_message(self, message: secsgem.common.Message) -> StreamFunction:
        """Decode a stream function from a message.

        Args:
            message: message to decode

        Returns:
            decoded stream function

        """
        return self.function(message.header.stream, message.header.function, Item.decode(message.data))
