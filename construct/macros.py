from sys import maxsize

from construct.lib.py3compat import int2byte
from construct.lib import BitStreamReader, BitStreamWriter, encode_bin, decode_bin
from construct.core import Construct, Struct, MetaField, StaticField, FormatField, OnDemand, Pointer, Switch, Computed, RepeatUntil, MetaArray, Sequence, Range, Select, Pass, SizeofError, Buffered, Restream, Reconfig, Padding, Const
from construct.core import _read_stream, _write_stream
from construct.adapters import BitIntegerAdapter, CStringAdapter, LengthValueAdapter, IndexingAdapter, PaddedStringAdapter, FlagsAdapter, StringAdapter, MappingAdapter


#===============================================================================
# fields
#===============================================================================
def Field(name, length):
    r"""
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

def BitField(name, length, swapped=False, signed=False, bytesize=8):
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

def Flag(name, truth=1, falsehood=0, default=False):
    r"""
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
    """A 1-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 1)
def Nibble(name):
    """A 4-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 4)
def Octet(name):
    """An 8-bit BitField; must be enclosed in a BitStruct"""
    return BitField(name, 8)

def UBInt8(name):
    """Unsigned, big endian 8-bit integer"""
    return FormatField(name, ">", "B")
def UBInt16(name):
    """Unsigned, big endian 16-bit integer"""
    return FormatField(name, ">", "H")
def UBInt32(name):
    """Unsigned, big endian 32-bit integer"""
    return FormatField(name, ">", "L")
def UBInt64(name):
    """Unsigned, big endian 64-bit integer"""
    return FormatField(name, ">", "Q")

def SBInt8(name):
    """Signed, big endian 8-bit integer"""
    return FormatField(name, ">", "b")
def SBInt16(name):
    """Signed, big endian 16-bit integer"""
    return FormatField(name, ">", "h")
def SBInt32(name):
    """Signed, big endian 32-bit integer"""
    return FormatField(name, ">", "l")
def SBInt64(name):
    """Signed, big endian 64-bit integer"""
    return FormatField(name, ">", "q")

def ULInt8(name):
    """Unsigned, little endian 8-bit integer"""
    return FormatField(name, "<", "B")
def ULInt16(name):
    """Unsigned, little endian 16-bit integer"""
    return FormatField(name, "<", "H")
def ULInt32(name):
    """Unsigned, little endian 32-bit integer"""
    return FormatField(name, "<", "L")
def ULInt64(name):
    """Unsigned, little endian 64-bit integer"""
    return FormatField(name, "<", "Q")

def SLInt8(name):
    """Signed, little endian 8-bit integer"""
    return FormatField(name, "<", "b")
def SLInt16(name):
    """Signed, little endian 16-bit integer"""
    return FormatField(name, "<", "h")
def SLInt32(name):
    """Signed, little endian 32-bit integer"""
    return FormatField(name, "<", "l")
def SLInt64(name):
    """Signed, little endian 64-bit integer"""
    return FormatField(name, "<", "q")

def UNInt8(name):
    """Unsigned, native endianity 8-bit integer"""
    return FormatField(name, "=", "B")
def UNInt16(name):
    """Unsigned, native endianity 16-bit integer"""
    return FormatField(name, "=", "H")
def UNInt32(name):
    """Unsigned, native endianity 32-bit integer"""
    return FormatField(name, "=", "L")
def UNInt64(name):
    """Unsigned, native endianity 64-bit integer"""
    return FormatField(name, "=", "Q")

def SNInt8(name):
    """Signed, native endianity 8-bit integer"""
    return FormatField(name, "=", "b")
def SNInt16(name):
    """Signed, native endianity 16-bit integer"""
    return FormatField(name, "=", "h")
def SNInt32(name):
    """Signed, native endianity 32-bit integer"""
    return FormatField(name, "=", "l")
def SNInt64(name):
    """Signed, native endianity 64-bit integer"""
    return FormatField(name, "=", "q")

def BFloat32(name):
    """Big endian, 32-bit IEEE floating point number"""
    return FormatField(name, ">", "f")
def LFloat32(name):
    """Little endian, 32-bit IEEE floating point number"""
    return FormatField(name, "<", "f")
def NFloat32(name):
    """Native endianity, 32-bit IEEE floating point number"""
    return FormatField(name, "=", "f")

def BFloat64(name):
    """Big endian, 64-bit IEEE floating point number"""
    return FormatField(name, ">", "d")
def LFloat64(name):
    """Little endian, 64-bit IEEE floating point number"""
    return FormatField(name, "<", "d")
def NFloat64(name):
    """Native endianity, 64-bit IEEE floating point number"""
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

def PrefixedArray(subcon, length_field=UBInt8("length")):
    r"""
    An array prefixed by a length field.

    :param subcon: the subcon to be repeated
    :param length_field: a construct returning an integer
    """
    def _length(ctx):
      if issubclass(ctx.__class__, (list, tuple)):
        return len(ctx)
      return ctx[length_field.name]

    return LengthValueAdapter(
        Sequence(subcon.name,
            length_field,
            Array(_length, subcon),
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
    r"""
    An optional construct. if parsing fails, returns None.

    :param subcon: the subcon to optionally parse or build
    """
    return Select(subcon.name, subcon, Pass)

def Bitwise(subcon):
    r"""
    Converts the stream to bits, and passes the bitstream to subcon

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


def SeqOfOne(name, *args, **kw):
    r"""
    A sequence of one element. only the first element is meaningful, the
    rest are discarded

    :param name: the name of the sequence
    :param \*args: subconstructs
    :param \*\*kw: any keyword arguments to Sequence
    """
    return IndexingAdapter(Sequence(name, *args, **kw), index = 0)

def Embedded(subcon):
    r"""
    Embeds a struct into the enclosing struct.

    :param subcon: the struct to embed
    """
    return Reconfig(subcon.name, subcon, subcon.FLAG_EMBED)

def Rename(newname, subcon):
    r"""
    Renames an existing construct

    :param newname: the new name
    :param subcon: the subcon to rename
    """
    return Reconfig(newname, subcon)

def Alias(newname, oldname):
    r"""
    Creates an alias for an existing element in a struct

    :param newname: the new name
    :param oldname: the name of an existing element
    """
    return Computed(newname, lambda ctx: ctx[oldname])


#===============================================================================
# mapping
#===============================================================================
def SymmetricMapping(subcon, mapping, default=NotImplemented):
    r"""
    Defines a symmetrical mapping: a->b, b->a.

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
    r"""
    A set of named values mapping.

    :param subcon: the subcon to map
    :param \*\*kw: keyword arguments which serve as the encoding mapping
    :param _default_: an optional, keyword-only argument that specifies the
                      default value to use when the mapping is undefined. if not given,
                      and exception is raised when the mapping is undefined. use `Pass` to
                      pass the unmapped value as-is
    """
    return SymmetricMapping(subcon, kw, kw.pop("_default_", NotImplemented))

def FlagsEnum(subcon, **kw):
    r"""
    A set of flag values mapping.

    :param subcon: the subcon to map
    :param \*\*kw: keyword arguments which serve as the encoding mapping
    """
    return FlagsAdapter(subcon, kw)


#===============================================================================
# structs
#===============================================================================
def AlignedStruct(name, *subcons, **kw):
    r"""
    A struct of aligned fields

    :param name: the name of the struct
    :param \*subcons: the subcons that make up this structure
    :param \*\*kw: keyword arguments to pass to Aligned: 'modulus' and 'pattern'
    """
    return Struct(name, *(Aligned(sc, **kw) for sc in subcons))

def BitStruct(name, *subcons):
    r"""
    A struct of bitwise fields

    :param name: the name of the struct
    :param \*subcons: the subcons that make up this structure
    """
    return Bitwise(Struct(name, *subcons))

def EmbeddedBitStruct(*subcons):
    r"""
    An embedded BitStruct. no name is necessary.

    :param \*subcons: the subcons that make up this structure
    """
    return Bitwise(Embedded(Struct(None, *subcons)))


#===============================================================================
# strings
#===============================================================================


#===============================================================================
# conditional
#===============================================================================
def IfThenElse(name, predicate, then_subcon, else_subcon):
    r"""
    An if-then-else conditional construct: if the predicate indicates True,
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

def If(predicate, subcon, elsevalue=None):
    r"""
    An if-then conditional construct: if the predicate indicates True,
    subcon will be used; otherwise, `elsevalue` will be returned instead.

    :param predicate: a function taking the context as an argument and returning True or False
    :param subcon: the subcon that will be used if the predicate returns True
    :param elsevalue: the value that will be used should the predicate return False.
                      by default this value is None.
    """
    return IfThenElse(subcon.name,
        predicate,
        subcon,
        Computed("elsevalue", lambda ctx: elsevalue)
    )


#===============================================================================
# misc
#===============================================================================
def OnDemandPointer(offsetfunc, subcon, force_build=True):
    r"""
    An on-demand pointer.

    :param offsetfunc: a function taking the context as an argument and returning
                       the absolute stream position
    :param subcon: the subcon that will be parsed from the `offsetfunc()` stream position on demand
    :param force_build: see OnDemand. by default True.
    """
    return OnDemand(Pointer(offsetfunc, subcon),
        advance_stream = False,
        force_build = force_build
    )


class PascalString(Construct):
    r"""
    A length-prefixed string.

    ``PascalString`` is named after the string types of Pascal, which are length-prefixed. Lisp strings also follow this convention.

    The length field will not appear in the same ``Container``, when parsing. Only the string will be returned. When building, the length is taken from len(the string). The length field can be anonymous (name is None) and can be variable length (such as VarInt).

    :param name: name
    :param lengthfield: a field which will store the length of the string
    :param encoding: encoding (e.g. "utf8") or None for bytes

    Example::

        PascalString("string", ULInt32(None))
        .parse(b"\x05\x00\x00\x00hello") -> "hello"
        .build("hello") -> -> b"\x05\x00\x00\x00hello"

        PascalString("string", ULInt32(None), encoding="utf8")
        .parse(b"\x05\x00\x00\x00hello") -> u"hello"
        .build(u"hello") -> -> b"\x05\x00\x00\x00hello"
    """
    __slots__ = ["name", "lengthfield", "encoding"]
    def __init__(self, name, lengthfield=UBInt8(None), encoding=None):
        super(PascalString, self).__init__(name)
        self.lengthfield = lengthfield
        self.encoding = encoding
    def _parse(self, stream, context):
        length = self.lengthfield._parse(stream, context)
        obj = _read_stream(stream, length)
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.decode(self.encoding)
            else:
                obj = self.encoding.decode(obj)
        return obj
    def _build(self, obj, stream, context):
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.encode(self.encoding)
            else:
                obj = self.encoding.encode(obj)
        else:
            if not isinstance(obj, bytes):
                raise StringError("no encoding provided but building from unicode string?")
        self.lengthfield._build(len(obj), stream, context)
        _write_stream(stream, len(obj), obj)
    def _sizeof(self, context):
        raise SizeofError("cannot calculate size")


class CString(Construct):
    r"""
    A string ending in a terminator bytes character.

    ``CString`` is similar to the strings of C, C++, and other related
    programming languages.

    By default, the terminator is the NULL byte (b'\x00'). Terminators field can be a longer bytes string, and any of the characters breaks parsing. First character is used when building.

    :param name: name
    :param terminators: sequence of valid terminators, in order of preference
    :param encoding: encoding (e.g. "utf8") or None for bytes

    Example::

        CString("text")
        .parse(b"hello\x00") -> b"hello"
        .build(b"hello") -> b"hello\x00"

        CString("text", terminators=b"XYZ")
        .parse(b"helloX") -> b"hello"
        .parse(b"helloY") -> b"hello"
        .parse(b"helloZ") -> b"hello"
        .build(b"hello") -> b"helloX"
    """
    __slots__ = ["name", "terminators", "encoding", "charfield"]
    def __init__(self, name, terminators=b"\x00", encoding=None):
        if len(terminators) < 1:
            raise ValueError("terminators must be a bytes string of length >= 1")
        super(CString, self).__init__(name)
        self.terminators = terminators
        self.encoding = encoding
    def _parse(self, stream, context):
        obj = b""
        while True:
            char = _read_stream(stream, 1)
            if char in self.terminators:
                break
            obj += char
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.decode(self.encoding)
            else:
                obj = self.encoding.decode(obj)
        return obj
    def _build(self, obj, stream, context):
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.encode(self.encoding)
            else:
                obj = self.encoding.encode(obj)
        else:
            if not isinstance(obj, bytes):
                raise StringError("no encoding provided but building from unicode string?")
        obj += self.terminators[:1]
        _write_stream(stream, len(obj), obj)
    def _sizeof(self, context):
        raise SizeofError("cannot calculate size")


class GreedyString(Construct):
    r"""
    A string that reads the rest of the stream until EOF, or writes a given string as is.

    :param name: name
    :param encoding: encoding (e.g. "utf8") or None for bytes

    Example::

        GreedyString("greedy")
        .parse(b"hello\x00") -> b"hello\x00"
        .build(b"hello\x00") -> b"hello\x00"

        GreedyString("greedy", encoding="utf8")
        .parse(b"hello\x00") -> u"hello\x00"
        .build(u"hello\x00") -> b"hello\x00"
    """
    __slots__ = ["name", "encoding"]
    def __init__(self, name, encoding=None):
        super(GreedyString, self).__init__(name)
        self.encoding = encoding
    def _parse(self, stream, context):
        obj = stream.read()
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.decode(self.encoding)
            else:
                obj = self.encoding.decode(obj)
        return obj
    def _build(self, obj, stream, context):
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.encode(self.encoding)
            else:
                obj = self.encoding.encode(obj)
        else:
            if not isinstance(obj, bytes):
                raise StringError("no encoding provided but building from unicode string?")
        _write_stream(stream, len(obj), obj)
    def _sizeof(self, context):
        raise SizeofError("cannot calculate size")


