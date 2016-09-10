from io import BytesIO

from construct.core import Adapter, AdaptationError, Pass, Validator
from construct.lib import int_to_bin, bin_to_int, swap_bytes
from construct.lib import FlagsContainer, HexString


#===============================================================================
# exceptions
#===============================================================================
class BitIntegerError(AdaptationError):
    pass
class MappingError(AdaptationError):
    pass


#===============================================================================
# adapters
#===============================================================================
class BitIntegerAdapter(Adapter):
    """
    Adapter for bit-integers (converts bitstrings to integers, and vice versa).
    See BitField.

    :param subcon: the subcon to adapt
    :param width: the size of the subcon, in bits
    :param swapped: whether to swap byte order (little endian/big endian).
                    default is False (big endian)
    :param signed: whether the value is signed (two's complement). the default
                   is False (unsigned)
    :param bytesize: number of bits per byte, used for byte-swapping (if swapped).
                     default is 8.
    """
    __slots__ = ["width", "swapped", "signed", "bytesize"]
    def __init__(self, subcon, width, swapped = False, signed = False,
                 bytesize = 8):
        super(BitIntegerAdapter, self).__init__(subcon)
        self.width = width
        self.swapped = swapped
        self.signed = signed
        self.bytesize = bytesize
    def _encode(self, obj, context):
        if obj < 0 and not self.signed:
            raise BitIntegerError("object is negative, but field is not signed",
                obj)
        obj2 = int_to_bin(obj, width = self.width(context) if callable(self.width) else self.width)
        if self.swapped:
            obj2 = swap_bytes(obj2, bytesize = self.bytesize)
        return obj2
    def _decode(self, obj, context):
        if self.swapped:
            obj = swap_bytes(obj, bytesize = self.bytesize)
        return bin_to_int(obj, signed = self.signed)


class MappingAdapter(Adapter):
    """
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
    def __init__(self, subcon, decoding, encoding,
                 decdefault = NotImplemented, encdefault = NotImplemented):
        super(MappingAdapter, self).__init__(subcon)
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


class FlagsAdapter(Adapter):
    """
    Adapter for flag fields. Each flag is extracted from the number, resulting
    in a FlagsContainer object. Not intended for direct usage. See FlagsEnum.

    :param subcon: the subcon to extract
    :param flags: a dictionary mapping flag-names to their value
    """
    __slots__ = ["flags"]
    def __init__(self, subcon, flags):
        super(FlagsAdapter, self).__init__(subcon)
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


class HexDumpAdapter(Adapter):
    """
    Adapter for hex-dumping strings. It returns a HexString, which is a string
    """
    __slots__ = ["linesize"]
    def __init__(self, subcon, linesize=16):
        super(HexDumpAdapter, self).__init__(subcon)
        self.linesize = linesize
    def _encode(self, obj, context):
        return obj
    def _decode(self, obj, context):
        return HexString(obj, linesize=self.linesize)


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

