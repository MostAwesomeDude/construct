============
The Advanced
============


Integers and floats
===================

Basic computer science 101. All integers follow Int{8,16,24,32,64}{u,s}{b,l,n} and floats follow Float{32,64}{b,l} a naming pattern. Endianness can be either big-endian, little-endian or native. Integers can be signed or unsigned (non-negative only). Floats do not have a native endianness nor unsigned type.

>>> Int64sl.build(500)
b'\xf4\x01\x00\x00\x00\x00\x00\x00'
>>> Int64sl.build(-23)
b'\xe9\xff\xff\xff\xff\xff\xff\xff'

Few fields have aliases, Byte among integers and Single/Double among floats.

>>> Byte.build(57)
b'9'
>>> Int8ul.parse(_)
57
>>> Float32b.build(123.456)
b'B\xf6\xe9y'
>>> Single.parse(_)
123.45600128173828

Integers can also be variable-length encoded for compactness. Google invented a popular encoding:

>>> VarInt.build(1234567890)
b'\xd2\x85\xd8\xcc\x04'

Long integers (or those of particularly odd sizes) can be encoded using a variable-length `VarInt` or fixed-sized `BytesInteger`. Here is a 128-bit integer.

>>> BytesInteger(16).build(255)
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff'



Bytes and bits
==============

"Strings" of bytes (`str` in PY2 and `bytes` in PY3) can be moved around as-is. Bits are discussed in a later chapter.

>>> Bytes(5).build(b"12345")
b'12345'
>>> Bytes(5).parse(b"12345")
b'12345'

Bytes can also be consumed until end of stream.

>>> GreedyBytes.parse(b"39217839219...")
b'39217839219...'


Strings
========

Strings in Construct work very much like strings in other languages.

<<< put examples, not auto>>>


Other short fields
===================

>>> Flag.parse(b"\x01")
True

>>> Enum(Byte, g=8, h=11).parse(b"\x08")
'g'
>>> Enum(Byte, g=8, h=11).build(11)
b'\x0b'

>>> FlagsEnum(Byte, a=1, b=2, c=4, d=8).parse(b"\x03")
Container(c=False)(b=True)(a=True)(d=False)


