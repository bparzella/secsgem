# secsgem

secsgem is a python package to communicate with a host or equipment
system in the semiconductor industry.

The use cases range from writing tests for implementations or features,
simulations in development environments to complete host/equipment
implementations. Some parts of the package can be used individually, for
example HSMS can be used without SECS-II, or the streams and functions
can be used with a different networking stack.

Currently there is no support for communication over serial port
(SECS-I, SEMI E04). Only ethernet (HSMS, SEMI E37) is available.

HSMS, SECS and GEM are standards from [SEMI](http://www.semi.org).

## Thanks

- [Carl Wolff](https://github.com/wolfc01) for his sample TCP socket implementation
- [Darius Sullivan](https://github.com/dariussullivan) for his [gist](https://gist.github.com/dariussullivan/8916e975e22054ff470d) on how to use the streams and functions with twisted
- [Massimo Vanetti](https://github.com/massimov) for his help on the equipment implementation

## Table of contents

```{toctree}
:maxdepth: 2
installation
firststeps
gem
secs
hsms
reference
changes
```
