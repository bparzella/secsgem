#####################################################################
# functions.py
#
# (c) Copyright 2016-2021, Benjamin Parzella. All rights reserved.
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
"""Contains helper functions."""
import errno
import sys
import types


def format_hex(text: bytes) -> str:
    """
    Return byte arrays (string) formated as hex numbers.

    **Example**::

        >>> import secsgem.common
        >>>
        >>> data = b"asdfg"
        >>> secsgem.common.format_hex(data)
        '61:73:64:66:67'


    :param text: byte array
    :type text: string
    :returns: Formated text
    :rtype: string
    """
    return ":".join(f"{c:02x}" for c in bytearray(text))


def is_windows() -> bool:
    """
    Return True if running on windows.

    :returns: Is windows system
    :rtype: bool
    """
    if sys.platform == "win32":  # pragma: no cover
        return True

    return False


def function_name(function) -> str:
    """
    Get name of function or method.

    :returns: function/method name
    :rtype: string
    """
    if isinstance(function, types.FunctionType):
        return function.__name__

    return function.__self__.__class__.__name__ + "." + function.__name__


def indent_line(line: str, spaces: int = 2) -> str:
    """
    Indent line by a number of spaces.

    :param line: input text
    :type line: string
    :param spaces: number of spaces to prepend
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    return f"{' ' * spaces}{line}"


def indent_block(block: str, spaces: int = 2) -> str:
    """
    Indent a multiline string by a number of spaces.

    :param block: input text
    :type block: string
    :param spaces: number of spaces to prepend to each line
    :type spaces: integer
    :returns: indented text
    :rtype: string
    """
    lines = block.split('\n')
    lines_filter = filter(None, lines)
    indented_lines = [indent_line(line, spaces) for line in lines_filter]
    return '\n'.join(indented_lines)


def is_errorcode_ewouldblock(errorcode: int) -> bool:
    """
    Check if the errorcode is a would-block error.

    :param errorcode: Code of the error
    :return: True if blocking error code
    """
    if errorcode in (errno.EAGAIN, errno.EWOULDBLOCK):
        return True

    return False
