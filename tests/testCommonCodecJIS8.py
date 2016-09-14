# -*- coding: utf-8 -*-
#####################################################################
# testCommonJIS8.py
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

import secsgem

class TestCodecJIS8(object):
    charMap = [
        [u"¥", b"\\"],
        [u"‾", b"~"],
    ]

    for i in range(0x00A1, 0x00E0):
        charMap.append([chr(i + 0xFEC0), bytes(bytearray([i]))])

    def checkEncodeText(self, unicodeText, byteText):
        assert unicodeText.encode("jis-8") == byteText
    
    def checkDecodeText(self, byteText, unicodeText):
        assert byteText.decode("jis-8") == unicodeText

    def testCoding(self):
        for charMapping in self.charMap:
            yield self.checkEncodeText, charMapping[0], charMapping[1] 
            yield self.checkDecodeText, charMapping[1], charMapping[0] 

    def testUnknownSearch(self):
        assert secsgem.common.codec_jis_x_0201.jis_x_0201_search("invalid") == None


