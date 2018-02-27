===================
Debugging Construct
===================


Programming data structures in Construct is much easier than writing the equivalent procedural code, both in terms of ease-of-use and correctness. However, sometimes things don't behave the way you expect them to. Yep, a bug.

Most end-user bugs originate from handling the context wrong. Sometimes you forget what nesting level you are at, or you move things around without taking into account the nesting, thus breaking context-based expressions. The two utilities described below should help you out.


Probe
=============

The Probe simply dumps information to the screen. It will help you inspect the context tree, the stream, and partially constructed objects, so you can understand your problem better. It has the same interface as any other field, and you can just stick it into a Struct, near the place you wish to inspect. Do note that the printout happens during the construction, before the final object is ready.

::

    >>> d = Struct(
    ...     "count" / Byte,
    ...     "items" / Byte[this.count],
    ...     Probe(lookahead=32),
    ... )
    >>> d.parse(b"\x05abcde\x01\x02\x03")

    --------------------------------------------------
    Probe, path is (parsing), into is None
    Stream peek: (hexlified) b'010203'...
    Container: 
        count = 5
        items = ListContainer: 
            97
            98
            99
            100
            101
    --------------------------------------------------

There is also feature that looks inside the context and extracts a part of it using a lambda instead of printing the entire context.

::

    >>> d = Struct(
    ...     "count" / Byte,
    ...     "items" / Byte[this.count],
    ...     Probe(this.count),
    ... )
    >>> d.parse(b"\x05abcde\x01\x02\x03")

    --------------------------------------------------
    Probe, path is (parsing), into is this.count
    5
    --------------------------------------------------


Debugger
=============

The Debugger is a pdb-based full python debugger. Unlike Probe, Debugger is a subconstruct (it wraps an inner construct), so you simply put it around the problematic construct. If no exception occurs, the return value is passed right through. Otherwise, an interactive debugger pops, letting you tweak around.

When an exception occurs while parsing, you can go up (using u) to the level of the debugger and set self.retval to the desired return value. This allows you to hot-fix the error. Then use q to quit the debugger prompt and resume normal execution with the fixed value. However, if you don't set self.retval, the exception will propagate up.


::

    >>> Debugger(Byte[3]).build([])

    --------------------------------------------------
    Debugging exception of <Array: None>
    path is (building)
      File "/media/arkadiusz/MAIN/GitHub/construct/construct/debug.py", line 192, in _build
        return self.subcon._build(obj, stream, context, path)
      File "/media/arkadiusz/MAIN/GitHub/construct/construct/core.py", line 2149, in _build
        raise RangeError("expected %d elements, found %d" % (count, len(obj)))
    construct.core.RangeError: expected 3 elements, found 0

    > /media/arkadiusz/MAIN/GitHub/construct/construct/core.py(2149)_build()
    -> raise RangeError("expected %d elements, found %d" % (count, len(obj)))
    (Pdb) q
    --------------------------------------------------
