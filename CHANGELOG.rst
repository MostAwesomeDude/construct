=========
Changelog
=========

2.5.3
=====
* Commits since bb1e037887860a23df833f4068c4fe39de55e56e

2.5.0
=====
* Adding ``this`` expressions
* Restructuring the library
* Adding Python 3 support
* Killing ``construct.text`` (it's highly inefficient and it was a side-project anyway)
* Adding Travis CI tests
* Kill old site in favor of ``readthedocs``

2.06
====

Bugfixes
--------

 * Fix regression with Containers not being printable (#10)

2.05
====

Bugfixes
--------

 * Add a license (#1)
 * Fix text parsing of hex and binary (#2)
 * Container fixups
   * Proper dictionary behavior in corner cases
   * Correct bool(), len(), and "in" operator

Enhancements
------------

 * Introduce strong unit tests
 * Container improvements
   * Fully implement dict interface
   * Speedups
     * Container creation is around 3.8x faster
     * Container attribute setting is around 4.1x faster
     * Container iteration is around 1.6x faster

Removals
--------

 * Completely replace AttrDict with Container

Other
-----

 * Too many whitespace cleanups to count
 * Lots of docstring cleanups
 * Lots of documentation
   * Documentation cleanups (#3, #8)
