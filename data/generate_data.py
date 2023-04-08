"""Generate DataItems from yaml config."""
import pathlib
import subprocess

import jinja2

from data_item import DataItem
from function import Function


def run():
    """Run the generation."""
    root = pathlib.Path(__file__).parent.resolve()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(root / 'templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    data_items = DataItem.load_all(root)
    functions = Function.load_all(root, {item.name: item for item in data_items})

    last = DataItem.render_list(data_items, env.get_template('data_items.py.j2'), root / "out")
    last = Function.render_list(functions, env.get_template('functions.py.j2'), root / "out_func")

    # pylint: disable=consider-using-with
    subprocess.Popen(["ksdiff", 
                      str((root / "out_func" / last).absolute()), 
                      str((root / ".." / "secsgem" / "secs" / "functions" / last).absolute())
                     ])


if __name__ == "__main__":
    run()
