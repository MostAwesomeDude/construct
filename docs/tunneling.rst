=================
Tunneling tactics
=================


Obtaining raw bytes
-------------------

When some value needs to be processed as both a parsed object and its raw bytes representation, both of these can be obtained using RawCopy. You can build from either the object or raw bytes as well. Dict also happen to contain the stream offsets, if you need to know at which position it resides in the stream or if you need to know its size in bytes.

>>> RawCopy(Byte).parse(b"\xff")
Container(data=b'\xff')(value=255)(offset1=0)(offset2=1)(length=1)
>>> RawCopy(Byte).build(dict(data=b"\xff"))
b'\xff'
>>> RawCopy(Byte).build(dict(value=255))
b'\xff'


Endianness
----------

When little endianness is needed, either use integer fields like `Int*l` or `BytesInteger(swapped=True)` or swap bytes of an arbitrary field:

::

    Int24ul <--> ByteSwapped(Int24ub) <--> BytesInteger(3, swapped=True) <--> ByteSwapped(BytesInteger(3))

>>> Int24ul.build(0x010203)
b'\x03\x02\x01'

When bits within each byte need to be swapped, there is another wrapper:

>>> Bitwise(Bytes(8)).parse(b"\x01")
b'\x00\x00\x00\x00\x00\x00\x00\x01'
>>> BitsSwapped(Bitwise(Bytes(8))).parse(b"\x01")
b'\x01\x00\x00\x00\x00\x00\x00\x00'


Working with bytes subsets
--------------------------------------------

Greedy* constructs consume as much data as possible. This is convenient when building from a list of unknown length but becomes a problem when parsing it back and the list needs to be separated from following data. This can be achieved either by prepending an element count (see PrefixedArray) or by prepending a byte count (see Prefixed):

>>> Prefixed(VarInt, GreedyRange(Int32ul)).parse(b"\x08abcdefgh")
[1684234849, 1751606885]

>>> PrefixedArray(VarInt, Int32ul).parse(b"\x02abcdefgh")
[1684234849, 1751606885]

VarInt encoding is recommended because it is both compact and never overflows. Also and optionally, the length field can include its own size. If so, length field must be of fixed size.


Working with different bytes
--------------------------------------------------

RestreamData allows you to insert a field that parses some data that came either from some other field, from the context (like Bytes) or some literal hardcoded value in your code. Comes handy when for example, you are testing a large struct by parsing null bytes, but some field is unable to parse null bytes (like Numpy). It substitutes the stream with another data for the purposes of parsing a particular field in a Struct (or Sequence for that matter).

::

    >>> d = RestreamData(b"\xff", Byte)
    >>> d.parse(b"")
    255
    >>> d.build(0)
    b''

::

    d = Struct(
        ...,
        "numpy_data" / Computed(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"),
        "numpy1" / RestreamData(this.numpy_data, Numpy),
        ...,
    )
    d.parse(bytes(1000))


TransformData allows you to process data before it gets into subcon (and after data left it) using simple bytes-to-bytes transformations. In fact, all core classes (like Bitwise) that use Restreamed also use TransformData. The only difference is that TransformData prefetches all bytes and transforms them in advance, but Restreamed fetches a unit at a time (few bytes usually). For example:

::

    >>> d = TransformData(Bytes(16), bytes2bits, 2, bits2bytes, 16//8)
    >>> d.parse(b"\x00\x00")
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

::

    # Bitwise implementation
    try:
        size = subcon.sizeof()
        macro = TransformData(subcon, bytes2bits, size//8, bits2bytes, size//8)
    except SizeofError:
        macro = Restreamed(subcon, bytes2bits, 1, bits2bytes, 8, lambda n: n//8)


Compression and checksuming
----------------------------------------

Data can be easily checksummed. Note that checksum field does not need to be Bytes, and lambda may return an integer or otherwise.

::

    import hashlib
    d = Struct(
        "fields" / RawCopy(Struct(
            Padding(1000),
        )),
        "checksum" / Checksum(Bytes(64),
            lambda data: hashlib.sha512(data).digest(),
            this.fields.data),
    )
    d.build(dict(fields=dict(value={})))

::

    import hashlib
    d = Struct(
        "offset" / Tell,
        "checksum" / Padding(64),
        "fields" / RawCopy(Struct(
            Padding(1000),
        )),
        "checksum" / Pointer(this.offset, Checksum(Bytes(64),
            lambda data: hashlib.sha512(data).digest(),
            this.fields.data)),
    )
    d.build(dict(fields=dict(value={})))


Data can also be easily compressed. Supported encodings include zlib/gzip/bzip2/lzma and entire codecs module. When parsing, entire stream is consumed. When building, puts compressed bytes without marking the end. This construct should be used with :class:`~construct.core.Prefixed` or entire stream.

>>> d = Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
>>> d.build(bytes(100))
b'\x0cx\x9cc`\xa0=\x00\x00\x00d\x00\x01'
