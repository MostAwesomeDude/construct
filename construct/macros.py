import six
from construct.lib.py3compat import int2byte
from construct.lib import (BitStreamReader, BitStreamWriter, encode_bin, decode_bin)
from construct.core import (Struct, MetaField, StaticField, FormatField,
    OnDemand, Pointer, Switch, Value, RepeatUntil, MetaArray, Sequence, Range,
    Select, Pass, SizeofError, Buffered, Restream, Reconfig)
from construct.adapters import (BitIntegerAdapter, PaddingAdapter,
    ConstAdapter, CStringAdapter, LengthValueAdapter, IndexingAdapter,
    PaddedStringAdapter, FlagsAdapter, StringAdapter, MappingAdapter)
try:
    from sys import maxsize
except ImportError:
    from sys import maxint as maxsize


#===============================================================================
# fields
#===============================================================================
def Field(name, length):
    """
    A field consisting of a specified number of bytes.

    :param name: the name of the field
    :param length: the length of the field. the length can be either an integer
      (StaticField), or a function that takes the context as an argument and
      returns the length (MetaField)
    """
    if callable(length):
        return MetaField(name, length)
    else:
        return StaticField(name, length)

def BitField(name, length, swapped = False, signed = False, bytesize = 8):
    r"""
    BitFields, as the name suggests, are fields that operate on raw, unaligned
    bits, and therefore must be enclosed in a BitStruct. Using them is very
    similar to all normal fields: they take a name and a length (in bits).

    :param name: name of the field
    :param length: number of bits in the field, or a function that takes
                   the context as its argument and returns the length
    :param swapped: whether the value is byte-swapped
    :param signed: whether the value is signed
    :param bytesize: number of bits per byte, for byte-swapping

    Example::
    
        >>> foo = BitStruct("foo",
        ...     BitField("a", 3),
        ...     Flag("b"),
        ...     Padding(3),
        ...     Nibble("c"),
        ...     BitField("d", 5),
        ... )
        >>> foo.parse("\xe1\x1f")
        Container(a = 7, b = False, c = 8, d = 31)
        >>> foo = BitStruct("foo",
        ...     BitField("a", 3),
        ...     Flag("b"),
        ...     Padding(3),
        ...     Nibble("c"),
        ...     Struct("bar",
        ...             Nibble("d"),
        ...             Bit("e"),
        ...     )
        ... )
        >>> foo.parse("\xe1\x1f")
        Container(a = 7, b = False, bar = Container(d = 15, e = 1), c = 8)
    """

    return BitIntegerAdapter(Field(name, length),
        length,
        swapped=swapped,
        signed=signed,
        bytesize=bytesize
    )

def Padding(length, pattern = six.b("\x00"), strict = False):
    r"""a padding field (value is discarded)
    
    :param length: the length of the field. the length can be either an integer,
                   or a function that takes the context as an argument and returns the length
    :param pattern: the padding pattern (character) to use. default is "\x00"
    :param strict: whether or not to raise an exception is the actual padding
                   pattern mismatches the desired pattern. default is False.
    """
    return PaddingAdapter(Field(None, length),
        pattern = pattern,
        strict = strict,
    )

def Flag(name, truth = 1, falsehood = 0, default = False):
    """
    A flag.

    Flags are usually used to signify a Boolean value, and this construct
    maps values onto the ``bool`` type.

    .. note:: This construct works with both bit and byte contexts.

    .. warning:: Flags default to False, not True. This is different from the
        C and Python way of thinking about truth, and may be subject to change
        in the future.

    :param name: field name
    :param truth: value of truth (default 1)
    :param falsehood: value of falsehood (default 0)
    :param default: default value (default False)
    """

    return SymmetricMapping(Field(name, 1),
        {True : int2byte(truth), False : int2byte(falsehood)},
        default = default,
    )

#===============================================================================
# field shortcuts
#===============================================================================
def Bit(name):
    """a 1-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 1)
def Nibble(name):
    """a 4-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 4)
def Octet(name):
    """an 8-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 8)

def UBInt8(name):
    """unsigned, big endian 8-bit integer"""
    return FormatField(name, ">", "B")
def UBInt16(name):
    """unsigned, big endian 16-bit integer"""
    return FormatField(name, ">", "H")
def UBInt32(name):
    """unsigned, big endian 32-bit integer"""
    return FormatField(name, ">", "L")
def UBInt64(name):
    """unsigned, big endian 64-bit integer"""
    return FormatField(name, ">", "Q")

def SBInt8(name):
    """signed, big endian 8-bit integer"""
    return FormatField(name, ">", "b")
def SBInt16(name):
    """signed, big endian 16-bit integer"""
    return FormatField(name, ">", "h")
def SBInt32(name):
    """signed, big endian 32-bit integer"""
    return FormatField(name, ">", "l")
def SBInt64(name):
    """signed, big endian 64-bit integer"""
    return FormatField(name, ">", "q")

def ULInt8(name):
    """unsigned, little endian 8-bit integer"""
    return FormatField(name, "<", "B")
def ULInt16(name):
    """unsigned, little endian 16-bit integer"""
    return FormatField(name, "<", "H")
def ULInt32(name):
    """unsigned, little endian 32-bit integer"""
    return FormatField(name, "<", "L")
def ULInt64(name):
    """unsigned, little endian 64-bit integer"""
    return FormatField(name, "<", "Q")

def SLInt8(name):
    """signed, little endian 8-bit integer"""
    return FormatField(name, "<", "b")
def SLInt16(name):
    """signed, little endian 16-bit integer"""
    return FormatField(name, "<", "h")
def SLInt32(name):
    """signed, little endian 32-bit integer"""
    return FormatField(name, "<", "l")
def SLInt64(name):
    """signed, little endian 64-bit integer"""
    return FormatField(name, "<", "q")

def UNInt8(name):
    """unsigned, native endianity 8-bit integer"""
    return FormatField(name, "=", "B")
def UNInt16(name):
    """unsigned, native endianity 16-bit integer"""
    return FormatField(name, "=", "H")
def UNInt32(name):
    """unsigned, native endianity 32-bit integer"""
    return FormatField(name, "=", "L")
def UNInt64(name):
    """unsigned, native endianity 64-bit integer"""
    return FormatField(name, "=", "Q")

def SNInt8(name):
    """signed, native endianity 8-bit integer"""
    return FormatField(name, "=", "b")
def SNInt16(name):
    """signed, native endianity 16-bit integer"""
    return FormatField(name, "=", "h")
def SNInt32(name):
    """signed, native endianity 32-bit integer"""
    return FormatField(name, "=", "l")
def SNInt64(name):
    """signed, native endianity 64-bit integer"""
    return FormatField(name, "=", "q")

def BFloat32(name):
    """big endian, 32-bit IEEE floating point number"""
    return FormatField(name, ">", "f")
def LFloat32(name):
    """little endian, 32-bit IEEE floating point number"""
    return FormatField(name, "<", "f")
def NFloat32(name):
    """native endianity, 32-bit IEEE floating point number"""
    return FormatField(name, "=", "f")

def BFloat64(name):
    """big endian, 64-bit IEEE floating point number"""
    return FormatField(name, ">", "d")
def LFloat64(name):
    """little endian, 64-bit IEEE floating point number"""
    return FormatField(name, "<", "d")
def NFloat64(name):
    """native endianity, 64-bit IEEE floating point number"""
    return FormatField(name, "=", "d")


#===============================================================================
# arrays
#===============================================================================
def Array(count, subcon):
    r"""
    Repeats the given unit a fixed number of times.

    :param count: number of times to repeat
    :param subcon: construct to repeat

    Example::
    
        >>> c = Array(4, UBInt8("foo"))
        >>> c.parse("\x01\x02\x03\x04")
        [1, 2, 3, 4]
        >>> c.parse("\x01\x02\x03\x04\x05\x06")
        [1, 2, 3, 4]
        >>> c.build([5,6,7,8])
        '\x05\x06\x07\x08'
        >>> c.build([5,6,7,8,9])
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 4..4, found 5
    """

    if callable(count):
        con = MetaArray(count, subcon)
    else:
        con = MetaArray(lambda ctx: count, subcon)
        con._clear_flag(con.FLAG_DYNAMIC)
    return con

def PrefixedArray(subcon, length_field = UBInt8("length")):
    """an array prefixed by a length field.
    
    :param subcon: the subcon to be repeated
    :param length_field: a construct returning an integer
    """
    return LengthValueAdapter(
        Sequence(subcon.name,
            length_field,
            Array(lambda ctx: ctx[length_field.name], subcon),
            nested = False
        )
    )

def OpenRange(mincount, subcon):
    return Range(mincount, maxsize, subcon)

def GreedyRange(subcon):
    r"""
    Repeats the given unit one or more times.

    :param subcon: construct to repeat

    Example::
    
        >>> from construct import GreedyRange, UBInt8
        >>> c = GreedyRange(UBInt8("foo"))
        >>> c.parse("\x01")
        [1]
        >>> c.parse("\x01\x02\x03")
        [1, 2, 3]
        >>> c.parse("\x01\x02\x03\x04\x05\x06")
        [1, 2, 3, 4, 5, 6]
        >>> c.parse("")
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 1..2147483647, found 0
        >>> c.build([1,2])
        '\x01\x02'
        >>> c.build([])
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 1..2147483647, found 0
    """
    return OpenRange(1, subcon)

def OptionalGreedyRange(subcon):
    r"""
    Repeats the given unit zero or more times. This repeater can't
    fail, as it accepts lists of any length.

    :param subcon: construct to repeat

    Example::
    
        >>> from construct import OptionalGreedyRange, UBInt8
        >>> c = OptionalGreedyRange(UBInt8("foo"))
        >>> c.parse("")
        []
        >>> c.parse("\x01\x02")
        [1, 2]
        >>> c.build([])
        ''
        >>> c.build([1,2])
        '\x01\x02'
    """
    return OpenRange(0, subcon)


#===============================================================================
# subconstructs
#===============================================================================
def Optional(subcon):
    """an optional construct. if parsing fails, returns None.
    
    :param subcon: the subcon to optionally parse or build
    """
    return Select(subcon.name, subcon, Pass)

def Bitwise(subcon):
    """converts the stream to bits, and passes the bitstream to subcon
    
    :param subcon: a bitwise construct (usually BitField)
    """
    # subcons larger than MAX_BUFFER will be wrapped by Restream instead
    # of Buffered. implementation details, don't stick your nose in :)
    MAX_BUFFER = 1024 * 8
    def resizer(length):
        if length & 7:
            raise SizeofError("size must be a multiple of 8", length)
        return length >> 3
    if not subcon._is_flag(subcon.FLAG_DYNAMIC) and subcon.sizeof() < MAX_BUFFER:
        con = Buffered(subcon,
            encoder = decode_bin,
            decoder = encode_bin,
            resizer = resizer
        )
    else:
        con = Restream(subcon,
            stream_reader = BitStreamReader,
            stream_writer = BitStreamWriter,
            resizer = resizer)
    return con

def Aligned(subcon, modulus = 4, pattern = six.b("\x00")):
    r"""aligns subcon to modulus boundary using padding pattern
    
    :param subcon: the subcon to align
    :param modulus: the modulus boundary (default is 4)
    :param pattern: the padding pattern (default is \x00)
    """
    if modulus < 2:
        raise ValueError("modulus must be >= 2", modulus)
    def padlength(ctx):
        return (modulus - (subcon._sizeof(ctx) % modulus)) % modulus
    return SeqOfOne(subcon.name,
        subcon,
        # ??????
        # ??????
        # ??????
        # ??????
        Padding(padlength, pattern = pattern),
        nested = False,
    )

def SeqOfOne(name, *args, **kw):
    r"""a sequence of one element. only the first element is meaningful, the
    rest are discarded
    
    :param name: the name of the sequence
    :param \*args: subconstructs
    :param \*\*kw: any keyword arguments to Sequence
    """
    return IndexingAdapter(Sequence(name, *args, **kw), index = 0)

def Embedded(subcon):
    """embeds a struct into the enclosing struct.
    
    :param subcon: the struct to embed
    """
    return Reconfig(subcon.name, subcon, subcon.FLAG_EMBED)

def Rename(newname, subcon):
    """renames an existing construct
    
    :param newname: the new name
    :param subcon: the subcon to rename
    """
    return Reconfig(newname, subcon)

def Alias(newname, oldname):
    """creates an alias for an existing element in a struct
    
    :param newname: the new name
    :param oldname: the name of an existing element
    """
    return Value(newname, lambda ctx: ctx[oldname])


#===============================================================================
# mapping
#===============================================================================
def SymmetricMapping(subcon, mapping, default = NotImplemented):
    """defines a symmetrical mapping: a->b, b->a.
    
    :param subcon: the subcon to map
    :param mapping: the encoding mapping (a dict); the decoding mapping is
                    achieved by reversing this mapping
    :param default: the default value to use when no mapping is found. if no
                    default value is given, and exception is raised. setting to Pass would
                    return the value "as is" (unmapped)
    """
    reversed_mapping = dict((v, k) for k, v in mapping.items())
    return MappingAdapter(subcon,
        encoding = mapping,
        decoding = reversed_mapping,
        encdefault = default,
        decdefault = default,
    )

def Enum(subcon, **kw):
    r"""a set of named values mapping.
    
    :param subcon: the subcon to map
    :param \*\*kw: - keyword arguments which serve as the encoding mapping
    :param _default_: an optional, keyword-only argument that specifies the
                      default value to use when the mapping is undefined. if not given,
                      and exception is raised when the mapping is undefined. use `Pass` to
                      pass the unmapped value as-is
    """
    return SymmetricMapping(subcon, kw, kw.pop("_default_", NotImplemented))

def FlagsEnum(subcon, **kw):
    r"""a set of flag values mapping.
    
    :param subcon: the subcon to map
    :param \*\*kw: keyword arguments which serve as the encoding mapping
    """
    return FlagsAdapter(subcon, kw)


#===============================================================================
# structs
#===============================================================================
def AlignedStruct(name, *subcons, **kw):
    r"""a struct of aligned fields
    
    :param name: the name of the struct
    :param \*subcons: the subcons that make up this structure
    :param \*\*kw: keyword arguments to pass to Aligned: 'modulus' and 'pattern'
    """
    return Struct(name, *(Aligned(sc, **kw) for sc in subcons))

def BitStruct(name, *subcons):
    r"""a struct of bitwise fields
    :param name: the name of the struct
    :param \*subcons: the subcons that make up this structure
    """
    return Bitwise(Struct(name, *subcons))

def EmbeddedBitStruct(*subcons):
    r"""an embedded BitStruct. no name is necessary.
    
    :param \*subcons: - the subcons that make up this structure
    """
    return Bitwise(Embedded(Struct(None, *subcons)))

#===============================================================================
# strings
#===============================================================================
def String(name, length, encoding=None, padchar=None, paddir="right",
        trimdir="right"):
    r"""
    A configurable, fixed-length string field.

    The padding character must be specified for padding and trimming to work.

    :param name: name
    :param length: length, in bytes
    :param encoding: encoding (e.g. "utf8") or None for no encoding
    :param padchar: optional character to pad out strings
    :param paddir: direction to pad out strings; one of "right", "left", or "both"
    :param str trim: direction to trim strings; one of "right", "left"

    Example::
    
        >>> from construct import String
        >>> String("foo", 5).parse("hello")
        'hello'
        >>>
        >>> String("foo", 12, encoding = "utf8").parse("hello joh\xd4\x83n")
        u'hello joh\u0503n'
        >>>
        >>> foo = String("foo", 10, padchar = "X", paddir = "right")
        >>> foo.parse("helloXXXXX")
        'hello'
        >>> foo.build("hello")
        'helloXXXXX'
    """
    con = StringAdapter(Field(name, length), encoding=encoding)
    if padchar is not None:
        con = PaddedStringAdapter(con, padchar=padchar, paddir=paddir,
            trimdir=trimdir)
    return con

def PascalString(name, length_field=UBInt8("length"), encoding=None):
    r"""
    A length-prefixed string.

    ``PascalString`` is named after the string types of Pascal, which are
    length-prefixed. Lisp strings also follow this convention.

    The length field will appear in the same ``Container`` as the
    ``PascalString``, with the given name.

    :param name: name
    :param length_field: a field which will store the length of the string
    :param encoding: encoding (e.g. "utf8") or None for no encoding

    Example::
    
        >>> foo = PascalString("foo")
        >>> foo.parse("\x05hello")
        'hello'
        >>> foo.build("hello world")
        '\x0bhello world'
        >>>
        >>> foo = PascalString("foo", length_field = UBInt16("length"))
        >>> foo.parse("\x00\x05hello")
        'hello'
        >>> foo.build("hello")
        '\x00\x05hello'
    """

    return StringAdapter(
        LengthValueAdapter(
            Sequence(name,
                length_field,
                Field("data", lambda ctx: ctx[length_field.name]),
            )
        ),
        encoding=encoding,
    )

def CString(name, terminators=six.b("\x00"), encoding=None,
            char_field=Field(None, 1)):
    r"""
    A string ending in a terminator.

    ``CString`` is similar to the strings of C, C++, and other related
    programming languages.

    By default, the terminator is the NULL byte (b``0x00``).

    :param name: name
    :param terminators: sequence of valid terminators, in order of preference
    :param encoding: encoding (e.g. "utf8") or None for no encoding
    :param char_field: construct representing a single character

    Example::

        >>> foo = CString("foo")
        >>> foo.parse(b"hello\x00")
        b'hello'
        >>> foo.build(b"hello")
        b'hello\x00'
        >>> foo = CString("foo", terminators = b"XYZ")
        >>> foo.parse(b"helloX")
        b'hello'
        >>> foo.parse(b"helloY")
        b'hello'
        >>> foo.parse(b"helloZ")
        b'hello'
        >>> foo.build(b"hello")
        b'helloX'
    """

    return Rename(name,
        CStringAdapter(
            RepeatUntil(lambda obj, ctx: obj in terminators, char_field),
            terminators=terminators,
            encoding=encoding,
        )
    )


#===============================================================================
# conditional
#===============================================================================
def IfThenElse(name, predicate, then_subcon, else_subcon):
    """an if-then-else conditional construct: if the predicate indicates True,
    `then_subcon` will be used; otherwise `else_subcon`
    
    :param name: the name of the construct
    :param predicate: a function taking the context as an argument and returning True or False
    :param then_subcon: the subcon that will be used if the predicate returns True
    :param else_subcon: the subcon that will be used if the predicate returns False
    """
    return Switch(name, lambda ctx: bool(predicate(ctx)),
        {
            True : then_subcon,
            False : else_subcon,
        }
    )

def If(predicate, subcon, elsevalue = None):
    """an if-then conditional construct: if the predicate indicates True,
    subcon will be used; otherwise, `elsevalue` will be returned instead.
    
    :param predicate: a function taking the context as an argument and returning True or False
    :param subcon: the subcon that will be used if the predicate returns True
    :param elsevalue: the value that will be used should the predicate return False.
                      by default this value is None.
    """
    return IfThenElse(subcon.name,
        predicate,
        subcon,
        Value("elsevalue", lambda ctx: elsevalue)
    )


#===============================================================================
# misc
#===============================================================================
def OnDemandPointer(offsetfunc, subcon, force_build = True):
    """an on-demand pointer.
    
    :param offsetfunc: a function taking the context as an argument and returning
                       the absolute stream position
    :param subcon: the subcon that will be parsed from the `offsetfunc()` stream position on demand
    :param force_build: see OnDemand. by default True.
    """
    return OnDemand(Pointer(offsetfunc, subcon),
        advance_stream = False,
        force_build = force_build
    )

def Magic(data):
    """a 'magic number' construct. it is used for file signatures, etc., to validate
    that the given pattern exists.
    
    Example::
        
        elf_header = Struct("elf_header",
            Magic("\x7fELF"),
            # ...
        )
    """
    return ConstAdapter(Field(None, len(data)), data)


