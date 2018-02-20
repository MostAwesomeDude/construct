=================
Transition to 2.9
=================

.. warning:: Construct is undergoing heavy changes at the moment, expect unstable API for about a month.

Overall
=======

**Compilation feature for faster performance!** Read `this tutorial chapter <https://construct.readthedocs.io/en/latest/compilation.html>`_, particularly its restrictions section.

**Docstrings of all classes were overhauled.** Check the `Core API pages <https://construct.readthedocs.io/en/latest/index.html#api-reference>`_.


General classes
-----------------

All constructs: `parse build sizeof` methods take context entries ONLY as keyword parameters \*\*kw (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html>`_)

All constructs: `compile benchmark testcompiled` methods were added (`see tutorial page <https://construct.readthedocs.io/en/latest/compilation.html#compiling-schemas>`_)

All constructs: operator * can be used for docstrings (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#documenting-fields>`_)

Compiled CompilableMacro Decompiled added (used internally)

String* require explicit encodings, all of them support UTF16 UTF32 encodings, but String CString dropped some parameters and support only encodings explicitly listed in `possiblestringencodings` (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#strings>`_)

String* build empty strings into empty bytes (despite for example UTF16 encoding empty string into 2 bytes marker)

Enum FlagsEnum can merge labels from IntEnum IntFlag, from enum34 module (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum dropped `default` parameter but returns integer if no mapping found (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum can build from integers and labels, and expose labels as attributes as bitwisable strings (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Mapping replaced SymmetricMapping, and dropped `default` parameter (`see API page <https://construct.readthedocs.io/en/latest/api/mappings.html#construct.Mapping>`_)

Struct Sequence Union FocusedSeq have new embedding semantics (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html#nesting-and-embedding>`_)

Struct Sequence Union FocusedSeq are exposing subcons in context (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html#refering-to-inlined-constructs>`_)

EmbeddedBitStruct removed

Array reimplemented without Range, does not use stream.tell()

Range removed, GreedyRange remains

Const has reordered parameters, like ``Const(b"\\x00")`` and ``Const(0, Int8ub)``. (`see API page <https://construct.readthedocs.io/en/latest/api/misc.html#construct.Const>`_)

Index added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#index>`_)

Pickled added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#pickled>`_)

Timestamp added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#timestamp>`_)

Hex HexDump reimplemented (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#hex-and-hexdump>`_)

If IfThenElse parameter renamed `predicate` to `condfunc`, and cannot be embedded (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.If>`_)

Switch dropped `includekey` parameter, and cannot be embedded (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.Switch>`_)

EmbeddedSwitch added, in Conditional (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#embeddedswitch>`_)

RestreamData added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#working-with-different-bytes>`_)

TransformData added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#working-with-different-bytes>`_)

ExprAdapter Mapping Restreamed changed parameters order (decoders before encoders)

Adapter changed parameters, added `path` to `_encode _decode _validate`

LazyStruct LazySequence LazyRange LazyField(OnDemand) removed

LazyBound remains, but changed to parameter-less lambda (`see tutorial page <https://construct.readthedocs.io/en/latest/lazy.html#lazybound>`_)

Probe Debugger updated, ProbeInto removed

FlagsContainer removed

HexString removed


Exceptions
-------------

FieldError was replaced with StreamError (raised when stream returns less than requested amount) and FormatFieldError (raised by FormatField class, for example if building Float from non-float value and struct.pack complains).

StreamError can be raised by most classes, when the stream is not seekable or tellable

StringError can be raised by most classes, when expected bytes but given unicode value

BitIntegerError was replaced with IntegerError

Struct Sequence can raise IndexError KeyError when dictionaries are missing entries

RepeatError added

IndexFieldError added

CheckError added

NamedTupleError added

RawCopyError added
