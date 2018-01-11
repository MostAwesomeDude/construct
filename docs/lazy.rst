============
Lazy parsing
============

.. warning::

    Struct members that depend on earlier context entries (meta-constructs) do not work properly, because since Struct is lazy, there is no guarantee that previous members were parsed and put into context dictionary.

Structs Sequences and Ranges
----------------------------

Lazy* constructs allow lazy deconstruction, meaning each member gets parsed only when resulting Container gets accessed (LazyStruct parsing only prepares a Container, it does not parse the members). Each member can be parsed only once, then it gets cached.

Essentially almost every code that uses the base classes also works on these but there are few things that one has to be aware of when using lazy equivalents.

`LazyStruct` works like Struct but parses into a LazyContainer.

    Equivalent to Struct construct, however fixed size members are parsed on demand, others are parsed immediately. If entire struct is fixed size then entire parse is essentially one seek.

`LazySequence` works like Sequence but parses into a LazySequenceContainer.

    Equivalent to Sequence construct, however fixed size members are parsed on demand, others are parsed immediately. If entire sequence is fixed size then entire parse is essentially one seek.

`LazyRange` works like Range but parses into a LazyRangeContainer.

    Equivalent to Range construct, but members are parsed on demand. Works only with fixed size subcon. Entire parse is essentially one seek.


OnDemand
--------

There is a different approach to lazy parsing, where only one field is made lazy. Parsing returns a parameterless lambda that when called, returns the parsed data. Right now, each time the lambda is called the object is parsed again, so if the inner subcon is non-deterministic, each parsing may return a different object. Builds from a parsed object or a lambda.

>>> OnDemand(Byte).parse(b"\xff")
<function OnDemand._parse.<locals>.<lambda> at 0x7fdc241cfc80>
>>> _()
255
>>> OnDemand(Byte).build(16)
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

