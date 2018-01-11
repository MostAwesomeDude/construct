===================
Extending Construct
===================

Adapters
========

Adapters are the standard way to extend and customize the library. Adapters operate at the object level (unlike constructs, which operate at the stream level), and are thus easy to write and more flexible. For more info see the adapter tutorial.

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

* It's a craft that requires skills and understanding of the internals of the library (which change over time).
* Adapters should really be all you need and are much more simpler to implement.
* To make things faster, try using pypy, or write your code in cython. The python-level classes are as fast as it gets, assuming generality.

The only reason you might want to write a custom class is to achieve something that's not currently possible. This might be a construct that computes/corrects the checksum of data, altough that already exists. Or a compression, or hashing. These also exist. But surely there is something that was not invented yet.

If you need a semantics modification to an existing class, you can post a question or feature request as an Issue, or copy paste the class code and modify it.

There are two kinds of constructs: raw construct and subconstructs.

Raw constructs
--------------

Deriving directly from class ``Construct``, raw constructs can do as they wish by implementing ``_parse``, ``_build``, and ``_sizeof``::

    class MyConstruct(Construct):
        def _parse(self, stream, context, path):
            # read from the stream
            # return object
            pass
        
        def _build(self, obj, stream, context, path):
            # write obj to the stream
            # no return value is necessary
            # if returns an object, it replaces previous value in context dict
            pass
        
        def _sizeof(self, context, path):
            # return computed size (when fixed size or depends on context)
            # or raise SizeofError (when variable size or unknown)
            pass

Variable size fields typically raise ``SizeofError``, for example VarInt and CString.


Subconstructs
-------------

Deriving from class Subconstruct, these wrap an inner construct, inheriting it's properties (name and flags). In their ``_parse`` and ``_build`` and ``_sizeof`` methods, they will call ``self.subcon._parse`` and ``self.subcon._build`` and ``self.subcon._sizeof`` respectively.  ::

    class MySubconstruct(Subconstruct):
        def _parse(self, stream, context, path):
            obj = self.subcon._parse(stream, context, path)
            # do something with obj
            return obj
        
        def _build(self, obj, stream, context, path):
            # do something with obj
            return self.subcon._build(obj, stream, context, path)
            # no return value is necessary
            # if returns an object, it replaces previous value in context dict

        def _sizeof(self, context, path):
            # if not overriden, defers to subcon size
            return self.subcon._sizeof(context, path)


