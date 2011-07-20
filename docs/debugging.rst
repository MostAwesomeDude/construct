===================
Debugging Construct
===================

Intro
=====

Programming data structures in Construct is much easier than writing the
equivalent procedural code, both in terms of RAD and correctness. However,
sometimes things don't behave the way you expect them to. Yep, a bug.

Most end-user bugs originate from handling the context wrong. Sometimes you
forget what nesting level you are at, or you move things around without taking
into account the nesting, thus breaking context-based expressions. The two
utilities described below should help you out.

Probe
=====

The Probe simply dumps information to the screen. It will help you inspect the
context tree, the stream, and partially constructed objects, so you can
understand your problem better. It has the same interface as any other field,
and you can just stick it into a Struct, near the place you wish to inspect.
Do note that the printout happens during the construction, before the final
object is ready.

>>> foo = Struct("foo",
...     UBInt8("bar"),
...     Probe(),
...     UBInt8("baz"),
... )
>>> foo.parse("spam spam spam spam bacon and eggs")
Probe <unnamed 1>
Container:
    stream_position = 1
    following_stream_data =
        0000   70 61 6d 20 73 70 61 6d 20 73 70 61 6d 20 73 70   pam spam spam
sp
        0010   61 6d 20 62 61 63 6f 6e 20 61 6e 64 20 65 67 67   am bacon and
egg
        0020   73                                                s
    context = {
        '_' : {}
        'bar' : 115
    }
    stack = [
        {
            'data' : 'spam spam spam spam bacon and eggs'
            'self' : Struct('foo')
        }
        {
            'self' : Struct('foo')
            'stream' : <cStringIO.StringI object at 0x0097A230>
        }
        {
            'context' : {
                '_' : {}
                'bar' : 115
            }
            'obj' : Container:
                bar = 115
            'sc' : Probe('<unnamed 1>')
            'self' : Struct('foo')
            'stream' : <cStringIO.StringI object at 0x0097A230>
            'subobj' : 115
        }
        {
            'context' : {
                '_' : {}
                'bar' : 115
            }
            'self' : Probe('<unnamed 1>')
            'stream' : <cStringIO.StringI object at 0x0097A230>
        }
    ]
Container(bar = 115, baz = 112)


Debugger
========

The Debugger is a pdb-based full python debugger. Unlike Probe, Debugger is a
subconstruct (it wraps an inner construct), so you simply put it around the
problematic construct. If no exception occurs, the return value is passed
right through. Otherwise, an interactive debugger pops, letting you tweak
around.

When an exception occurs while parsing, you can go up (using u) to the level
of the debugger and set self.retval to the desired return value. This allows
you to hot-fix the error. Then use q to quit the debugger prompt and resume
normal execution with the fixed value. However, if you don't set self.retval,
the exception will propagate up.

::

    >>> foo = Struct("foo",
    ...     UBInt8("bar"),
    ...     Debugger(
    ...         Enum(UBInt8("spam"),
    ...             ABC = 1,
    ...             DEF = 2,
    ...             GHI = 3,
    ...         )
    ...     ),
    ...     UBInt8("eggs"),
    ... )
    >>>
    >>>
    >>> print foo.parse("\x01\x02\x03")
    Container:
        bar = 1
        spam = 'DEF'
        eggs = 3
    >>>
    >>> print foo.parse("\x01\x04\x03")
    Debugging exception of MappingAdapter('spam'):
      File "d:\projects\construct\debug.py", line 112, in _parse
        return self.subcon._parse(stream, context)
      File "d:\projects\construct\core.py", line 174, in _parse
        return self._decode(self.subcon._parse(stream, context), context)
      File "d:\projects\construct\adapters.py", line 77, in _decode
        raise MappingError("no decoding mapping for %r"  % (obj,))
    MappingError: no decoding mapping for 4

    (you can set the value of 'self.retval', which will be returned)
    > d:\projects\construct\adapters.py(77)_decode()
    -> raise MappingError("no decoding mapping for %r"  % (obj,))
    (Pdb)
    (Pdb) u
    > d:\projects\construct\core.py(174)_parse()
    -> return self._decode(self.subcon._parse(stream, context), context)
    (Pdb) u
    > d:\projects\construct\debug.py(115)_parse()
    -> self.handle_exc("(you can set the value of 'self.retval', "
    (Pdb)
    (Pdb) l
    110         def _parse(self, stream, context):
    111             try:
    112                 return self.subcon._parse(stream, context)
    113             except:
    114                 self.retval = NotImplemented
    115  ->             self.handle_exc("(you can set the value of 'self.retval',
    "
    116                     "which will be returned)")
    117                 if self.retval is NotImplemented:
    118                     raise
    119                 else:
    120                     return self.retval
    (Pdb)
    (Pdb) self.retval = "QWERTY"
    (Pdb) q
    Container:
        bar = 1
        spam = 'QWERTY'
        eggs = 3
    >>>
