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

## v0.2.1 [planned]

* Update documentation

## v0.3.0 [planned]

* [Fail when initializing settings with invalid arguments](#fail-when-initializing-settings-with-invalid-arguments)

### Fail when initializing settings with invalid arguments

Due to the multi-layered settings structure the keyword arguments of the 'Settings' initializers were not checked for invalid arguments.
A ValueError is now raised if an unknown parameter is passed to the settings constructor.

This is implemented for HsmsSettings, SecsISettings and SecsITcpSettings.

Also tests for the settings were added.
