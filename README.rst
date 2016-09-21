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
Construct 2.8 is the fresh stable release. There were significant API and implementation changes. Fields are now name-less and operators / >> are used to construct Structs and Sequences. Many classes were added or removed or renamed or their fields or behavior changes. You should read the documentation again. Docstrings are up-to-date. **Website is currently stale and broken.**

Warning: Union class is currently broken.

Previous stable 2.5 release is not actively maintained. Only bugfixes will be added.

`Construct3 <http://tomerfiliba.com/blog/Survey-of-Construct3/>`_ is a rewrite from scratch and belongs to another developer, it diverged from this project. As far as I can tell, it was not even released yet.


Example
-------
(removed pending update)


Resources
---------
Construct's homepage is `<http://construct.readthedocs.org>`_, where you can find all kinds of docs and resources. The library itself is developed on `github <https://github.com/construct/construct>`_; please use `github issues <https://github.com/construct/construct/issues>`_ to ask general questions, make feature requests, report issues and bugs, and to send patches. There is also the `mailing list <https://groups.google.com/d/forum/construct3>`_ but GitHub should be preffered.


Requirements
------------
Construct should run on any Python 2.6 2.7 3.3 3.4 3.5 and pypy pypy3 implementation.

