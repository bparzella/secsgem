# Secs Function Definition Language

SFDL is derived from SML but allows the definition of a function without obfuscated, redundant type definitions.

## Data items

Data items are defined with their name in a set of pointed brackets.

```{code-block}
:caption: Structure definition for standard S6F2

< ACKC6 >
```

```{code-block}
:caption: Structure definition for standard S2F36

< LRACK >
```

## List

Lists are described with 'L' on the opening bracket in a set of pointed brackets.

### Fixed length lists

A list with multiple different data items is mapped to a dict or object.
This can be accessed with the data item name as key.

```{code-block}
:caption: Structure definition for standard S5F1

< L
    < ALCD >
    < ALID >
    < ALTX >
>
```
### Open length lists

Open lists are defined with only one data item.
They can hold multiple values with the same data type.

```{code-block}
:caption: Structure definition for standard S1F3

< L
    < SVID >
>
```

### Nesting

Lists can be nested within each other.

```{code-block}
:caption: Structure definition for standard S1F22

< L
    < L
        < VID >
        < DVVALNAME >
        < UNITS >
    >
>
```

#### Nesting open length lists in fixed length lists

If an open list with a single data item is nested within a fixed length list ( mapped to a dict/object), the name of the nested data item is used to override the key of the parent list.

```{code-block}
:caption: Structure definition for standard S2F23

< L
    < TRID >
    < DSPER >
    < TOTSMP >
    < REPGSZ >
    < L 
        < SVID >
    >
>
```

This will make the list of SVIDs available with the key/attribute SVID.

If an open list of fixed length is nested in a fixed length list (oof) resolving the name doesn't work like in the previous example.
In this case the item is simply named "DATA".
But this name can be overridden, by passing the name after the L tag

```{code-block}
:caption: Structure definition for standard S2F33

< L
    < DATAID >
    < L REPORTS
        <L
            < RPTID >
            < L
                < VID >
            >
        >
    >
>
```

In this case the list of reports will accessible with the key/attribute REPORTS.

But also other nested lists can be named this way

```{code-block}
:caption: Structure definition for standard S2F23

< L
    < TRID >
    < DSPER >
    < TOTSMP >
    < REPGSZ >
    < L SVIDS
        < SVID >
    >
>
```

This will make the list of SVIDs available with the key/attribute SVIDS.

```{code-block}
:caption: Structure definition for standard S6F8

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
```

## Comments

Comments start with a `#` and end with the line break.

```{code-block}
:caption: Structure definition for custom message

< L  # Sample list
    < DATAID >  # The data id
    < CEID >    # The collection event id
>
```

## Why create a custom function definition language?

While there is a function definition language named SML, it doesn't meet the requirements for definition the generic function format itself.
It shines when visualizing the actual data sent/received in a message.

The specification lacks the definition of open lists (n elements).
Also defining multiple data formats for a data item is not described in the specification. (e.g.)

## Why not create a completely new definition language?

SML is quite spread in the semiconductor industry and a lot of people had contact with it.
For that reason it is better to stick with a format that is at least similar to the known format.