============
Lazy parsing
============


LazyField
--------

There is a different approach to lazy parsing, where only one field is made lazy. Parsing returns a parameterless lambda that when called, returns the parsed data. Right now, each time the lambda is called the object is parsed again, so if the inner subcon is non-deterministic, each parsing may return a different object. Builds from a parsed object or a lambda.

>>> LazyField(Byte).parse(b"\xff")
<function LazyField._parse.<locals>.<lambda> at 0x7fdc241cfc80>
>>> _()
255
>>> LazyField(Byte).build(16)
b'\x10'


LazyBound
---------

A lazy-bound construct that binds to the construct only at runtime. Useful for recursive data structures (like linked lists or trees), where a construct needs to refer to itself (while it doesn't exist yet).

>>> st = Struct(
...     "value"/Byte,
...     "next"/If(this.value > 0, LazyBound(lambda ctx: st)),
... )
...
>>> st.parse(b"\x05\x09\x00")
Container(value=5)(next=Container(value=9)(next=Container(value=0)(next=None)))
...
>>> print(st.parse(b"\x05\x09\x00"))
Container: 
    value = 5
    next = Container: 
        value = 9
        next = Container: 
            value = 0
            next = None
