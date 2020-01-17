============
Lazy parsing
============

.. warning:: This feature is fully implemented but may not be fully mature.


Lazy
---------------

This wrapper allows you to do lazy parsing of individual fields inside a normal Struct (without using LazyStruct which may not in every scenario). It is also used by KaitaiStruct compiler to emit `instances` because those are not processed greedily, and they may refer to other not yet parsed fields. Those are 2 entirely different applications but semantics are the same.

>>> d = Lazy(Byte)
>>> x = d.parse(b'\x00')
>>> x
<function construct.core.Lazy._parse.<locals>.execute>
>>> x()
0
>>> d.build(0)
b'\x00'
>>> d.build(x)
b'\x00'
>>> d.sizeof()
1


LazyStruct
---------------

Equivalent to :class:`~construct.core.Struct`, but when this class is parsed, most fields are not parsed (they are skipped if their size can be measured by _actualsize or _sizeof method). See its docstring for details.

Fields are parsed depending on some factors:

* Some fields like Int* Float* Bytes(5) Array(5,Byte) Pointer are fixed-size and are therefore skipped. Stream is not read.
* Some fields like Bytes(this.field) are variable-size but their size is known during parsing when there is a corresponding context entry. Those fields are also skipped. Stream is not read.
* Some fields like Prefixed PrefixedArray PascalString are variable-size but their size can be computed by partially reading the stream. Only first few bytes are read (the lengthfield).
* Other fields like VarInt need to be parsed. Stream position that is left after the field was parsed is used.
* Some fields may not work properly, due to the fact that this class attempts to skip fields, and parses them only out of necessity. Miscellaneous fields often have size defined as 0, and fixed sized fields are skippable.

Note there are restrictions:

* If a field like Bytes(this.field) references another field in the same struct, you need to access the referenced field first (to trigger its parsing) and then you can access the Bytes field. Otherwise it would fail due to missing context entry.
* If a field references another field within inner (nested) or outer (super) struct, things may break. Context is nested, but this class was not rigorously tested in that manner.

Building and sizeof are greedy, like in Struct.


LazyArray
---------------

Equivalent to :class:`~construct.core.Array`, but the subcon is not parsed when possible (it gets skipped if the size can be measured by _actualsize or _sizeof method). See its docstring for details. The restrictions are identical as in LazyStruct.


LazyBound
---------------

Field that binds to the subcon only at runtime (during parsing and building, not ctor). Useful for recursive data structures, like linked-lists and trees, where a construct needs to refer to itself (while it does not exist yet in the namespace).

Note that it is possible to obtain same effect without using this class, using a loop. However there are usecases where that is not possible (if remaining nodes cannot be sized-up, and there is data following the recursive structure). There is also a significant difference, namely that LazyBound actually does greedy parsing while the loop does lazy parsing. See examples.

To break recursion, use `If` field. See examples.

::

    d = Struct(
        "value" / Byte,
        "next" / If(this.value > 0, LazyBound(lambda: d)),
    )

    >>> print(d.parse(b"\x05\x09\x00"))
    Container: 
        value = 5
        next = Container: 
            value = 9
            next = Container: 
                value = 0
                next = None

::

    d = Struct(
        "value" / Byte,
        "next" / GreedyBytes,
    )

    data = b"\x05\x09\x00"
    while data:
        x = d.parse(data)
        data = x.next
        print(x)

    # print outputs
    Container: 
        value = 5
        next = \t\x00 (total 2)
    # print outputs
    Container: 
        value = 9
        next = \x00 (total 1)
    # print outputs
    Container: 
        value = 0
        next =  (total 0)
