Implementing a GEM equipment
============================

This package can be used to create a GEM equipment implementation.
This is done by subclassing the :class:`secsgem.gem.equipmenthandler.GemEquipmentHandler` class::

    import secsgem.gem
    import code

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

    h = SampleEquipment("127.0.0.1", 5000, False, 0, "sampleequipment")
    h.enable()

    code.interact("equipment object is available as variable 'h', press ctrl-d to stop", local=locals())

    h.disable()


Using your own name
-------------------

To use your own modelname and version for S1F14 reply you can override the :attr:`secsgem.gem.handler.GemHandler.MDLN` and :attr:`secsgem.gem.handler.GemHandler.SOFTREV` members of the GemHandler::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.MDLN = "gemequp"
            self.SOFTREV = "1.0.0"

Adding status variables
-----------------------

A status variable can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.StatusVariable` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.status_variables` dictionary::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.status_variables.update({
                10: secsgem.gem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.secs.variables.U4, False),
                "SV2": secsgem.gem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.secs.variables.String, False),
            })

            self.status_variables[10].value = 123
            self.status_variables["SV2"].value = "sample sv"


Alternatively the values can be acquired using a callback by setting the use_callback parameter of the constructor to True::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.sv1 = 123
            self.sv2 = "sample sv"

            self.status_variables.update({
                10: secsgem.gem.StatusVariable(10, "sample1, numeric SVID, SecsVarU4", "meters", secsgem.secs.variables.U4, True),
                "SV2": secsgem.gem.StatusVariable("SV2", "sample2, text SVID, SecsVarString", "chars", secsgem.secs.variables.String, True),
            })

        def on_sv_value_request(self, svid, sv):
            if sv.svid == 10:
                return sv.value_type(value=self.sv1)
            elif sv.svid == "SV2":
                return sv.value_type(value=self.sv2)

            return []


Adding equipment constants
--------------------------

An equipment constant can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.EquipmentConstant` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.status_variables` dictionary::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.equipment_constants.update({
                20: secsgem.gem.EquipmentConstant(20, "sample1, numeric ECID, SecsVarU4", 0, 500, 50, "degrees", secsgem.secs.variables.U4, False),
                "EC2": secsgem.gem.EquipmentConstant("EC2", "sample2, text ECID, SecsVarString", "", "", "", "chars", secsgem.secs.variables.String, False),
            })

            self.status_variables[20].value = 321
            self.status_variables["EC2"].value = "sample ec"


Alternatively the values can be acquired and updated using callbacks by setting the use_callback parameter of the constructor to True::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.ec1 = 321
            self.ec2 = "sample ec"

            self.equipment_constants.update({
                20: secsgem.gem.EquipmentConstant(20, "sample1, numeric ECID, SecsVarU4", 0, 500, 50, "degrees", secsgem.secs.variables.U4, True),
                "EC2": secsgem.gem.EquipmentConstant("EC2", "sample2, text ECID, SecsVarString", "", "", "", "chars", secsgem.secs.variables.String, True),
            })

        def on_ec_value_request(self, ecid, ec):
            if ec.ecid == 20:
                return ec.value_type(value=self.ec1)
            elif ec.ecid == "EC2":
                return ec.value_type(value=self.ec2)

            return []

        def on_ec_value_update(self, ecid, ec, value):
            if ec.ecid == 20:
                self.ec1 = value
            elif ec.ecid == "EC2":
                self.ec2 = value

Adding collection events
------------------------

A collection event can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.CollectionEvent` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.collection_events` dictionary.
Data values can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.DataValue` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.data_values` dictionary.
The data values for a collection event can be passed while creating the :class:`secsgem.gem.equipmenthandler.CollectionEvent` instance::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.dv1 = 31337

            self.data_values.update({
                30: secsgem.gem.DataValue(30, "sample1, numeric DV, SecsVarU4", secsgem.secs.variables.U4, True),
            })

            self.collection_events.update({
                50: secsgem.gem.CollectionEvent(50, "test collection event", [30]),
            })

        def on_dv_value_request(self, dvid, dv):
            if dv.dvid == 30:
                return dv.value_type(value=self.dv1)

            return []

        def trigger_sample_collection_event():
            self.trigger_collection_events([50])

Adding alarms
-------------

An alarm can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.Alarm` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.alarms` dictionary.
The collection events for the alarm must be provided when adding the alarm. For an example see the section above::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.collection_events.update({
                100025: secsgem.gem.CollectionEvent(100025, "test collection event alarm set", []),
                200025: secsgem.gem.CollectionEvent(200025, "test collection event alarm clear", []),
            })

            self.alarms.update({
                25: secsgem.gem.Alarm(25, "test alarm", "test text", secsgem.secs.data_items.ALCD.PERSONAL_SAFETY | secsgem.secs.data_items.ALCD.EQUIPMENT_SAFETY, 100025, 200025),
            })

        def set_sample_alarm():
            self.set_alarm(25)

        def clear_sample_alarm():
            self.clear_alarm(25)

Adding remote commands
----------------------

A remote command can be added by inserting an instance of the :class:`secsgem.gem.equipmenthandler.RemoteCommand` class to the :attr:`secsgem.gem.equipmenthandler.GemEquipmentHandler.remote_commands` dictionary.
The collection event and parameters for the remote command must be provided when adding it. For an example see the section above::

    class SampleEquipment(secsgem.gem.GemEquipmentHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.gem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.collection_events.update({
                5001: secsgem.gem.CollectionEvent(5001, "TEST_RCMD complete", []),
            })
            self.remote_commands.update({
                "TEST_RCMD": secsgem.gem.RemoteCommand("TEST_RCMD", "test rcmd", ["TEST_PARAMETER"], 5001),
            })

        def on_rcmd_TEST_RCMD(self, TEST_PARAMETER):
            print "remote command TEST_RCMD received"

