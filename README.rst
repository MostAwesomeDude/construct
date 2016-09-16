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

Notes
-----

**There are significant ongoing API and implementation changes. Previous branch in maintained as stable 2.5 releases. If you want to test the new 2.7 code, please be aware. Currently both docstrings and webpages are stale.**

`Construct3 <http://tomerfiliba.com/blog/Survey-of-Construct3/>`_ is a rewrite from scratch and diverged from this project.

Construct 2.5 drops the experimental text parsing support that was added in Construct 2.0; it was highly inefficient.

Example
-------

(removed pending update)

Resources
---------
Construct's homepage is `<http://construct.readthedocs.org>`_, where you can find all kinds of docs and resources. The library itself is developed on `github <https://github.com/construct/construct>`_; please use `github issues <https://github.com/construct/construct/issues>`_ to ask general questions, report issues and bugs, and to send patches. There is also the `mailing list <https://groups.google.com/d/forum/construct3>`_ but GitHub should be preffered.

Requirements
------------
Construct should run on any Python 2.6 2.7 3.3 3.4 3.5 and pypy pypy3 implementation.

