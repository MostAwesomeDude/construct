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

The only reason you might want to write a construct is to achieve something that's not currently possible. This might be a construct that computes/corrects the checksum of data... altough that already exists. Or a compression, or hashing. These also exist. But surely there is something that was not invented yet.

If you need a semantics modification to existing construct, you can post a question or request as an Issue, or copy paste its code and modify it.

There are two kinds of constructs: raw construct and subconstructs.

Raw constructs
--------------

Deriving directly of class ``Construct``, raw construct can do as they wish by implementing ``_parse``, ``_build``, and ``_sizeof``::

    class MyConstruct(Construct):
        def _parse(self, stream, context, path):
            # read from the stream (usually not directly)
            # return object
            pass
        
        def _build(self, obj, stream, context, path):
            # write obj to the stream (usually not directly)
            # no return value is necessary
            pass
        
        def _sizeof(self, context, path):
            # return computed size (when fixed size or depends on context)
            # or raise SizeofError if not possible (when variable size)
            pass

Variable size fields typically raise SizeofError, for example VarInt CString.


Subconstructs
-------------

Deriving of class Subconstruct, these wrap an inner construct, inheriting it's properties (name and flags). In their ``_parse`` and ``_build`` methods, they will call ``self.subcon._parse`` or ``self.subcon._build`` respectively. Most subconstructs do not need to override ``_sizeof``. ::

    class MySubconstruct(Subconstruct):
        def _parse(self, stream, context, path):
            obj = self.subcon._parse(stream, context, path)
            # do something with obj
            return obj
        
        def _build(self, obj, stream, context, path):
            # do something with obj
            return self.subcon._build(obj, stream, context, path)
            # no return value is necessary
            # but if returns one, it will be replace previous context value

        def _sizeof(self, context, path):
            # if not overriden, mimics sub size
            return self.subcon._sizeof(context, path)


