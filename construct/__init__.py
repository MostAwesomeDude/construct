r"""
Construct 2 -- Parsing Made Fun

Homepage:
	https://github.com/construct/construct
    http://construct.readthedocs.org

Hands-on example:
    >>> from construct import *
    >>> s = Struct(
    ...     "a" / Byte,
    ...     "b" / Short,
    ... )
    >>> print s.parse(b"\x01\x02\x03")
    Container:
        a = 1
        b = 515
    >>> s.build(Container(a=1, b=0x0203))
    b"\x01\x02\x03"
"""

from construct.core import *
from construct.expr import *
from construct.debug import *
from construct.version import *
from construct import lib


#===============================================================================
# metadata
#===============================================================================
__author__ = "Arkadiusz Bulski <arek.bulski@gmail.com>, Tomer Filiba <tomerfiliba@gmail.com>, Corbin Simpson <MostAwesomeDude@gmail.com>"
__version__ = version_string

#===============================================================================
# exposed names
#===============================================================================
__all__ = [
    '__author__',
    '__version__',
    'abs_',
    'AdaptationError',
    'Adapter',
    'Aligned',
    'AlignedStruct',
    'Array',
    'Bit',
    'BitsInteger',
    'BitsSwapped',
    'BitStruct',
    'Bitwise',
    'Byte',
    'Bytes',
    'BytesInteger',
    'ByteSwapped',
    'Bytewise',
    'Check',
    'Checksum',
    'ChecksumError',
    'CompilableMacro',
    'Compiled',
    'Compressed',
    'Computed',
    'Const',
    'ConstError',
    'Construct',
    'ConstructError',
    'Container',
    'CString',
    'Debugger',
    'Decompiled',
    'Default',
    'Double',
    'Embedded',
    'Enum',
    'Error',
    'ExplicitError',
    'ExprAdapter',
    'ExprSymmetricAdapter',
    'ExprValidator',
    'Filter',
    'Flag',
    'FlagsContainer',
    'FlagsEnum',
    'FocusedSeq',
    'FormatField',
    'FormatFieldError',
    'FuncPath',
    'globalfullprinting',
    'globalstringencoding',
    'GreedyBytes',
    'GreedyRange',
    'GreedyString',
    'Hex',
    'HexDump',
    'If',
    'IfThenElse',
    'Index',
    'IndexFieldError',
    'Indexing',
    'Int',
    'IntegerError',
    'LazyBound',
    'LazyField',
    'len_',
    'lib',
    'list_',
    'ListContainer',
    'Long',
    'Mapping',
    'MappingError',
    'max_',
    'min_',
    'NamedTuple',
    'Nibble',
    'NoneOf',
    'Numpy',
    'obj_',
    'Octet',
    'OneOf',
    'Optional',
    'Padded',
    'Padding',
    'PaddingError',
    'PascalString',
    'Pass',
    'Path',
    'Path2',
    'Peek',
    'Pointer',
    'possiblestringencodings',
    'Prefixed',
    'PrefixedArray',
    'Probe',
    'ProbeInto',
    'RangeError',
    'RawCopy',
    'Rebuffered',
    'RebufferedBytesIO',
    'Rebuild',
    'release_date',
    'Renamed',
    'RepeatError',
    'RepeatUntil',
    'RestreamData',
    'Restreamed',
    'RestreamedBytesIO',
    'Seek',
    'Select',
    'SelectError',
    'Sequence',
    'setglobalfullprinting',
    'setglobalstringencoding',
    'Short',
    'Single',
    'SizeofError',
    'Slicing',
    'StopIf',
    'StreamError',
    'String',
    'StringEncoded',
    'StringError',
    'StringNullTerminated',
    'StringPaddedTrimmed',
    'StringsAsBytes',
    'Struct',
    'Subconstruct',
    'sum_',
    'Switch',
    'SwitchError',
    'SymmetricAdapter',
    'SymmetricMapping',
    'Tell',
    'Terminated',
    'TerminatedError',
    'this',
    'Tunnel',
    'Union',
    'UnionError',
    'ValidationError',
    'Validator',
    'VarInt',
    'version',
    'version_string',
]
__all__ += ["Int%s%s%s" % (n,us,bln) for n in (8,16,24,32,64) for us in "us" for bln in "bln"]
__all__ += ["Float%s%s" % (n,bl) for n in (32,64) for bl in "bl"]
