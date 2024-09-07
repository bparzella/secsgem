"""Data item class definition."""
from __future__ import annotations

import typing

import jsonschema
import yaml

data_item_schema = {
    "description": "Root array of data items definition",
    "type": "object",
    "properties": {
        "/": {}
    },
    "patternProperties": {
        "^[A-Z0-9]+$": {
            "description": "Data item definition",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                },
                "type": {
                    "oneOf": [
                        {
                            "type": ["array", "string"],
                            "enum": ["A", "Array", "Binary", "Boolean", "F4", "F8", "I1", "I2", "I4", "I8", "String", "U1", "U2", "U4", "U8"],
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["A", "Array", "Binary", "Boolean", "F4", "F8", "I1", "I2", "I4", "I8", "String", "U1", "U2", "U4", "U8"],
                            }
                        }

                    ],
                },
                "length": {
                    "type": "integer",
                },
                "values": {
                    "type": "object",
                    "patternProperties": {
                        "^[0-9-]+$": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                },
                                "constant": {
                                    "type": "string",
                                },
                            },
                            "additionalProperties": False,
                        },
                    },
                    "additionalProperties": False,
                },
                "linter_message": {
                    "type": "string",
                },
                "help": {
                    "type": "string",
                },
            },
            "required": ["description", "type"],
            "additionalProperties": False,
        }
    },
    "additionalProperties": False,
}


class DataItem:
    """Data item configuration from yaml."""

    def __init__(self, name, data) -> None:
        """Initialize item config."""
        self._name = name
        self._data = data

        self._rendered = None

        assert "type" in data
        assert "description" in data

    @classmethod
    def load_all(cls, root) -> typing.List["DataItem"]:
        """Load all data item objects."""
        data = (root / "data_items.yaml").read_text(encoding="utf8")
        yaml_data = yaml.safe_load(data)
        jsonschema.validate(instance=yaml_data, schema=data_item_schema)
        return [cls(data_item, data_item_data) for data_item, data_item_data in yaml_data.items()]

    @staticmethod
    def render_list(data_items, env, functions, target_path):
        """Render a list of data items."""
        last = None

        data_item_template = env.get_template('data_items.py.j2')
        data_item_init_template = env.get_template('data_items_init.py.j2')
        data_item_md_template = env.get_template('data_items.md.j2')

        for data_item in data_items:
            print(f"# generate data item {data_item.name}")

            used_by = [function for function in functions if data_item in function.data_items]
            last = data_item.render(data_item_template, target_path, used_by)

        init_code = data_item_init_template.render(
            data_items=data_items,
        )

        out_path = target_path / "__init__.py"
        out_path.write_text(init_code)

        md_code = data_item_md_template.render(
            data_items=data_items,
        )

        out_path = target_path.parent.parent.parent / "docs" / "reference" / "secs" / "data_items.md"
        out_path.write_text(md_code)

        return last

    def render(self, data_item_template, target_path, used_by):
        """Render the data item file."""
        self._rendered = data_item_template.render(
            data=self,
            used_by=used_by
        )

        out_path = target_path / self.file_name
        out_path.write_text(self._rendered)
        return self.file_name

    @property
    def name(self) -> str:
        """Get the name of the data item."""
        return self._name

    @property
    def type(self) -> typing.List[str]:
        """Get the type of the data item."""
        if not isinstance(self._data["type"], list):
            return [self._data["type"]]

        return self._data["type"]

    @property
    def linter_message(self) -> str:
        """Get the linter message of the data item."""
        if "linter_message" not in self._data:
            return ""

        return self._data["linter_message"]

    @property
    def single_type(self) -> bool:
        """Check if this is a single type object."""
        if not isinstance(self._data["type"], list):
            return True

        if len(self._data["type"]) == 1:
            return True

        return False

    @property
    def description(self) -> str:
        """Get the description of the data item."""
        return self._data["description"]

    @property
    def help(self) -> str:
        """Get the help of the data item."""
        if "help" not in self._data:
            return ""

        return self._data["help"]

    @property
    def length(self) -> int:
        """Get the length of the data item."""        
        return self._data["length"] if "length" in self._data else -1

    @property
    def values(self) -> str:
        """Get the values of the data item."""
        if len(self.type) == 1:
            if self.type[0] == "Boolean":
                return self._values_boolean

        return self._values_binary

    @property
    def extra_variables(self) -> str:
        """Get the extra variables of the data item."""
        if len(self.type) == 1:
            if self.type[0] in ("Boolean"):
                return ""
        return self._extra_variables_binary

    @property
    def _values_boolean(self) -> str:
        if "values" not in self._data:
            return ""

        table_data = [
            ["Value", ""],
            ["True", self._data["values"][True]],
            ["False", self._data["values"][False]],
        ]

        table = self._markdown_table(table_data, 8)

        text = f"    **Values**\n{table}\n"
        return text

    @property
    def _values_binary(self) -> str:
        if "values" not in self._data:
            return ""

        table_data = [
            ["Value", "Description", "Constant"],
        ]
        for value_name, value in self._data["values"].items():
            constant = f":const:`secsgem.secs.data_items.{self.name}.{value['constant']}`" \
                if "constant" in value else ""
            table_data.append([str(value_name), value["description"], constant])

        table = self._markdown_table(table_data, 8)

        text = f"    **Values**\n{table}\n"
        return text

    @property
    def _extra_variables_binary(self) -> str:
        if "values" not in self._data:
            return ""

        variables = []
        for name, value in self._data["values"].items():
            if "constant" not in value:
                continue

            val = str(name)
            if "-" in val:
                val = val.split("-", maxsplit=1)[0]

            variables.append(f"{value['constant']} = {val}")

        if len(variables) < 1:
            return ""

        join_text = '\n    '
        text = f"\n    {join_text.join(variables)}\n"
        return text

    @property
    def file_name(self) -> str:
        """Get the file name."""
        return f"{self.module_name}.py"

    @property
    def module_name(self) -> str:
        """Get the file name."""
        return self.name.lower()

    def _markdown_line_separator(self, lengths, separator="-"):
        line = "+"
        for length in lengths:
            line += separator * (length + 2)
            line += "+"

        return line

    def _markdown_line(self, lengths, values):
        line = "|"
        for index, length in enumerate(lengths):
            line += " "
            line += f"{values[index]:{length}}"
            line += " |"

        return line

    def _markdown_table(self, data, indent=4):
        lengths = [0] * len(data[0])
        for line, line_value in enumerate(data):
            for col, _ in enumerate(lengths):
                length = len(data[line][col])
                lengths[col] = max(lengths[col], length)

        indent_text = " " * indent
        text = f"{indent_text}{self._markdown_line_separator(lengths)}"
        for line, line_value in enumerate(data):
            text += f"\n{indent_text}{self._markdown_line(lengths, line_value)}"
            text += f"\n{indent_text}{self._markdown_line_separator(lengths, '-' if line != 0 else '=')}"

        text += "\n"

        return text
