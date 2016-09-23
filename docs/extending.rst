===================
Extending Construct **
===================

Adapters
========

Adapters are the standard way to extend and customize the library. Adapters
operate at the object level (unlike constructs, which operate at the stream
level), and are thus easy to write and more flexible. For more info see, the
adapter tutorial.

In order to write custom adapters, implement ``_encode`` and ``_decode``::

    class MyAdapter(Adapter):
        def _encode(self, obj, context):
            # called at building time to return a modified version of obj
            # reverse version of _decode
            pass
        
        def _decode(self, obj, context):
            # called at parsing time to return a modified version of obj
            # reverse version of _encode
            pass

Constructs
==========

Generally speaking, you should not write constructs by yourself:

* It's a craft that requires skills and understanding of the internals of the
  library (which change over time).
* Adapters should really be all you need and are much more simpler to
  implement.
* To make things faster, try using psyco, or write your code in pyrex. The
  python-level classes are as fast as it gets, assuming generality.


The only reason you might want to write a construct is to achieve something
that's not currently possible. This might be a construct that
computes/corrects the checksum of data... the reason there's no such construct
yet is because I couldn't find an elegant way to do that (although Buffered or
Union may be a good place to start).

There are two kinds of constructs: raw construct and subconstructs.

Raw constructs
--------------

Deriving directly of class ``Construct``, raw construct can do as they wish by
implementing ``_parse``, ``_build``, and ``_sizeof``::

    class MyConstruct(Construct):
        def _parse(self, stream, context):
            # read from the stream (usually not directly)
            # return object
            pass
        
        def _build(self, obj, stream, context):
            # write obj to the stream (usually not directly)
            # no return value is necessary
            pass
        
        def _sizeof(self, context):
            # return computed size, or raise SizeofError if not possible
            pass


Subconstructs
-------------

Deriving of class Subconstruct, subconstructs wrap an inner construct,
inheriting it's properties (name, flags, etc.). In their ``_parse`` and
``_build`` methods, they will call ``self.subcon._parse`` or
``self.subcon._build`` respectively. Most subconstruct do not need to override
``_sizeof``. ::

    class MySubconstruct(Subconstruct):
        def _parse(self, stream, context):
            obj = self.subcon._parse(stream, context)
            # do something with obj
            # return object
        
        def _build(self, obj, stream, context):
            # do something with obj
            self.subcon._build(obj, stream, context)
            # no return value is necessary
