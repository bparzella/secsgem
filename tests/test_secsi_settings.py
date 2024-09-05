#####################################################################
# test_secsi_settings.py
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

import pytest

import secsgem.common
import secsgem.secsi
import secsgem.secs.functions

class TestSecsISettings:
    def test_without_args(self):
        settings = secsgem.secsi.SecsISettings()

        assert settings.device_type == secsgem.common.DeviceType.HOST
        assert isinstance(settings.streams_functions, secsgem.secs.functions.StreamsFunctions)
        assert settings.session_id == 0
        assert settings.establish_communication_timeout == 10

        assert settings.port == ""
        assert settings.speed == 9600

    def test_with_args(self):
        settings = secsgem.secsi.SecsISettings(
            device_type=secsgem.common.DeviceType.HOST,
            session_id=1,
            establish_communication_timeout=1,
            port="SomePort",
            speed=1234,
        )

        assert settings.device_type == secsgem.common.DeviceType.HOST
        assert isinstance(settings.streams_functions, secsgem.secs.functions.StreamsFunctions)
        assert settings.session_id == 1
        assert settings.establish_communication_timeout == 1

        assert settings.port == "SomePort"
        assert settings.speed == 1234

    def test_with_invalid(self):
        with pytest.raises(ValueError) as exc:
            settings = secsgem.secsi.SecsISettings(
                invalid_arg=-1,
            )
        assert str(exc.value) == "SecsISettings initialized with unknown arguments: invalid_arg"
