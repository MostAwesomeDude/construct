============
Lazy parsing
============

.. note:: There is incoming effort to add truly lazy parsing (like Struct). Stay tuned. Feature request at `Issue #549 <https://github.com/construct/construct/issues/549>`_ .


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
