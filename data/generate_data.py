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

    data_items = DataItem.load_all()
    function_data_items = {item.name: item for item in data_items}
    functions = Function.load_all(function_data_items)

    last = DataItem.render_list(data_items, env.get_template('data_items.py.j2'), pathlib.Path("out"))
    last = Function.render_list(functions, env.get_template('functions.py.j2'), pathlib.Path("out_func"))

    # pylint: disable=consider-using-with
    subprocess.Popen(["ksdiff", f"out_func/{last}", f"../secsgem/secs/functions/{last}"])


if __name__ == "__main__":
    run()
