===================
Debugging Construct
===================

Programming data structures in Construct is much easier than writing the equivalent procedural code, both in terms of RAD and correctness. However, sometimes things don't behave the way you expect them to. Yep, a bug.

Most end-user bugs originate from handling the context wrong. Sometimes you forget what nesting level you are at, or you move things around without taking into account the nesting, thus breaking context-based expressions. The two utilities described below should help you out.

Probe
=====

The Probe simply dumps information to the screen. It will help you inspect the context tree, the stream, and partially constructed objects, so you can understand your problem better. It has the same interface as any other field, and you can just stick it into a Struct, near the place you wish to inspect. Do note that the printout happens during the construction, before the final object is ready.

::

    >>> Struct("count"/Byte, "items"/Byte[this.count], Probe()).parse(b"\x05abcde")
    ================================================================================
    Probe <unnamed 3>
    path is parsing, func is None
    EOF reached
    Container: 
        count = 5
        items = ListContainer: 
            97
            98
            99
            100
            101
    ================================================================================
    Container(count=5)(items=[97, 98, 99, 100, 101])

    >>> (Byte >> Probe()).parse(b"?")
    ================================================================================
    Probe <unnamed 1>
    path is parsing, func is None
    EOF reached
    Container: 
        0 = 63
    ================================================================================
    [63, None]

There is also `ProbeInto` looks inside the context and extracts a part of it using a lambda instead of printing the entire context.

>>> st = "junk"/RepeatUntil(obj_ == 0,Byte) + "num"/Byte + Probe()
>>> st.parse(b"xcnzxmbjskahuiwerhquiehnsdjk\x00\xff")
================================================================================
Probe <unnamed 5>
path is parsing, func is None
EOF reached
Container: 
    junk = ListContainer: 
        120
        99
        110
        122
        120
        109
        98
        106
        115
        107
        97
        104
        117
        105
        119
        101
        114
        104
        113
        117
        105
        101
        104
        110
        115
        100
        106
        107
        0
    num = 255
================================================================================
Container(junk=[120, 99, 110, 122, 120, 109, 98, 106, 115, 107, 97, 104, 117, 105, 119, 101, 114, 104, 113, 117, 105, 101, 104, 110, 115, 100, 106, 107, 0])(num=255)

>>> st = "junk"/RepeatUntil(obj_ == 0,Byte) + "num"/Byte + ProbeInto(this.num)
>>> st.parse(b"xcnzxmbjskahuiwerhquiehnsdjk\x00\xff")
================================================================================
Probe <unnamed 6>
path is parsing, func is this.num
EOF reached
255
================================================================================
Container(junk=[120, 99, 110, 122, 120, 109, 98, 106, 115, 107, 97, 104, 117, 105, 119, 101, 114, 104, 113, 117, 105, 101, 104, 110, 115, 100, 106, 107, 0])(num=255)


Debugger
========

The Debugger is a pdb-based full python debugger. Unlike Probe, Debugger is a subconstruct (it wraps an inner construct), so you simply put it around the problematic construct. If no exception occurs, the return value is passed right through. Otherwise, an interactive debugger pops, letting you tweak around.

When an exception occurs while parsing, you can go up (using u) to the level of the debugger and set self.retval to the desired return value. This allows you to hot-fix the error. Then use q to quit the debugger prompt and resume normal execution with the fixed value. However, if you don't set self.retval, the exception will propagate up.

::

    >>> Debugger(Byte[3]).build([])
    ================================================================================
    Debugging exception of <Range: None>:
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/debug.py", line 116, in _build
        obj.stack.append(a)
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 1069, in _build
        raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
    construct.core.RangeError: expected from 3 to 3 elements, found 0

    > /home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py(1069)_build()
    -> raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
    (Pdb) 
    ================================================================================

    >>> format = Struct(
    ...     "spam" / Debugger(Enum(Byte, A=1,B=2,C=3)),
    ... )
    >>> format.parse(b"\xff")
    ================================================================================
    Debugging exception of <Mapping: None>:
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 2578, in _decode
        return self.decoding[obj]
    KeyError: 255

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/debug.py", line 127, in _parse
        return self.subcon._parse(stream, context)
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 308, in _parse
        return self._decode(self.subcon._parse(stream, context), context)
      File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 2583, in _decode
        raise MappingError("no decoding mapping for %r" % (obj,))
    construct.core.MappingError: no decoding mapping for 255

    (you can set the value of 'self.retval', which will be returned)
    > /home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py(2583)_decode()
    -> raise MappingError("no decoding mapping for %r" % (obj,))
    (Pdb) self.retval = "???"
    (Pdb) q

Error
=====

Raises an exception when triggered by parse or build. Can be used as a sentinel that blows a whistle when a conditional branch goes the wrong way, or to raise an error explicitly the declarative way.

>>> d = "x"/Int8sb >> IfThenElse(this.x > 0, Int8sb, Error)
>>> d.parse(b"\xff\x05")
construct.core.ExplicitError: Error field was activated during parsing


