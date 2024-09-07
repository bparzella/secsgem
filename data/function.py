"""Function class definition."""  # noqa: INP001

from __future__ import annotations

import collections
import re
import typing

import jsonschema
import yaml

import secsgem.secs.functions.sfdl_tokenizer

if typing.TYPE_CHECKING:
    from data_item import DataItem

STRUCTURE_CODE = """
import secsgem.secs
{imports}

data_item = {data_item}

var = secsgem.secs.variables.functions.get_format(data_item)
"""

SAMPLE_DATA_CODE = """
import secsgem.secs
import secsgem.common
{imports}

data_item = {data_item}

data = secsgem.secs.variables.functions.generate(data_item)
data.set({sample_value})
var = secsgem.common.indent_block(repr(data))
if data is not None:
    preferred_type = data.preferred_type
else:
    preferred_type = None
"""

SAMPLE_DATA_CODE_EMPTY = """
import secsgem.secs
import secsgem.common
{imports}

data_item = {data_item}

data = secsgem.secs.variables.functions.generate(data_item)
var = secsgem.common.indent_block(repr(data))
if data is not None:
    preferred_type = data.preferred_type
else:
    preferred_type = None
"""


function_schema = {
    "description": "Root array of functions definition",
    "type": "object",
    "patternProperties": {
        "^S\\d+F\\d+$": {
            "description": "Function definition",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                },
                "to_host": {
                    "type": "boolean",
                },
                "to_equipment": {
                    "type": "boolean",
                },
                "reply": {
                    "type": "boolean",
                },
                "reply_required": {
                    "type": "boolean",
                },
                "multi_block": {
                    "type": "boolean",
                },
                "structure": {
                    "type": ["array", "string"],
                },
                "sample_data": {
                    "type": ["array", "string"],
                },
                "extra_help": {
                    "type": "string",
                },
            },
            "required": ["description", "to_host", "to_equipment", "reply", "reply_required", "multi_block"],
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}


class Function:  # pylint: disable=too-many-instance-attributes
    """Function configuration from yaml."""

    sf_regex = re.compile(r"[sS](\d+)[fF](\d+)")

    def __init__(
        self,
        name: str,
        data: dict[str, typing.Any],
        data_items: dict[str, typing.Any],
    ) -> None:
        """Initialize item config."""
        self._name = name
        self._data = data

        self._data_items = data_items

        self._rendered = None

        match = self.sf_regex.match(self._name)
        if not match:
            raise ValueError(f"Function name not valid {name}")

        self._stream = int(match.group(1))
        self._function = int(match.group(2))

        self._samples: list[dict[str, typing.Any]] | None = None
        self._preferred_type: type | None = None

    @classmethod
    def load_all(cls, root, data_items: dict[str, DataItem]) -> list[Function]:
        """Load all function objects."""
        data = (root / "functions.yaml").read_text(encoding="utf8")
        yaml_data = yaml.safe_load(data)
        jsonschema.validate(instance=yaml_data, schema=function_schema)
        return [cls(function, function_data, data_items) for function, function_data in yaml_data.items()]

    @classmethod
    def render_list(cls, functions: list[Function], env, target_path):
        """Render all functions to file."""
        last = None

        function_template = env.get_template("functions.py.j2")
        function_init_template = env.get_template("functions_init.py.j2")
        function_all_template = env.get_template("functions_all.py.j2")
        function_md_template = env.get_template("functions.md.j2")

        for function in functions:
            last = function.render(function_template, target_path)

        init_code = function_init_template.render(
            functions=functions,
            streams_functions=cls.stream_function_dict(functions),
        )

        out_path = target_path / "__init__.py"
        out_path.write_text(init_code)

        all_code = function_all_template.render(
            functions=functions,
            streams_functions=cls.stream_function_dict(functions),
        )

        out_path = target_path / "_all.py"
        out_path.write_text(all_code)

        md_code = function_md_template.render(
            functions=functions,
            streams_functions=cls.stream_function_dict(functions),
        )

        out_path = target_path.parent.parent.parent / "docs" / "reference" / "secs" / "functions.md"
        out_path.write_text(md_code)

        return last

    @staticmethod
    def stream_function_dict(functions: list[Function]) -> dict:
        """Get streams functions in a dict."""
        # build the old style streams functions dictionary
        secs_streams_functions: dict[int, dict[int, Function]] = collections.OrderedDict()

        for function in functions:
            if function.stream not in secs_streams_functions:
                secs_streams_functions[function.stream] = collections.OrderedDict()

            secs_streams_functions[function.stream][function.function] = function

        return secs_streams_functions

    def render(self, function_template, target_path):
        """Render a function to file."""
        print(f"# generate function {self.name}")  # noqa: T201

        self._rendered = function_template.render(
            data=self,
        )

        out_path = target_path / self.file_name
        out_path.write_text(self._rendered)
        return self.file_name

    @property
    def file_name(self) -> str:
        """Get the file name."""
        return f"{self.module_name}.py"

    @property
    def module_name(self) -> str:
        """Get the file name."""
        return f"s{self._stream:02d}f{self._function:02d}"

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    @property
    def stream(self) -> int:
        """Get the stream number."""
        return self._stream

    @property
    def function(self) -> int:
        """Get the function number."""
        return self._function

    @property
    def description(self) -> str:
        """Get the description of the function."""
        return self._data["description"]

    @property
    def to_host(self) -> bool:
        """Get the to_host flag."""
        return self._data["to_host"]

    @property
    def to_equipment(self) -> bool:
        """Get the to_equipment flag."""
        return self._data["to_equipment"]

    @property
    def has_reply(self) -> bool:
        """Get the reply flag."""
        return self._data["reply"]

    @property
    def is_reply_required(self) -> bool:
        """Get the reply_required flag."""
        return self._data["reply_required"]

    @property
    def is_multi_block(self) -> bool:
        """Get the multi_block flag."""
        return self._data["multi_block"]

    @property
    def raw_structure(self) -> str | list | None:
        """Get the raw, textual structure."""
        if "structure" not in self._data:
            return None

        return self._data["structure"]

    @property
    def is_sfdl(self) -> bool:
        """Get if the function is defined in sfdl."""
        return isinstance(self.raw_structure, str) and self.raw_structure.strip().startswith("<")

    @property
    def structure(self) -> str:
        """Get the python structure."""
        if self.raw_structure is None:
            return "None"

        if self.is_sfdl:
            return f'"""\n{self.raw_structure}"""'

        return self._format_struct_as_string(self.raw_structure)

    def _format_struct_as_string(self, structure, indent_level=0, indent_width=4):
        indent_text = " " * indent_level
        if isinstance(structure, list):
            if len(structure) == 1 and not isinstance(structure[0], list):
                return f"{indent_text}[{structure[0]}]"

            items = [
                self._format_struct_as_string(item, indent_level + indent_width, indent_width) for item in structure
            ]
            items_text = ",\n".join(items)
            return f"{indent_text}[\n{items_text},\n{indent_text}]"

        if structure not in self._data_items:
            return f'{indent_text}"{structure}"'

        return f"{indent_text}{structure}"

    @property
    def data_items(self) -> list[DataItem]:
        """Get the data items used."""
        if self.raw_structure is None:
            return []

        if self.is_sfdl and isinstance(self.raw_structure, str):
            tokenizer = secsgem.secs.functions.sfdl_tokenizer.SFDLTokenizer(self.raw_structure)
            return list(dict.fromkeys([self._data_items[data_item] for data_item in tokenizer.tokens.data_items]))

        items: list[DataItem] = []
        self._find_items(self.raw_structure, items)
        return items

    @property
    def data_items_sorted(self) -> list[DataItem]:
        """Get the data items used sorted alphabetically."""
        return sorted(self.data_items, key=lambda data_item: data_item.name)

    def _find_items(self, structure, items):
        if not isinstance(structure, list):
            if structure in self._data_items:
                data_item = self._data_items[structure]
                if data_item not in items:
                    items.append(data_item)
        else:
            for item in structure:
                self._find_items(item, items)

    @property
    def data_structure_text(self) -> str:
        """Get the output of the data structure."""
        if self.raw_structure is None:
            return "Header only"

        imports = "\n".join([f"from secsgem.secs.data_items import {item.name}" for item in self.data_items])

        code = STRUCTURE_CODE.format(imports=imports, data_item=self.structure)

        glob: dict[str, typing.Any] = {}
        loc: dict[str, typing.Any] = {}

        exec(code, glob, loc)  # pylint: disable=exec-used  # noqa: S102

        return loc["var"]

    @property
    def samples(self) -> list[dict[str, typing.Any]]:
        """Get samples and result data."""
        if self._samples is None:
            self._samples, self._preferred_type = self._load_samples()

        return self._samples

    @property
    def preferred_type(self) -> type | None:
        """Get preferred type."""
        if self._samples is None:
            self._samples, self._preferred_type = self._load_samples()

        return self._preferred_type

    def _load_samples(self) -> tuple[list[dict[str, typing.Any]], type | None]:
        if "sample_data" not in self._data:
            sample_data = [{"data": ""}]
        else:
            sample_data = self._data["sample_data"]
            if isinstance(sample_data, str):
                sample_data = [{"data": sample_data}]

        samples = []
        preferred_type = None

        for sample in sample_data:
            imports = "\n".join([f"from secsgem.secs.data_items import {item.name}" for item in self.data_items])

            if not sample["data"]:
                code = SAMPLE_DATA_CODE_EMPTY.format(
                    imports=imports, data_item=self.structure, sample_value=sample["data"],
                )
            else:
                code = SAMPLE_DATA_CODE.format(imports=imports, data_item=self.structure, sample_value=sample["data"])

            glob: dict[str, typing.Any] = {}
            loc: dict[str, typing.Any] = {}

            exec(code, glob, loc)  # pylint: disable=exec-used  # noqa: S102

            samples.append(
                {
                    "data": sample["data"],
                    "comment": f" # {sample['info']}" if "info" in sample else "",
                    "text": loc["var"],
                },
            )
            preferred_type = loc["preferred_type"]

        return samples, preferred_type

    @property
    def extra_help(self) -> str:
        """Get the configured extra help."""
        if "extra_help" not in self._data:
            return ""

        return self._data["extra_help"]
