=================
Streaming tactics
=================


Pointer
-------

Pointer allows for non-sequential construction. The pointer first changes the stream position, does the construction, and restores the original stream position.

.. note::

    Pointers are available only for seekable streams (in-memory and files). Sockets and pipes do not support seeking, so you'll have to first read the data from the stream, and parse it in-memory. That or use the :func:`~construct.core.Rebuffered` wrapper.

.. autoclass:: construct.core.Pointer


Anchor
------

Anchor is not really a meta construct, but it strongly coupled with Pointer, so I chose to list it here. Anchor simply returns the stream position at the moment it's invoked, so Pointers can "anchor" relative offsets to absolute stream positions using it. See the following example:

.. autoclass:: construct.core.Anchor


