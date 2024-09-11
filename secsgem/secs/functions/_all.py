#####################################################################
# _all.py
#
# (c) Copyright 2023, Benjamin Parzella. All rights reserved.
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
"""List of all SECS stream and functions."""

from .s00f00 import SecsS00F00
from .s01f00 import SecsS01F00
from .s01f01 import SecsS01F01
from .s01f02 import SecsS01F02
from .s01f03 import SecsS01F03
from .s01f04 import SecsS01F04
from .s01f11 import SecsS01F11
from .s01f12 import SecsS01F12
from .s01f13 import SecsS01F13
from .s01f14 import SecsS01F14
from .s01f15 import SecsS01F15
from .s01f16 import SecsS01F16
from .s01f17 import SecsS01F17
from .s01f18 import SecsS01F18
from .s01f21 import SecsS01F21
from .s01f22 import SecsS01F22
from .s01f23 import SecsS01F23
from .s01f24 import SecsS01F24
from .s02f00 import SecsS02F00
from .s02f13 import SecsS02F13
from .s02f14 import SecsS02F14
from .s02f15 import SecsS02F15
from .s02f16 import SecsS02F16
from .s02f17 import SecsS02F17
from .s02f18 import SecsS02F18
from .s02f21 import SecsS02F21
from .s02f22 import SecsS02F22
from .s02f23 import SecsS02F23
from .s02f24 import SecsS02F24
from .s02f25 import SecsS02F25
from .s02f26 import SecsS02F26
from .s02f29 import SecsS02F29
from .s02f30 import SecsS02F30
from .s02f33 import SecsS02F33
from .s02f34 import SecsS02F34
from .s02f35 import SecsS02F35
from .s02f36 import SecsS02F36
from .s02f37 import SecsS02F37
from .s02f38 import SecsS02F38
from .s02f41 import SecsS02F41
from .s02f42 import SecsS02F42
from .s02f43 import SecsS02F43
from .s02f44 import SecsS02F44
from .s02f45 import SecsS02F45
from .s02f46 import SecsS02F46
from .s02f47 import SecsS02F47
from .s02f48 import SecsS02F48
from .s02f49 import SecsS02F49
from .s02f50 import SecsS02F50
from .s05f00 import SecsS05F00
from .s05f01 import SecsS05F01
from .s05f02 import SecsS05F02
from .s05f03 import SecsS05F03
from .s05f04 import SecsS05F04
from .s05f05 import SecsS05F05
from .s05f06 import SecsS05F06
from .s05f07 import SecsS05F07
from .s05f08 import SecsS05F08
from .s05f09 import SecsS05F09
from .s05f10 import SecsS05F10
from .s05f11 import SecsS05F11
from .s05f12 import SecsS05F12
from .s05f13 import SecsS05F13
from .s05f14 import SecsS05F14
from .s05f15 import SecsS05F15
from .s05f16 import SecsS05F16
from .s05f17 import SecsS05F17
from .s05f18 import SecsS05F18
from .s06f00 import SecsS06F00
from .s06f01 import SecsS06F01
from .s06f02 import SecsS06F02
from .s06f05 import SecsS06F05
from .s06f06 import SecsS06F06
from .s06f07 import SecsS06F07
from .s06f08 import SecsS06F08
from .s06f11 import SecsS06F11
from .s06f12 import SecsS06F12
from .s06f15 import SecsS06F15
from .s06f16 import SecsS06F16
from .s06f19 import SecsS06F19
from .s06f20 import SecsS06F20
from .s06f21 import SecsS06F21
from .s06f22 import SecsS06F22
from .s06f23 import SecsS06F23
from .s06f24 import SecsS06F24
from .s07f00 import SecsS07F00
from .s07f01 import SecsS07F01
from .s07f02 import SecsS07F02
from .s07f03 import SecsS07F03
from .s07f04 import SecsS07F04
from .s07f05 import SecsS07F05
from .s07f06 import SecsS07F06
from .s07f17 import SecsS07F17
from .s07f18 import SecsS07F18
from .s07f19 import SecsS07F19
from .s07f20 import SecsS07F20
from .s09f00 import SecsS09F00
from .s09f01 import SecsS09F01
from .s09f03 import SecsS09F03
from .s09f05 import SecsS09F05
from .s09f07 import SecsS09F07
from .s09f09 import SecsS09F09
from .s09f11 import SecsS09F11
from .s09f13 import SecsS09F13
from .s10f00 import SecsS10F00
from .s10f01 import SecsS10F01
from .s10f02 import SecsS10F02
from .s10f03 import SecsS10F03
from .s10f04 import SecsS10F04
from .s12f00 import SecsS12F00
from .s12f01 import SecsS12F01
from .s12f02 import SecsS12F02
from .s12f03 import SecsS12F03
from .s12f04 import SecsS12F04
from .s12f05 import SecsS12F05
from .s12f06 import SecsS12F06
from .s12f07 import SecsS12F07
from .s12f08 import SecsS12F08
from .s12f09 import SecsS12F09
from .s12f10 import SecsS12F10
from .s12f11 import SecsS12F11
from .s12f12 import SecsS12F12
from .s12f13 import SecsS12F13
from .s12f14 import SecsS12F14
from .s12f15 import SecsS12F15
from .s12f16 import SecsS12F16
from .s12f17 import SecsS12F17
from .s12f18 import SecsS12F18
from .s12f19 import SecsS12F19
from .s14f00 import SecsS14F00
from .s14f01 import SecsS14F01
from .s14f02 import SecsS14F02
from .s14f03 import SecsS14F03
from .s14f04 import SecsS14F04

secs_streams_functions = [
    SecsS00F00,
    SecsS01F00,
    SecsS01F01,
    SecsS01F02,
    SecsS01F03,
    SecsS01F04,
    SecsS01F11,
    SecsS01F12,
    SecsS01F13,
    SecsS01F14,
    SecsS01F15,
    SecsS01F16,
    SecsS01F17,
    SecsS01F18,
    SecsS01F21,
    SecsS01F22,
    SecsS01F23,
    SecsS01F24,
    SecsS02F00,
    SecsS02F13,
    SecsS02F14,
    SecsS02F15,
    SecsS02F16,
    SecsS02F17,
    SecsS02F18,
    SecsS02F21,
    SecsS02F22,
    SecsS02F23,
    SecsS02F24,
    SecsS02F25,
    SecsS02F26,
    SecsS02F29,
    SecsS02F30,
    SecsS02F33,
    SecsS02F34,
    SecsS02F35,
    SecsS02F36,
    SecsS02F37,
    SecsS02F38,
    SecsS02F41,
    SecsS02F42,
    SecsS02F43,
    SecsS02F44,
    SecsS02F45,
    SecsS02F46,
    SecsS02F47,
    SecsS02F48,
    SecsS02F49,
    SecsS02F50,
    SecsS05F00,
    SecsS05F01,
    SecsS05F02,
    SecsS05F03,
    SecsS05F04,
    SecsS05F05,
    SecsS05F06,
    SecsS05F07,
    SecsS05F08,
    SecsS05F09,
    SecsS05F10,
    SecsS05F11,
    SecsS05F12,
    SecsS05F13,
    SecsS05F14,
    SecsS05F15,
    SecsS05F16,
    SecsS05F17,
    SecsS05F18,
    SecsS06F00,
    SecsS06F01,
    SecsS06F02,
    SecsS06F05,
    SecsS06F06,
    SecsS06F07,
    SecsS06F08,
    SecsS06F11,
    SecsS06F12,
    SecsS06F15,
    SecsS06F16,
    SecsS06F19,
    SecsS06F20,
    SecsS06F21,
    SecsS06F22,
    SecsS06F23,
    SecsS06F24,
    SecsS07F00,
    SecsS07F01,
    SecsS07F02,
    SecsS07F03,
    SecsS07F04,
    SecsS07F05,
    SecsS07F06,
    SecsS07F17,
    SecsS07F18,
    SecsS07F19,
    SecsS07F20,
    SecsS09F00,
    SecsS09F01,
    SecsS09F03,
    SecsS09F05,
    SecsS09F07,
    SecsS09F09,
    SecsS09F11,
    SecsS09F13,
    SecsS10F00,
    SecsS10F01,
    SecsS10F02,
    SecsS10F03,
    SecsS10F04,
    SecsS12F00,
    SecsS12F01,
    SecsS12F02,
    SecsS12F03,
    SecsS12F04,
    SecsS12F05,
    SecsS12F06,
    SecsS12F07,
    SecsS12F08,
    SecsS12F09,
    SecsS12F10,
    SecsS12F11,
    SecsS12F12,
    SecsS12F13,
    SecsS12F14,
    SecsS12F15,
    SecsS12F16,
    SecsS12F17,
    SecsS12F18,
    SecsS12F19,
    SecsS14F00,
    SecsS14F01,
    SecsS14F02,
    SecsS14F03,
    SecsS14F04,
]
