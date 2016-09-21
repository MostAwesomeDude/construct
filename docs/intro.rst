============
Introduction
============

What is Construct?
==================

In a nutshell, Construct is a declarative binary parser and builder library. To break that down into each different part, Construct is...

Declarative
-----------

Construct does not force users to write code in order to create parsers and builders. Instead, Construct gives users a **domain-specific language**, or DSL, for specifying their data structures.

Binary
------

Construct operates on bytes, not strings, and is specialized for binary data. In the past, there was an experimental support for parsing text but it was dropped in version 2.5.

Parser and Builder
------------------

Structures declared in Construct are symmetrical and describe both the parser and the builder. This eliminates the possibility of disparity between the parsing and building actions, and reduces the amount of code required to implement a format.

Library
-------

Construct is not a framework. It does not have any dependencies besides the Python standard library, and does not require users to adapt their code to its whims.

What is Construct good for?
===========================

Construct has been used to parse:

 * Networking formats like IP, DNS, SSL
 * Binary file formats like Bitmaps, JPEG, PNG
 * Executable binaries formats like ELF32, PE32
 * Filesystem layouts like Ext2, Fat16, MBR

And many other things! Just look into the `examples <https://github.com/construct/construct/tree/master/construct/examples>`_ folder.

What isn't Construct good at?
=============================

As previously mentioned, Construct is not a good choice for parsing text, due to the typical complexity of text-based grammars and the relative difficulty of parsing Unicode correctly. In the past, there was an experimental support for parsing text but it was dropped in version 2.5.

