# -*- coding: utf-8 -*-
#####################################################################
# codec_jis_x_0201.py
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
"""JIS X 0201 Codec required for JIS8 encoding of SecsVarJIS8"""

import codecs

jis8_decoding_map = codecs.make_identity_dict(range(256))
jis8_decoding_map.update({
    0x005C: 0x00A5,  # Yen Sign
    0x007E: 0x203E,  # Overline
})

for i in range(0x00A1, 0x00E0):
    jis8_decoding_map[i] = i + 0xFEC0

jis8_encoding_map = codecs.make_encoding_map(jis8_decoding_map)

def jis_x_0201_encode(data, errors='strict'):
    return codecs.charmap_encode(data,errors,jis8_encoding_map)

def jis_x_0201_decode(data, errors='strict'):
    return codecs.charmap_decode(data,errors,jis8_decoding_map)
    
def jis_x_0201_search(name):
    if name == "jis-8":
        return codecs.CodecInfo(encode=jis_x_0201_encode, decode=jis_x_0201_decode, name="jis-8")

    return None

# register the codec
codecs.register(jis_x_0201_search)
