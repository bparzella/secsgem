#####################################################################
# test_secs_streams_functions.py
#
# (c) Copyright 2024, Benjamin Parzella. All rights reserved.
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
from secsgem.secs.functions import StreamsFunctions, SecsS01F00
from secsgem.secs.functions.base import SecsStreamFunction

class DummyS01F00(SecsStreamFunction):
    _stream = 1
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False


class TestStreamsFunctions:
    def test_default_values(self):
        sf = StreamsFunctions()

        assert sf.function(1, 0) == SecsS01F00

    def test_update(self):
        sf = StreamsFunctions()

        sf.update(DummyS01F00)

        assert sf.function(1, 0) != SecsS01F00
        assert sf.function(1, 0) == DummyS01F00
