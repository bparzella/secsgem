"""Generate DataItems from yaml config."""  # noqa: INP001

from __future__ import annotations

import pathlib

import jinja2
import markupsafe
from data_item import DataItem
from function import Function


def py_indent(
    text: str,
    width: int | str = 4,
    first: bool = False,
    blank: bool = False,
) -> str:
    """Return a copy of the string with each line indented by 4 spaces.

    The first line and blank lines are not indented by default.

    Args:
        text: source text
        width: Number of spaces, or a string, to indent by.
        first: Don't skip indenting the first line.
        blank: Don't skip indenting empty lines.

    .. versionchanged:: 3.0
        ``width`` can be a string.

    .. versionchanged:: 2.10
        Blank lines are not indented by default.

        Rename the ``indentfirst`` argument to ``first``.
    """
    indention = width if isinstance(width, str) else " " * width

    newline = "\n"

    if isinstance(text, markupsafe.Markup):
        indention = markupsafe.Markup(indention)
        newline = markupsafe.Markup(newline)

    text += newline  # this quirk is necessary for splitlines method

    if blank:
        result = (newline + indention).join(text.splitlines())
    else:
        lines = text.splitlines()
        result = lines.pop(0)

        if lines:
            result += newline + newline.join(indention + "...     " + line if line else line for line in lines)

    if first:
        result = indention + result

    return result


def run():
    """Run the generation."""
    root = pathlib.Path(__file__).parent.resolve()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(root / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,  # noqa: S701
    )

    env.filters["py_indent"] = py_indent

    data_items = DataItem.load_all()
    functions = Function.load_all({item.name: item for item in data_items})

    DataItem.render_list(data_items, env, functions, root / ".." / "secsgem" / "secs" / "data_items")

    Function.render_list(functions, env, root / ".." / "secsgem" / "secs" / "functions")


if __name__ == "__main__":
    run()
