#####################################################################
# testSecsFunctions.py
#
# (c) Copyright 2013-2016, Benjamin Parzella. All rights reserved.
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

import inspect
import nose

import secsgem.secs.dataitems

def find_subclasses(module):
    return [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and not cls.__name__.startswith("SecsVar")]

class TestDataItems(object):
    def checkConstructorWithoutValue(self, cls):
        cls()

    def testDataItems(self):
        for cls in find_subclasses(secsgem.secs.dataitems):
            yield self.checkConstructorWithoutValue, cls
