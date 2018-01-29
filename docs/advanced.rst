============
The Basics, part 2
============


Integers and floats
===================

Basic computer science 101. All integers follow the Int{8,16,24,32,64}{u,s}{b,l,n} and floats follow the Float{32,64}{b,l} naming patterns. Endianness can be either big-endian, little-endian or native. Integers can be signed or unsigned (non-negative only). Floats do not have a unsigned type.

>>> Int64sl.build(500)
b'\xf4\x01\x00\x00\x00\x00\x00\x00'
>>> Int64sl.build(-23)
b'\xe9\xff\xff\xff\xff\xff\xff\xff'

Few fields have aliases, Byte among integers and Single among floats.

::

    Byte    <-->  Int8ub
    Short   <-->  Int16ub
    Int     <-->  Int32ub
    Long    <-->  Int64ub
    Single  <-->  Float32b
    Double  <-->  Float64b

Integers can also be variable-length encoded for compactness. Google invented a popular encoding:

>>> VarInt.build(1234567890)
b'\xd2\x85\xd8\xcc\x04'

Long integers (or those of particularly odd sizes) can be encoded using a fixed-sized `BytesInteger`. Here is a 128-bit integer.

>>> BytesInteger(16).build(255)
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff'

Some numerical classes are implemented using `struct` module, others use BytesInteger field.

>>> FormatField("<","l").build(1)
b'\x01\x00\x00\x00'
>>> BytesInteger(4, swapped=True).build(1)
b'\x01\x00\x00\x00'



Bytes and bits
==============

"Strings" of bytes (`str` in PY2 and `bytes` in PY3) can be moved around as-is. Bits are discussed in a later chapter.

>>> Bytes(5).build(b"12345")
b'12345'
>>> Bytes(5).parse(b"12345")
b'12345'

Bytes can also be consumed until end of stream. Tunneling is discussed in a later chapter.

>>> GreedyBytes.parse(b"39217839219...")
b'39217839219...'


Strings
========

.. warning::

    Python 3 known problem:

    Unprefixed string literals like "data" are on Python 3 interpreted as unicode (not bytes). If you look at the documentation on this site, you will notice that most examples use b"\\x00" literals (so called b-strings). Unicode strings are processed by String* classes, and require explicit encoding like "utf8".

.. warning:: Encoding needs to be specified explicitly, however if you specify None instead of "utf8", those constructs work on byte strings (not unicode), similar to Bytes and GreedyBytes fields.

.. note:: Encoding can be set once, globally using :func:`~construct.core.setglobalstringencoding` or provided with each field separately.

.. warning:: Do not use >1 byte encodings like UTF16 or UTF32 with String and CString classes. This a known bug that has something to do with the fact that library inherently works with bytes (not codepoints) and codepoint-to-byte conversions are too tricky.

.. note:: Encodings like UTF16 or UTF32 work fine with PascalString and GreedyString.

String is a fixed-length construct that pads builded string with null bytes, and strips those same null bytes when parsing. Note that some encodings do not work properly because they return null bytes within the encoded stream, utf-16 and utf-32 for example.

>>> String(10).build(b"hello")
b'hello\x00\x00\x00\x00\x00'

>>> String(10, encoding="utf8").build("Афон")
b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00\x00'

You can use different bytes for padding (although they will break any encoding using those within the stream). Strings can also be trimmed when building. If you supply a too long string, the construct will chop it off apart instead of raising a StringError.

To be honest, using this class is not recommended. There are safer ways to handle variable length strings.

>>> String(10, padchar=b"XYZ", paddir="center").build(b"abc")
b'XXXabcXXXX'

>>> String(10, trimdir="right").build(b"12345678901234567890")
b'1234567890'

PascalString is a variable length string that is prefixed by a length field. This scheme was invented in Pascal language that put Byte field instead of C convention of appending null \\0 byte at the end. Note that the length field can be variable length itself, as shown below. VarInt should be preferred when building new protocols.

>>> PascalString(VarInt, encoding="utf8").build("Афон")
b'\x08\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd'

CString is an another variable length string, that always ends with a null \\0 terminating byte at the end. This scheme was invented in C language and is known in the computer science community very well. One of the authors, Kernighan or Ritchie, admitted that it was one of the most regretable design decisions in history.

>>> CString(encoding="utf8").build(b"hello")
b'hello\x00'

Last but not least, GreedyString does the same thing as GreedyBytes. It reads until the end of stream and then decodes it using the specified encoding. Tunneling is discussed later.

>>> GreedyString(encoding="utf8").parse(b"329817392189")
'329817392189'


Mappings
==========

Booleans are flags:

>>> Flag.parse(b"\x01")
True

Enums translate between string names and usually integer values:

>>> Enum(Byte, g=8, h=11).parse(b"\x08")
'g'
>>> Enum(Byte, g=8, h=11).build(11)
b'\x0b'

FlagsEnum decomposes an integer value into a set of string labels:

>>> FlagsEnum(Byte, a=1, b=2, c=4, d=8).parse(b"\x03")
Container(c=False)(b=True)(a=True)(d=False)


Processing files (or data)
===========================

.. warning::

    Python 3 known problem:

    Opening a file without mode like ``open(filename)`` implies text mode, which cannot be parsed or build.

Constructs can parse both in-memory data (bytes) and binary files:

>>> d = Struct(...)
>>> d.parse(bytes(1000))

>>> with open('/dev/zero', 'rb') as f:
...     d.parse_stream(f)
