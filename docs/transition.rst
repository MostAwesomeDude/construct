=================
Transition to 2.8
=================

Overall
=======

All fields and complex constructs are now nameless. Look at Struct and Sequence, and also Range and Array.



Integers and floats
-------------------

{U,S}{L,B,N}Int{8,16,24,32,64} was made Int{8,16,24,32,64}{u,s}{l,b,n}

Byte, Short, Int, Long were made aliases to Int{8,16,32,64}ub

{B,L,N}Float{32,64} was made Float{32,64}{b,l,n}

Single, Double were made aliases to Float{32,64}b

VarInt was added

Bit, Nibble, Octet remain

All above were made singletons.



Fields
------

Field was made Bytes (operates on b-strings)

BytesInteger was added (operates on integers)

BitField was made BitsInteger (operates on integers)

GreedyBytes was added

Flag was made a singleton

Enum takes the `default` keyword argument, no underscores

FlagsEnum remains



Strings
-------

String remains

PascalString argument `length_field=UBInt8` was made `lengthfield`

CString dropped `char_field`

GreedyString dropped `char_field`

All above use optional `encoding` or use global encoding (see ``setglobalstringencoding()``).



Structures and Sequences
------------------------

Struct uses syntax like ``Struct("num"/Int32ub, "text"/CString())``

Sequence uses syntax like ``Byte >> Int16ul`` and ``Sequence(Byte, Int16ul)``

On Python 3.6 you can use ``Struct(num=Int32ub, text=CString())``


Ranges and Arrays
-----------------

Array uses syntax like ``Byte[10]`` and ``Array(10, Byte)``.

PrefixedArray takes explicit `lengthfield` before subcon

Range uses syntax like ``Byte[0:]`` ``Byte[:10]`` ``Byte[0:10]`` and ``Range(min=?, max=?, Byte)``

OpenRange and GreedyRange were dropped

OptionalGreedyRange was renamed to GreedyRange

RepeatUntil takes 3-argument (last element, list, context) lambda



Lazy collections
----------------

LazyStruct LazyRange LazySequence were added

OnDemand now returns a paramterless lambda that returns the parsed object

OnDemandPointer dropped `force_build` parameter

LazyBound remains



Padding and Alignment
---------------------

Aligned takes explicit `modulus` before the subcon

Padded was added, also takes explicit `modulus` before the subcon

Padding remains



Optional
--------

If dropped `elsevalue` and always returns None

IfThenElse parameters renamed to `thensubcon` and `elsesubcon`

Switch remains

Optional remains

Union takes optional `buildfrom` and seeks back on parsing otherwise, indexes by id or name

Select remains



Miscellaneous and others
------------------------

Value was made Computed

Embed was made Embedded

Const incorporated Magic field

Pass remains but Terminator was renamed Terminated

Error added

OneOf Noneof remain

Filter added

LengthValueAdapter was replaced by Prefixed, and gained `includelength` option

Hex added

HexDumpAdapter was made HexDump

HexDump builds from hexdumped data, not from raw bytes

SlicingAdapter and IndexingAdapter were made Slicing and Indexing

ExprAdapter ExprSymmetricAdapter ExprValidator added or remain

SeqOfOne was replaced by FocusedSeq

Numpy added

NamedTuple added

Check added

Default added

Alias was removed

StopIf added



Stream manipulation
-------------------

Bitwise was reimplemented using Restreamed, and Bytewise was added

Restreamed and Rebuffered were redesigned

Anchor was made Tell and a singleton

Seek was added

Pointer remains

Peek dropped `perform_build` parameter, never builds



Tunneling
---------

RawCopy was added, returns both parsed object and raw bytes consumed

Prefixed was added, allows to put greedy fields inside structs and sequences

ByteSwapped and BitsSwapped added

Checksum and Compressed added
