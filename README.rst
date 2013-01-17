Construct2
==========
Construct is a powerful **declarative** parser (and builder) for binary data.

Instead of writing *imperative code* to parse a piece of data, you declaratively
define a *data structure* that describes your data. As this data structure is not
code, you can use it in one direction to *parse* data into Pythonic objects, 
and in the other direction, convert ("build") objects into binary data.

The library provides both simple, atomic constructs (such as integers of various sizes), 
as well as composite ones which allow you form hierarchical structures of increasing complexity.
Construct features **bit and byte granularity**, easy debugging and testing, an 
**easy-to-extend subclass system**, and lots of primitive constructs to make your 
work easier:

* Fields: raw bytes or numerical types
* Structs and Sequences: combine simpler constructs into more complex ones
* Adapters: change how data is represented
* Arrays/Ranges: duplicate constructs
* Meta-constructs: use the context (history) to compute the size of data
* If/Switch: branch the computational path based on the context
* On-demand (lazy) parsing: read only what you require
* Pointers: jump from here to there in the data stream 

.. note::
   `Construct3 <http://tomerfiliba.com/blog/Survey-of-Construct3/>`_ is a rewrite of Construct2; 
   the two are incompatible, thus ``construct3`` will be released as a *different package*. 
   Construct 2.5 is the last release of the 2.x codebase.
   
   Construct 2.5 drops the experimental text parsing support that was added in Construct 2.0;
   it was highly inefficient and I chose to concentrate on binary data.

Example
-------

A ``PascalString`` is a string prefixed by its length::

    >>> from construct import *
    >>>
    >>> PascalString = Struct("PascalString",
    ...     UBInt8("length"),
    ...     Bytes("data", lambda ctx: ctx.length),
    ... )
    >>>
    >>> PascalString.parse("\x05helloXXX")
    Container({'length': 5, 'data': 'hello'})
    >>> PascalString.build(Container(length = 6, data = "foobar"))
    '\x06foobar'

Instead of specifying the length manually, let's use an adapter::

    >>> PascalString2 = ExprAdapter(PascalString, 
    ...     encoder = lambda obj, ctx: Container(length = len(obj), data = obj), 
    ...     decoder = lambda obj, ctx: obj.data
    ... )
    >>> PascalString2.parse("\x05hello")
    'hello'
    >>> PascalString2.build("i'm a long string")
    "\x11i'm a long string"

See more examples of `file formats <https://github.com/construct/construct/tree/master/construct/formats>`_
and `network protocols <https://github.com/construct/construct/tree/master/construct/protocols>`_ 
in the repository.

Resources
---------
Construct's homepage is `<http://construct.readthedocs.org>`_, where you can find all kinds
of docs and resources. The library itself is developed on `github <https://github.com/construct/construct>`_;
please use `github issues <https://github.com/construct/construct/issues>`_ to report bugs, and
github pull-requests to send in patches. For general discussion or questions, please use the 
`new discussion group <https://groups.google.com/d/forum/construct3>`_.

Requirements
------------
Construct should run on any Python 2.5-3.3 implementation. 

Its only requirement is `six <http://pypi.python.org/pypi/six>`_, which is used to overcome the 
differences between Python 2 and 3.

