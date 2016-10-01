=================
Streaming tactics **
=================

.. note::

    Certain constructs are available only for seekable streams (in-memory and files) and some require tellable streams (which in fact is a subset of seekability). Sockets and pipes do not support seeking, so you'll have to first read the data from the stream, and parse it in-memory, or use the :func:`~construct.core.Rebuffered` wrapper.

Wrappers
========

Pointer
-------

Pointer allows for non-sequential construction. The pointer first changes the stream position, does the construction, and restores the original stream position.

>>> Pointer(8, Bytes(1)).parse(b"abcdefghijkl")
b'i'
>>> Pointer(8, Bytes(1)).build(b"x")
b'\x00\x00\x00\x00\x00\x00\x00\x00x'

Peek
----

Parses the subconstruct but restores the stream position afterwards (it does "peeking").

>>> Sequence(Peek(Byte), Peek(Int16ub)).parse(b"\x01\x02")
[1, 258]



Pure side effects
=================

Seek makes a jump within the stream and leaves it at that point. It does not read or write anything to the stream by itself.

.. autoclass:: construct.core.Seek

Tell checks the current stream position and returns it, also putting it into the context. It does not read or write anything to the stream by itself.

.. autofunction:: construct.core.Tell


Stream manipulation
===================

.. autofunction:: construct.core.Rebuffered

.. autofunction:: construct.core.Restreamed


