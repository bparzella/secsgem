# GEM Compliance

**GEM COMPLIANCE STATEMENT**

| **Fundamental GEM Requirements** | **Implemented** | **GEM Compliant** |
|---|---|---|
| [State Models](#state-models) | Yes ✓ | No |
| [Equipment Processing States](#equipment-processing-states) | No | No |
| Host-Initiated S1,F13/F14 Scenario | Yes ✓ | Yes ✓ |
| Event Notification | Yes ✓ | Yes ✓ |
| On-Line Identification | Yes ✓ | Yes ✓ |
| Error Messages | Yes ✓ | Yes ✓ |
| [Documentation](#documentation) | Yes ✓ | No|
| [Control (Operator Initiated)](#control-operator-initiated) | Yes ✓ | No |

| **Additional Capabilities** | **Implemented** | **GEM Compliant** |
|---|---|---|
| Establish Communications | Yes ✓ | Yes ✓ |
| [Dynamic Event Report Configuration](#dynamic-event-report-configuration) | Yes ✓ | No |
| Variable Data Collection | Yes ✓ | Yes ✓ |
| [Trace Data Collection](#trace-data-collection) | No | No |
| Status Data Collection | Yes ✓ | Yes ✓ |
| [Alarm Management](#alarm-management) | Yes ✓ | No |
| [Remote Control](#remote-control) | Yes ✓ | Yes ✓ |
| [Equipment Constants](#equipment-constants) | Yes ✓ | No |
| [Process RecipeManagement](#process-recipe-management) | No | No |
| [Material Movement](#material-movement) | No | No |
| [Equipment Terminal Services](#equipment-terminal-services) | Yes ✓ | Yes ✓ |
| [Clock](#clock) | No | No |
| [Limits Monitoring](#limits-monitoring) | No | No |
| [Spooling](#spooling) | No | No |
| Control (Host-Initiated) | Yes ✓ | Yes ✓ |

## State Models

-   While the communication and control state models are implemented,
    especially the control state model needs rework.

## Equipment Processing States

-   Not implemented yet.

## Documentation

-   The documentation isn\'t complete yet.

## Control (Operator Initiated)

-   Persistence for the ONLINE LOCAL/REMOTE is not yet implemented.
-   The final UI (or hardware) needs the buttons required by this
    section.

## Dynamic Event Report Configuration

-   Persistence for report definitions, report-to-event links and enable
    status is not yet implemented.

## Trace Data Collection

-   Not implemented yet.

## Alarm Management

-   Persistence of en-/disable states and report definitions is not
    implemented yet.

## Remote Control

-   The START and STOP remote commands must be implemented to be GEM
    compliant. Currently only dummy functions are provided

## Equipment Constants

-   Persistence of the equipment constants is not implemented yet.
-   Limiting changing equipment to \"safe\" states is not yet
    implemented?
-   Equipment constant changed collection event is not yet implemented.

## Process Recipe Management

-   Not implemented yet.

## Material Movement

-   Not implemented yet.

## Equipment Terminal Services

-   The UI requirements can\'t be fulfilled by the library

## Clock

-   Not implemented yet.

## Limits Monitoring

-   Not implemented yet.

## Spooling

-   Not implemented yet.
