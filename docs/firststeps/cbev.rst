Callbacks and events
====================

:doc:`Callbacks <cbev_callback>` are used to handle requests from the remote system and return a user defined result (eg an alarm has been received and a response is required).
:doc:`Events <cbev_event>` can notify the implementation about something that occurred (eg the hsms connection was selected).
Events don't return any result to the remote and are executed in the background

.. toctree::

    cbev_callback
    cbev_event
