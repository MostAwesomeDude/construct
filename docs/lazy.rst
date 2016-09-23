=============
Lazy parsing **
=============

<<< to be filled >>>



OnDemand
--------

OnDemand allows lazy construction, meaning the data is actually parsed (or built) only when it's requested (demanded). On-demand parsing is very useful with record-oriented data, where you don't have to actually parse the data unless it's actually needed. The result of OnDemand is an OnDemandContainer -- a special object that "remembers" the stream position where its data is found, and parses it when you access its .value property.

.. note::

    Lazy construction is available only for seekable streams (in-memory and files). Sockets and pipes do not suppose seeking, so you'll have to first read the data from the stream, and parse it in-memory.

>>> foo = Struct("foo",
...     Byte("a"),
...     OnDemand(Bytes("bigdata", 20)),  # <-- this will be read only on
demand
...     Byte("b"),
... )
>>>
>>> x = foo.parse("\x0101234567890123456789\x02")
>>> x
Container(a = 1, b = 2, bigdata = OnDemandContainer(<unread>))
>>>
>>> x.bigdata
OnDemandContainer(<unread>)
>>> x.bigdata.has_value                      # <-- still unread
False
>>>
>>> x.bigdata.value                          # <-- demand the data
'01234567890123456789'
>>>
>>> x.bigdata.has_value                      # <-- already demanded
True
>>> x.bigdata
OnDemandContainer('01234567890123456789')



LazyBound
---------

A lazy-bound construct; it binds to the construct only at runtime. Useful for recursive data structures (like linked lists or trees), where a construct needs to refer to itself (while it doesn't exist yet).

>>> foo = Struct("foo",
...     Flag("has_next"),
...     If(lambda ctx: ctx["has_next"], LazyBound("next", lambda: foo)),
... )
>>>
>>> print foo.parse("\x01\x01\x01\x00")
Container:
    has_next = True
    next = Container:
        has_next = True
        next = Container:
            has_next = True
            next = Container:
                has_next = False
                next = None
>>>

