===================
Stream manipulation
===================

.. note::

    Certain constructs are available only for seekable or tellable streams (in-memory and files). Sockets and pipes do not support seeking, so you'll have to first read the data from the stream and parse it in-memory, or use experimental :func:`~construct.core.Rebuffered` wrapper.


Field wrappers
==============

Pointer allows for non-sequential construction. The pointer first changes the stream position, does the construction, and restores the original stream position.

.. autoclass:: construct.core.Pointer

Peek parses the subconstruct but restores the stream position afterwards (it does peeking). Building does nothing, it does NOT defer to subcon when building.

.. autoclass:: construct.core.Peek


Pure side effects
=================

Seek makes a jump within the stream and leaves it at that point. It does not read or write anything to the stream by itself.

.. autofunction:: construct.core.Seek

Tell checks the current stream position and returns it, also putting it into the context. It does not read or write anything to the stream by itself.

.. autofunction:: construct.core.Tell

.. autofunction:: construct.core.Pass

.. autofunction:: construct.core.Terminated


Stream wrappers
===================

.. autoclass:: construct.core.Restreamed

.. autoclass:: construct.core.Rebuffered

