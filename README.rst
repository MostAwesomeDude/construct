Construct 2.8
=============

Construct is a powerful **declarative** parser (and builder) for binary data.

Instead of writing *imperative code* to parse a piece of data, you declaratively define a *data structure* that describes your data. As this data structure is not code, you can use it in one direction to *parse* data into Pythonic objects, and in the other direction, build objects into binary data.

The library provides both simple, atomic constructs (such as integers of various sizes), as well as composite ones which allow you form hierarchical and sequential structures of increasing complexity. Construct features **bit and byte granularity**, easy debugging and testing, an **easy-to-extend subclass system**, and lots of primitive constructs to make your work easier:

* Fields: raw bytes or numerical types
* Structs and Sequences: combine simpler constructs into more complex ones
* Bitwise: splitting bytes into bit-grained fields
* Adapters: change how data is represented
* Arrays/Ranges: duplicate constructs
* Meta-constructs: use the context (history) to compute the size of data
* If/Switch: branch the computational path based on the context
* On-demand (lazy) parsing: read and parse only what you require
* Pointers: jump from here to there in the data stream 


Example
---------

A ``Struct`` is a collection of ordered, named fields::

    >>> format = Struct(
    ...     "signature" / Const(b"BMP"),
    ...     "width" / Int8ub,
    ...     "height" / Int8ub,
    ...     "pixels" / Array(this.width * this.height, Byte),
    ... )
    >>> format.build(dict(width=3,height=2,pixels=[7,8,9,11,12,13]))
    b'BMP\x03\x02\x07\x08\t\x0b\x0c\r'
    >>> format.parse(b'BMP\x03\x02\x07\x08\t\x0b\x0c\r')
    Container(signature=b'BMP')(width=3)(height=2)(pixels=[7, 8, 9, 11, 12, 13])

A ``Sequence`` is a collection of ordered fields, and differs from a ``Range`` in that latter is homogenous::

    >>> format = PascalString(Byte, encoding="utf8") >> GreedyRange(Byte)
    >>> format.build([u"lalalaland", [255,1,2]])
    b'\nlalalaland\xff\x01\x02'
    >>> format.parse(b"\x004361789432197")
    ['', [52, 51, 54, 49, 55, 56, 57, 52, 51, 50, 49, 57, 55]]

See more examples of `file formats <https://github.com/construct/construct/tree/master/construct/examples/formats>`_ and `network protocols <https://github.com/construct/construct/tree/master/construct/examples/protocols>`_ in the repository.


Sticky
--------
Version 2.5.5 is the previous stable release. If you are maintaining a project that depended on this framework for a long time, you should probably use this version. This branch is not actively maintained. Only bugfixes will be added.

Version 2.8 was released September, 2016. There are significant API and implementation changes. Fields are now name-less and operators / >> are used to construct Structs and Sequences. Most classes were redesigned and reimplemented. You should read the documentation again.


Development and support
-------------------------
Please use the `github issues <https://github.com/construct/construct/issues>`_ to ask general questions, make feature requests, report issues and bugs, and to send in patches. There is also the `mailing list <https://groups.google.com/d/forum/construct3>`_ but GitHub should be preffered.

Construct's main documentation is at `construct.readthedocs.org <http://construct.readthedocs.org>`_, where you can find all kinds of examples. The library itself is developed on `github <https://github.com/construct/construct>`_. Releases are also available on `pypi <https://pypi.python.org/pypi/construct>`_.

`Construct3 <http://tomerfiliba.com/blog/Survey-of-Construct3/>`_ is a different project. It is a rewrite from scratch and belongs to another developer, it diverged from this project. As far as I can tell, it was not released yet.


Requirements
--------------
Construct should run on any Python 2.7 3.3 3.4 3.5 3.6 and pypy pypy3 implementation.

Best should be 3.6 and pypy because they both support ordered keyword arguments which comes handy when declaring Struct members or manually crafting Containers.


