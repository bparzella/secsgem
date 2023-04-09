"""Function class definition."""
import collections
import re
import typing

import yaml

from data_item import DataItem


structure_code = """
import secsgem.secs
{imports}

data_item = {data_item}

var = secsgem.secs.variables.functions.get_format(data_item)
"""

sample_data_code = """
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

sample_data_code_empty = """
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

class Function:
    """Function configuration from yaml."""

    sf_regex = re.compile(r"[sS](\d+)[fF](\d+)")

    def __init__(
        self, 
        name: str, 
        data: typing.Dict[str, typing.Any], 
        data_items: typing.Dict[str, typing.Any]
    ) -> None:
        """Initialize item config."""
        self._name = name
        self._data = data

        self._data_items = data_items

        self._rendered = None

        assert "description" in data
        assert "to_host" in data
        assert "to_equipment" in data
        assert "reply" in data
        assert "reply_required" in data
        assert "multi_block" in data

        match = self.sf_regex.match(self._name)
        if not match:
            raise ValueError(f"Function name not valid {name}")
        
        self._stream = int(match.group(1))
        self._function = int(match.group(2))

        self._samples = None
        self._preferred_type = None

    @classmethod
    def load_all(cls, root, data_items: typing.Dict[str, DataItem]) -> typing.List["Function"]:
        """Load all function objects."""
        data = (root / "functions.yaml").read_text(encoding="utf8")
        yaml_data = yaml.safe_load(data)
        return [cls(function, function_data, data_items) for function, function_data in yaml_data.items()]

    @classmethod
    def render_list(cls, functions: typing.List["Function"], env, target_path):
        """Render all functions to file."""
        last = None

        function_template = env.get_template('functions.py.j2')
        function_init_template = env.get_template('functions_init.py.j2')

        for function in functions:
            last = function.render(function_template, target_path)
        
        init_code = function_init_template.render(
            functions=functions,
            streams_functions=cls.stream_function_dict(functions)
        )

        out_path = target_path / "__init__.py"
        out_path.write_text(init_code)

        return last

    @staticmethod
    def stream_function_dict(functions: typing.List["Function"]) -> typing.Dict:
        """Get streams functions in a dict."""
        # build the old style streams functions dictionary
        secs_streams_functions = collections.OrderedDict()

        for function in functions:
            if function.stream not in secs_streams_functions:
                secs_streams_functions[function.stream] = collections.OrderedDict()

            secs_streams_functions[function.stream][function.function] = function
        
        return secs_streams_functions

    def render(self, function_template, target_path):
        """Render a function to file."""
        print(f"# generate function {self.name}")

        self._rendered = function_template.render(
            data=self
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
    def raw_structure(self) -> typing.Optional[typing.Union[str, typing.List]]:
        """Get the raw, textual structure."""
        if "structure" not in self._data:
            return None
        
        return self._data["structure"]

    @property
    def structure(self) -> str:
        """Get the python structure."""
        if self.raw_structure is None:
            return "None"
        
        return self._format_struct_as_string(self.raw_structure)
    
    def _format_struct_as_string(self, structure, indent_level = 0, indent_width = 4):
        indent_text = " " * indent_level
        if isinstance(structure, list):
            if len(structure) == 1 and not isinstance(structure[0], list):
                return f"{indent_text}[{structure[0]}]"
            
            items = [self._format_struct_as_string(item, indent_level + indent_width, indent_width)
                        for item in structure]
            items_text = ',\n'.join(items)
            return f"{indent_text}[\n{items_text}\n{indent_text}]"
        
        if structure not in self._data_items:
            return f'{indent_text}"{structure}"'
        
        return f"{indent_text}{structure}"
        
    
    @property
    def data_items(self) -> typing.List[DataItem]:
        """Get the data items used."""
        if self.raw_structure is None:
            return []
        
        items = []
        self._find_items(self.raw_structure, items)
        return items

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

        code = structure_code.format(imports=imports, data_item=self.structure)

        glob = {}
        loc = {}

        exec(code, glob, loc)

        return loc["var"]
    
    @property
    def samples(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Get samples and result data."""
        if self._samples is None:
            self._load_samples()
        
        return self._samples
    
    @property
    def preferred_type(self) -> str:
        """Get preferred type."""
        if self._samples is None:
            self._load_samples()
        
        return self._preferred_type
    
    def _load_samples(self) -> typing.List[typing.Dict[str, typing.Any]]:
        if "sample_data" not in self._data:
            sample_data = [{"data": ""}]
        else:
            sample_data = self._data["sample_data"]
            if isinstance(sample_data, str):
                sample_data = [{"data": sample_data}]
        
        self._samples = []

        for sample in sample_data:
            imports = "\n".join([f"from secsgem.secs.data_items import {item.name}" for item in self.data_items])

            if not sample["data"]:
                code = sample_data_code_empty.format(
                    imports=imports,
                    data_item=self.structure,
                    sample_value=sample["data"])
            else:
                code = sample_data_code.format(
                    imports=imports,
                    data_item=self.structure,
                    sample_value=sample["data"])

            glob = {}
            loc = {}

            exec(code, glob, loc)

            self._samples.append({
                "data": sample["data"],
                "comment": f" # {sample['info']}" if "info" in sample else "",
                "text": loc["var"]
            })
            self._preferred_type = loc["preferred_type"]

    @property
    def extra_help(self) -> str:
        """Get the configured extra help."""
        if "extra_help" not in self._data:
            return ""
        
        return self._data["extra_help"]
