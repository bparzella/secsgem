#####################################################################
# common.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
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

def formatHex(text):
    """Returns byte arrays (string) formated as hex numbers.

    **Example**::

        >>> data = "asdfg"
        >>> secsgem.common.formatHex(data)
        '61:73:64:66:67'


    :param text: byte array
    :type text: string
    :returns: Formated text
    :rtype: string
    """
    return ":".join("{0:02x}".format(ord(c)) for c in text)

def isWindows():
    """Returns True if running on windows

    :returns: Is windows system
    :rtype: bool
    """
    if sys.platform == "win32":
        return True

    return False
