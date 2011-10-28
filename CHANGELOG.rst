=========
Changelog
=========

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
