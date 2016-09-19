import struct
from struct import Struct as Packer
from struct import error as PackerError
from io import BytesIO, StringIO
from binascii import hexlify
import sys
import collections
import codecs

from construct.lib.container import Container, FlagsContainer, ListContainer, LazyContainer, LazyRangeContainer, LazySequenceContainer
from construct.lib.binary import integer2bits, integer2bytes, onebit2integer, bits2integer, bytes2integer, bytes2bits, bits2bytes, swapbytes
from construct.lib.bitstream import RestreamedBytesIO
from construct.lib.hex import HexString, hexdump
from construct.lib.py3compat import PY3, PY26, PYPY, stringtypes, int2byte, byte2int, str2bytes, bytes2str, str2unicode, unicode2str, iteratebytes, iterateints


#===============================================================================
# exceptions
#===============================================================================
class ConstructError(Exception):
    pass
class FieldError(ConstructError):
    pass
class SizeofError(ConstructError):
    pass
class AdaptationError(ConstructError):
    pass
class ArrayError(ConstructError):
    pass
class RangeError(ConstructError):
    pass
class SwitchError(ConstructError):
    pass
class SelectError(ConstructError):
    pass
class TerminatorError(ConstructError):
    pass
class OverwriteError(ConstructError):
    pass
class PaddingError(ConstructError):
    pass
class ConstError(ConstructError):
    pass
class StringError(ConstructError):
    pass
class ChecksumError(ConstructError):
    pass
class ValidationError(ConstructError):
    pass
class BitIntegerError(ConstructError):
    pass
class MappingError(AdaptationError):
    pass


#===============================================================================
# internal code
#===============================================================================
def singleton(cls):
    return cls()

def singletonfunction(func):
    return func()

def _read_stream(stream, length):
    # if not isinstance(length, int):
    #     raise TypeError("expected length to be int")
    if length < 0:
        raise ValueError("length must be >= 0", length)
    data = stream.read(length)
    if len(data) != length:
        raise FieldError("could not read enough bytes, expected %d, found %d" % (length, len(data)))
    return data

def _write_stream(stream, length, data):
    # if not isinstance(data, bytes):
    #     raise TypeError("expected data to be a bytes")
    if length < 0:
        raise ValueError("length must be >= 0", length)
    if len(data) != length:
        raise FieldError("could not write bytes, expected %d, found %d" % (length, len(data)))
    written = stream.write(data)
    if written != length:
        raise FieldError("could not write bytes, written %d, should %d" % (written, length))

def _subobj(sc, obj):
    if sc.flagembedded:
        return obj
    else:
        return obj[sc.name]

def _updcon(con, sc, obj):
    if sc.flagembedded:
        con.update(obj)
    else:
        con[sc.name] = obj


#===============================================================================
# abstract constructs
#===============================================================================
class Construct(object):
    r"""
    The mother of all constructs.

    This object is generally not directly instantiated, and it does not directly implement parsing and building, so it is largely only of interest to subclass implementors.

    The external user API:

     * ``parse()``
     * ``parse_stream()``
     * ``build()``
     * ``build_stream()``
     * ``sizeof()``

    Subclass authors should not override the external methods. Instead, another API is available:

     * ``_parse()``
     * ``_build()``
     * ``_sizeof()``

    There is also a flag API:

     * ``_inherit_flags()``

    And stateful copying:

     * ``__getstate__()``
     * ``__setstate__()``

    Attributes and Inheritance
    ==========================

    All constructs have a name and flags. The name is used for naming struct members and context dictionaries. Note that the name can either be a string, or None if the name is not needed. A single underscore ("_") is a reserved name, and so are names starting with a less-than character ("<"). The name should be descriptive, short, and valid as a Python identifier, although these rules are not enforced.

    The flags specify additional behavioral information about this construct. Flags are used by enclosing constructs to determine a proper course of action. Flags are inherited by default, from inner subconstructs to outer constructs. The enclosing construct may set new flags or clear existing ones, as necessary.
    """

    __slots__ = ["name", "flagbuildnone", "flagembedded"]
    def __init__(self):
        self.name = None
        self.flagbuildnone = False
        self.flagembedded = False

    def __repr__(self):
        return "<%s: %s%s%s>" % (self.__class__.__name__, self.name, " nonbuild" if self.flagbuildnone else "", " embedded" if self.flagembedded else "")

    def _inherit_flags(self, *subcons):
        for sc in subcons:
            self.flagbuildnone |= sc.flagbuildnone
            self.flagembedded |= sc.flagembedded

    def __getstate__(self):
        # Obtain a dictionary representing this construct's state.
        attrs = {}
        if hasattr(self, "__dict__"):
            attrs.update(self.__dict__)
        slots = []
        c = self.__class__
        while c is not None:
            if hasattr(c, "__slots__"):
                slots.extend(c.__slots__)
            c = c.__base__
        for name in slots:
            if hasattr(self, name):
                attrs[name] = getattr(self, name)
        return attrs

    def __setstate__(self, attrs):
        # Set this construct's state to a given state.
        for name, value in attrs.items():
            setattr(self, name, value)

    def __copy__(self):
        # Returns a copy of this construct.
        self2 = object.__new__(self.__class__)
        self2.__setstate__(self, self.__getstate__())
        return self2

    def parse(self, data, context=None):
        """
        Parse an in-memory buffer.

        Strings, buffers, memoryviews, and other complete buffers can be parsed with this method.
        """
        return self.parse_stream(BytesIO(data), context)

    def parse_stream(self, stream, context=None):
        """
        Parse a stream.

        Files, pipes, sockets, and other streaming sources of data are handled by this method.
        """
        if context is None:
            context = Container()
        return self._parse(stream, context)

    def _parse(self, stream, context):
        """
        Override in your subclass.
        """
        raise NotImplementedError()

    def build(self, obj, context=None):
        """
        Build an object in memory.

        :returns: bytes
        """
        stream = BytesIO()
        self.build_stream(obj, stream, context)
        return stream.getvalue()

    def build_stream(self, obj, stream, context=None):
        """
        Build an object directly into a stream.

        :returns: None
        """
        if context is None:
            context = Container()
        self._build(obj, stream, context)

    def _build(self, obj, stream, context):
        """
        Override in your subclass.
        """
        raise NotImplementedError()

    def sizeof(self, context=None):
        """
        Calculate the size of this object, optionally using a context.

        Some constructs have no fixed size and can only know their size for a given hunk of data. These constructs will raise an error if they are not passed a context.

        :param context: a container

        :returns: int of the length of this construct
        :raises SizeofError: the size could not be determined
        """
        if context is None:
            context = Container()
        return self._sizeof(context)

    def _sizeof(self, context):
        """
        Override in your subclass.
        """
        raise SizeofError("cannot calculate size")

    def __getitem__(self, count):
        if isinstance(count, slice):
            if count.step:
                raise ValueError("Slice must not contain as step: %r" % (count,))
            return Range(count.start, count.stop, self)
        elif isinstance(count, int) or hasattr(count, "__call__"):
            return Range(count, count, self)
        else:
            raise TypeError("Expected a number, a contextual expression or a slice thereof, got %r" % (count,))

    def __rshift__(self, other):
        if isinstance(self, Sequence):
            return Sequence(*(list(self.subcons)+[other]))
        else:
            return Sequence(self, other)

    def __rtruediv__(self, name):
        if name is not None:
            if not isinstance(name, stringtypes):
                raise TypeError("name must be b-string or u-string or None", name)
        return Renamed(name, self)
    __rdiv__ = __rtruediv__


class Subconstruct(Construct):
    r"""
    Abstract subconstruct (wraps an inner construct, inheriting its name and flags).

    Subconstructs wrap an inner Construct, inheriting its name and flags.

    :param subcon: the construct to wrap
    """
    __slots__ = ["subcon"]
    def __init__(self, subcon):
        if not isinstance(subcon, Construct):
            raise TypeError("subcon should be a Construct field")
        super(Subconstruct, self).__init__()
        self.name = subcon.name
        self.subcon = subcon
        self._inherit_flags(subcon)
    def _parse(self, stream, context):
        return self.subcon._parse(stream, context)
    def _build(self, obj, stream, context):
        return self.subcon._build(obj, stream, context)
    def _sizeof(self, context):
        return self.subcon._sizeof(context)


class Adapter(Subconstruct):
    r"""
    Abstract adapter parent class.

    Needs to implement ``_decode()`` and ``_encode()``.

    :param subcon: the construct to wrap
    """
    def _parse(self, stream, context):
        return self._decode(self.subcon._parse(stream, context), context)
    def _build(self, obj, stream, context):
        return self.subcon._build(self._encode(obj, context), stream, context)
    def _decode(self, obj, context):
        raise NotImplementedError()
    def _encode(self, obj, context):
        raise NotImplementedError()


class SymmetricAdapter(Subconstruct):
    r"""
    Abstract adapter parent class.

    Needs to implement ``_decode()`` only.

    :param subcon: the construct to wrap
    """
    def _parse(self, stream, context):
        return self._decode(self.subcon._parse(stream, context), context)
    def _build(self, obj, stream, context):
        return self.subcon._build(self._decode(obj, context), stream, context)
    def _decode(self, obj, context):
        raise NotImplementedError()


class Validator(SymmetricAdapter):
    r"""
    Abstract class: validates a condition on the encoded/decoded object.
    
    Needs to implement ``_validate()`` that returns bool.

    :param subcon: the subcon to validate
    """
    def _decode(self, obj, context):
        if not self._validate(obj, context):
            raise ValidationError("invalid object", obj)
        return obj
    def _validate(self, obj, context):
        raise NotImplementedError()


class Tunnel(Subconstruct):
    def _parse(self, stream, context):
        data = stream.read()  # reads entire stream
        data = self._decode(data, context)
        return self.subcon.parse(data, context)
    def _build(self, obj, stream, context):
        data = self.subcon.build(obj, context)
        data = self._encode(data, context)
        _write_stream(stream, len(data), data)
        return data
    def _sizeof(self, context):
        raise SizeofError("cannot calculate size")
    def _decode(self, data, context):
        raise NotImplementedError()
    def _encode(self, data, context):
        raise NotImplementedError()


#===============================================================================
# bytes and bits
#===============================================================================
class Bytes(Construct):
    r"""
    A field consisting of a specified number of bytes.

    :param length: the length of the field. the length can be either an integer
      (StaticField), or a function that takes the context as an argument and
      returns the length (MetaField)
    A fixed size byte field. 

    Can build from a byte string, or an integer.

    :param name: field name
    :param length: number of bytes in the field

    A variable-length field. The length is obtained at runtime from a function.

    :param name: name of the field
    :param lengthfunc: callable that takes a context and returns length as an int

    Example::

        >>> foo = Struct("foo",
        ...     Byte("length"),
        ...     MetaField("data", lambda ctx: ctx["length"])
        ... )
        >>> foo.parse("\x03ABC")
        Container(data = 'ABC', length = 3)
        >>> foo.parse("\x04ABCD")
        Container(data = 'ABCD', length = 4)
    """
    __slots__ = ["length"]
    def __init__(self, length):
        super(Bytes, self).__init__()
        self.length = length
    def _parse(self, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        return _read_stream(stream, length)
    def _build(self, obj, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        data = int2byte(obj) if isinstance(obj, int) else obj
        _write_stream(stream, length, data)
    def _sizeof(self, context):
        return self.length(context) if callable(self.length) else self.length


@singleton
class GreedyBytes(Construct):
    r"""
    A variable size byte field.

    Parses the stream to the end, and builds into the stream as is.

    Example::

        GreedyBytes

        .parse(b'hello') -> b'hello
        .build(b'hello') -> b'hello'
    """
    def _parse(self, stream, context):
        return stream.read()
    def _build(self, obj, stream, context):
        stream.write(obj)


class FormatField(Bytes):
    r"""
    A field that uses ``struct`` module to pack and unpack data.

    See ``struct`` documentation for instructions on crafting format strings.

    :param endianness: format endianness string, one of "<", ">", or "="
    :param format: a single format character
    """
    __slots__ = ["packer"]
    def __init__(self, endianity, format):
        if endianity not in (">", "<", "="):
            raise ValueError("endianity must be be '=', '<', or '>'",
                endianity)
        if len(format) != 1:
            raise ValueError("must specify one and only one format character")
        self.packer = Packer(endianity + format)
        super(FormatField, self).__init__(self.packer.size)
    def __getstate__(self):
        attrs = super(FormatField, self).__getstate__()
        attrs["packer"] = attrs["packer"].format
        return attrs
    def __setstate__(self, attrs):
        attrs["packer"] = Packer(attrs["packer"])
        return super(FormatField, self).__setstate__(attrs)
    def _parse(self, stream, context):
        try:
            return self.packer.unpack(_read_stream(stream, self.length))[0]
        except Exception:
            raise FieldError("packer %r error during parsing" % self.packer.format)
    def _build(self, obj, stream, context):
        try:
            _write_stream(stream, self.length, self.packer.pack(obj))
        except Exception:
            raise FieldError("packer %r error during building, given value %s" % (self.packer.format, obj))


def Bitwise(subcon):
    r"""
    Converts the stream to bits, and passes the bitstream to subcon.

    .. warning:: Do not use pointers inside.

    :param subcon: any field that works with bits: Bits, BitStruct, BitsNumber, Bit, Nibble, Octet, etc.
    """
    return Restreamed(subcon, bits2bytes, 8, bytes2bits, 1, lambda n: n//8)


def Bytewise(subcon):
    return Restreamed(subcon, bytes2bits, 1, bits2bytes, 8, lambda n: n*8)


class BytesInteger(Construct):
    __slots__ = ["length", "signed", "swapped", "bytesize"]
    def __init__(self, length, signed=False, swapped=False, bytesize=1):
        super(BytesInteger, self).__init__()
        self.length = length
        self.signed = signed
        self.swapped = swapped
        self.bytesize = bytesize
    def _parse(self, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        data = _read_stream(stream, length)
        if self.swapped:
            data = swapbytes(data, self.bytesize)
        return bytes2integer(data, self.signed)
    def _build(self, obj, stream, context):
        if obj < 0 and not self.signed:
            raise BitIntegerError("object is negative, but field is not signed", obj)
        length = self.length(context) if callable(self.length) else self.length
        data = integer2bytes(obj, length)
        if self.swapped:
            data = swapbytes(data, self.bytesize)
        _write_stream(stream, len(data), data)
    def _sizeof(self, context):
        return self.length(context) if callable(self.length) else self.length


class BitsInteger(Construct):
    r"""
    BitsInteger operates on raw, unaligned bits, and therefore must be enclosed in a BitStruct. Using it is very similar to BytesInteger.

    :param length: number of bits in the field, or a function that takes context and returns int
    :param signed: whether the value is signed (two's complement), default is False (unsigned)
    :param swapped: whether to swap byte order (little endian), default is False (big endian)
    :param bytesize: number of bits per byte as used for byte swapping (if swapped), default is 8

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
    __slots__ = ["length", "signed", "swapped", "bytesize"]
    def __init__(self, length, signed=False, swapped=False, bytesize=8):
        super(BitsInteger, self).__init__()
        self.length = length
        self.signed = signed
        self.swapped = swapped
        self.bytesize = bytesize
    def _parse(self, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        data = _read_stream(stream, length)
        if self.swapped:
            data = swapbytes(data, self.bytesize)
        return bits2integer(data, self.signed)
    def _build(self, obj, stream, context):
        if obj < 0 and not self.signed:
            raise BitIntegerError("object is negative, but field is not signed", obj)
        length = self.length(context) if callable(self.length) else self.length
        data = integer2bits(obj, length)
        if self.swapped:
            data = swapbytes(data, self.bytesize)
        _write_stream(stream, len(data), data)
    def _sizeof(self, context):
        return self.length(context) if callable(self.length) else self.length


#===============================================================================
# integers and floats
#===============================================================================
@singletonfunction
def Bit():
    """A 1-bit BitField; must be enclosed in a BitStruct"""
    return BitsInteger(1)
@singletonfunction
def Nibble():
    """A 4-bit BitField; must be enclosed in a BitStruct"""
    return BitsInteger(4)
@singletonfunction
def Octet():
    """An 8-bit BitField; must be enclosed in a BitStruct"""
    return BitsInteger(8)

@singletonfunction
def UBInt8():
    """Unsigned, big endian 8-bit integer"""
    return FormatField(">", "B")
@singletonfunction
def UBInt16():
    """Unsigned, big endian 16-bit integer"""
    return FormatField(">", "H")
@singletonfunction
def UBInt32():
    """Unsigned, big endian 32-bit integer"""
    return FormatField(">", "L")
@singletonfunction
def UBInt64():
    """Unsigned, big endian 64-bit integer"""
    return FormatField(">", "Q")

@singletonfunction
def SBInt8():
    """Signed, big endian 8-bit integer"""
    return FormatField(">", "b")
@singletonfunction
def SBInt16():
    """Signed, big endian 16-bit integer"""
    return FormatField(">", "h")
@singletonfunction
def SBInt32():
    """Signed, big endian 32-bit integer"""
    return FormatField(">", "l")
@singletonfunction
def SBInt64():
    """Signed, big endian 64-bit integer"""
    return FormatField(">", "q")

@singletonfunction
def ULInt8():
    """Unsigned, little endian 8-bit integer"""
    return FormatField("<", "B")
@singletonfunction
def ULInt16():
    """Unsigned, little endian 16-bit integer"""
    return FormatField("<", "H")
@singletonfunction
def ULInt32():
    """Unsigned, little endian 32-bit integer"""
    return FormatField("<", "L")
@singletonfunction
def ULInt64():
    """Unsigned, little endian 64-bit integer"""
    return FormatField("<", "Q")

@singletonfunction
def SLInt8():
    """Signed, little endian 8-bit integer"""
    return FormatField("<", "b")
@singletonfunction
def SLInt16():
    """Signed, little endian 16-bit integer"""
    return FormatField("<", "h")
@singletonfunction
def SLInt32():
    """Signed, little endian 32-bit integer"""
    return FormatField("<", "l")
@singletonfunction
def SLInt64():
    """Signed, little endian 64-bit integer"""
    return FormatField("<", "q")

@singletonfunction
def UNInt8():
    """Unsigned, native endianity 8-bit integer"""
    return FormatField("=", "B")
@singletonfunction
def UNInt16():
    """Unsigned, native endianity 16-bit integer"""
    return FormatField("=", "H")
@singletonfunction
def UNInt32():
    """Unsigned, native endianity 32-bit integer"""
    return FormatField("=", "L")
@singletonfunction
def UNInt64():
    """Unsigned, native endianity 64-bit integer"""
    return FormatField("=", "Q")

@singletonfunction
def SNInt8():
    """Signed, native endianity 8-bit integer"""
    return FormatField("=", "b")
@singletonfunction
def SNInt16():
    """Signed, native endianity 16-bit integer"""
    return FormatField("=", "h")
@singletonfunction
def SNInt32():
    """Signed, native endianity 32-bit integer"""
    return FormatField("=", "l")
@singletonfunction
def SNInt64():
    """Signed, native endianity 64-bit integer"""
    return FormatField("=", "q")

@singletonfunction
def BFloat32():
    """Big endian, 32-bit IEEE floating point number"""
    return FormatField(">", "f")
@singletonfunction
def LFloat32():
    """Little endian, 32-bit IEEE floating point number"""
    return FormatField("<", "f")
@singletonfunction
def NFloat32():
    """Native endianity, 32-bit IEEE floating point number"""
    return FormatField("=", "f")

@singletonfunction
def BFloat64():
    """Big endian, 64-bit IEEE floating point number"""
    return FormatField(">", "d")
@singletonfunction
def LFloat64():
    """Little endian, 64-bit IEEE floating point number"""
    return FormatField("<", "d")
@singletonfunction
def NFloat64():
    """Native endianity, 64-bit IEEE floating point number"""
    return FormatField("=", "d")


@singletonfunction
def UBInt24():
    r"""
    A 3-byte big-endian integer, as used in ancient file formats.
    """
    return BytesInteger(3)
@singletonfunction
def ULInt24():
    r"""
    A 3-byte little-endian integer, as used in ancient file formats.
    """
    return BytesInteger(3, swapped=True)


@singleton
class VarInt(Construct):
    r"""
    Varint encoded integer. Each 7 bits of the number are encoded in one byte in the stream.

    Scheme defined at Google's site:
    https://developers.google.com/protocol-buffers/docs/encoding

    Example::

        VarInt("number")
        .parse(b"\x85\x05") -> 645
        .build(645) -> b"\x85\x05"
    """
    def _parse(self, stream, context):
        acc = 0
        while True:
            b = ord(_read_stream(stream, 1))
            acc = (acc << 7) | (b & 127)
            if not b & 128:
                break
        return acc
    def _build(self, obj, stream, context):
        if obj < 0:
            raise ValueError("varint cannot build from negative number")
        while obj > 127:
            b = 128 | (obj & 127)
            obj >>= 7
            _write_stream(stream, 1, int2byte(b))
        _write_stream(stream, 1, int2byte(obj))


#===============================================================================
# structures and sequences
#===============================================================================
class Struct(Construct):
    r"""
    A sequence of named constructs, similar to structs in C. The elements are parsed and built in the order they are defined.

    .. seealso:: The :func:`~construct.macros.Embedded` macro.

    :param subcons: a sequence of subconstructs that make up this structure.
    :param nested: a keyword-only argument that indicates whether this struct creates a nested context. The default is True. This parameter is considered "advanced usage", and may be removed in the future.

    ONE OF TWO EMBEDDABLE CLASSES

    Example::

        Struct("foo",
            UBInt8("first_element"),
            UBInt16("second_element"),
            Padding(2),
            UBInt8("third_element"),
        )
    """
    __slots__ = ["subcons"]
    def __init__(self, *subcons, **kw):
        super(Struct, self).__init__()
        self.subcons = subcons
    def _parse(self, stream, context):
        obj = Container()
        context = Container(_ = context)
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = sc._parse(stream, context).items()
                obj.update(subobj)
            else:
                subobj = sc._parse(stream, context)
                if sc.name is not None:
                    obj[sc.name] = subobj
                    context[sc.name] = subobj
            context[i] = subobj
        return obj
    def _build(self, obj, stream, context):
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = obj
            elif sc.flagbuildnone:
                subobj = None
            else:
                subobj = obj[sc.name]
                context[sc.name] = subobj
            context[i] = subobj
            buildret = sc._build(subobj, stream, context)
            if buildret is not None:
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret
    def _sizeof(self, context):
        return sum(sc._sizeof(context) for sc in self.subcons)


class Sequence(Struct):
    r"""
    A sequence of unnamed constructs. The elements are parsed and built in the order they are defined.

    .. seealso:: The :func:`~construct.macros.Embedded` macro.

    :param subcons: a sequence of subconstructs that make up this structure.
    :param nested: a keyword-only argument that indicates whether this struct creates a nested context. The default is True. This parameter is considered "advanced usage", and may be removed in the future.

    Example::

        Sequence("foo",
            UBInt8("first_element"),
            UBInt16("second_element"),
            Padding(2),
            UBInt8("third_element"),
        )
    """
    def _parse(self, stream, context):
        obj = ListContainer()
        context = Container(_ = context)
        for i,sc in enumerate(self.subcons):
            subobj = sc._parse(stream, context)
            if sc.flagembedded:
                obj.extend(subobj)
            else:
                obj.append(subobj)
                if sc.name is not None:
                    context[sc.name] = subobj
            context[i] = subobj
        return obj
    def _build(self, obj, stream, context):
        objiter = iter(obj)
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = objiter
            else:
                subobj = next(objiter)
                if sc.name is not None:
                    context[sc.name] = subobj
            context[i] = subobj
            buildret = sc._build(subobj, stream, context)
            if buildret is not None:
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret


#===============================================================================
# arrays and repeaters
#===============================================================================
class Array(Subconstruct):
    r"""
    An array (repeater) of a meta-count. The array will iterate exactly ``countfunc()`` times. Will raise ArrayError if less elements are found.

    .. seealso::

        The :func:`~construct.macros.Array` macro, :func:`Range` and :func:`RepeatUntil`.

    :param countfunc: a function that takes the context as a parameter and returns the number of elements of the array (count)
    :param subcon: the subcon to repeat ``countfunc()`` times

    Example::

        MetaArray(lambda ctx: 5, UBInt8("foo"))

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
    __slots__ = ["count"]
    def __init__(self, count, subcon):
        super(Array, self).__init__(subcon)
        self.count = count
    def _parse(self, stream, context):
        count = self.count(context) if callable(self.count) else self.count
        try:
            obj = ListContainer()
            for i in range(count):
                obj.append(self.subcon._parse(stream, context))
            return obj
        except ConstructError:
            raise ArrayError("expected %d, found %d" % (count, len(obj)))
    def _build(self, obj, stream, context):
        count = self.count(context) if callable(self.count) else self.count
        if len(obj) != count:
            raise ArrayError("expected %d elements, found %d" % (count, len(obj)))
        for subobj in obj:
            self.subcon._build(subobj, stream, context)
    def _sizeof(self, context):
        count = self.count(context) if callable(self.count) else self.count
        return self.subcon._sizeof(context) * count


class PrefixedArray(Construct):
    r"""
    An array prefixed by a length field.

    :param lengthfield: a field returning an integer
    :param subcon: the subcon to be repeated

    Example::

        PrefixedArray(UBInt8("array"), UBInt8(None))
        .parse(b"\x03\x01\x01\x01") -> [1,1,1]
        .build([1,1,1]) -> b"\x03\x01\x01\x01"
    """
    def __init__(self, lengthfield, subcon):
        super(PrefixedArray, self).__init__()
        self.lengthfield = lengthfield
        self.subcon = subcon
    def _parse(self, stream, context):
        try:
            count = self.lengthfield._parse(stream, context)
            return list(self.subcon._parse(stream, context) for i in range(count))
        except Exception:
            raise ArrayError("could not read prefix or enough elements, stream too short")
    def _build(self, obj, stream, context):
        self.lengthfield._build(len(obj), stream, context)
        for element in obj:
            self.subcon._build(element, stream, context)


class Range(Subconstruct):
    r"""
    A range-array. The subcon will iterate between ``min`` to ``max`` times. If less than ``min`` elements are found, raises RangeError.

    .. seealso::

        The :func:`~construct.macros.GreedyRange` macro.

    The general-case repeater. Repeats the given unit for at least ``min`` times, and up to ``max`` times. If an exception occurs (EOF, validation error), the repeater exits cleanly. If less than ``min`` units have been successfully parsed, a RangeError is raised.

    .. note:: This object requires a seekable stream for parsing.

    :param min: the minimal count
    :param max: the maximal count
    :param subcon: the subcon to repeat

    Example::

        >>> c = Range(3, 7, UBInt8("foo"))
        >>> c.parse("\x01\x02")
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 3..7, found 2
        >>> c.parse("\x01\x02\x03")
        [1, 2, 3]
        >>> c.parse("\x01\x02\x03\x04\x05\x06")
        [1, 2, 3, 4, 5, 6]
        >>> c.parse("\x01\x02\x03\x04\x05\x06\x07")
        [1, 2, 3, 4, 5, 6, 7]
        >>> c.parse("\x01\x02\x03\x04\x05\x06\x07\x08\x09")
        [1, 2, 3, 4, 5, 6, 7]
        >>> c.build([1,2])
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 3..7, found 2
        >>> c.build([1,2,3,4])
        '\x01\x02\x03\x04'
        >>> c.build([1,2,3,4,5,6,7,8])
        Traceback (most recent call last):
          ...
        construct.core.RangeError: expected 3..7, found 8
    """
    __slots__ = ["min", "max"]
    def __init__(self, min, max, subcon):
        if not 0 <= min <= max <= sys.maxsize:
            raise RangeError("unsane min %s and max %s" % (min,max))
        super(Range, self).__init__(subcon)
        self.min = min
        self.max = max
    def _parse(self, stream, context):
        obj = ListContainer()
        try:
            while len(obj) < self.max:
                fallback = stream.tell()
                obj.append(self.subcon._parse(stream, context))
                context[len(obj)-1] = obj[-1]
        except ConstructError:
            if len(obj) < self.min:
                raise RangeError("expected %d to %d, found %d" % (self.min, self.max, len(obj)))
            stream.seek(fallback)
        return obj
    def _build(self, obj, stream, context):
        if not isinstance(obj, collections.Sequence):
            raise RangeError("expected sequence type, found %s" % type(obj))
        if not self.min <= len(obj) <= self.max:
            raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
        try:
            for i,subobj in enumerate(obj):
                context[i] = subobj
                self.subcon._build(subobj, stream, context)
        except ConstructError:
            if len(obj) < self.min:
                raise RangeError("expected %d to %d, found %d" % (self.min, self.max, len(obj)))
    def _sizeof(self, context):
        if self.min == self.max:
            return self.min * self.subcon._sizeof(context)
        else:
            raise SizeofError("cannot calculate size")


def GreedyRange(subcon):
    return Range(0, sys.maxsize, subcon)


class RepeatUntil(Subconstruct):
    r"""
    An array that repeats until the predicate indicates it to stop. Note that the last element (which caused the repeat to exit) is included in the return value.

    :param predicate: a predicate function that takes (obj, context) and returns True if the stop-condition is met, or False to continue
    :param subcon: the subcon used to parse and build each element

    Example::

        # will read chars until '\x00' (inclusive)
        RepeatUntil(lambda obj, ctx: obj == b"\x00",
            Field("chars", 1)
        )
    """
    __slots__ = ["predicate"]
    def __init__(self, predicate, subcon):
        super(RepeatUntil, self).__init__(subcon)
        self.predicate = predicate
    def _parse(self, stream, context):
        try:
            obj = ListContainer()
            while True:
                subobj = self.subcon._parse(stream, context)
                obj.append(subobj)
                if self.predicate(subobj, context):
                    break
        except ConstructError:
            raise ArrayError("missing terminator")
        return obj
    def _build(self, obj, stream, context):
        for subobj in obj:
            self.subcon._build(subobj, stream, context)
            if self.predicate(subobj, context):
                break
        else:
            raise ArrayError("missing terminator")
    def _sizeof(self, context):
        raise SizeofError("cannot calculate size")


#===============================================================================
# subconstructs
#===============================================================================
class RawCopy(Subconstruct):
    def __init__(self, subcon):
        super(RawCopy, self).__init__(subcon)
    def _parse(self, stream, context):
        offset1 = stream.tell()
        obj = self.subcon._parse(stream, context)
        offset2 = stream.tell()
        stream.seek(offset1)
        data = _read_stream(stream, offset2-offset1)
        return dict(data=data, value=obj, offset1=offset1, offset2=offset2, length=(offset2-offset1))
    def _build(self, obj, stream, context):
        if 'data' in obj:
            data = obj['data']
            _write_stream(stream, len(data), data)
            return dict(data=data, length=len(data))
        elif 'value' in obj:
            value = obj['value']
            data = self.subcon.build(value, context)
            _write_stream(stream, len(data), data)
            return dict(data=data, value=value, length=len(data))
        else:
            raise ConstructError('both data and value keys are missing')


class Padded(Subconstruct):
    __slots__ = ["length", "pattern", "strict"]
    def __init__(self, length, subcon, pattern=b"\x00", strict=False):
        if not isinstance(pattern, bytes) or len(pattern) != 1:
            raise PaddingError("pattern expected to be b-string character")
        super(Padded, self).__init__(subcon)
        self.length = length
        self.pattern = pattern
        self.strict = strict
    def _parse(self, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        position1 = stream.tell()
        obj = self.subcon._parse(stream, context)
        position2 = stream.tell()
        padlen = length - (position2 - position1)
        if padlen < 0:
            raise PaddingError("subcon parsed more bytes than was allowed by length")
        pad = _read_stream(stream, padlen)
        if self.strict:
            if pad != self.pattern * padlen:
                raise PaddingError("expected %r times %r, found %r" % (self.pattern, padlen, pad))
        return obj
    def _build(self, obj, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        position1 = stream.tell()
        subobj = self.subcon._build(obj, stream, context)
        position2 = stream.tell()
        padlen = length - (position2 - position1)
        if padlen < 0:
            raise PaddingError("subcon parsed more bytes than was allowed by length")
        _write_stream(stream, padlen, self.pattern * padlen)
        return subobj
    def _sizeof(self, context):
        return self.length(context) if callable(self.length) else self.length


class Aligned(Subconstruct):
    r"""
    Aligns subcon to modulus boundary using padding pattern

    :param subcon: the subcon to align
    :param modulus: the modulus boundary (default is 4)
    :param pattern: the padding pattern (default is \x00)

    Example::

        Aligned(
            Byte("num"),
            modulus=4,
        )

        .parse(b"\xff\x00\x00\x00") -> Container(num=255)
        .build(Container(num=255)) -> b"\xff\x00\x00\x00"
        .sizeof() -> 4

        Aligned(
            ULInt16("num"),
            modulus=4,
        )

        .parse(b"\xff\x00\x00\x00") -> Container(num=255)
        .build(Container(num=255)) -> b"\xff\x00\x00\x00"
        .sizeof() -> 4
    """
    __slots__ = ["subcon", "modulus", "pattern"]
    def __init__(self, subcon, modulus, pattern=b"\x00"):
        if modulus < 2:
            raise ValueError("modulus must be at least 2", modulus)
        if len(pattern) != 1:
            raise PaddingError("pattern expected to be b-string character")
        super(Aligned, self).__init__(subcon)
        self.modulus = modulus
        self.pattern = pattern
    def _parse(self, stream, context):
        position1 = stream.tell()
        obj = self.subcon._parse(stream, context)
        position2 = stream.tell()
        pad = -(position2 - position1) % self.modulus
        _read_stream(stream, pad)
        return obj
    def _build(self, obj, stream, context):
        position1 = stream.tell()
        subobj = self.subcon._build(obj, stream, context)
        position2 = stream.tell()
        pad = -(position2 - position1) % self.modulus
        _write_stream(stream, pad, self.pattern * pad)
        return subobj
    def _sizeof(self, context):
        sublen = self.subcon._sizeof(context)
        return sublen + (-sublen % self.modulus)


def AlignedStruct(name, *subcons, **kw):
    r"""
    A struct of aligned fields

    :param \*subcons: the subcons that make up this structure
    :param \*\*kw: keyword arguments to pass to Aligned: 'modulus' and 'pattern'
    """
    return Struct(name, *(Aligned(sc, **kw) for sc in subcons))


def BitStruct(*subcons):
    r"""
    A struct of bitwise fields

    :param \*subcons: the subcons that make up this structure
    """
    return Bitwise(Struct(*subcons))


def EmbeddedBitStruct(*subcons):
    r"""
    An embedded BitStruct. no name is necessary.

    :param \*subcons: the subcons that make up this structure
    """
    return Bitwise(Embedded(Struct(*subcons)))


#===============================================================================
# conditional
#===============================================================================
class Union(Construct):
    r"""
    Set of overlapping fields (like unions in C). When parsing, all fields read the same data. When building, either the first subcon that builds without exception is allowed to put into the stream, or the subcon is selected by index or name. Size is the maximum of subcon sizes.

    .. note:: Requires a seekable stream.

    :param buildfrom: the subcon used for building and calculating the total size, can be integer index or string name or None (then tries each subcon)
    :param subcons: subconstructs for parsing, one of them used for building

    Example::

        Union("union",
            Struct("sub1", ULInt8("a"), ULInt8("b") ),
            Struct("sub2", ULInt16("c") ),
        )

        .build(dict(sub1=dict(a=1,b=2))) -> b"\x01\x02"
        .build(dict(sub2=dict(c=3)))     -> b"\x03\x00"

        Union("union",
            Embedded(Struct("sub1", ULInt8("a"), ULInt8("b") )),
            Embedded(Struct("sub2", ULInt16("c") )),
        )

        .build(dict(a=1,b=2)) -> b"\x01\x02"
        .build(dict(c=3)) -> b"\x03\x00"
    """
    __slots__ = ["subcons","buildfrom"]
    def __init__(self, *subcons, **kw):
        super(Union, self).__init__()
        self.subcons = [Peek(sc) for sc in subcons]
        self.buildfrom = kw.get("buildfrom", None)
    def _parse(self, stream, context):
        ret = Container()
        for sc in self.subcons:
            _updcon(ret, sc, sc._parse(stream, context))
        return ret
    def _build(self, obj, stream, context):
        if self.buildfrom is not None:
            if isinstance(self.buildfrom, int):
                index = self.buildfrom
                name = self.subcons[index].name
                self.subcons[index].subcon._build(_subobj(self.subcons[index], obj), stream, context)
            elif isinstance(self.buildfrom, str):
                index = next(i for i,sc in enumerate(self.subcons) if sc.name == self.buildfrom)
                name = self.subcons[index].name
                self.subcons[index].subcon._build(_subobj(self.subcons[index], obj), stream, context)
            else:
                raise TypeError("buildfrom is not int or str")
        else:
            for sc in self.subcons:
                try:
                    data = sc.subcon.build(_subobj(sc, obj), context)
                except Exception:
                    pass
                else:
                    stream.write(data)
                    break
            else:
                raise SelectError("no subconstruct matched", obj)


class Select(Construct):
    """
    Selects the first matching subconstruct. It will literally try each of the subconstructs, until one matches.

    .. note:: Requires a seekable stream.

    :param subcons: the subcons to try (order-sensitive)
    :param include_name: a keyword only argument, indicating whether to include the name of the selected subcon in the return value of parsing. default is false.

    Example::

        Select("foo",
            UBInt64("large"),
            UBInt32("medium"),
            UBInt16("small"),
            UBInt8("tiny"),
        )
    """
    __slots__ = ["subcons", "includename"]
    def __init__(self, *subcons, **kw):
        includename = kw.pop("includename", False)
        super(Select, self).__init__()
        self.subcons = subcons
        self.includename = includename
        self._inherit_flags(*subcons)
    def _parse(self, stream, context):
        for sc in self.subcons:
            fallback = stream.tell()
            context2 = context.__copy__()
            try:
                obj = sc._parse(stream, context2)
            except ConstructError:
                stream.seek(fallback)
            else:
                context.__update__(context2)
                if self.includename:
                    return sc.name, obj
                else:
                    return obj
        raise SelectError("no subconstruct matched")
    def _build(self, obj, stream, context):
        if self.includename:
            name, obj = obj
            for sc in self.subcons:
                if sc.name == name:
                    sc._build(obj, stream, context)
                    return
        else:
            for sc in self.subcons:
                context2 = context.__copy__()
                try:
                    data = sc.build(obj, context2)
                except Exception:
                    pass
                else:
                    context.__update__(context2)
                    stream.write(data)
                    return
        raise SelectError("no subconstruct matched", obj)


def Optional(subcon):
    r"""
    An optional construct.

    If parsing fails, returns None. If building fails, writes nothing.

    Note: sizeof returns subcon size, although no bytes could be consumed or produced. Just something to consider.

    :param subcon: the subcon to optionally parse or build
    """
    return Select(subcon, Pass)


class Switch(Construct):
    """
    A conditional branch. Switch will choose the case to follow based on the return value of keyfunc. If no case is matched, and no default value is given, SwitchError will be raised.

    .. seealso:: The :func:`Pass` singleton.

    :param keyfunc: a function that takes the context and returns a key, which will be used to choose the relevant case.
    :param cases: a dictionary mapping keys to constructs. the keys can be any values that may be returned by keyfunc.
    :param default: a default field to use when the key is not found in the cases. if not supplied, an exception will be raised when the key is not found. You can use the builtin construct Pass for do-nothing.
    :param includekey: whether or not to include the key in the return value of parsing. defualt is False.

    Example::

        Struct(
            "type" / UBInt8,
            "value" / Switch(lambda ctx: ctx.type, {
                1 : UBInt8,
                2 : UBInt16,
                3 : UBInt32,
                4 : UBInt64,
            }))
    """
    @singleton
    class NoDefault(Construct):
        def _parse(self, stream, context):
            raise SwitchError("no default case defined")
        def _build(self, obj, stream, context):
            raise SwitchError("no default case defined")
        def _sizeof(self, context):
            raise SwitchError("no default case defined")

    __slots__ = ["subcons", "keyfunc", "cases", "default", "includekey"]
    def __init__(self, keyfunc, cases, default=NoDefault, includekey=False):
        super(Switch, self).__init__()
        self._inherit_flags(*cases.values())
        self.keyfunc = keyfunc
        self.cases = cases
        self.default = default
        self.includekey = includekey
    def _parse(self, stream, context):
        key = self.keyfunc(context)
        obj = self.cases.get(key, self.default)._parse(stream, context)
        if self.includekey:
            return key, obj
        else:
            return obj
    def _build(self, obj, stream, context):
        if self.includekey:
            key, obj = obj
        else:
            key = self.keyfunc(context)
        case = self.cases.get(key, self.default)
        case._build(obj, stream, context)
    # def _sizeof(self, context):
    #     case = self.cases.get(self.keyfunc(context), self.default)
    #     return case._sizeof(context)


def IfThenElse(predicate, thensubcon, elsesubcon):
    r"""
    An if-then-else conditional construct. If the predicate indicates True, `thensubcon` will be used, otherwise `elsesubcon` will be used.

    :param predicate: a function taking the context as an argument and returning a bool
    :param thensubcon: the subcon that will be used if the predicate indicates True
    :param elsesubcon: the subcon that will be used if the predicate indicates False
    """
    return Switch(
        lambda ctx: bool(predicate(ctx)),
        {
            True : thensubcon,
            False : elsesubcon,
        },
    )


def If(predicate, subcon):
    r"""
    An if-then conditional construct. If the predicate indicates True, the `subcon` will be used for parsing and building, otherwise parsing returns None and building is no-op.

    :param predicate: a function taking the context as an argument and returning bool
    :param subcon: the subcon that will be used if the predicate returns True
    """
    return IfThenElse(
        predicate,
        subcon,
        Pass,
    )


#===============================================================================
# stream manipulation
#===============================================================================
class Pointer(Subconstruct):
    r"""
    Changes the stream position to a given offset, where the construction should take place, and restores the stream position when finished.

    .. seealso:: The :func:`~construct.macros.OnDemandPointer` field, which also seeks to a given offset.

    .. note:: Requires a seekable stream.

    :param offset: an int or a function that takes context and returns absolute stream position, where the construction would take place
    :param subcon: the subcon to use at the offset

    Example::

        ?
    """
    __slots__ = ["offset"]
    def __init__(self, offset, subcon):
        super(Pointer, self).__init__(subcon)
        self.offset = offset
    def _parse(self, stream, context):
        offset = self.offset(context) if callable(self.offset) else self.offset
        fallback = stream.tell()
        stream.seek(offset, 2 if offset < 0 else 0)
        obj = self.subcon._parse(stream, context)
        stream.seek(fallback)
        return obj
    def _build(self, obj, stream, context):
        offset = self.offset(context) if callable(self.offset) else self.offset
        fallback = stream.tell()
        stream.seek(offset, 2 if offset < 0 else 0)
        buildret = self.subcon._build(obj, stream, context)
        stream.seek(fallback)
        return buildret
    def _sizeof(self, context):
        return 0


class Peek(Subconstruct):
    r"""
    Peeks at the stream.

    Parses the subcon without changing the stream position. If the end of the stream is reached when peeking, returns None. Size is defined as size of the subcon, even tho the stream is not advanced during parsing.

    .. seealso:: The :class:`~construct.core.Union` class.
  
    .. note:: Requires a seekable stream.

    :param subcon: the subcon to peek at

    Example::

        Struct("struct",
            Peek(Byte("a")),
            Peek(Bytes("b", 2)),
        )
        .parse(b"\x01\x02") -> Container(a=1)(b=258)
        .build(dict(a=0,b=258)) -> b"\x01\x02"
        .build(dict(a=1,b=258)) -> b"\x01\x02"
    """
    def __init__(self, subcon):
        super(Peek, self).__init__(subcon)
    def _parse(self, stream, context):
        fallback = stream.tell()
        try:
            return self.subcon._parse(stream, context)
        except FieldError:
            pass
        finally:
            stream.seek(fallback)
    def _build(self, obj, stream, context):
        pass
    def _sizeof(self, context):
        return 0


class Restreamed(Subconstruct):
    r"""
    Transforms bytes between the underlying stream and the subcon.

    When the parsing or building is done, the wrapper stream is closed. If read buffer or write buffer is not empty, then error is raised.

    .. seealso:: The :func:`~construct.macros.Bitwise` macro.

    .. warning:: Do not use pointers inside.

    :param subcon: the subcon which will operate on the buffer
    :param encoder: a function that takes a b-string and returns a b-string (used when building)
    :param encoderunit: ratio as int, encoder takes that many bytes at once
    :param decoder: a function that takes a b-string and returns a b-string (used when parsing)
    :param decoderunit: ratio as int, decoder takes that many bytes at once

    Example::

        Restreamed(BitsInteger(8), bits2bytes, 8, bytes2bits, 1)
        .parse(b"\x0f") == 15
        .build(15) == b"\x0f"
    """
    __slots__ = ["stream2", "sizecomputer"]
    def __init__(self, subcon, encoder, encoderunit, decoder, decoderunit, sizecomputer):
        super(Restreamed, self).__init__(subcon)
        self.stream2 = RestreamedBytesIO(None, encoder, encoderunit, decoder, decoderunit)
        self.sizecomputer = sizecomputer
    def _parse(self, stream, context):
        self.stream2.substream = stream
        return self.subcon._parse(self.stream2, context)
    def _build(self, obj, stream, context):
        self.stream2.substream = stream
        return self.subcon._build(obj, self.stream2, context)
    def _sizeof(self, context):
        if self.sizecomputer is None:
            raise SizeofError("cannot calculate size")
        return self.sizecomputer(self.subcon._sizeof(context))


#===============================================================================
# miscellaneous
#===============================================================================
class Padding(Construct):
    r"""
    A padding field (adds bytes when building, discards bytes when parsing).

    :param length: length of the field. can be either an integer or a function that takes the context as an argument and returns the length
    :param pattern: the padding pattern (b-string character). default is b"\x00"
    :param strict: whether to verify during parsing that the stream contains the pattern. raises an exception if actual padding differs from the pattern. default is False.

    Example::

        Struct("struct",
            Byte("num"),
            Padding(4),
        )

        .parse(b"\xff\x00\x00\x00\x00") -> Container(num=255)
        .build(Container(num=255)) -> b"\xff\x00\x00\x00\x00"
        .sizeof() -> 5
    """
    __slots__ = ["length", "pattern", "strict"]
    def __init__(self, length, pattern=b"\x00", strict=False):
        if not isinstance(pattern, bytes) or len(pattern) != 1:
            raise PaddingError("pattern expected to be b-string character")
        super(Padding, self).__init__()
        self.length = length
        self.pattern = pattern
        self.strict = strict
        self.flagbuildnone = True
    def _parse(self, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        read = _read_stream(stream, length)
        if self.strict:
            expected = length * self.pattern
            if read != expected:
                raise PaddingError("expected %r, found %r" % (expected, read))
    def _build(self, obj, stream, context):
        length = self.length(context) if callable(self.length) else self.length
        padding = length * self.pattern
        _write_stream(stream, length, padding)
    def _sizeof(self, context):
        return self.length(context) if callable(self.length) else self.length


class Const(Subconstruct):
    r"""
    Constant field enforcing a constant value. It is used for file signatures, to validate that the given pattern exists. When parsed, the value must match.

    :param data: a bytes object
    :param subcon: the subcon to validate
    :param value: the expected value

    Example::

        Const(b"IHDR")

        Const(ULInt64, 123)
    """
    __slots__ = ["value"]
    def __init__(self, subcon, value=None):
        if value is None:
            subcon, value = Bytes(len(subcon)), subcon
        if isinstance(subcon, str):
            subcon, value = Bytes(len(value)), value
        super(Const, self).__init__(subcon)
        self.value = value
        self.flagbuildnone = True
    def _parse(self, stream, context):
        obj = self.subcon._parse(stream, context)
        if obj != self.value:
            raise ConstError("expected %r but parsed %r" % (self.value,obj))
        return obj
    def _build(self, obj, stream, context):
        if obj is not None and obj != self.value:
            raise ConstError("expected None (its a build from none thing) or the right value")
        return self.subcon._build(self.value, stream, context)
    def _sizeof(self, context):
        return self.subcon._sizeof(context)


@singleton
class Anchor(Construct):
    r"""
    Gets the stream position when parsing or building.

    Anchors are useful for adjusting relative offsets to absolute positions, or to measure sizes of Constructs. To get an absolute pointer, use an Anchor plus a relative offset. To get a size, place two Anchors and measure their difference using a Compute.

    .. note:: Requires a tellable stream.

    Example::

        Struct("struct",
            Anchor("offset1"),
            Byte("a")
            Anchor("offset1"),
            Computed("length", lambda ctx: ctx.offset2 - ctx.offset1),
        )
        .parse(b"\xff") -> Container(offset1=0)(a=255)(ofsset2=1)(length=1)
        .build(dict(a=255)) -> b"\xff"
        .sizeof() -> 1
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context):
        return stream.tell()
    def _build(self, obj, stream, context):
        return stream.tell()
    def _sizeof(self, context):
        return 0


class Computed(Construct):
    r"""
    A computed value.

    Underlying byte stream is unaffected. When parsing `func(context)` provides the value.

    :param func: a function that takes the context and return the computed value

    Example::

        Struct("struct",
            UBInt8("width"),
            UBInt8("height"),
            Computed("total", lambda ctx: ctx.width * ctx.height),
        )

        .parse(b'\x04\x05') -> Container(width=4,height=5,total=20)
        .build(dict(width=4,height=5)) -> b'\x04\x05'
    """
    __slots__ = ["func"]
    def __init__(self, func):
        super(Computed, self).__init__()
        self.func = func
        self.flagbuildnone = True
    def _parse(self, stream, context):
        return self.func(context)
    def _build(self, obj, stream, context):
        return self.func(context)
    def _sizeof(self, context):
        return 0


@singleton
class Pass(Construct):
    r"""
    A do-nothing construct, useful as the default case for Switch. Returns None on parsing, puts nothing on building.

    Example::

        Pass

        .parse(b'') -> None
        .build(None) -> b''
        .sizeof() -> 0
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context):
        return None
    def _build(self, obj, stream, context):
        pass
    def _sizeof(self, context):
        return 0


@singleton
class Terminator(Construct):
    r"""
    Asserts the end of the stream has been reached at the point it was placed. You can use this to ensure no more unparsed data follows.

    This construct is only meaningful for parsing. For building, it's a no-op.

    Example::

        Terminator

        .parse(b'') -> None
        .parse(b'remaining') -> TerminatorError
        .sizeof() -> 0
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.flagbuildnone = True
    def _parse(self, stream, context):
        if stream.read(1):
            raise TerminatorError("expected end of stream")
    def _build(self, obj, stream, context):
        pass
    def _sizeof(self, context):
        return 0


@singleton
class Numpy(Construct):
    r"""
    Preserves numpy arrays (both shape, dtype and values).

    Example::

        Numpy

        .parse(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00") -> array([1, 2, 3])
        .build(array([1, 2, 3])) -> b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        try:
            import numpy
            self.lib = numpy
        except ImportError:
            pass
    def _parse(self, stream, context):
        return self.lib.load(stream)
    def _build(self, obj, stream, context):
        self.lib.save(stream, obj)


#===============================================================================
# tunneling and other
#===============================================================================
class Checksum(Construct):
    r"""
    A field that is build or validated by a hash of a given byte range.

    :param checksumfield: a subcon field that reads the checksum, usually Bytes(int), it's name is reused
    :param hashfunc: a function taking bytes and returning whatever checksumfield takes
    :param anchors: name of an AnchorRange

    Example::

        def sha512(b):
            return hashlib.sha512(b).digest()

        Struct("struct",
            AnchorRange("range"),
            Byte("a"),
            AnchorRange("range"),
            Checksum(Bytes("checksum",64), sha512, "range"),
        )
        .parse(b"\xff<hash>") -> Container(range=Container(offset1=0)(ofsset2=1)(length=1))(a=255)(checksum=?)
        .build(dict(a=255)) -> b"\xff<hash>"
    """
    __slots__ = ["checksumfield", "hashfunc", "rawcopy"]
    def __init__(self, checksumfield, hashfunc, rawcopy):
        super(Checksum, self).__init__()
        self.checksumfield = checksumfield
        self.hashfunc = hashfunc
        self.rawcopy = rawcopy
        self.flagbuildnone = True
    def _parse(self, stream, context):
        hash1 = self.checksumfield._parse(stream, context)
        hash2 = self.hashfunc(context[self.rawcopy]["data"])
        if hash1 != hash2:
            raise ChecksumError("wrong checksum, read %r, computed %r" % (hexlify(hash1), hexlify(hash2)))
        return hash1
    def _build(self, obj, stream, context):
        # print('in Checksum ',obj,context)
        hash2 = self.hashfunc(context[self.rawcopy]["data"])
        self.checksumfield._build(hash2, stream, context)
    def _sizeof(self, context):
        return self.checksumfield._sizeof(context)


class ByteSwapped(Subconstruct):
    r"""
    Swap the byte order within aligned boundaries of given size.

    :param subcon: the subcon on top of byte swapped bytes
    :param size: int of how many bytes are to be swapped, None by default meaning subcon size

    Example::

        ByteSwapped(Struct("struct",
            Byte("a"),
            Byte("b"),
        ))

        .parse(b"\x01\x02") -> Container(a=2)(b=1)
        .parse(dict(a=2,b=1)) -> b"\x01\x02"
    """
    def __init__(self, subcon):
        super(ByteSwapped, self).__init__(subcon)
    def _parse(self, stream, context):
        size = self.subcon._sizeof(context)
        data = _read_stream(stream, size)[::-1]
        return self.subcon._parse(BytesIO(data), context)
    def _build(self, obj, stream, context):
        data = self.subcon.build(obj, context)[::-1]
        _write_stream(stream, len(data), data)
    def _sizeof(self, context):
        return self.subcon._sizeof(context)


def BitsSwapped(subcon):
    return Restreamed(subcon,
        lambda s: bits2bytes(bytes2bits(s)[::-1]), 1,
        lambda s: bits2bytes(bytes2bits(s)[::-1]), 1,
        lambda n: n)


class Prefixed(Subconstruct):
    r"""
    Parses the length field. Then reads that amount of bytes and parses the subcon using only those bytes. Constructs that consume entire remaining stream are constrained to consuming only the specified amount of bytes. When building, bytes are passed as is.

    Name of the subcon is used for this construct.

    :param lengthfield: a subcon used for storing the length
    :param subcon: the subcon used for storing the value

    Example::

        Prefixed(VarInt(None), GreedyBytes(None))
        .parse(b"\x03xyzgarbage") -> b"xyz"
        .build(b"xyz") -> b'\x03xyz'
    """
    __slots__ = ["name", "lengthfield", "subcon"]
    def __init__(self, lengthfield, subcon):
        super(Prefixed, self).__init__(subcon)
        self.lengthfield = lengthfield
    def _parse(self, stream, context):
        length = self.lengthfield._parse(stream, context)
        data = _read_stream(stream, length)
        return self.subcon.parse(data, context)
    def _build(self, obj, stream, context):
        data = self.subcon.build(obj, context)
        subobj = self.lengthfield._build(len(data), stream, context)
        _write_stream(stream, len(data), data)
        return subobj
    def _sizeof(self, context):
        return self.lengthfield._sizeof(context) + self.subcon._sizeof(context)


class Compressed(Tunnel):
    r"""
    Compresses or decompresses a subcon.

    When parsing, entire stream is consumed. When building, puts compressed bytes without marking the end. This construct should either be used with Prefixed or on entire stream.

    Name of the subcon is used for this construct.

    .. seealso:: The :class:`~construct.core.Prefixed` class.

    :param subcon: the subcon used for storing the value
    :param encoding: any of the codecs module bytes<->bytes encodings, ie. "zlib"

    Example::

        Compressed(CString(None), "zlib")
        .parse(b'x\x9c30\xc0\n\x18\x008(\x04Q') -> b"00000000000000000000000"
        .build(b"00000000000000000000000") -> b'x\x9c30\xc0\n\x18\x008(\x04Q'

        Prefixed(Byte(None), Compressed(CString(None), "zlib"))
        .parse(b"\x0cx\x9c30\xc0\n\x18\x008(\x04Q") -> b"00000000000000000000000"
        .build(b"00000000000000000000000") -> b"\x0cx\x9c30\xc0\n\x18\x008(\x04Q"
   """
    def __init__(self, subcon, encoding):
        super(Compressed, self).__init__(subcon)
        self.encoding = encoding
    def _decode(self, data, context):
        return codecs.decode(data, self.encoding)
    def _encode(self, data, context):
        return codecs.encode(data, self.encoding)


#===============================================================================
# lazy equivalents
#===============================================================================
class LazyStruct(Construct):
    r"""
    A sequence of named constructs, similar to structs in C. The elements are parsed and built in the order they are defined.

    If entire struct is fixed size, then all fields are parsed only when their keys are first accessed. Otherwise variable length fields are parsed immediately and fixed length fields are parsed later.

    :param subcons: a sequence of subconstructs that make up this structure.

    Example::

        LazyStruct("struct",
            UBInt8("a"),
            UBInt16("b"),
            CString("c"),
        )
        .parse(b"\x01\x00\x02abcde") -> LazyContainer(a=1,b=2,c=?)
    """
    __slots__ = ["subcons", "offsetmap", "totalsize", "subsizes", "keys"]
    def __init__(self, *subcons, **kw):
        super(LazyStruct, self).__init__()
        self.subcons = subcons

        try:
            keys = Container()
            self.offsetmap = {}
            at = 0
            for sc in self.subcons:
                if sc.flagembedded:
                    raise SizeofError
                if sc.name is not None:
                    keys[sc.name] = None
                    self.offsetmap[sc.name] = (at, sc)
                at += sc.sizeof()
            self.totalsize = at
            self.keys = keys.keys()
        except SizeofError:
            self.offsetmap = None
            self.totalsize = None

        self.subsizes = []
        for sc in self.subcons:
            try:
                self.subsizes.append(sc.sizeof())
            except SizeofError:
                self.subsizes.append(None)

    def _parse(self, stream, context):
        if self.offsetmap is not None:
            position = stream.tell()
            stream.seek(self.totalsize, 1)
            return LazyContainer(self.keys, self.offsetmap, {}, stream, position, context)
        offsetmap = {}
        keys = Container()
        values = {}
        position = stream.tell()
        for i,(sc,size) in enumerate(zip(self.subcons, self.subsizes)):
            if sc.flagembedded:
                subobj = sc._parse(stream, context).items()
                keys.update(subobj)
                values.update(subobj)
            elif size is None:
                subobj = sc._parse(stream, context)
                if sc.name is not None:
                    keys[sc.name] = None
                    values[sc.name] = subobj
                    context[sc.name] = subobj
                context[i] = subobj
            else:
                if sc.name is not None:
                    keys[sc.name] = None
                    offsetmap[sc.name] = (stream.tell(), sc)
                stream.seek(size, 1)
        return LazyContainer(keys.keys(), offsetmap, values, stream, 0, context)

    def _build(self, obj, stream, context):
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = obj
            elif sc.flagbuildnone:
                subobj = None
            else:
                subobj = obj[sc.name]
                context[sc.name] = subobj
            context[i] = subobj
            buildret = sc._build(subobj, stream, context)
            if buildret is not None:
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret

    def _sizeof(self, context):
        if self.totalsize is not None:
            return self.totalsize
        else:
            raise SizeofError("cannot calculate size")


class LazyRange(Construct):
    r"""
    A sequence of named constructs, similar to structs in C. The elements are parsed and built in the order they are defined.

    If entire struct is fixed size, then all fields are parsed only when their keys are first accessed. Otherwise variable length fields are parsed immediately and fixed length fields are parsed later.

    :param subcons: a sequence of subconstructs that make up this structure.

    Example::

        LazyStruct("struct",
            UBInt8("a"),
            UBInt16("b"),
            CString("c"),
        )
        .parse(b"\x01\x00\x02abcde") -> LazyContainer(a=1,b=2,c=?)
    """
    __slots__ = ["subcon", "min", "max", "subsize"]
    def __init__(self, min, max, subcon):
        if not 0 <= min <= max <= sys.maxsize:
            raise RangeError("unsane min %s and max %s" % (min,max))
        super(LazyRange, self).__init__()
        self.subcon = subcon
        self.min = min
        self.max = max
        self.subsize = subcon.sizeof()

    def _parse(self, stream, context):
        starts = stream.tell()
        ends = stream.seek(0,2)
        remaining = ends - starts
        objcount = min(remaining//self.subsize, self.max)
        if objcount < self.min:
            raise RangeError("not enough bytes %d to read the min %d of %d bytes each" % (remaining,self.min,self.subsize))
        stream.seek(starts + objcount*self.subsize, 0)
        return LazyRangeContainer(self.subcon, self.subsize, objcount, stream, starts, context)

    def _build(self, obj, stream, context):
        if not isinstance(obj, collections.Sequence):
            raise RangeError("expected sequence type, found %s" % type(obj))
        if not self.min <= len(obj) <= self.max:
            raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
        try:
            for i,subobj in enumerate(obj):
                context[i] = subobj
                self.subcon._build(subobj, stream, context)
        except ConstructError:
            if len(obj) < self.min:
                raise RangeError("expected %d to %d, found %d" % (self.min, self.max, len(obj)))

    def _sizeof(self, context):
        if self.min == self.max:
            return self.min * self.subsize
        else:
            raise SizeofError("cannot calculate size")


class LazySequence(Construct):
    __slots__ = ["subcons", "offsetmap", "totalsize", "subsizes"]
    def __init__(self, *subcons, **kw):
        super(LazySequence, self).__init__()
        self.subcons = subcons

        try:
            self.offsetmap = {}
            at = 0
            for i,sc in enumerate(self.subcons):
                self.offsetmap[i] = at
                at += sc.sizeof()
            self.totalsize = at
        except SizeofError:
            self.offsetmap = None
            self.totalsize = None

        self.subsizes = []
        for sc in self.subcons:
            try:
                self.subsizes.append(sc.sizeof())
            except SizeofError:
                self.subsizes.append(None)

    def _parse(self, stream, context):
        if self.totalsize is not None:
            position = stream.tell()
            stream.seek(self.totalsize, 1)
            return LazySequenceContainer(self.subcons, self.offsetmap, {}, stream, position, context)
        offsetmap = {}
        values = {}
        for i,(sc,size) in enumerate(zip(self.subcons, self.subsizes)):
            if size is None:
                obj = sc._parse(stream, context)
                values[i] = obj
                context[i] = obj
            else:
                offsetmap[i] = stream.tell()
                stream.seek(size, 1)
        return LazySequenceContainer(self.subcons, offsetmap, values, stream, 0, context)

    def _build(self, obj, stream, context):
        objiter = iter(obj)
        for i,sc in enumerate(self.subcons):
            if sc.flagembedded:
                subobj = objiter
            else:
                subobj = next(objiter)
                if sc.name is not None:
                    context[sc.name] = subobj
            context[i] = subobj
            buildret = sc._build(subobj, stream, context)
            if buildret is not None:
                if sc.name is not None:
                    context[sc.name] = buildret
                context[i] = buildret

    def _sizeof(self, context):
        if self.totalsize is not None:
            return self.totalsize
        else:
            raise SizeofError("cannot calculate size")


class OnDemand(Subconstruct):
    r"""
    Allows for on-demand (lazy) parsing. When parsing, it will return a LazyContainer that represents a pointer to the data, but does not actually parse it from the stream until it is "demanded". By accessing the 'value' property of LazyContainers, you will demand the data from the stream. The data will be parsed and cached for later use. You can use the 'has_value' property to know whether the data has already been demanded.

    .. seealso:: The :func:`~construct.macros.OnDemandPointer` macro.

    :param subcon: the subcon to read/write on demand. must be fixed size

    Example::

        OnDemand(Array(10000, UBInt8("foo"))
    """
    def __init__(self, subcon):
        super(OnDemand, self).__init__(subcon)
    def _parse(self, stream, context):
        data = _read_stream(stream, self.subcon._sizeof(context))
        return lambda: self.subcon.parse(data, context)


class OnDemandPointer(Subconstruct):
    r"""
    An on-demand pointer.

    :param offsetfunc: an int or a function taking context and returning the absolute stream position
    :param subcon: the subcon that will be parsed or built at the `offset` stream position
    """
    __slots__ = ["offset"]
    def __init__(self, offset, subcon):
        super(OnDemandPointer, self).__init__(subcon)
        self.offset = offset
    def _parse(self, stream, context):
        def effectuate():
            offset = self.offset(context) if callable(self.offset) else self.offset
            fallback = stream.tell()
            stream.seek(offset)
            obj = self.subcon._parse(stream, context)
            stream.seek(fallback)
            return obj
        return effectuate
    def _build(self, obj, stream, context):
        offset = self.offset(context) if callable(self.offset) else self.offset
        fallback = stream.tell()
        stream.seek(offset)
        buildret = self.subcon._build(obj, stream, context)
        stream.seek(fallback)
        return buildret
    def _sizeof(self, context):
        return 0


class LazyBound(Construct):
    r"""
    Lazily bound construct, useful for constructs that need to make cyclic references (linked-lists, expression trees).

    :param subconfunc: function taking context and returning a new construct

    ??? look at test suite ???
    """
    __slots__ = ["subconfunc"]
    def __init__(self, subconfunc):
        super(LazyBound, self).__init__()
        self.subconfunc = subconfunc
    def _parse(self, stream, context):
        return self.subconfunc(context)._parse(stream, context)
    def _build(self, obj, stream, context):
        return self.subconfunc(context)._build(obj, stream, context)
    def _sizeof(self, context):
        return self.subconfunc(context)._sizeof(context)


#===============================================================================
# special
#===============================================================================
class Embedded(Subconstruct):
    r"""
    Embeds a struct into the enclosing struct, merging fields. Can also embed sequences into sequences.

    :param subcon: the struct to embed
    """
    def __init__(self, subcon):
        super(Embedded, self).__init__(subcon)
        self.flagembedded = True


class Renamed(Subconstruct):
    r"""
    Renames an existing construct. This creates a wrapper so underlying subcon retains it's original name.

    :param newname: the new name
    :param subcon: the subcon to rename
    """
    def __init__(self, newname, subcon):
        super(Renamed, self).__init__(subcon)
        self.name = newname


def Alias(newname, oldname):
    r"""
    Creates an alias for an existing element in a struct.

    When parsing, value is available under both keys. Build is no-op.

    :param newname: the new name
    :param oldname: the name of an existing element
    """
    return Renamed(newname, Computed(lambda ctx: ctx[oldname]))


#===============================================================================
# mappings
#===============================================================================
class Mapping(Adapter):
    r"""
    Adapter that maps objects to other objects.
    See SymmetricMapping and Enum.

    :param subcon: the subcon to map
    :param decoding: the decoding (parsing) mapping (a dict)
    :param encoding: the encoding (building) mapping (a dict)
    :param decdefault: the default return value when the object is not found
                       in the decoding mapping. if no object is given, an exception is raised.
                       if ``Pass`` is used, the unmapped object will be passed as-is
    :param encdefault: the default return value when the object is not found
                       in the encoding mapping. if no object is given, an exception is raised.
                       if ``Pass`` is used, the unmapped object will be passed as-is
    """
    __slots__ = ["encoding", "decoding", "encdefault", "decdefault"]
    def __init__(self, subcon, decoding, encoding, decdefault=NotImplemented, encdefault=NotImplemented):
        super(Mapping, self).__init__(subcon)
        self.decoding = decoding
        self.encoding = encoding
        self.decdefault = decdefault
        self.encdefault = encdefault
    def _encode(self, obj, context):
        try:
            return self.encoding[obj]
        except (KeyError, TypeError):
            if self.encdefault is NotImplemented:
                raise MappingError("no encoding mapping for %r [%s]" % (
                    obj, self.subcon.name))
            if self.encdefault is Pass:
                return obj
            return self.encdefault
    def _decode(self, obj, context):
        try:
            return self.decoding[obj]
        except (KeyError, TypeError):
            if self.decdefault is NotImplemented:
                raise MappingError("no decoding mapping for %r [%s]" % (
                    obj, self.subcon.name))
            if self.decdefault is Pass:
                return obj
            return self.decdefault


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
    return Mapping(subcon,
        encoding = mapping,
        decoding = dict((v, k) for k, v in mapping.items()),
        encdefault = default,
        decdefault = default,
    )


@singletonfunction
def Flag():
    return SymmetricMapping(UBInt8, {True : 1, False : 0}, default=True)


def Enum(subcon, mapping, default=NotImplemented):
    r"""
    A set of named values mapping.

    :param subcon: the subcon to map
    :param \*\*kw: keyword arguments which serve as the encoding mapping
    :param _default_: an optional, keyword-only argument that specifies the
                      default value to use when the mapping is undefined. if not given,
                      and exception is raised when the mapping is undefined. use `Pass` to
                      pass the unmapped value as-is
    """
    return SymmetricMapping(subcon, mapping, default)


class FlagsEnum(Adapter):
    r"""
    A set of flag values mapping.

    Adapter for flag fields. Each flag is extracted from the number, resulting
    in a FlagsContainer object. Not intended for direct usage. See FlagsEnum.

    :param subcon: the subcon to extract
    :param flags: a dictionary mapping flag-names to their value
    :param \*\*kw: keyword arguments which serve as the encoding mapping
    """
    __slots__ = ["flags"]
    def __init__(self, subcon, flags):
        super(FlagsEnum, self).__init__(subcon)
        self.flags = flags
    def _encode(self, obj, context):
        flags = 0
        try:
            for name, value in obj.items():
                if value:
                    flags |= self.flags[name]
        except AttributeError:
            raise MappingError("not a mapping type: %r" % (obj,))
        except KeyError:
            raise MappingError("unknown flag: %s" % name)
        return flags
    def _decode(self, obj, context):
        obj2 = FlagsContainer()
        for name, value in self.flags.items():
            obj2[name] = bool(obj & value)
        return obj2


#===============================================================================
# adapters
#===============================================================================
class ExprAdapter(Adapter):
    """
    A generic adapter that accepts 'encoder' and 'decoder' as parameters. You
    can use ExprAdapter instead of writing a full-blown class when only a
    simple expression is needed.

    :param subcon: the subcon to adapt
    :param encoder: a function that takes (obj, context) and returns an encoded version of obj
    :param decoder: a function that takes (obj, context) and returns an decoded version of obj

    Example::

        ExprAdapter(UBInt8("foo"),
            encoder = lambda obj, ctx: obj / 4,
            decoder = lambda obj, ctx: obj * 4,
        )
    """
    __slots__ = ["_encode", "_decode"]
    def __init__(self, subcon, encoder, decoder):
        super(ExprAdapter, self).__init__(subcon)
        self._encode = encoder
        self._decode = decoder


class HexDump(Adapter):
    """
    Adapter for hex-dumping strings. It returns a HexString, which is a string
    """
    __slots__ = ["linesize"]
    def __init__(self, subcon, linesize=16):
        super(HexDump, self).__init__(subcon)
        self.linesize = linesize
    def _encode(self, obj, context):
        return obj
    def _decode(self, obj, context):
        return hexdump(obj, linesize=self.linesize)


class Slicing(Adapter):
    r"""
    Adapter for slicing a list (getting a slice from that list)

    :param subcon: the subcon to slice
    :param count: expected number of elements, needed during building
    :param start: start index (or None for entire list)
    :param stop: stop index (or None for up-to-end)
    :param step: step (or 1 for every element)
    :param empty: value to fill the list with during building
    """
    __slots__ = ["count", "start", "stop", "step", "empty"]
    def __init__(self, subcon, count, start, stop=None, step=1, empty=None):
        super(Slicing, self).__init__(subcon)
        self.count = count
        self.start = start
        self.stop = stop
        self.step = step
        self.empty = empty
    def _encode(self, obj, context):
        if self.start is None:
            return obj
        elif self.stop is None:
            output = [self.empty] * self.count
            output[self.start::self.step] = obj
        else:
            output = [self.empty] * self.count
            output[self.start:self.stop:self.step] = obj
        return output
    def _decode(self, obj, context):
        return obj[self.start:self.stop:self.step]


class Indexing(Adapter):
    r"""
    Adapter for indexing a list (getting a single item from that list)

    :param subcon: the subcon to index
    :param count: expected number of elements, needed during building
    :param index: the index of the list to get
    :param empty: value to fill the list with during building
    """
    __slots__ = ["count", "index", "empty"]
    def __init__(self, subcon, count, index, empty):
        super(Indexing, self).__init__(subcon)
        self.count = count
        self.index = index
        self.empty = empty
    def _encode(self, obj, context):
        output = [self.empty] * self.count
        output[self.index] = obj
        return output
    def _decode(self, obj, context):
        return obj[self.index]


#===============================================================================
# validators
#===============================================================================
class OneOf(Validator):
    r"""
    Validates that the object is one of the listed values.

    :param subcon: object to validate
    :param valids: a collection implementing `in`

    Example::

        >>> OneOf(UBInt8("num"), [4,5,6,7]).parse(b"\x05")
        5

        >>> OneOf(UBInt8("num"), [4,5,6,7]).parse(b"\x08")
        construct.core.ValidationError: ('invalid object', 8)

        >>> OneOf(UBInt8("num"), [4,5,6,7]).build(5)
        b"\x05"

        >>> OneOf(UBInt8("num"), [4,5,6,7]).build(8)
        construct.core.ValidationError: ('invalid object', 8)
    """
    __slots__ = ["valids"]
    def __init__(self, subcon, valids):
        super(OneOf, self).__init__(subcon)
        self.valids = valids
    def _validate(self, obj, context):
        return obj in self.valids


class NoneOf(Validator):
    r"""
    Validates that the object is none of the listed values.

    :param subcon: object to validate
    :param invalids: a collection implementing `in`

    Example::

        >>> NoneOf(UBInt8("num"), [4,5,6,7]).parse(b"\x08")
        8

        >>> NoneOf(UBInt8("num"), [4,5,6,7]).parse(b"\x06")
        construct.core.ValidationError: ('invalid object', 6)

        >>> NoneOf(UBInt8("num"), [4,5,6,7]).build(8)
        b"\x08"

        >>> NoneOf(UBInt8("num"), [4,5,6,7]).build(6)
        construct.core.ValidationError: ('invalid object', 6)
    """
    __slots__ = ["invalids"]
    def __init__(self, subcon, invalids):
        super(NoneOf, self).__init__(subcon)
        self.invalids = invalids
    def _validate(self, obj, context):
        return obj not in self.invalids


#===============================================================================
# strings
#===============================================================================
class StringEncoded(Adapter):
    __slots__ = ["encoding"]
    def __init__(self, subcon, encoding):
        super(StringEncoded, self).__init__(subcon)
        self.encoding = encoding
    def _decode(self, obj, context):
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.decode(self.encoding)
            else:
                obj = self.encoding.decode(obj)
        return obj
    def _encode(self, obj, context):
        if self.encoding:
            if isinstance(self.encoding, str):
                obj = obj.encode(self.encoding)
            else:
                obj = self.encoding.encode(obj)
        else:
            if not isinstance(obj, bytes):
                raise StringError("no encoding provided but building from unicode string?")
        return obj


class StringPaddedTrimmed(Adapter):
    __slots__ = ["length", "padchar", "paddir", "trimdir"]
    def __init__(self, length, subcon, padchar=b"\x00", paddir="right", trimdir="right"):
        if not isinstance(padchar, bytes):
            raise StringError("padchar must be b-string character")
        super(StringPaddedTrimmed, self).__init__(subcon)
        self.length = length
        self.padchar = padchar
        self.paddir = paddir
        self.trimdir = trimdir
    def _decode(self, obj, context):
        length = self.length(context) if callable(self.length) else self.length
        if self.paddir == "right":
            obj = obj.rstrip(self.padchar)
        elif self.paddir == "left":
            obj = obj.lstrip(self.padchar)
        elif self.paddir == "center":
            obj = obj.strip(self.padchar)
        else:
            raise StringError("paddir must be one of: right left center")
        return obj
    def _encode(self, obj, context):
        length = self.length(context) if callable(self.length) else self.length
        if self.paddir == "right":
            obj = obj.ljust(length, self.padchar)
        elif self.paddir == "left":
            obj = obj.rjust(length, self.padchar)
        elif self.paddir == "center":
            obj = obj.center(length, self.padchar)
        else:
            raise StringError("paddir must be one of: right left center")
        if len(obj) > length:
            if self.trimdir == "right":
                obj = obj[:length]
            elif self.trimdir == "left":
                obj = obj[-length:]
            else:
                raise StringError("expected a string of length %s given %s (%r)" % (length,len(obj),obj))
        return obj


def String(length, encoding=None, padchar=b"\x00", paddir="right", trimdir="right"):
    r"""
    A configurable, variable-length string field.

    When parsing, the byte string is stripped of pad character (as specified) from the direction (as specified) then decoded (as specified). Length is a constant integer or a function of the context.
    When building, the string is encoded (as specified) then padded (as specified) from the direction (as specified) or trimmed as bytes (as specified).

    The padding character and direction must be specified for padding to work. The trim direction must be specified for trimming to work.

    :param length: length in bytes (not unicode characters), as int or function
    :param encoding: encoding (e.g. "utf8") or None for bytes
    :param padchar: optional byte or unicode character to pad out strings
    :param paddir: direction to pad out strings (one of: right left both)
    :param trimdir: direction to trim strings (one of: right left)

    Example::

        String("string", 5)
        .parse(b"hello") -> b"hello"
        .build(u"hello") raises StringError
        .sizeof() -> 5

        String("string", 12, encoding="utf8")
        .parse(b"hello joh\xd4\x83n") -> u'hello joh\u0503n'
        .build(u'abc') -> b'abc\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        .sizeof() -> 12

        String("string", 10, padchar="X", paddir="right")
        .parse(b"helloXXXXX") -> b"hello"
        .build(u"hello") -> b"helloXXXXX"

        String("string", 5, trimdir="right")
        .build(u"hello12345") -> b"hello"

        String("string", lambda ctx: ctx.somefield)
        .sizeof() -> ?
    """
    return StringEncoded(
        StringPaddedTrimmed(
            length, Bytes(length),
            padchar, paddir, trimdir),
        encoding)


def PascalString(lengthfield, encoding=None):
    r"""
    A length-prefixed string.

    ``PascalString`` is named after the string types of Pascal, which are length-prefixed. Lisp strings also follow this convention.

    The length field will not appear in the same ``Container``, when parsing. Only the string will be returned. When building, the length is taken from len(the string). The length field can be anonymous (name is None) and can be variable length (such as VarInt).

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
    return StringEncoded(Prefixed(lengthfield, GreedyBytes), encoding)


def CString(terminators=b"\x00", encoding=None):
    r"""
    A string ending in a terminator bytes character.

    ``CString`` is similar to the strings of C, C++, and other related programming languages.

    By default, the terminator is the NULL byte (b'\x00'). Terminators field can be a longer bytes string, and any of the characters breaks parsing. First character is used when building.

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
    return StringEncoded(
        ExprAdapter(
            RepeatUntil(lambda obj,ctx: int2byte(obj) in terminators, UBInt8),
            encoder = lambda obj,ctx: iterateints(obj+terminators),
            decoder = lambda obj,ctx: b''.join(int2byte(c) for c in obj[:-1])),
        encoding)

    # return StringEncoded(
    #     ExprAdapter(
    #         RepeatUntil(lambda obj,ctx: obj in terminators, Bytes(1)),
    #         encoder = lambda obj,ctx: iteratebytes(obj+terminators),
    #         decoder = lambda obj,ctx: b''.join(obj[:-1])),
    #     encoding)


def GreedyString(encoding=None):
    r"""
    A string that reads the rest of the stream until EOF, or writes a given string as is.

    If no encoding is given, this is essentially GreedyBytes.

    :param encoding: encoding (e.g. "utf8") or None for bytes

    .. seealso:: The :class:`~construct.core.GreedyBytes` class.

    Example::

        GreedyString("greedy")
        .parse(b"hello\x00") -> b"hello\x00"
        .build(b"hello\x00") -> b"hello\x00"

        GreedyString("greedy", encoding="utf8")
        .parse(b"hello\x00") -> u"hello\x00"
        .build(u"hello\x00") -> b"hello\x00"
    """
    return StringEncoded(GreedyBytes, encoding)


#===============================================================================
# end of file
#===============================================================================

