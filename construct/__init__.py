"""
Construct 2 -- Parsing Made Fun

Homepage:
    http://construct.readthedocs.org

Hands-on example:
    >>> from construct import *
    >>> s = Struct("foo",
    ...     UBInt8("a"),
    ...     UBInt16("b"),
    ... )
    >>> print s.parse(b"\\x01\\x02\\x03")
    Container:
        a = 1
        b = 515
    >>> s.build(Container(a = 1, b = 0x0203))
    b"\\x01\\x02\\x03"
"""

from construct.core import AdaptationError, Adapter, Anchor, ArrayError, Buffered, Construct, ConstructError, Container, FieldError, FormatField, LazyBound, LazyContainer, ListContainer, MetaArray, MetaField, OnDemand, OverwriteError, Packer, Pass, Peek, Pointer, Range, RangeError, Reconfig, RepeatUntil, Restream, Select, SelectError, Sequence, SizeofError, StaticField, Struct, Subconstruct, Switch, SwitchError, Terminator, TerminatorError, ULInt24, Union, Computed, Padding, PaddingError, Const, ConstError, Aligned
from construct.adapters import BitIntegerAdapter, BitIntegerError, CStringAdapter, ExprAdapter, FlagsAdapter, FlagsContainer, HexDumpAdapter, HexString, IndexingAdapter, LengthValueAdapter, MappingAdapter, MappingError, NoneOf, OneOf, PaddedStringAdapter, SlicingAdapter, StringAdapter, TunnelAdapter, ValidationError, Validator
from construct.macros import Alias, AlignedStruct, Array, BFloat32, BFloat64, Bit, BitField, BitStreamReader, BitStreamWriter, BitStruct, Bitwise, CString, Embedded, EmbeddedBitStruct, Enum, Field, Flag, FlagsEnum, GreedyRange, If, IfThenElse, LFloat32, LFloat64, NFloat32, NFloat64, Nibble, Octet, OnDemandPointer, OpenRange, Optional, OptionalGreedyRange, PascalString, PrefixedArray, Rename, SBInt16, SBInt32, SBInt64, SBInt8, SLInt16, SLInt32, SLInt64, SLInt8, SNInt16, SNInt32, SNInt64, SNInt8, SeqOfOne, String, SymmetricMapping, UBInt16, UBInt32, UBInt64, UBInt8, ULInt16, ULInt32, ULInt64, ULInt8, UNInt16, UNInt32, UNInt64, UNInt8, GreedyString
from construct.lib.expr import this
from construct.debug import Probe, Debugger
from construct.version import version, version_string as __version__


#===============================================================================
# Metadata
#===============================================================================
__author__ = "Arkadiusz Bulski <arek.bulski@gmail.com>, Tomer Filiba <tomerfiliba@gmail.com>, Corbin Simpson <MostAwesomeDude@gmail.com>"

#===============================================================================
# Shorthand expressions
#===============================================================================
Bits = BitField
Byte = UBInt8
Bytes = Field
Tunnel = TunnelAdapter
Embed = Embedded

#===============================================================================
# exposed names
#===============================================================================
__all__ = [
    'AdaptationError', 'Adapter', 'Alias', 'Aligned', 'AlignedStruct', 'Anchor', 'Array', 'ArrayError', 'BFloat32', 'BFloat64', 'Bit', 'BitField', 'BitIntegerAdapter', 'BitIntegerError', 'BitStreamReader', 'BitStreamWriter', 'BitStruct', 'Bitwise', 'Buffered', 'CString', 'CStringAdapter', 'Construct', 'ConstructError', 'Container', 'Debugger', 'Embedded', 'EmbeddedBitStruct', 'Enum', 'ExprAdapter', 'Field', 'FieldError', 'Flag', 'FlagsAdapter', 'FlagsContainer', 'FlagsEnum', 'FormatField', 'GreedyRange', 'HexDumpAdapter', 'HexString', 'If', 'IfThenElse', 'IndexingAdapter', 'LFloat32', 'LFloat64', 'LazyBound', 'LazyContainer', 'LengthValueAdapter', 'ListContainer', 'MappingAdapter', 'MappingError', 'MetaArray', 'MetaField', 'NFloat32', 'NFloat64', 'Nibble', 'NoneOf', 'Octet', 'OnDemand', 'OnDemandPointer', 'OneOf', 'OpenRange', 'Optional', 'OptionalGreedyRange', 'OverwriteError', 'Packer', 'PaddedStringAdapter', 'Padding', 'PaddingError', 'PascalString', 'Pass', 'Peek', 'Pointer', 'PrefixedArray', 'Probe', 'Range', 'RangeError', 'Reconfig', 'Rename', 'RepeatUntil', 'Restream', 'SBInt16', 'SBInt32', 'SBInt64', 'SBInt8', 'SLInt16', 'SLInt32', 'SLInt64', 'SLInt8', 'SNInt16', 'SNInt32', 'SNInt64', 'SNInt8', 'Select', 'SelectError', 'SeqOfOne', 'Sequence', 'SizeofError', 'SlicingAdapter', 'StaticField', 'String', 'StringAdapter', 'Struct', 'Subconstruct', 'Switch', 'SwitchError', 'SymmetricMapping', 'Terminator', 'TerminatorError', 'TunnelAdapter', 'UBInt16', 'UBInt32', 'UBInt64', 'UBInt8', 'ULInt16', 'ULInt24', 'ULInt32', 'ULInt64', 'ULInt8', 'UNInt16', 'UNInt32', 'UNInt64', 'UNInt8', 'Union', 'ValidationError', 'Validator', 'Computed', 'this', 'Bits', 'Byte', 'Bytes', 'Tunnel', 'Embed', 'Const', 'ConstError', 
]
