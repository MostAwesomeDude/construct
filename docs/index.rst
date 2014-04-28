.. raw:: html

    <div style="float:right; margin:1em; padding: 1em 2em 1em 2em; background-color: #efefef;
        border-radius: 5px; border-width: thin; border-style: dotted; border-color: #0C3762;">
    <strong>Quick Links</strong><br/>
    <ul>
    <li><a href="#user-guide" title="Jump to user guide">User Guide</a></li>
    <li><a href="#api-reference" title="Jump to API reference">API Reference</a></li>
    <li><a href="http://pypi.python.org/pypi/construct#downloads">Download</a></li>
    <li><a href="https://groups.google.com/d/forum/construct3">Discussion Group</a></li>
    </ul>
    <hr/>
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
   
   <a class="reference external" href="https://pypi.python.org/pypi/construct">Version 2.5.2</a> 
   was released on April 28th, 2014<br/>
   
   Please use the 
   <a class="reference external" href="https://groups.google.com/d/forum/construct3">mailing list</a> 
   to ask questions and use 
   <a class="reference external" href="https://github.com/construct/construct/issues">github issues</a> 
   to report problems. <strong>Please do not email me directly</strong>.
   
   </div>

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

User Guide
==========

.. toctree::
   :maxdepth: 2

   intro
   basics
   bitwise
   adapters
   meta
   api/string
   misc
   extending
   debugging

API Reference
=============

.. toctree::
   :maxdepth: 2

   api/core
   api/adapters
   api/macros
   api/debugging

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

