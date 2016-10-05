=================
Tunneling tactics
=================

Obtaining raw bytes as well
---------------------------

When some value needs to be processed as both a parsed object and raw bytes, both of these can be obtained using RawCopy. You can build from either the object or raw bytes as well.

>>> RawCopy(Byte).parse(b"\xff")
Container(data='\xff')(value=255)(offset1=0L)(offset2=1L)(length=1L)
...
>>> RawCopy(Byte).build(dict(data=b"\xff"))
'\xff'
>>> RawCopy(Byte).build(dict(value=255))
'\xff'

Endianness
----------

When little endianness is needed, either use fields like Int*l or swap bytes of an arbitrary field:

::

    Int24ul <--> ByteSwapped(Int24ub)

>>> ByteSwapped(Int32ub).build(0x01020304)
'\x04\x03\x02\x01'

When bits within each byte need to be swapped, there is another wrapper:

>>> Bitwise(Bytes(8)).parse(b"\x01")
'\x00\x00\x00\x00\x00\x00\x00\x01'
>>> BitsSwapped(Bitwise(Bytes(8))).parse(b"\x01")
'\x01\x00\x00\x00\x00\x00\x00\x00'

Working with bytes subsets
--------------------------

Greedy* constructs consume as much data as possible. This is convenient when building from a list of unknown length but becomes a problem when parsing it back and the list needs to be separated from following data. This can be achieved either by prepending a count (see PrefixedArray) or by prepending a byte count:

>>> Prefixed(VarInt, GreedyBytes).parse(b"\x05hello????remainins")
b'hello'
...
>>> Prefixed(VarInt, Byte[:]).parse(b"\x03\x01\x02\x03following")
[1, 2, 3]

Note that VarInt encoding should be preferred because it is both compact and never overflows.

Working with compression and checksuming
----------------------------------------

Data can be checksummed easily:

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

and can also be compressed easily:

::

    Compressed(GreedyBytes, "zlib")
    ...
    Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
    Struct("inner"/above)
    ...
    Compressed(Struct(...), "zlib")


