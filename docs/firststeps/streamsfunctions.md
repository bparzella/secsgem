# Custom streams and functions

## Custom data item

A new data item is created by overriding the {py:class}`secsgem.secs.data_items.DataItemBase` class:

```python
class UNITS_New(DataItemBase):
    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]
```

In this case the `UNITS` field allows all types instead only a string.

## Custom stream function

To integrate this new data item in a stream function then you need to inherit {py:class}`secsgem.secs.functions.SecsStreamFunction` :

```python
class SecsS01F12_New(secsgem.secs.functions.SecsStreamFunction):
    _stream = 1
    _function = 12

    _data_format = """
        <L
            <L
                <SVID>
                <SVNAME>
                <UNITS_New>
            >
        >
    """

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
```

The data format is defined in a definition language that is based on SML.
For more information on the definition language see [Secs Function Definition Language](sfdl.md)

Data can also be defined using an old, python type based format.
This was the format the functions were initially coded in.
The format still works, but will be deprecated in the near future.

```python
class SecsS01F12_New(secsgem.secs.functions.SecsStreamFunction):
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
```

## Integrate a stream function

Now we want to integrate this stream/function into the {py:class}`secsgem.gem.handler.GemHandler`.
You create a new class inherited from it and update the function list of that class:

```python
class NewHandler(secsgem.gem.GemHostHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)

        self.settings.streams_functions.update(SecsS01F12_New)
```

You can also add new methods and properties to the class if required.

The streams functions list can also be updated outside of the Handler:

```python
settings = secsgem.hsms.HsmsSettings()
settings.streams_functions.update(SecsS01F12_New)

handler = NewHandler(settings)
```
