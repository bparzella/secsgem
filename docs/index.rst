.. title:: secsgem

secsgem
=======

secsgem is a python package to communicate with a host or equipment system in the semiconductor industry.

The use cases range from writing tests for implementations or features, simulations in development environments to complete host/equipment implementations.
Some parts of the package can be used individually, for example HSMS can be used without SECS-II, or the streams and functions can be used with a different networking stack.

Currently there is no support for communication over serial port (SECS-I, SEMI E04). Only ethernet (HSMS, SEMI E37) is available.

HSMS, SECS and GEM are standards from `SEMI <http://www.semi.org>`_.

Namespaces
----------

All classes can be accessed with their full module name or directly from the secsgem module.

   >>> secsgem.format_hex("Hallo")
   '48:61:6c:6c:6f'

   >>> secsgem.common.format_hex("Hello")
   '48:65:6c:6c:6f'

Thanks
------

   * `Carl Wolff <https://github.com/wolfc01>`_ for his sample TCP socket implementation
   * `Darius Sullivan <https://github.com/dariussullivan>`_ for his `gist <https://gist.github.com/dariussullivan/8916e975e22054ff470d>`_ on how to use the streams and functions with twisted
   * `Massimo Vanetti <https://github.com/massimov>`_ for his help on the equipment implementation

Table of contents
-----------------

.. toctree::
   :maxdepth: 4

   installation
   firststeps
   gem
   secs
   hsms
   reference

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

