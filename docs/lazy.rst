============
Lazy parsing
============

.. note:: There is incoming effort to add truly lazy parsing (like Struct). Stay tuned. Feature request at `Issue #549 <https://github.com/construct/construct/issues/549>`_ .


LazyBound
---------

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
