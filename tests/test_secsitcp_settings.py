#####################################################################
# test_secsitcp_settings.py
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
import secsgem.secsitcp
import secsgem.secs.functions

class TestSecsITcpSettings:
    def test_without_args(self):
        settings = secsgem.secsitcp.SecsITcpSettings()

        assert settings.device_type == secsgem.common.DeviceType.HOST
        assert isinstance(settings.streams_functions, secsgem.secs.functions.StreamsFunctions)
        assert settings.device_id == 0
        assert settings.establish_communication_timeout == 10

        assert settings.connect_mode == secsgem.secsitcp.SecsITcpConnectMode.CLIENT
        assert settings.address == "127.0.0.1"
        assert settings.port == 5000

    def test_with_args(self):
        settings = secsgem.secsitcp.SecsITcpSettings(
            device_type=secsgem.common.DeviceType.HOST,
            device_id=1,
            establish_communication_timeout=1,
            connect_mode=secsgem.secsitcp.SecsITcpConnectMode.SERVER,
            address="123.123.123.123",
            port=1234,
        )

        assert settings.device_type == secsgem.common.DeviceType.HOST
        assert isinstance(settings.streams_functions, secsgem.secs.functions.StreamsFunctions)
        assert settings.device_id == 1
        assert settings.establish_communication_timeout == 1

        assert settings.connect_mode == secsgem.secsitcp.SecsITcpConnectMode.SERVER
        assert settings.address == "123.123.123.123"
        assert settings.port == 1234

    def test_with_invalid(self):
        with pytest.raises(ValueError) as exc:
            secsgem.secsitcp.SecsITcpSettings(
                invalid_arg=-1,
            )
        assert str(exc.value) == "SecsITcpSettings initialized with unknown arguments: invalid_arg"
