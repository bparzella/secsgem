"""Generate DataItems from yaml config."""
import pathlib
import subprocess

import jinja2

from data_item import DataItem
from function import Function


def run():
    """Run the generation."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    data_item_template = env.get_template('data_items.py.j2')
    function_template = env.get_template('functions.py.j2')

    data_items = DataItem.load_all()
    function_data_items = {item.name: item for item in data_items}
    functions = Function.load_all(function_data_items)

    last = None
    for data_item in data_items:
        print(f"# generate data item {data_item.name}")

        data_item_code = data_item_template.render(
            data=data_item
        )

        out_path = pathlib.Path("out") / data_item.file_name
        out_path.write_text(data_item_code)
        last = data_item.file_name

    for function in functions:
        print(f"# generate data item {function.name}")

        function_code = function_template.render(
            data=function
        )

        print(function.structure)

        out_path = pathlib.Path("out_func") / function.file_name
        out_path.write_text(function_code)
        last = function.file_name

    # pylint: disable=consider-using-with
    subprocess.Popen(["ksdiff", f"out_func/{last}", f"../secsgem/secs/functions/{last}"])


if __name__ == "__main__":
    run()