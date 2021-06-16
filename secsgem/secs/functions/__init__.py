#####################################################################
# functions.py
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
"""Wrappers for SECS stream and functions."""
import importlib
import inspect
import pathlib
import typing

from .base import SecsStreamFunction


def _load_function_classes() -> typing.Dict[str, SecsStreamFunction]:
    # search for stream/function files in current path (sXXfYY.py)
    module_path = pathlib.Path(__file__).parent
    function_modules = module_path.glob("s[0-9][0-9]f[0-9][0-9].py")

    function_classes = {}

    # iterate all module paths
    for function_module_path in function_modules:
        # load the module
        spec = importlib.util.spec_from_file_location(function_module_path.stem, function_module_path)
        function_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(function_module)

        # get all stream function classes from the module
        module_function_classes = {name: obj for name, obj in inspect.getmembers(function_module)
                                   if inspect.isclass(obj)
                                   and issubclass(obj, SecsStreamFunction)
                                   and obj is not SecsStreamFunction}

        # store found functions in
        function_classes.update(module_function_classes)

    return function_classes


__all__ = [
    "SecsStreamFunction", "secs_streams_functions"
]

# load all available stream/function classes into a dictionary
functions = _load_function_classes()

# update this module to include all loaded function classes
globals().update(functions)

# add the loaded class names into the __all__ list
__all__.extend(functions.keys())

# build the old style streams functions dictionary
secs_streams_functions = {}

for name, function in functions.items():
    # pylint: disable=protected-access
    if function._stream not in secs_streams_functions:
        secs_streams_functions[function._stream] = {}

    secs_streams_functions[function._stream][function._function] = function
