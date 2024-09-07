#####################################################################
# functions.py
#
# (c) Copyright 2021-2023, Benjamin Parzella. All rights reserved.
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
"""SECS variable helper functions."""

from __future__ import annotations

import inspect
import typing

from secsgem.secs import data_items
from secsgem.secs.functions.sfdl_tokenizer import SFDLTokenizer

from .base import Base

if typing.TYPE_CHECKING:
    from secsgem.secs.functions.sfdl_tokenizer import SFDLToken


def _generate_item_from_sfdl(tokenizer: SFDLTokenizer, item_token: SFDLToken, item_name: str):
    item = getattr(data_items, item_name, None)

    if item is None:
        raise item_token.exception(f"Unknown data type {item_name}")

    if not tokenizer.tokens.available:
        raise item_token.exception("Closing tag '>' expected", end=True)

    closing_token = tokenizer.tokens.next()

    if closing_token.value != ">":
        raise closing_token.exception("Closing tag '>' expected")

    return item


def _generate_from_sfdl(tokenizer: SFDLTokenizer, token_name: str | None = None):
    opening_token = tokenizer.tokens.next()

    if opening_token.value != "<":
        raise opening_token.exception("Opening tag '<' expected")

    item_token = tokenizer.tokens.next()
    item_name = item_token.value.upper()

    if item_name != "L":
        return _generate_item_from_sfdl(tokenizer, item_token, item_name)

    item_key_token = None
    if tokenizer.tokens.peek().value not in "<>":
        item_key_token = tokenizer.tokens.next()

    sub_items: list = []

    if tokenizer.tokens.peek(ahead=2).value != "L" and token_name:
        sub_items.append(token_name)
        token_name = None

    while True:
        if not tokenizer.tokens.available or tokenizer.tokens.peek().value not in "<>":
            last_token = item_key_token if item_key_token else item_token
            raise last_token.exception("Expected opening '<' or closing '>' tag", end=True)

        if tokenizer.tokens.peek().value == ">":
            tokenizer.tokens.next()
            return list(sub_items)

        sub_items.append(_generate_from_sfdl(tokenizer, item_key_token.value if item_key_token else None))


def generate(data_format):
    """Generate actual variable from data format.

    :param data_format: data format to create variable for
    :type data_format: list/Base based class
    :returns: created variable
    :rtype: Base based class
    """
    from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import
    from .list_type import List  # pylint: disable=import-outside-toplevel,cyclic-import

    if data_format is None:
        return None

    if isinstance(data_format, str):
        tokenizer = SFDLTokenizer(data_format)

        data_format = _generate_from_sfdl(tokenizer)

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return Array(data_format[0])
        return List(data_format)
    if inspect.isclass(data_format):
        if issubclass(data_format, Base):
            return data_format()
        raise TypeError(f"Can't generate item of class {data_format.__name__}")
    raise TypeError(f"Can't handle item of class {data_format.__class__.__name__}")


def get_format(data_format, showname=False):
    """Get the format of the function.

    :returns: returns the string representation of the function
    :rtype: string
    """
    del showname  # unused variable

    from .array import Array  # pylint: disable=import-outside-toplevel,cyclic-import
    from .list_type import List  # pylint: disable=import-outside-toplevel,cyclic-import

    if data_format is None:
        return None

    if isinstance(data_format, str):
        tokenizer = SFDLTokenizer(data_format)

        data_format = _generate_from_sfdl(tokenizer)

    if isinstance(data_format, list):
        if len(data_format) == 1:
            return Array.get_format(data_format[0])
        return List.get_format(data_format)

    if inspect.isclass(data_format):
        if issubclass(data_format, Base):
            return data_format.get_format()
        raise TypeError(f"Can't generate data_format for class {data_format.__name__}")

    raise TypeError(f"Can't handle item of class {data_format.__class__.__name__}")
