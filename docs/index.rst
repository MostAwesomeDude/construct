.. raw:: html

    <div style="float:right; margin:1em; padding: 1em 2em 1em 2em; background-color: #efefef;
        border-radius: 5px; border-width: thin; border-style: dotted; border-color: #0C3762;">
    <strong>Quick Links</strong><br/>
    <ul>
    <li><a href="#user-guide" title="Jump to user guide">User Guide</a></li>
    <li><a href="#api-reference" title="Jump to API reference">API Reference</a></li>
    <li><a href="https://github.com/construct/construct/releases">Download</a></li>
    <li><a href="https://github.com/construct/construct/issues">Questions and Issues</a></li>
    </ul>
    <hr/>
    <a href="https://arekbulski.github.io/" target="_blank">
    <img style="display: block; margin-left: auto; margin-right: auto" 
    src="_static/constructocatab120p.png" title="Arkadiusz'es personal site"/></a>
    <br/>
    <a href="http://tomerfiliba.com" target="_blank">
    <img style="display: block; margin-left: auto; margin-right: auto" 
    src="_static/fish-text-black.png" title="Tomer's Blog"/></a>
    <br/>
    <a href="http://github.com/construct/construct" target="_blank">
    <img style="display: block; margin-left: auto; margin-right: auto; opacity: 0.7; width: 70px;" 
    src="_static/github-logo.png" title="Github Repo"/></a>
    <br/>
    <a href="http://travis-ci.org/construct/construct" target="_blank">
    <img src="https://travis-ci.org/construct/construct.png?branch=master" 
    style="display: block; margin-left: auto; margin-right: auto;" title="Travis CI status"></a>
    </div>


Construct
=========
.. raw:: html

    <div style="width:770px; margin: 1em 0 2em 0; display: block; padding: 1em; border: 1px dotted #DDD; 
    background-color: rgba(255, 255, 202, 0.69); border-radius: 5px;">

    <strong>Sticky</strong><br/>

    <a class="reference external" href="https://github.com/construct/construct/releases">Version 2.5.5</a> is the previous stable release. If you are maintaining a project that depended on this framework for a long time, you should probably use this version. This branch is not actively maintained. Only bugfixes will be added.<br/>
    <br/>

    <a class="reference external" href="https://github.com/construct/construct/releases">Version 2.8</a> was released on September, 2016. There are significant API and implementation changes. Fields are now name-less and operators / >> are used to construct Structs and Sequences. Most classes were redesigned and reimplemented. You should read the documentation again.<br/>
    <br/>

    Please use the <a class="reference external" href="https://github.com/construct/construct/issues">github issues</a> to ask general questions, make feature requests, report issues and bugs, and to send in patches.<br/>
    </div>


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


Development and support
-------------------------
Please use the `github issues <https://github.com/construct/construct/issues>`_ to ask general questions, make feature requests, report issues and bugs, and to send in patches. There is also the `mailing list <https://groups.google.com/d/forum/construct3>`_ but GitHub should be preffered.

Construct's main documentation is at `construct.readthedocs.org <http://construct.readthedocs.org>`_, where you can find all kinds of examples. The library itself is developed on `github <https://github.com/construct/construct>`_. Releases are also available on `pypi <https://pypi.python.org/pypi/construct>`_.

`Construct3 <http://tomerfiliba.com/blog/Survey-of-Construct3/>`_ is a different project. It is a rewrite from scratch and belongs to another developer, it diverged from this project. As far as I can tell, it was not released yet.


Requirements
--------------
Construct should run on any Python 2.7 3.3 3.4 3.5 3.6 and pypy pypy3 implementation.

Best should be 3.6 and pypy because they both support ordered keyword arguments which comes handy when declaring Struct members or manually crafting Containers.


User Guide
==========

Sections marked with ** are stale and broken.

.. toctree::
   :maxdepth: 2

   intro
   transition
   basics
   advanced
   bitwise
   adapters
   meta
   misc
   streaming
   tunneling
   lazy
   extending
   debugging

API Reference
=============

.. toctree::
   :maxdepth: 2

   api/bytes
   api/strings
   api/structseq
   api/repeaters
   api/lazy
   api/streaming
   api/tunneling
   api/debugging

   api/core
   api/lib

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

