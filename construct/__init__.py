"""
Construct 2 -- Parsing Made Fun

Homepage:
    http://construct.readthedocs.org

Hands-on example:
    >>> from construct import *
    >>> s = Struct("struct",
    ...     UBInt8("a"),
    ...     UBInt16("b"),
    ... )
    >>> print s.parse(b"\\x01\\x02\\x03")
    Container:
        a = 1
        b = 515
    >>> s.build(Container(a=1, b=0x0203))
    b"\\x01\\x02\\x03"
"""

# from construct.core import AdaptationError, Anchor, ArrayError, Buffered, Construct, ConstructError, Container, FieldError, FormatField, LazyBound, LazyContainer, ListContainer, MetaArray, MetaField, OnDemand, OverwriteError, Packer, Pass, Peek, Pointer, Range, RangeError, Reconfig, RepeatUntil, Restream, Select, SelectError, Sequence, SizeofError, StaticField, Struct, Subconstruct, Switch, SwitchError, Terminator, TerminatorError, Union, Computed, Padding, PaddingError, Const, ConstError, Aligned, String, VarInt, StringError, GreedyString, CString, Checksum, AnchorRange, ByteSwapped, LazyStruct, Numpy, ValidationError, Validator, Adapter, SymmetricAdapter, Tunnel, Compressed, GreedyBytes, BitIntegerError, Prefixed, UBInt24, ULInt24
from construct.core import *
# from construct.adapters import ExprAdapter, FlagsAdapter, FlagsContainer, HexDump, HexString, Indexing, MappingAdapter, MappingError, NoneOf, OneOf, Slicing
# from construct.macros import Alias, AlignedStruct, Array, BFloat32, BFloat64, Bit, BitField, BitStreamReader, BitStreamWriter, BitStruct, Bitwise, Embedded, EmbeddedBitStruct, Enum, Field, Flag, FlagsEnum, GreedyRange, If, IfThenElse, LFloat32, LFloat64, NFloat32, NFloat64, Nibble, Octet, OnDemandPointer, OpenRange, Optional, OptionalGreedyRange, PrefixedArray, Renamed, SBInt16, SBInt32, SBInt64, SBInt8, SLInt16, SLInt32, SLInt64, SLInt8, SNInt16, SNInt32, SNInt64, SNInt8, SeqOfOne, SymmetricMapping, UBInt16, UBInt32, UBInt64, UBInt8, ULInt16, ULInt32, ULInt64, ULInt8, UNInt16, UNInt32, UNInt64, UNInt8, PascalString
from construct.expr import this, Path
from construct.debug import Probe, Debugger
from construct.version import version, version_string as __version__


#===============================================================================
# metadata
#===============================================================================
__author__ = "Arkadiusz Bulski <arek.bulski@gmail.com>, Tomer Filiba <tomerfiliba@gmail.com>, Corbin Simpson <MostAwesomeDude@gmail.com>"

#===============================================================================
# aliases
#===============================================================================

#===============================================================================
# exposed names
#===============================================================================
__all__ = [
    'AdaptationError', 'Alias', 'Aligned', 'AlignedStruct', 'Anchor', 'Array', 'ArrayError', 'Bit', 'BitIntegerError', 'BitStruct', 'Bitwise', 'CString', 'Construct', 'ConstructError', 'Container', 'Debugger', 'EmbeddedBitStruct', 'Enum', 'ExprAdapter', 'FieldError', 'Flag', 'FlagsContainer', 'FlagsEnum', 'Bytes', 'FormatField', 'GreedyRange', 'HexDump', 'HexString', 'If', 'IfThenElse', 'Indexing', 'LazyBound', 'LazyContainer', 'ListContainer', 'Mapping', 'MappingError', 'Nibble', 'NoneOf', 'Octet', 'OnDemand', 'OnDemandPointer', 'OneOf', 'Optional', 'OverwriteError', 'Packer', 'Padding', 'PaddingError', 'PascalString', 'Pass', 'Peek', 'Pointer', 'PrefixedArray', 'Probe', 'Range', 'RangeError', 'Renamed', 'RepeatUntil', 'Select', 'SelectError', 'Sequence', 'SizeofError', 'Slicing', 'String', 'Struct', 'Subconstruct', 'Switch', 'SwitchError', 'SymmetricMapping', 'Terminator', 'TerminatorError', 'Union', 'ValidationError', 'Validator', 'Computed', 'Byte', 'Bytes', 'Tunnel', 'Embedded', 'Const', 'ConstError', 'VarInt', 'StringError', 'Checksum', 'ByteSwapped', 'LazyStruct', 'Numpy', 'Adapter', 'SymmetricAdapter', 'Tunnel', 'Compressed', 'GreedyBytes', 'Prefixed', 'Padded', 'GreedyString', 'RawCopy', 'LazyRange', 'LazySequence', 'LazySequenceContainer', 'BitsInteger', 'BytesInteger', '__author__', 'Restreamed', 'RestreamedBytesIO', 'this', 'Path', 'Bytewise', 'LazyRangeContainer', 'BitsSwapped',

] + ["Int%s%s%s" % (n,us,bln) for n in (8,16,32,64) for us in "us" for bln in "bln"] + ["Int24ub","Int24ul"] + ["Float%s%s" % (n,bl) for n in (32,64) for bl in "bl"] + ["Single","Double"]

