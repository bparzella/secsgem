.. title:: secsgem

secsgem
=======

secsgem is a python package to communicate with a host or equipment system in the semiconductor industry.

It is designed to be independent of any external dependencies, making it usable in a closed fab environment without internet connection.

The use cases range from writing tests for implementations or features, simulations in development environments to complete host/equipment implementations.
Some parts of the package can be used individually, for example HSMS can be used without SECS-II, or the streams and functions can be used with a different networking stack.

Currently there is no support for communication over serial port (SECS-I, SEMI E04) only ethernet (HSMS, SEMI E37) is available.

HSMS, SECS and GEM are standards from `SEMI <http://www.semi.org>`_.

Thanks
------

   * `Carl Wolff <https://github.com/wolfc01>`_ for his sample TCP socket implementation
   * `Darius Sullivan <https://github.com/dariussullivan>`_ for his `gist <https://gist.github.com/dariussullivan/8916e975e22054ff470d>`_ on how to use the streams and functions with twisted

Table of contents
-----------------

.. toctree::
   :maxdepth: 4

   hsms
   secs
   gem
   reference

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

