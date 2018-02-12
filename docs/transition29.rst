=================
Transition to 2.9
=================

Overall
=======

**Compilation feature for faster performance!** Read `this chapter <https://construct.readthedocs.io/en/latest/compilation.html>`_ for tutorial, particularly its restrictions section.

**Docstrings of all classes were overhauled.** Check the `Core API pages <https://construct.readthedocs.io/en/latest/index.html#api-reference>`_.


General classes
-----------------

All constructs: `parse build sizeof` methods take context entries ONLY as keyword parameters \*\*kw (see `this chapter <https://construct.readthedocs.io/en/latest/meta.html>`_)

All constructs: `compile benchmark testcompiled` methods were added (see `this chapter <https://construct.readthedocs.io/en/latest/compilation.html#compiling-schemas>`_)

Compiled CompilableMacro Decompiled added (used internally)

String* classes require explicit encoding (see `this page <https://construct.readthedocs.io/en/latest/advanced.html#strings>`_)

String* classes apply global encoding during ctor (not during parsing and building)

String* classes (all of them) support UTF16 UTF32 encodings, but String CString dropped some parameters

Enum FlagsEnum can merge labels from IntEnum IntFlag (enum module), but dropped `default` parameter

Enum FlagsEnum can build from integers and labels (see `this page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum expose labels as attributes (see `this page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum attributes are bitwisable strings (see `this page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Struct Sequence Union FocusedSeq are nesting context (in parse build and sizeof)

Struct Sequence Union FocusedSeq are supporting new embedding semantics (see `this page <https://construct.readthedocs.io/en/latest/meta.html#nesting-and-embedding>`_)

EmbeddedBitStruct removed

Array reimplemented without Range, does not use stream.tell()

Range removed, GreedyRange remains

Index added, in Miscellaneous

Hex HexDump reimplemented (see `this page <https://construct.readthedocs.io/en/latest/misc.html#hex-and-hexdump>`_)

If IfThenElse parameter renamed `predicate` to `condfunc`

Switch dropped `includekey` parameter, and cannot be embedded

RestreamData added, in Tunneling

ExprAdapter Restreamed Mapping* classes changed parameters order (decoders before encoders)

OnDemand was renamed to LazyField

LazyStruct LazySequence LazyRange removed

FlagsContainer removed

HexString removed


Exceptions
-------------

FieldError was replaced with StreamError (raised when stream returns less than requested amount) and FormatFieldError (raised by FormatField class, for example if building Float from non-float value and struct.pack complains).

StreamError can be raised by most classes, when the stream is not seekable or tellable

StringError can be raised by most classes, when expected bytes but given unicode value

BitIntegerError was replaced with IntegerError

Struct Sequence can raise IndexError and KeyError when dictionaries are missing entries

RepeatError added

IndexFieldError added

CheckError added

NamedTupleError added

RawCopyError added
