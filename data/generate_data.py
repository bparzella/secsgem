"""Generate DataItems from yaml config."""
import pathlib

import jinja2
import yaml


class DataItem:
    """Data item configuration from yaml."""

    def __init__(self, name, data) -> None:
        """Initialize item config."""
        self._name = name
        self._data = data

        assert "type" in data
        assert "description" in data

    @property
    def name(self) -> str:
        """Get the name of the data item."""
        return self._name

    @property
    def type(self) -> str:
        """Get the type of the data item."""
        return self._data["type"]

    @property
    def description(self) -> str:
        """Get the description of the data item."""
        return self._data["description"]

    @property
    def length(self) -> int:
        """Get the length of the data item."""
        return self._data["length"] if "length" in self._data else 1

    @property
    def values(self) -> str:
        """Get the values of the data item."""
        if self.type == "Boolean":
            return self._values_boolean
        if self.type == "Binary":
            return self._values_binary
        return "Hallo"

    @property
    def extra_variables(self) -> str:
        """Get the extra variables of the data item."""
        if self.type == "Binary":
            return self._extra_variables_binary
        return ""

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
            ["Value", "Description      ", "Constant"],  # TODO: remove spaces
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

        join_text = '\n    '
        text = f"\n    {join_text.join(variables)}\n"
        return text

    @property
    def file_name(self) -> str:
        """Get the file name."""
        return f"{self.name.lower()}.py"

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


def _load_data_items():
    data = pathlib.Path("data_items.yaml").read_text(encoding="utf8")
    return yaml.safe_load(data)


def run():
    """Run the generation."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    data_item_template = env.get_template('data_items.tmpl.py')

    data_items = _load_data_items()

    for data_item in data_items:
        print(f"# generate data item {data_item}")
        data = DataItem(data_item, data_items[data_item])

        data_item_code = data_item_template.render(
            data=data
        )

        out_path = pathlib.Path("out") / data.file_name
        out_path.write_text(data_item_code)


if __name__ == "__main__":
    run()