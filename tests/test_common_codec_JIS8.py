# -*- coding: utf-8 -*-
#####################################################################
# test_common_codec_JIS8.py
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

from builtins import chr

import pytest

import secsgem.common


class TestCodecJIS8:
    charMap = [
        [u"¥", b"\\"],
        [u"‾", b"~"],
    ]

    for i in range(0x00A1, 0x00E0):
        charMap.append([chr(i + 0xFEC0), bytes(bytearray([i]))])

    @pytest.mark.parametrize("char_map", charMap)
    def test_encode_text(self, char_map):
        assert char_map[0].encode("jis_8") == char_map[1]
    
    @pytest.mark.parametrize("char_map", charMap)
    def test_decode_text(self, char_map):
        assert char_map[1].decode("jis_8") == char_map[0]

    def test_unknown_search(self):
        assert secsgem.common.codec_jis_x_0201._jis_x_0201_search("invalid") == None


