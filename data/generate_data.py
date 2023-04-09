"""Generate DataItems from yaml config."""
import pathlib
import typing

import jinja2
import markupsafe

from data_item import DataItem
from function import Function

def py_indent(
    s: str, width: typing.Union[int, str] = 4, first: bool = False, blank: bool = False
) -> str:
    """
    Return a copy of the string with each line indented by 4 spaces.

    The first line and blank lines are not indented by default.

    :param width: Number of spaces, or a string, to indent by.
    :param first: Don't skip indenting the first line.
    :param blank: Don't skip indenting empty lines.

    .. versionchanged:: 3.0
        ``width`` can be a string.

    .. versionchanged:: 2.10
        Blank lines are not indented by default.

        Rename the ``indentfirst`` argument to ``first``.
    """
    if isinstance(width, str):
        indention = width
    else:
        indention = " " * width

    newline = "\n"

    if isinstance(s, markupsafe.Markup):
        indention = markupsafe.Markup(indention)
        newline = markupsafe.Markup(newline)

    s += newline  # this quirk is necessary for splitlines method

    if blank:
        rv = (newline + indention).join(s.splitlines())
    else:
        lines = s.splitlines()
        rv = lines.pop(0)

        if lines:
            rv += newline + newline.join(
                indention + "...     " + line if line else line for line in lines
            )

    if first:
        rv = indention + rv

    return rv


def run():
    """Run the generation."""
    root = pathlib.Path(__file__).parent.resolve()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(root / 'templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.filters['py_indent'] = py_indent

    data_items = DataItem.load_all(root)
    functions = Function.load_all(root, {item.name: item for item in data_items})

    DataItem.render_list(
        data_items,
        env.get_template('data_items.py.j2'),
        functions,
        root / ".." / "secsgem" / "secs" / "data_items")

    # subprocess.Popen(["ksdiff", 
    #                   str((root / ".." / "secsgem" / "secs" / "data_items" / last).absolute()),
    #                   str((root / "out" / last).absolute()), 
    #                  ])

    Function.render_list(
        functions,
        env.get_template('functions.py.j2'),
        root / ".." / "secsgem" / "secs" / "functions")

    # subprocess.Popen(["ksdiff", 
    #                   str((root / ".." / "secsgem" / "secs" / "functions" / last).absolute()),
    #                   str((root / "out_func" / last).absolute()), 
    #                  ])


if __name__ == "__main__":
    run()
