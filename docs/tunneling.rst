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

When little endianness is needed, either use fields like ``Int*l`` or swap bytes of an arbitrary field:

::

    Int24ul <--> ByteSwapped(Int24ub) <--> BytesInteger(3, swapped=True)

>>> Int24ul.build(0x010203)
b'\x03\x02\x01'

When bits within each byte need to be swapped, there is another wrapper:

>>> Bitwise(Bytes(8)).parse(b"\x01")
b'\x00\x00\x00\x00\x00\x00\x00\x01'
>>> BitsSwapped(Bitwise(Bytes(8))).parse(b"\x01")
b'\x01\x00\x00\x00\x00\x00\x00\x00'


Working with bytes subsets (or substreams)
--------------------------------------------

Greedy* constructs consume as much data as possible. This is convenient when building from a list of unknown length but becomes a problem when parsing it back and the list needs to be separated from following data. This can be achieved either by prepending an element count (see PrefixedArray) or by prepending a byte count (see Prefixed):

>>> Prefixed(VarInt, GreedyRange(Int32ul)).parse(b"\x08abcdefgh")
[1684234849, 1751606885]

>>> PrefixedArray(VarInt, Int32ul).parse(b"\x02abcdefgh")
[1684234849, 1751606885]

VarInt encoding is recommended because it is both compact and never overflows. Also and optionally, the length field can include its own size. If so, length field must be of fixed size.


Working with different bytes (outside of stream)
--------------------------------------------------

RestreamData allows you to insert a field that parses some data that came either from some other field, from the context (like Bytes) or some literal hardcoded value in your code. Comes handy when for example, you are testing a large struct by parsing null bytes, but some field is unable to parse null bytes (like Numpy). It substitutes the stream with another data for the purposes of parsing a particular field in a Struct (or Sequence for that matter).

::

    d = Struct(
        ...,
        "numpy_data" / Computed(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"),
        "numpy1" / RestreamData(this.numpy_data, Numpy),
        ...,
    )
    d.parse(bytes(1000))


Compression and checksuming
----------------------------------------

Data can be easily checksummed. Note that checksum field does not need to be Bytes, and lambda may return an integer or otherwise.

::

    import hashlib
    d = Struct(
        "fields" / RawCopy(Struct(
            "a" / Byte,
            "b" / Byte,
        )),
        "checksum" / Checksum(Bytes(64), lambda data: hashlib.sha512(data).digest(), this.fields.data),
    )
    data = d.build(dict(fields=dict(value=dict(a=1,b=2))))
    # returned b'\x01\x02\xbd\xd8\x1a\xb23\xbc\xebj\xd23\xcd\x18qP\x93 \xa1\x8d\x035\xa8\x91\xcf\x98s\t\x90\xe8\x92>\x1d\xda\x04\xf35\x8e\x9c~\x1c=\x16\xb1o@\x8c\xfa\xfbj\xf52T\xef0#\xed$6S8\x08\xb6\xca\x993'

Also data can be easily compressed. Supported encodings include zlib/gzip/bzip2/lzma and entire codecs module. When parsing, entire stream is consumed. When building, puts compressed bytes without marking the end. This construct should be used with :func:`~construct.core.Prefixed` or entire stream.

>>> d = Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
>>> d.build(bytes(100))
b'\x0cx\x9cc`\xa0=\x00\x00\x00d\x00\x01'
