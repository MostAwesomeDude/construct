============
Introduction
============

Construct is a powerful **declarative** and **symmetrical** parser and builder for binary data.

Instead of writing *imperative code* to parse a piece of data, you declaratively define a *data structure* that describes your data. As this data structure is not code, you can use it in one direction to *parse* data into Pythonic objects, and in the other direction, to *build* objects into binary data.

The library provides both simple, atomic constructs (such as integers of various sizes), as well as composite ones which allow you form hierarchical and sequential structures of increasing complexity. Construct features **bit and byte granularity**, easy debugging and testing, an **easy-to-extend subclass system**, and lots of primitive constructs to make your work easier:

* Fields: raw bytes or numerical types
* Structs and Sequences: combine simpler constructs into more complex ones
* Bitwise: splitting bytes into bit-grained fields
* Adapters: change how data is represented
* Arrays/Ranges: duplicate constructs
* Meta-constructs: use the context (history) to compute the size of data
* If/Switch: branch the computational path based on the context
* On-demand (lazy) parsing: read and parse only the fields what you require
* Pointers: jump from here to there in the data stream
* Tunneling: prefix data with a byte count or compress it


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

A ``Sequence`` is a collection of ordered fields, and differs from ``Array`` and ``Range`` in that those two are homogenous::

    >>> format = Sequence(PascalString(Byte, encoding="utf8"), GreedyRange(Byte))
    >>> format.build([u"lalaland", [255,1,2]])
    b'\nlalaland\xff\x01\x02'
    >>> format.parse(b"\x004361789432197")
    ['', [52, 51, 54, 49, 55, 56, 57, 52, 51, 50, 49, 57, 55]]


Construct has been used to parse:

* Networking formats like Ethernet, IP, ICMP, IGMP, TCP, UDP, DNS, DHCP
* Binary file formats like Bitmaps, PNG, GIF, EMF, WMF
* Executable binaries formats like ELF32, PE32
* Filesystem layouts like Ext2, Fat16, MBR

See more examples of `file formats <https://github.com/construct/construct/tree/master/construct/examples/formats>`_ and `network protocols <https://github.com/construct/construct/tree/master/construct/examples/protocols>`_ in the repository.


Development and support
-------------------------
Please use `github issues <https://github.com/construct/construct/issues>`_ to ask general questions, make feature requests, report issues and bugs, and to send in patches. Feel free to request any changes that would support your project. There also used to be a `mailing list <https://groups.google.com/d/forum/construct3>`_ but github issues should be preffered.

Main documentation is at `readthedocs <http://construct.readthedocs.org>`_, where you can find all kinds of examples. Source is on `github <https://github.com/construct/construct>`_. Releases are available on `pypi <https://pypi.org/project/construct/>`_.


Requirements
--------------
Construct should run on any Python 2.7 3.3 3.4 3.5 3.6 3.7 pypy pypy3 implementation. Best would be 3.6 because it supports ordered keyword arguments. Second best would be 3.4 because it supports compilation feature.

Numpy is optional, if you want to serialize numpy arrays using Numpy protocol. Otherwise arrays can still be serialized using Array construct.

Different Python versions support different compression modules (like gzip), if you want to use Compressed construct.
