=================
Transition to 2.9
=================


Overall
==========

**Compilation feature for faster performance!** Read `this tutorial chapter <https://construct.readthedocs.io/en/latest/compilation.html>`_, particularly its restrictions section.

**Docstrings of all classes were overhauled.** Check the `Core API pages <https://construct.readthedocs.io/en/latest/index.html#api-reference>`_.


General classes
-------------------

All constructs: `parse build sizeof` methods take context entries ONLY as keyword parameters \*\*contextkw (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html>`_)

All constructs: `parse_file` and `build_file` methods were added (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#processing-files>`_)

All constructs: operator * can be used for docstrings and parsed hooks (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#documenting-fields>`_ and `tutorial page <https://construct.readthedocs.io/en/latest/basics.html#processing-on-the-fly>`_)

All constructs: added `compile` and `benchmark` methods (`see tutorial page <https://construct.readthedocs.io/en/latest/compilation.html#compiling-schemas>`_)

All constructs: added `parsed` hook/callback (`see tutorial page <https://construct.readthedocs.io/en/latest/basics.html#processing-on-the-fly>`_)

Compiled added (used internally)

Half was added alongside Single, Double

String* require explicit encodings, all of them support UTF16 UTF32 encodings, but PaddedString CString dropped some parameters and support only encodings explicitly listed in `possiblestringencodings` (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#strings>`_)

PaddedString CString classes reimplemented using NullTerminated NullStripped

String* build empty strings into empty bytes (despite for example UTF16 encoding empty string into 2 bytes marker)

String class renamed to PaddedString

Enum FlagsEnum can merge labels from IntEnum IntFlag, from enum34 module (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum dropped `default` parameter but returns integer if no mapping found (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

Enum FlagsEnum can build from integers and labels, and expose labels as attributes, as bitwisable strings (`see tutorial page <https://construct.readthedocs.io/en/latest/advanced.html#mappings>`_)

FlagsEnum had parsing semantics fixed (affecting multi-bit flags)

Mapping replaced SymmetricMapping, and dropped `default` parameter (`see API page <https://construct.readthedocs.io/en/latest/api/mappings.html#construct.Mapping>`_)

Struct Sequence FocusedSeq Union LazyStruct have new embedding semantics (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html#nesting-and-embedding>`_)

Struct Sequence FocusedSeq Union LazyStruct are exposing subcons, as attributes and in _subcons context entry (`see tutorial page <https://construct.readthedocs.io/en/latest/meta.html#refering-to-inlined-constructs>`_)

Struct Sequence FocusedSeq Union LazyStruct are exposing _ _params _root _parsing _building _sizing _subcons _io _index entries in the context (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#ifthenelse>`_)

EmbeddedBitStruct removed, instead use BitStruct with Bytewise-wrapped fields (`see tutorial page <https://construct.readthedocs.io/en/latest/bitwise.html#fields-that-work-with-bytes>`_)

Array reimplemented without Range, does not use stream.tell()

Range removed, GreedyRange does not support [:] syntax

Array GreedyRange RepeatUntil added `discard` parameter (`see tutorial page <https://construct.readthedocs.io/en/latest/basics.html#processing-on-the-fly>`_)

Const has reordered parameters, `value` before `subcon` (`see API page <https://construct.readthedocs.io/en/latest/api/misc.html#construct.Const>`_)

Index added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#index>`_)

Pickled added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#pickled>`_)

Timestamp added, in Miscellaneous (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#timestamp>`_)

Hex HexDump reimplemented, return bytes and not hexlified strings (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#hex-and-hexdump>`_)

Select dropped `includename` parameter (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.Select>`_)

Select allows to build from none if any of its subcons can

If IfThenElse parameter `predicate` renamed to `condfunc`, and cannot be embedded (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.If>`_)

Switch updated, `default` parameter is `Pass` instead of `NoDefault`, dropped `includekey` parameter, and cannot be embedded (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.Switch>`_)

EmbeddedSwitch added, in Conditional (`see tutorial page <https://construct.readthedocs.io/en/latest/misc.html#embeddedswitch>`_)

StopIf raises `StopFieldError` instead of `StopIteration` (`see API page <https://construct.readthedocs.io/en/latest/api/conditional.html#construct.StopIf>`_)

Pointer changed size to 0, can be parsed lazily, can also select a stream from context entry

PrefixedArray parameter `lengthfield` renamed to `countfield` (`see API page <https://construct.readthedocs.io/en/latest/api/tunneling.html#construct.PrefixedArray>`_)

FixedSized NullTerminated NullStripped added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#working-with-bytes-subsets>`_)

RestreamData added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#working-with-different-bytes>`_)

Transformed added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#working-with-different-bytes>`_)

ProcessXor and ProcessRotateLeft added, in Tunneling (`see tutorial page <https://construct.readthedocs.io/en/latest/tunneling.html#processing-data-with-xor-and-algorithms>`_)

ExprAdapter Mapping Restreamed changed parameters order (decoders before encoders)

Adapter changed parameters, added `path` parameter to `_encode _decode _validate` methods (`see tutorial page <https://construct.readthedocs.io/en/latest/adapters.html>`_)

Lazy added, in Lazy equivalents category (`see tutorial page <https://construct.readthedocs.io/en/latest/lazy.html#lazy>`_)

LazyStruct LazyArray reimplemented with new lazy parsing semantics (`see tutorial page <https://construct.readthedocs.io/en/latest/lazy.html#lazystruct>`_)

LazySequence LazyRange LazyField(OnDemand) removed

LazyBound remains, but changed to parameter-less lambda (`see tutorial page <https://construct.readthedocs.io/en/latest/lazy.html#lazybound>`_)

Probe Debugger updated, ProbeInto removed (`see tutorial page <https://construct.readthedocs.io/en/latest/debugging.html>`_)


Support classes
--------------------

Container updated, uses `globalPrintFullStrings globalPrintFalseFlags globalPrintPrivateEntries`

Container updated, equality does not check hidden keys like _private or keys order

FlagsContainer removed

RestreamedBytesIO supports reading till EOF, enabling GreedyBytes GreedyString inside Bitwise Bytewise

HexString removed


Exceptions
-------------

Exceptions always display path information

FieldError was replaced with StreamError (raised when stream returns less than requested amount) and FormatFieldError (raised by FormatField class, for example if building Float from non-float value and struct.pack complains).

StreamError can be raised by most classes, when the stream is not seekable or tellable

StringError can be raised by classes like Bytes Const, when expected bytes but given unicode string as build value

BitIntegerError was replaced by IntegerError

Struct Sequence can raise IndexError KeyError when dictionaries are missing entries

RepeatError added

IndexFieldError added

CheckError added

NamedTupleError added

RawCopyError added
