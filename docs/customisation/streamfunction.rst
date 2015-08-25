Streams and functions
---------------------

To create a new stream/function you only need to inherit :class:`secsgem.secs.functionbase.SecsStreamFunction`.
Three members need to be overridden: _stream, _function and _formatDescriptor.

The last one defines the structure of the data transferred for the stream/function.

For example you want to allow the UNITS field of stream to not only be a string, but any type.
You create a new class and define the format descriptor::

    class SecsS01F12_New(secsgem.SecsStreamFunction):
        _stream = 1
        _function = 12

        _formatDescriptor = secsgem.SecsVarArray(secsgem.SecsVarList(OrderedDict((
            ("SVID", secsgem.SecsVarU4(1)),
            ("SVNAME", secsgem.SecsVarString()),
            ("UNITS", secsgem.SecsVarDynamic([])),
        )), 3))


To see how to integrate that into the handlers, see the next page :doc:`/customisation/handlers`