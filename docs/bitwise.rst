======================
The Bit/Byte Duality
======================


History
=======

In Construct 1.XX, parsing and building were performed at the bit level: the entire data was converted to a string of 1's and 0's, so you could really work with bit fields. Every construct worked with bits, except some (which were named ByteXXX) that worked on whole octets. This made it very easy to work with single bits, such as the flags of the TCP header, 7-bit ASCII characters, or fields that were not aligned to the byte boundary (nibbles et al).

This approach was easy and flexible, but had two main drawbacks:

* Most data is byte-aligned (with very few exceptions)
* The overhead was too big

Since constructs worked on bits, the data had to be first converted to a bit-string, which meant you had to hold the entire data set in memory. Not only that, but you actually held 8 times the size of the original data (it was a bit-string). According to some tests I made, you were limited to files of about 50MB (and that was slow due to page-thrashing).

So as of Construct 2.XX, all constructs work with bytes:

* Less memory consumption
* No unnecessary bytes-to-bits and bits-to-bytes coversions
* Can rely on python's built in struct module for numeric packing/unpacking (faster and tested)
* Can directly parse from and build to file-like objects (without in-memory buffering)

But how are we supposed to work with raw bits? The only difference is that we must explicitly declare that: certain fields like BitsInteger (Bit Nibble Octet are instances of BitsInteger) handle parsing and building of bit strings. There are also few fields like Struct and Flag that work with both byte-strings and bit-strings.


BitStruct
=========

A BitStruct is a sequence of constructs that are parsed/built in the specified order, much like normal Structs. The difference is that BitStruct operates on bits rather than bytes. When parsing a BitStruct, the data is first converted to a bit stream (a stream of \\x01 and \\x00), and only then is it fed to the subconstructs. The subconstructs are expected to operate on bits instead of bytes. For reference look at the code below:

>>> format = BitStruct(
...     "a" / Flag,
...     "b" / Nibble,
...     "c" / BitsInteger(10),
...     "d" / Padding(1),
... )
>>> format.parse(b"\xbe\xef")
Container(a=True)(b=7)(c=887)(d=None)
>>> format.sizeof()
2

BitStruct is actually just a wrapper for the :class:`~construct.core.Bitwise` around a :class:`~construct.core.Struct` .


Important notes
===============

* BitStructs are non-nestable (because Bitwise are not nestable) so writing something like ``BitStruct(BitStruct(Octet))`` will not work. You can use regular Structs inside BitStructs.
* Byte aligned - The total size of the elements of a BitStruct must be a multiple of 8 (due to alignment issues). RestreamedBytesIO will raise an error if the amount of bits and bytes does not align properly.
* Pointers and Lazy* - Do not place fields that do seeking/telling or lazy parsing inside bitwise because it uses an internal stream, so external stream offsets will turn out wrong, have unknown side-effects or raise exceptions.
* Normal (byte-oriented) classes like Int* Float* can be used by wrapping in Bytewise. If you need to mix byte- and bit-oriented fields, you should use a BitStruct and Bytewise.
* Advanced classes like tunneling may not work in bitwise context. Only basic fields like integers were throughly tested.


Fields that work with bits
=============================

::

    Bit    <--> BitsInteger(1)
    Nibble <--> BitsInteger(4)
    Octet  <--> BitsInteger(8)


Fields that work with bytes
=============================

Normal classes, that is those working with byte-streams, can be used on bit-streams by wrapping them with Bytewise. Its a wrapper that does the opposite of Bitwise, it transforms each 8 bits into 1 byte. The enclosing stream is a bit-stream but the subcon is provided a byte-stream.

::

    >>> d = Bitwise(Struct(
    ...     'a' / Nibble,
    ...     'b' / Bytewise(Float32b),
    ...     'c' / Padding(4),
    ... ))
    >>> d.parse(bytes(5))
    Container(a=0)(b=0.0)(c=None)
    >>> d.sizeof()
    5


Fields that do both
=============================

Some simple fields (such as Flag Padding Pass Terminated) are ignorant to the granularity of the data they operate on. The actual granularity depends on the enclosing layers. Same applies to classes that are wrappers or adapters like Enum EnumFlags. Those classes do not care about granularity because they dont interact with the stream, its their subcons.

Here's a snippet of a code that operates on bytes:

>>> format = Struct(
...     Padding(2),
...     "x" / Flag,
...     Padding(5),
... )
>>> format.build(dict(x=5))
b'\x00\x00\x01\x00\x00\x00\x00\x00'

And here's a snippet of a code that operates on bits. The only difference is BitStruct in place of a normal Struct:

>>> format = BitStruct(
...     Padding(2),
...     "x" / Flag,
...     Padding(5),
... )
>>> format.build(dict(x=5))
b' '

So unlike "classical Construct", there's no need for BytePadding and BitPadding. If Padding is enclosed by a BitStruct, it operates on bits, otherwise, it operates on bytes.
