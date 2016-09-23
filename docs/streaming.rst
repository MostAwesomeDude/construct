=================
Streaming tactics **
=================


Pointer
-------

Pointer allows for non-sequential construction. The pointer first changes the stream position, does the construction, and restores the original stream position.

.. note::

    Pointers are available only for seekable streams (in-memory and files). Sockets and pipes do not support seeking, so you'll have to first read the data from the stream, and parse it in-memory. That or use the :func:`~construct.core.Rebuffered` wrapper.

.. autoclass:: construct.core.Pointer




Pure side effects
-----------------

Seek makes a jump within the stream and leave it at point. It does not parse or build anything by itself.

.. autoclass:: construct.core.Seek

Tell checks the current stream position and returns it, also to the context. It does not parse or build anything by itself.

.. autofunction:: construct.core.Tell


