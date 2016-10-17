#####################################################################
# functions.py
#
# (c) Copyright 2016, Benjamin Parzella. All rights reserved.
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
"""Contains helper functions"""

import sys
import types

def format_hex(text):
    """Returns byte arrays (string) formated as hex numbers.

    **Example**::

        >>> import secsgem
        >>>
        >>> data = b"asdfg"
        >>> secsgem.common.format_hex(data)
        '61:73:64:66:67'


    :param text: byte array
    :type text: string
    :returns: Formated text
    :rtype: string
    """
    return ":".join("{0:02x}".format(c) for c in bytearray(text))

def is_windows():
    """Returns True if running on windows

    :returns: Is windows system
    :rtype: bool
    """
    if sys.platform == "win32":  # pragma: no cover
        return True

    return False

def function_name(function):
    """Gets name of function or method

    :returns: function/method name
    :rtype: string
    """
    if isinstance(function, types.FunctionType):
        return function.__name__
    else:
        return function.__self__.__class__.__name__ + "." + function.__name__

def indent_line(line, spaces=2):
    """Indent line by a number of spaces

    :param line: input text
    :type line: string
    :param spaces: number of spaces to prepend
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    return (' ' * spaces) + line

def indent_block(block, spaces=2):
    """Indent a multiline string by a number of spaces

    :param block: input text
    :type block: string
    :param spaces: number of spaces to prepend to each line
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    lines = block.split('\n')
    lines = filter(None, lines)
    lines = map(lambda line, spc=spaces: indent_line(line, spc), lines)
    return '\n'.join(lines)
