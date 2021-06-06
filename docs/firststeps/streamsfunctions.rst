Custom streams and functions
============================

Custom data item
----------------

A new data item is created by overriding the :code:`DataItemBase` class::

    class UNITS_New(DataItemBase):
        __type__ = SecsVarDynamic    
        __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
            SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]

In this case the :code:`UNITS` field allows all types instead only a string.

Custom stream function
----------------------

To integrate this new data item in a stream function then you need to inherit :class:`secsgem.secs.functionbase.SecsStreamFunction` ::

    class SecsS01F12_New(secsgem.secs.SecsStreamFunction):
        _stream = 1
        _function = 12

        _data_format = [
            [
                SVID,
                SVNAME,
                UNITS_New
            ]
        ]

        _to_host = True
        _to_equipment = False

        _has_reply = False
        _is_reply_required = False

        _is_multi_block = True


Integrate a stream function
---------------------------

Now we want to integrate this stream/function into the :class:`secsgem.gem.handler.GemHandler`.
You create a new class inherited from it and update the function list of that class::

    class NewHandler(secsgem.GemHostHandler):
        def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
            secsgem.GemHostHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)

            self.secs_streams_functions[1].update({
                12: SecsS01F12_New,
            })

You can also add new methods and properties to the class if required.

This new class can be used with the :class:`secsgem.hsms.connectionmanager.HsmsConnectionManager` (see parameter connection_handler of :func:`secsgem.hsms.connectionmanager.HsmsConnectionManager.add_peer`)