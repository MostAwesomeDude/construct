===================
Stream manipulation
===================

.. note::

    Certain constructs are available only for seekable or tellable streams (in-memory and files). Sockets and pipes do not support neither, so you'll have to first read the data from the stream and parse it in-memory, or use experimental :class:`~construct.core.Rebuffered` wrapper.


Field wrappers
==============

Pointer allows for non-sequential construction. The pointer first moves the stream into new position, does the construction, and then restores the stream back to original position. This allows for random access within the stream.

>>> d = Pointer(8, Bytes(1))
>>> d.parse(b"abcdefghijkl")
b'i'
>>> d.build(b"Z")
b'\x00\x00\x00\x00\x00\x00\x00\x00Z'

Peek parses a field but restores the stream position afterwards (it peeks into the stream). Building does nothing, it does NOT defer to subcon.

>>> d = Sequence(Peek(Int16ul), Peek(Int16ub))
>>> d.parse(b"\x01\x02")
[513, 258]
>>> d.sizeof()
0


Pure side effects
=================

Seek makes a jump within the stream and leaves it there, for other constructs to follow up from that location. It does not read or write anything to the stream by itself.

>>> d = Sequence(Bytes(10), Seek(5), Byte)
>>> d.build([b"0123456789", None, 255])
b'01234\xff6789'

Tell checks the current stream position and returns it. The returned value gets automatically inserted into the context dictionary. It also does not read or write anything to the stream by itself.

>>> d = Struct("num"/VarInt, "offset"/Tell)
>>> d.parse(b"X")
Container(num=88, offset=1)
>>> d.build(dict(num=88))
b'X'


Other fields
=================

Pass literally does nothing. It is mostly used internally by If(IfThenElse) and Padding(Padded).

>>> Pass.parse(b"")
None
>>> Pass.build(None)
b''
>>> Pass.sizeof()
0

Terminated only works during parsing. It checks if the stream reached EOF and raises error if not.

>>> Terminated.parse(b"")
None
>>> Terminated.parse(b"remaining")
construct.core.TerminatedError: expected end of stream
