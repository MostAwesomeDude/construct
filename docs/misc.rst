=============
Miscellaneous
=============

Miscellaneous
=============

Padding
-------

Padding is a sequence of bytes or bits that contains no data (its value is discarded), and is necessary only for padding, or it can be used simply to discard some amount of garbage data. Notice that Padding does not require a name, because it does not need a value to be built from. Struct detects that and does not even search the dictionary for a value mathing Padding's name.

>>> st = Struct(
...     Padding(4),
... )
>>> st.build({})
b'\x00\x00\x00\x00'


Const
-----

A constant value that is required to exist in the data and match a given value. If the value is not matched, ConstError is raised. Useful for so called magic numbers, signatures, asserting correct protocol version, etc.

>>> Const(b"IHDR").build()
>>> Const(b"IHDR").build(None)
b'IHDR'
>>> Const(b"IHDR").parse(b"JPEG")
construct.core.ConstError: expected b'IHDR' but parsed b'JPEG'

By default, Const uses a Bytes field with size mathing the value. However, other fields can also be used:

>>> Const(Int32ul, 1).build(None)
b'\x01\x00\x00\x00'


Computed
--------

Represents a computed value. Value does not read or write anything to the stream. It only returns its computed value as the result. Usually Computed fields are used for computations on the context. Look at the previous chapter. However, Computed can also produce values based on external environment, random module, or constants. For example:

>>> st = Struct(
...     "width" / Byte,
...     "height" / Byte,
...     "total" / Computed(this.width * this.height),
... )
>>> st.parse(b"12")
Container(width=49)(height=50)(total=2450)
>>> st.build(dict(width=4,height=5))
b'\x04\x05'

>>> Computed(lambda ctx: os.urandom(10)).parse(b"")
b'[\x86\xcc\xf1b\xd9\x10\x0f?\x1a'


Pass
----

A do-nothing construct, useful in Switches and Enums.

.. note:: Pass is a singleton object. Do not try to instantiate it, ``Pass()`` will not work.

>>> Pass.parse(b"123123")
>>> Pass.build(None)
b''


Terminated
----------

Asserts the end of the stream has been reached (so that no more trailing data is left unparsed).

.. note:: Terminated is a singleton object. Do not try to instantiate it, ``Terminated()`` will not work.

>>> Terminated.parse(b"")
>>> Terminated.parse(b"x")
construct.core.TerminatedError: expected end of stream


Numpy
-----

Numpy arrays can be preserved and retrived along with their dtype, shape and size, and all. Otherwise, if dtype is constant, you could use PrefixedArray or Range to store enumerables.

>>> import numpy
>>> Numpy.build(numpy.asarray([1,2,3]))
b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"


NamedTuple
----------

Both arrays, structs and sequences can be mapped to a namedtuple from collections module. To create a named tuple, you need to provide a name and a sequence of fields, either a string with space-separated names or a list of strings. Just like the std library namedtuple does.

>>> NamedTuple("coord", "x y z", Byte[3]).parse(b"123")
coord(x=49, y=50, z=51)
>>> NamedTuple("coord", "x y z", Byte >> Byte >> Byte).parse(b"123")
coord(x=49, y=50, z=51)
>>> NamedTuple("coord", "x y z", Struct("x"/Byte, "y"/Byte, "z"/Byte)).parse(b"123")
coord(x=49, y=50, z=51)


Rebuild
-------

When there is an array separated from its length field, the Rebuild wrapped can be used to measure the len of the list at building. Note that both the `len_` and `this` expressions are used as discussed in meta chapter.

>>> st = Struct(
...     "count" / Rebuild(Byte, len_(this.items)),
...     "items" / Byte[this.count],
... )
>>> st.build(dict(items=[1,2,3]))
b'\x03\x01\x02\x03'

When the length field is directly before the items, `PrefixedArray` can be used instead:

>>> d = PrefixedArray(Byte, Byte)
>>> d.build([1,2,3])
b'\x03\x01\x02\x03'


Check
-----

When fields are expected to be coherent in some way but integrity cannot be checked easily using Const or otherwise, then a Check field can be put in place that will compute from the context if the integrity is preserved. For example, maybe there is a count field (implied being non-negative but the field is signed):

>>>> st = Struct(num=Int8sb, integrity1=Check(this.num > 0))
>>>> st.parse(b"\xff")
ValidationError: check failed during parsing

Or there is a collection and a count provided and the count is expected to match the collection length (which might go out of sync by mistake). Note that Rebuild is more appropriate but the check is also possible:

>>>> st = Struct(count=Byte, items=Byte[this.count])
FieldError: packer '>B' error during building, given value 9090
...
>>>> st = Struct(integrity=Check(this.count == len_(this.items)), count=Byte, items=Byte[this.count])
ValidationError: check failed during building


FocusedSeq
----------

When a sequence is has some fields that could be ommited like Const and Terminated, user can focus on the particular fields that are useful:

>>> d = FocusedSeq("num", Const(b"MZ"), "num"/Byte, Terminated)
>>> d = FocusedSeq(1, Const(b"MZ"), "num"/Byte, Terminated)
...
>>> d.parse(b"MZ\xff")
255
>>> d.build(255)
b'MZ\xff'



Conditional
===========

Union
-----

Treats the same data as multiple constructs (similar to C union statement). When parsing, each subconstruct parses the same data (so you can "look" at the data in multiple views).

>>> Union("raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8]).parse(b"12345678")
Container(raw=b'12345678')(ints=[825373492, 892745528])(shorts=[12594, 13108, 13622, 14136])(chars=[49, 50, 51, 52, 53, 54, 55, 56])

>>> Union("raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8], buildfrom=3).build(dict(chars=range(8)))
b'\x00\x01\x02\x03\x04\x05\x06\x07'
>>> Union("raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8], buildfrom="chars").build(dict(chars=range(8)))
b'\x00\x01\x02\x03\x04\x05\x06\x07'

Note that this syntax works ONLY on python 3.6 and pypy due to unordered keyword arguments:
>>> Union(raw=Bytes(8), ints=Int32ub[2], shorts=Int16ub[4], chars=Byte[8], buildfrom=3)

Select
------

Attempts to parse or build each of the subcons, in order they were provided.

>>> Select(Int32ub, CString(encoding="utf8")).build(1)
b'\x00\x00\x00\x01'
>>> Select(Int32ub, CString(encoding="utf8")).build("Афон")
b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00'

Note that this syntax works ONLY on python 3.6 and pypy due to unordered keyword arguments:
>>> Select(num=Int32ub, text=CString(encoding="utf8"))

Optional
--------

Attempts to parse or build the subconstruct. If it fails during parsing, returns a None. If it fails during building, it puts nothing into the stream.

>>> Optional(Int64ul).parse(b"1234")
>>> Optional(Int64ul).parse(b"12345678")
4050765991979987505

>>> Optional(Int64ul).build(1)
b'\x01\x00\x00\x00\x00\x00\x00\x00'
>>> Optional(Int64ul).build("1")
b''


If
--

Parses or builds the subconstruct only if a certain condition is met. Otherwise, returns a None and puts nothing.

>>> If(this.x > 0, Byte).build(255, dict(x=1))
b'\xff'
>>> If(this.x > 0, Byte).build(255, dict(x=0))
b''


IfThenElse
----------

Branches the construction path based on a given condition. If the condition is met, the ``thensubcon`` is used, otherwise the ``elsesubcon`` is used.

>>> IfThenElse(this.x > 0, VarInt, Byte).build(255, dict(x=1))
b'\xff\x01'
>>> IfThenElse(this.x > 0, VarInt, Byte).build(255, dict(x=0))
b'\xff'

Switch
------

Branches the construction based on a return value from a function. This is a more general version of IfThenElse.

>>> Switch(this.n, { 1:Byte, 2:Int32ub }).build(5, dict(n=1))
b'\x05'
>>> Switch(this.n, { 1:Byte, 2:Int32ub }).build(5, dict(n=2))
b'\x00\x00\x00\x05'



Alignment and Padding
=====================

Aligned
-------

Aligns the subconstruct to a given modulus boundary.

>>> Aligned(4, Int16ub).build(1)
b'\x00\x01\x00\x00'

AlignedStruct
-------------

Automatically aligns all the fields of the Struct to the modulus boundary. It does NOT align entire Struct.

>>> AlignedStruct(4, "a"/Int8ub, "b"/Int16ub).build(dict(a=1,b=5))
b'\x01\x00\x00\x00\x00\x05\x00\x00'

Padding
-------

Adds and removes bytes without returning the to the user. Analog to Padded but does not wrap around another construct.

>>> Padding(4).build(None)
b'\x00\x00\x00\x00'
>>> Padding(4, strict=True).parse(b"****")
construct.core.PaddingError: expected b'\x00\x00\x00\x00', found b'****'

Padded
------

Appends additional null bytes to achieve a fixed length.

>>> Padded(4, Byte).build(255)
b'\xff\x00\x00\x00'



Special Constructs
==================

Those are either used internally or have no practical use. They are referenced just for completeness.

.. autoclass:: construct.Embedded


