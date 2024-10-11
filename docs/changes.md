# Changes

## v0.2.0

* [Use settings to setup connection parameters](#use-settings-to-setup-connection-parameters)
* [Add SECS-I support](#add-secs-i-and-secs-i-over-tcp-support)
* [Serialized message callback](#serialized-message-callback)
* [Split big secsgem namespace and rename classes](#split-big-secsgem-namespace-and-rename-classes)
* [Data item and stream/function classes are now auto-generated](#data-item-and-streamfunction-classes-are-now-auto-generated)


### Use settings to setup connection parameters

The SecsHandler and GemHandler classes were initialized using the hsms configuration as parameters.

```python
import secsgem

secsgem.GemHandler("10.211.55.33", 5000, False, 0, "test")
```

As new a new protocol and a new connection layer was added, this initialisation doesn't fit all instances any more.
For this reason new Settings classes were introduced:

```python
import secsgem.common

import secsgem.hsms
import secsgem.secsi
import secsgem.secsitcp

hsms_settings = secsgem.hsms.HsmsSettings(
    device_type=secsgem.common.DeviceType.EQUIPMENT,
    connect_mode=secsgem.hsms.HsmsConnectMode.ACTIVE,
    address="127.0.0.1",
    port=5001,
)

secsi_settings = secsgem.secsi.SecsISettings(
    device_type=secsgem.common.DeviceType.HOST,
    port="COM1",
    speed=9600,
)

secsi_tcp_settings = secsgem.secsitcp.SecsITcpSettings(
    device_type=secsgem.common.DeviceType.EQUIPMENT,
    connect_mode=secsgem.secsitcp.SecsITcpConnectMode.CLIENT,
    address="127.0.0.1",
    port=5555,
)

# initialize handler with settings
import secsgem.gem

handler = secsgem.gem.GemEquipmentHandler(secsi_settings)

```

### Add SECS-I and SECS-I over TCP support

The SECS-II and GEM handlers were built upon and inheriting the HSMS handler, making the communication and protocol mingled with the higher level message handling.
This required separation of the communication and protocol from the message handling.

#### Communication layer

```{uml}
:caption: Old structure
:align: center
HsmsHandler <|-- SecsHandler : inherits
SecsHandler <|-- GemHandler : inherits
GemHandler <|-- GemEquipmentHandler : inherits
GemHandler <|-- GemHostHandler : inherits
```

The old class structure was quite linear, inheriting functionality from the basic class.

```{uml}
:caption: New Structure
:align: center
class Settings {
    +create_connection()
    +create_protocol()
}

SecsHandler <|-- GemHandler : inherits
GemHandler <|-- GemEquipmentHandler : inherits
GemHandler <|-- GemHostHandler : inherits

Settings <- SecsHandler : initialized with

Connection <-- Settings::create_connection : returns
Protocol <-- Settings::create_protocol : returns
Protocol <-- SecsHandler : uses
Connection <- Protocol : uses
```

Now the handlers are initialized with a `Settings` object, which in turn creates the `Protocol` and `Communication` classes used by the handler.
This way the communication layer can be switched by simply passing different settings.

```{uml}
:caption: Initialisation
:align: center

SecsHandler --> SecsISettings : create_protocol
activate SecsISettings
SecsISettings --> SecsIProtocol : constuct
activate SecsIProtocol
SecsIProtocol --> SecsISettings : create_connection
activate SecsISettings
SecsISettings --> SerialConnection : construct
activate SerialConnection
SerialConnection --> SecsISettings : created
deactivate SerialConnection
SecsISettings -> SecsIProtocol : return
deactivate SecsISettings
SecsIProtocol -> SecsISettings : created
deactivate SecsIProtocol
SecsISettings -> SecsHandler : return
deactivate SecsISettings

```

#### Packets

The incoming data was encapsulated in a `HsmsPacket` object.
But this was protocol specific.

Now every protocol type has an own message type, inherited from a base `Message` class.
This base class defines the interface for the Messages.
It uses a protocol specific header object inherited from `Header` and is made up of blocks using the `Block` class.

#### Renamed events

Due to the new communication layer (serial) and protocol (SECS-I) some events are renamed to match the use case:

| old | new |
|---|---|
| hsms_connected | connected |
| hsms_selected | communicating |
| hsms_disconnected | disconnected |
| packet_received | message_received |

### Serialized message callback

Each message callback was called from a new thread to allow the receiver thread to be responsive for new packets.
This could lead to messages not arriving in an expected order.

```{uml}
:caption: Old callback handling
:align: center

Receiver --> Handler : message received
activate Handler
Handler --> Thread : start thread
activate Thread
Handler -> Receiver : continue
deactivate Handler
Thread --> Callback : start callback
activate Callback
Callback -> Thread : callback finished
deactivate Callback
deactivate Thread
```

Now incoming packets are added to a queue, which is processed by a single, separate thread.
This allows the receiver thread to be responsive and the callbacks to be called in the order the packets are received.

```{uml}
:caption: New callback handling
:align: center

participant Receiver
participant Handler
database Queue
participant Processor
participant Callback

activate Processor
Receiver --> Handler : message received
activate Handler
Handler --> Queue : queue message
Handler -> Receiver : continue
deactivate Handler
Queue --> Processor : read queue
Processor --> Callback : start callback
activate Callback
Callback -> Processor : callback finished
deactivate Callback

```

### Split big secsgem namespace and rename classes

All the classes were available in the toplevel `secsgem` namespace (e.g. `secsgem.CallbackHandler`).
This global namespace made the classes easy to access, but it was pretty big and the classes had names that were redundant with the individual namespaces.

In this version the classes need to be imported and accessed using the sub-namespace.

**Old**:
```python
import secgem
from secsgem import SecsHandler

secsgem.GemEquipmentHandler(...)
SecsHandler(...)
```

**New**:
```python
import secgem.gem
from secsgem.secs import SecsHandler

secsgem.gem.GemEquipmentHandler(...)
SecsHandler(...)
```

### Data item and stream/function classes are now auto-generated

As these classes are quite similar in code, the differences are extracted and included in yaml files in the `data` directory. (`data/data_items.yaml` and `data/functions.yaml`)
The contents of the files in the directories `secsgem/secs/data_items` and `secsgem/secs/functions` are generated from these yaml files using templates.
Also the class API documentation file is generated using the yaml files.

All generator data is located in the `data` directory in the project root, including the generator script (`data/generate_data.py`) and the template files (`data/*.j2`)

## v0.3.0

* [Fail when initializing settings with invalid arguments](#fail-when-initializing-settings-with-invalid-arguments)
* [Add simple customization of equipment specific functions](#add-simple-customization-of-equipment-specific-functions)
* [Add function definition language](#add-function-definition-language)
* [Change data item and data item access](#change-data-item-and-data-item-access)

### Fail when initializing settings with invalid arguments

Due to the multi-layered settings structure the keyword arguments of the 'Settings' initializers were not checked for invalid arguments.
A ValueError is now raised if an unknown parameter is passed to the settings constructor.

This is implemented for HsmsSettings, SecsISettings and SecsITcpSettings.

Also tests for the settings were added.

### Add simple customization of equipment specific functions

The old, documented way for replacing / adding a customized function to a handler doesn't work with 0.2.0 any more.
So a new way to simply modify the function list for an equipment was added.

To allow equipment specific modifications of the function list, it was moved to the settings in 0.2.0.
With this move a container for the function list was added, to allow simple lookups.

Now a function was added to this container, to update its function list.
This will either add or update the function in the list.
The container is accessible from the settings.

```python
class UNITS_New(DataItemBase):
    name = "UNITS"

    __type__ = SecsVarDynamic  # changed
    __allowedtypes__ = [SecsVarU1, SecsVarU2, SecsVarU4, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarString]  # changed

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
    _to_equipment = True  # Changed

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True

settings = secsgem.hsms.HsmsSettings()
settings.streams_functions.update(SecsS01F12_New)

handler = secsgem.gem.GemHostHandler(settings)
```

### Add function definition language
Defining the data item for a function is a quite complex and confusing task.
Wrapping the function definition in python data types is not very intuitive.

So a new description language was added, based on SML, which is known in combination with secs.
For more information check the documentation ([Secs Function Definition Language](firststeps/sfdl.md)).

```{attention}
Custom data types are currently not supported with SFDL.
```

Old:
```python
class SecsS06F08(SecsStreamFunction):
    _stream = 6
    _function = 8

    _data_format = [
        DATAID,
        CEID,
        [
            [
                "DS",
                DSID,
                [
                    [
                        "DV",
                        DVNAME,
                        DVVAL
                    ]
                ]
            ]
        ]
    ]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
```

New:
```python
class SecsS06F08(SecsStreamFunction):
    _stream = 6
    _function = 8

    _data_format = """
        < L
            < DATAID >
            < CEID >
            < L DS
                < L
                    < DSID >
                    < L DV
                        < L
                            < DVNAME >
                            < DVVAL >
                        >
                    >
                >
            >
        >
    """

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
```

### Change data item and data item access
A new container for the data items was introduced.
This container is usually accessible via the settings object and the handler, as it represents the equipment specific data items.
This allows the customization of the data items on a per-equipment level.

Custom data item classes need new attributes to work.

```python
class UNITS_New(DataItemBase):
    name = "UNITS"

    __type__ = SecsVarDynamic
    __allowedtypes__ = [SecsVarArray, SecsVarBoolean, SecsVarU1, SecsVarU2, SecsVarU4, SecsVarU8, SecsVarI1, SecsVarI2, SecsVarI4, SecsVarI8, \
        SecsVarF4, SecsVarF8, SecsVarString, SecsVarBinary]
```

The `name` attribute marks the name of the data item.
This is required for lookup of the data item class using the settings / handler.
It is also used when updating the data item using the container in the settings.

The `_value` attribute is the mapping used for the constants as a dictionary.
It is used for lookup of the constants.

The downside of this implementation is that code suggestions in the IDE won't work any more.

#### Recommendation: Start accessing the data items using the handler / settings.
The plan is to remove the function and data item classes and read the configuration directly from the yaml files.
This means code written using the classes will need to be rechanged.

## v0.4.0 [planned]

* [Rename session_id to device_id](#rename-session-id-to-device-id)

### Rename session_id to device_id

```{danger}
This might break your code, changes to your code might be required.
```

Rename all session_id fields to device_id.
This changes the naming of the variable to match the semi naming of the variable and to avoid confusion about this variable.

### Update python minimum requirement to 3.9

As the version 3.8 is now EOL, the minimum requirement was raised to 3.9.

### Load data item definition from yaml directly

Data item class files were generated using the yaml file.
This made it necessary to run the class generator after changing the yaml file.

Instead of using the classes the data item definitions are now loaded from the yaml file directly.
This makes the boilerplate class definition obsolete.
No generator step is needed in between any more.

For now the data item classes are generated dynamically using the same base class as before.
But the goal is to make the data item definition more flexible, without the use of data item classes.

The generated data item files are deleted from the package.
This means that development IDEs won't recognize the data items for autocompletion any more.

If you use data item classes directly, you need to update the way you get the data items.
The data item list is available using the settings in the handler / protocol / connection.

Old:
```python
lrack = secsgem.secs.data_items.LRACK.ACK
```

New:
```python
lrack = secsgem.secs.data_items.DataItems().LRACK.ACK

# or

lrack = handler.settings.data_items.LRACK.ACK

```

The streams / functions now need the data_items as first parameter to initialize.

To find stream function initialization using the classes directly use the following regex:
```regex
SecsS\d\dF\d\d\s*\(
```

To find new setting / handler based function initialization use the following regex:
```regex
\.stream_function\(
```