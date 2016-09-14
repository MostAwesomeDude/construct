import unittest
import warnings
import traceback
warnings.filterwarnings("ignore", category=DeprecationWarning)

from construct import *
from construct.lib import LazyContainer

import sys
import zlib
import codecs

try:
    codecs.lookup("zlib")
    zlibcodecraises = None
except LookupError:
    zlibcodecraises = LookupError

class ZlibCodec(object):
    encode = staticmethod(zlib.compress)
    decode = staticmethod(zlib.decompress)

class IpAddress(Adapter):
    def _encode(self, obj, context):
        return list(map(int, obj.split(".")))
    def _decode(self, obj, context):
        return "{0}.{1}.{2}.{3}".format(*obj)
IpAddress = IpAddress(Array(4,Byte))



class TestAll(unittest.TestCase):
    alltests = [

        [("string_name" / Byte).parse, b"\x01", 1, None],
        [(u"unicode_name" / Byte).parse, b"\x01", 1, None],
        [(b"bytes_name" / Byte).parse, b"\x01", 1, None],

        [Byte.parse, b"\x00", 0, None],
        [Byte.sizeof, None, 1, None],

        [UBInt8.parse, b"\x01", 0x01, None],
        [UBInt8.build, 0x01, b"\x01", None],
        [UBInt16.parse, b"\x01\x02", 0x0102, None],
        [UBInt16.build, 0x0102, b"\x01\x02", None],
        [UBInt32.parse, b"\x01\x02\x03\x04", 0x01020304, None],
        [UBInt32.build, 0x01020304, b"\x01\x02\x03\x04", None],
        [UBInt64.parse, b"\x01\x02\x03\x04\x05\x06\x07\x08", 0x0102030405060708, None],
        [UBInt64.build, 0x0102030405060708, b"\x01\x02\x03\x04\x05\x06\x07\x08", None],
        [SBInt8.parse, b"\x01", 0x01, None],
        [SBInt8.build, 0x01, b"\x01", None],
        [SBInt16.parse, b"\x01\x02", 0x0102, None],
        [SBInt16.build, 0x0102, b"\x01\x02", None],
        [SBInt32.parse, b"\x01\x02\x03\x04", 0x01020304, None],
        [SBInt32.build, 0x01020304, b"\x01\x02\x03\x04", None],
        [SBInt64.parse, b"\x01\x02\x03\x04\x05\x06\x07\x08", 0x0102030405060708, None],
        [SBInt64.build, 0x0102030405060708, b"\x01\x02\x03\x04\x05\x06\x07\x08", None],
        [ULInt8.parse, b"\x01", 0x01, None],
        [ULInt8.build, 0x01, b"\x01", None],
        [ULInt16.parse, b"\x01\x02", 0x0201, None],
        [ULInt16.build, 0x0201, b"\x01\x02", None],
        [ULInt32.parse, b"\x01\x02\x03\x04", 0x04030201, None],
        [ULInt32.build, 0x04030201, b"\x01\x02\x03\x04", None],
        [ULInt64.parse, b"\x01\x02\x03\x04\x05\x06\x07\x08", 0x0807060504030201, None],
        [ULInt64.build, 0x0807060504030201, b"\x01\x02\x03\x04\x05\x06\x07\x08", None],
        [SLInt8.parse, b"\x01", 0x01, None],
        [SLInt8.build, 0x01, b"\x01", None],
        [SLInt16.parse, b"\x01\x02", 0x0201, None],
        [SLInt16.build, 0x0201, b"\x01\x02", None],
        [SLInt32.parse, b"\x01\x02\x03\x04", 0x04030201, None],
        [SLInt32.build, 0x04030201, b"\x01\x02\x03\x04", None],
        [SLInt64.parse, b"\x01\x02\x03\x04\x05\x06\x07\x08", 0x0807060504030201, None],
        [SLInt64.build, 0x0807060504030201, b"\x01\x02\x03\x04\x05\x06\x07\x08", None],
        # missing sizeof testing

        [UBInt24.parse, b"\x01\x02\x03", 0x010203, None],
        [UBInt24.build, 0x010203, b"\x01\x02\x03", None],
        [UBInt24.sizeof, None, 3, None],
        [Struct('int24' / UBInt24).parse, b"\x01\x02\x03", Container(int24=0x010203), None],
        [Struct('int24' / UBInt24).build, Container(int24=0x010203), b"\x01\x02\x03", None],
        [Struct('int24' / UBInt24).sizeof, None, 3, None],
        [ULInt24.parse, b"\x01\x02\x03", 0x030201, None],
        [ULInt24.build, 0x030201, b"\x01\x02\x03", None],
        [ULInt24.sizeof, None, 3, None],
        [Struct('int24' / ULInt24).parse, b"\x01\x02\x03", Container(int24=0x030201), None],
        [Struct('int24' / ULInt24).build, Container(int24=0x030201), b"\x01\x02\x03", None],
        [Struct('int24' / ULInt24).sizeof, None, 3, None],

        [VarInt.parse, b"\x05", 5, None],
        [VarInt.parse, b"\x85\x05", 645, None],
        [VarInt.build, 5, b"\x05", None],
        [VarInt.build, 645, b"\x85\x05", None],
        [VarInt.parse, b"", None, FieldError],
        [VarInt.build, -1, None, ValueError],
        [VarInt.sizeof, None, None, SizeofError],

        [Bytes(4).parse, b"12345678", b"1234", None],
        [Bytes(4).build, b"1234", b"1234", None],
        # TODO: issue #99
        # [Bytes(4).build, 1, b"\x00\x00\x00\x01", None],
        [Bytes(4).parse, b"", None, FieldError],
        [Bytes(4).build, b"toolong", None, FieldError],
        [Bytes(4).sizeof, None, 4, None],

        # TODO: issue #100
        # TODO: should work with dict(n=4) and this.n
        [Bytes(lambda ctx: ctx.n).parse, (b"12345678",Container(n=4)), b"1234", None],
        [Bytes(lambda ctx: ctx.n).build, (b"1234",Container(n=4)), b"1234", None],
        # TODO: issue #99
        # [Bytes(lambda ctx: ctx.n).build, (1,Container(n=4)), b"\x00\x00\x00\x01", None],
        [Bytes(lambda ctx: ctx.n).parse, (b"",Container(n=4)), None, FieldError],
        [Bytes(lambda ctx: ctx.n).build, (b"toolong",Container(n=4)), None, FieldError],
        [Bytes(lambda ctx: ctx.n).sizeof, None, None, AttributeError],
        [Bytes(lambda ctx: ctx.n).sizeof, Container(n=4), 4, None],

        [GreedyBytes.parse, b"1234", b"1234", None],
        [GreedyBytes.build, b"1234", b"1234", None],
        [GreedyBytes.sizeof, None, None, SizeofError],

        # Note: FormatField is not tested because all *Int{8,16,32,64} fields use that.

        [Array(3,Byte).parse, b"\x01\x02\x03", [1,2,3], None],
        [Array(3,Byte).parse, b"\x01\x02\x03additionalgarbage", [1,2,3], None],
        # issue #101
        # [Array(3,Byte).parse, b"", [1,2,3], ArrayError],
        [Array(3,Byte).build, [1,2,3], b"\x01\x02\x03", None],
        [Array(3,Byte).build, [1,2], None, ArrayError],
        [Array(3,Byte).build, [1,2,3,4,5,6,7,8], None, ArrayError],
        [Array(3,Byte).sizeof, None, 3, None],

        [Array(lambda ctx: 3, Byte).parse, (b"\x01\x02\x03",Container(n=3)), [1,2,3], None],
        [Array(lambda ctx: 3, Byte).parse, (b"\x01\x02\x03additionalgarbage",Container(n=3)), [1,2,3], None],
        # issue #101
        # [Array(lambda ctx: 3, Byte).parse, (b"",Container(n=3)), None, ArrayError],
        [Array(lambda ctx: 3, Byte).build, ([1,2,3],Container(n=3)), b"\x01\x02\x03", None],
        [Array(lambda ctx: 3, Byte).build, ([1,2],Container(n=3)), None, ArrayError],
        [Array(lambda ctx: ctx.n, Byte).parse, (b"\x01\x02\x03",Container(n=3)), [1,2,3], None],
        [Array(lambda ctx: ctx.n, Byte).build, ([1,2,3],Container(n=3)), b"\x01\x02\x03", None],
        [Array(lambda ctx: ctx.n, Byte).sizeof, None, None, AttributeError],
        [Array(lambda ctx: ctx.n, Byte).sizeof, Container(n=4), 4, None],

        [PrefixedArray(Byte,Byte).parse, b"\x02\x0a\x0b", [10,11], None],
        [PrefixedArray(Byte,Byte).build, [10,11], b"\x02\x0a\x0b", None],
        [PrefixedArray(Byte,Byte).sizeof, None, None, SizeofError],

        [Range(3, 5, Byte).parse, b"\x01\x02\x03", [1,2,3], None],
        [Range(3, 5, Byte).parse, b"\x01\x02\x03\x04", [1,2,3,4], None],
        [Range(3, 5, Byte).parse, b"\x01\x02\x03\x04\x05", [1,2,3,4,5], None],
        [Range(3, 5, Byte).parse, b"\x01\x02\x03\x04\x05\x06", [1,2,3,4,5], None],
        [Range(3, 5, Byte).parse, b"", None, RangeError],
        [Range(3, 5, Byte).build, [1,2,3], b"\x01\x02\x03", None],
        [Range(3, 5, Byte).build, [1,2,3,4], b"\x01\x02\x03\x04", None],
        [Range(3, 5, Byte).build, [1,2,3,4,5], b"\x01\x02\x03\x04\x05", None],
        [Range(3, 5, Byte).build, [1,2], None, RangeError],
        [Range(3, 5, Byte).build, [1,2,3,4,5,6], None, RangeError],
        [Range(3, 5, Byte).build, 0, None, RangeError],
        [Range(3, 5, Byte).sizeof, None, None, SizeofError],

        [Range(0,100,Struct("id"/Byte)).parse, b'\x01\x02', [Container(id=1),Container(id=2)], None],
        [Range(0,100,Struct("id"/Byte)).build, [dict(id=i) for i in range(5)], b'\x00\x01\x02\x03\x04', None],
        [Range(0,100,Struct("id"/Byte)).build, dict(id=1), None, RangeError],
        [Range(0,100,Struct("id"/Byte)).sizeof, None, None, SizeofError],
        [lambda none: Range(-2,+7,Byte), None, None, RangeError],
        [lambda none: Range(-2,-7,Byte), None, None, RangeError],
        [lambda none: Range(+2,-7,Byte), None, None, RangeError],

        [GreedyRange(Byte).parse, b"", [], None],
        [GreedyRange(Byte).build, [], b"", None],
        [GreedyRange(Byte).parse, b"\x01\x02", [1,2], None],
        [GreedyRange(Byte).build, [1,2], b"\x01\x02", None],
        [GreedyRange(Byte).sizeof, None, None, SizeofError],

        [RepeatUntil(lambda obj,ctx: obj == 9, Byte).parse, b"\x02\x03\x09garbage", [2,3,9], None],
        [RepeatUntil(lambda obj,ctx: obj == 9, Byte).parse, b"\x02\x03\x08", None, ArrayError],
        [RepeatUntil(lambda obj,ctx: obj == 9, Byte).build, [2,3,9,1,1,1], b"\x02\x03\x09", None],
        [RepeatUntil(lambda obj,ctx: obj == 9, Byte).build, [2,3,8], None, ArrayError],
        [RepeatUntil(lambda obj,ctx: obj == 9, Byte).sizeof, None, None, SizeofError],

        [Struct("a" / ULInt16, "b" / Byte).parse, b"\x01\x00\x02", Container(a=1)(b=2), None],
        [Struct("a" / Byte, "b" / UBInt16, "inner" / Struct("c" / Byte, "d" / Byte)).parse, b"\x01\x00\x02\x03\x04", Container(a=1)(b=2)(inner=Container(c=3)(d=4)), None],
        [Struct("a" / Byte, "b" / UBInt16, Embedded("inner" / Struct("c" / Byte, "d" / Byte))).parse, b"\x01\x00\x02\x03\x04", Container(a=1)(b=2)(c=3)(d=4), None],
        [Struct("a" / ULInt16, "b" / Byte).build, Container(a=1)(b=2), b"\x01\x00\x02", None],
        [Struct("a" / Byte, "b" / UBInt16, "inner" / Struct("c" / Byte, "d" / Byte)).build, Container(a=1)(b=2)(inner=Container(c=3)(d=4)), b"\x01\x00\x02\x03\x04", None],
        [Struct("a" / Byte, "b" / UBInt16, Embedded("inner" / Struct("c" / Byte, "d" / Byte))).build, Container(a=1)(b=2)(c=3)(d=4), b"\x01\x00\x02\x03\x04", None],

        [Sequence(UBInt8, UBInt16).parse, b"\x01\x00\x02", [1,2], None],
        [Sequence(UBInt8, UBInt16).build, [1,2], b"\x01\x00\x02", None],
        [Sequence(UBInt8, UBInt16, Sequence(UBInt8, UBInt8)).parse, b"\x01\x00\x02\x03\x04", [1,2,[3,4]], None],
        [Sequence(UBInt8, UBInt16, Sequence(UBInt8, UBInt8)).build, [1,2,[3,4]], b"\x01\x00\x02\x03\x04", None],
        [Sequence(UBInt8, UBInt16, Embedded(Sequence(UBInt8, UBInt8))).parse, b"\x01\x00\x02\x03\x04", [1,2,3,4], None],
        [Sequence(UBInt8, UBInt16, Embedded(Sequence(UBInt8, UBInt8))).build, [1,2,3,4], b"\x01\x00\x02\x03\x04", None],

        [Computed(lambda ctx: "moo").parse, b"", "moo", None],
        [Computed(lambda ctx: "moo").build, None, b"", None],
        [Computed(lambda ctx: "moo").sizeof, None, 0, None],
        [Struct("c" / Computed(lambda ctx: "moo")).parse, b"", Container(c="moo"), None],
        [Struct("c" / Computed(lambda ctx: "moo")).build, Container(c=None), b"", None],
        # issue #102
        # [Struct("c" / Computed(lambda ctx: "moo")).build, Container(), b"", None],

        [Anchor.parse, b"", 0, None],
        [Anchor.build, None, b"", None],
        [Anchor.sizeof, None, 0, None],

        [AnchorRange.parse, b"", 0, None],
        [AnchorRange.build, None, b"", None],
        [AnchorRange.sizeof, None, 0, None],
        [Struct("anchorrange"/AnchorRange, "a"/Byte, "anchorrange"/AnchorRange,allow_overwrite=True).parse, b"\xff", Container(anchorrange=Container(offset1=0)(offset2=1)(length=1))(a=255), None],
        [Struct("anchorrange"/AnchorRange, "a"/Byte, "anchorrange"/AnchorRange,allow_overwrite=True).build, dict(a=255), b"\xff", None],

        [Pass.parse, b"", None, None],
        [Pass.build, None, b"", None],
        [Pass.sizeof, None, 0, None],

        [Terminator.parse, b"", None, None],
        [Terminator.parse, b"x", None, TerminatorError],
        [Terminator.build, None, b"", None],
        [Terminator.sizeof, None, 0, None],

        [Pointer(lambda ctx: 2, "pointer" / UBInt8).parse, b"\x00\x00\x07", 7, None],
        [Pointer(lambda ctx: 2, "pointer" / UBInt8).build, 7, b"\x00\x00\x07", None],
        [Pointer(lambda ctx: 2, "pointer" / UBInt8).sizeof, None, 0, None],

        [Const(b"MZ").parse, b"MZ", b"MZ", None],
        [Const(b"MZ").parse, b"ELF", None, ConstError],
        [Const(b"MZ").build, None, b"MZ", None],
        [Const(b"MZ").build, b"MZ", b"MZ", None],
        [Const(b"MZ").sizeof, None, 2, None],
        [Const(ULInt32, 255).parse, b"\xff\x00\x00\x00", 255, None],
        [Const(ULInt32, 255).parse, b"\x00\x00\x00\x00", 255, ConstError],
        [Const(ULInt32, 255).build, None, b"\xff\x00\x00\x00", None],
        [Const(ULInt32, 255).build, 255, b"\xff\x00\x00\x00", None],
        [Const(ULInt32, 255).sizeof, None, 4, None],

        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}).parse, b"\x00\x02", 2, None],
        [Switch(lambda ctx: 6, {1:Byte, 5:UBInt16}).parse, b"\x00\x02", None, SwitchError],
        [Switch(lambda ctx: 6, {1:Byte, 5:UBInt16}, default=Byte).parse, b"\x00\x02", 0, None],
        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}, include_key=True).parse, b"\x00\x02", (5, 2), None],
        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}).build, 2, b"\x00\x02", None],
        [Switch(lambda ctx: 6, {1:Byte, 5:UBInt16}).build, 9, None, SwitchError],
        [Switch(lambda ctx: 6, {1:Byte, 5:UBInt16}, default=Byte).build, 9, b"\x09", None],
        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}, include_key=True).build, ((5, 2),), b"\x00\x02", None],
        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}, include_key=True).build, ((89, 2),), None, SwitchError],
        [Switch(lambda ctx: 5, {1:Byte, 5:UBInt16}).sizeof, None, None, SizeofError],

        [IfThenElse(lambda ctx: True,  UBInt8, UBInt16).parse, b"\x01", 1, None],
        [IfThenElse(lambda ctx: False, UBInt8, UBInt16).parse, b"\x00\x01", 1, None],
        [IfThenElse(lambda ctx: True,  UBInt8, UBInt16).build, 1, b"\x01", None],
        [IfThenElse(lambda ctx: False, UBInt8, UBInt16).build, 1, b"\x00\x01", None],
        [IfThenElse(lambda ctx: False, UBInt8, UBInt16).sizeof, None, None, SizeofError],

        [If(lambda ctx: True,  UBInt8).parse, b"\x01", 1, None],
        [If(lambda ctx: False, UBInt8).parse, b"", None, None],
        [If(lambda ctx: True,  UBInt8).build, 1, b"\x01", None],
        [If(lambda ctx: False, UBInt8).build, None, b"", None],
        [If(lambda ctx: False, UBInt8).sizeof, None, None, SizeofError],

        [Padding(4).parse, b"\x00\x00\x00\x00", None, None],
        [Padding(4).build, None, b"\x00\x00\x00\x00", None],
        [Padding(4).sizeof, None, 4, None],
        [Padding(4, strict=True).parse, b"\x00\x00\x00\x00", None, None],
        [Padding(4, strict=True).parse, b"????", None, PaddingError],
        [Padding(4, strict=True).build, None, b"\x00\x00\x00\x00", None],
        [Padding(4, pattern=b'x', strict=True).parse, b"xxxx", None, None],
        [Padding(4, pattern=b'x', strict=True).parse, b"????", None, PaddingError],
        [lambda none: Padding(4, pattern=b"??"), None, None, PaddingError],
        [lambda none: Padding(4, pattern=u"?"), None, None, PaddingError],

        [Padded(4, Byte).parse, b"\x01\x00\x00\x00", 1, None],
        [Padded(4, Byte).build, 1, b"\x01\x00\x00\x00", None],
        [Padded(4, Byte).sizeof, None, 4, None],
        [Padded(4, Byte, strict=True).parse, b"\x01\x00\x00\x00", 1, None],
        [Padded(4, Byte, strict=True).parse, b"\x01???", None, PaddingError],
        [Padded(4, Byte, strict=True).build, 1, b"\x01\x00\x00\x00", None],
        [Padded(4, Byte, pattern=b'x', strict=True).parse, b"\x01xxx", 1, None],
        [Padded(4, Byte, pattern=b'x', strict=True).parse, b"\x01???", None, PaddingError],
        [lambda none: Padded(4, Byte, pattern=b"??"), None, None, PaddingError],
        [lambda none: Padded(4, Byte, pattern=u"?"), None, None, PaddingError],

        [Aligned(Byte, modulus=4).parse, b"\x01\x00\x00\x00", 1, None],
        [Aligned(Byte, modulus=4).build, 1, b"\x01\x00\x00\x00", None],
        [Aligned(Byte, modulus=4).sizeof, None, 4, None],
        [Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).parse, b"\x01\x00\x00\x00\x02", Container(a=1)(b=2), None],
        [Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).build, Container(a=1)(b=2), b"\x01\x00\x00\x00\x02", None],
        [Struct(Aligned("a"/Byte, modulus=4), "b"/Byte).sizeof, None, 5, None],

        [Enum(Byte,q=3,r=4,t=5).parse, b"\x04", "r", None],
        [Enum(Byte,q=3,r=4,t=5).parse, b"\x07", None, MappingError],
        [Enum(Byte,q=3,r=4,t=5, _default_="spam").parse, b"\x07", "spam", None],
        [Enum(Byte,q=3,r=4,t=5, _default_=Pass).parse, b"\x07", 7, None],
        [Enum(Byte,q=3,r=4,t=5).build, "r", b"\x04", None],
        [Enum(Byte,q=3,r=4,t=5).build, "spam", None, MappingError],
        [Enum(Byte,q=3,r=4,t=5, _default_=9).build, "spam", b"\x09", None],
        [Enum(Byte,q=3,r=4,t=5, _default_=Pass).build, 9, b"\x09", None],
        [Enum(Byte,q=3,r=4,t=5).sizeof, None, 1, None],

        [Flag.parse, b"\x00", False, None],
        [Flag.parse, b"\x01", True, None],
        [Flag.parse, b"\xff", True, None],
        [Flag.build, False, b"\x00", None],
        [Flag.build, True, b"\x01", None],
        [Flag.sizeof, None, 1, None],

        # testing / >> [] operators
        [Struct("new" / ("old" / Byte)).parse, b"\x01", Container(new=1), None],
        [Struct("new" / ("old" / Byte)).build, Container(new=1), b"\x01", None],
        [Byte[4].parse, b"\x01\x02\x03\x04", [1,2,3,4], None],
        [Byte[4].build, [1,2,3,4], b"\x01\x02\x03\x04", None],
        [Byte[2:3].parse, b"\x01", None, RangeError],
        [Byte[2:3].parse, b"\x01\x02", [1,2], None],
        [Byte[2:3].parse, b"\x01\x02\x03", [1,2,3], None],
        [Byte[2:3].parse, b"\x01\x02\x03", [1,2,3], None],
        [Byte[2:3].parse, b"\x01\x02\x03\x04", [1,2,3], None],
        [Struct("nums" / Byte[4]).parse, b"\x01\x02\x03\x04", Container(nums=[1,2,3,4]), None],
        [Struct("nums" / Byte[4]).build, Container(nums=[1,2,3,4]), b"\x01\x02\x03\x04", None],
        [(UBInt8 >> UBInt16).parse, b"\x01\x00\x02", [1,2], None],
        [(UBInt8 >> UBInt16 >> UBInt32).parse, b"\x01\x00\x02\x00\x00\x00\x03", [1,2,3], None],
        [(UBInt8[2] >> UBInt16[2]).parse, b"\x01\x02\x00\x03\x00\x04", [[1,2],[3,4]], None],

        # testing underlying Renamed
        [Struct(Renamed("new",Renamed("old",Byte))).parse, b"\x01", Container(new=1), None],
        [Struct(Renamed("new",Renamed("old",Byte))).build, Container(new=1), b"\x01", None],

        [BitField(8).parse, b"\x01\x01\x01\x01\x01\x01\x01\x01", 255, None],
        [BitField(8).build, 255, b"\x01\x01\x01\x01\x01\x01\x01\x01", None],
        [BitField(8).sizeof, None, 8, None],
        [BitField(8, signed=True).parse, b"\x01\x01\x01\x01\x01\x01\x01\x01", -1, None],
        [BitField(8, signed=True).build, -1, b"\x01\x01\x01\x01\x01\x01\x01\x01", None],
        [BitField(8, swapped=True, bytesize=4).parse, b"\x01\x01\x01\x01\x00\x00\x00\x00", 0x0f, None],
        [BitField(8, swapped=True, bytesize=4).build, 0x0f, b"\x01\x01\x01\x01\x00\x00\x00\x00", None],
        [BitField(lambda ctx: 8).parse, b"\x01" * 8, 255, None],
        [BitField(lambda ctx: 8).build, 255, b"\x01" * 8, None],
        [BitField(lambda ctx: 8).sizeof, None, 8, None],

        [Bitwise(Bytes(8)).parse, b"\xff", b"\x01\x01\x01\x01\x01\x01\x01\x01", None],
        [Bitwise(Bytes(8)).build, b"\x01\x01\x01\x01\x01\x01\x01\x01", b"\xff", None],
        [Bitwise(Bytes(8)).sizeof, None, 1, None],
        [Bitwise(Bytes(lambda ctx: 8)).parse, b"\xff", b"\x01\x01\x01\x01\x01\x01\x01\x01", None],
        [Bitwise(Bytes(lambda ctx: 8)).build, b"\x01\x01\x01\x01\x01\x01\x01\x01", b"\xff", None],
        [Bitwise(Bytes(lambda ctx: 8)).sizeof, None, 1, None],

        [ByteSwapped(Bytes(5)).parse, b"12345?????", b"54321", None],
        [ByteSwapped(Bytes(5)).build, b"12345", b"54321", None],
        [ByteSwapped(Bytes(5)).sizeof, None, 5, None],
        [ByteSwapped(Struct("a"/Byte,"b"/Byte)).parse, b"\x01\x02", Container(a=2)(b=1), None],
        [ByteSwapped(Struct("a"/Byte,"b"/Byte)).build, Container(a=2)(b=1), b"\x01\x02", None],
        [ByteSwapped(Bytes(5), size=4).parse, b"54321", None, FieldError],
        # from issue #70
        [ByteSwapped(BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitField(16), Padding(4))).parse, b'\xd0\xbc\xfa', Container(flag1=1)(flag2=1)(number=0xabcd), None],
        [BitStruct("flag1"/Bit, "flag2"/Bit, Padding(2), "number"/BitField(16), Padding(4)).parse, b'\xfa\xbc\xd1', Container(flag1=1)(flag2=1)(number=0xabcd), None],

        [Slicing(Array(4,Byte), 4, 1, 3, empty=0).parse, b"\x01\x02\x03\x04", [2,3], None],
        [Slicing(Array(4,Byte), 4, 1, 3, empty=0).build, [2,3], b"\x00\x02\x03\x00", None],
        [Slicing(Array(4,Byte), 4, 1, 3, empty=0).sizeof, None, 4, None],

        [Indexing(Array(4,Byte), 4, 2, empty=0).parse, b"\x01\x02\x03\x04", 3, None],
        [Indexing(Array(4,Byte), 4, 2, empty=0).build, 3, b"\x00\x00\x03\x00", None],
        [Indexing(Array(4,Byte), 4, 2, empty=0).sizeof, None, 4, None],

        [Select(UBInt32, UBInt16).parse, b"\x07", None, SelectError],
        [Select(UBInt32, UBInt16, UBInt8).parse, b"\x07", 7, None],
        [Select(UBInt32, UBInt16, UBInt8).build, 7, b"\x00\x00\x00\x07", None],
        [Select(UBInt32, UBInt16, UBInt8).sizeof, None, None, SizeofError],
        [Select("a"/UBInt32, "b"/UBInt16, "c"/UBInt8, includename=True).parse, b"\x07", ("c", 7), None],
        [Select("a"/UBInt32, "b"/UBInt16, "c"/UBInt8, includename=True).build, (("c", 7),), b"\x07", None],
        [Select("a"/UBInt32, "b"/UBInt16, "c"/UBInt8, includename=True).build, (("d", 7),), None, SelectError],
        [Select("a"/UBInt32, "b"/UBInt16, "c"/UBInt8, includename=True).sizeof, None, None, SizeofError],

        [Peek(UBInt8).parse, b"\x01", 1, None],
        [Peek(UBInt8).parse, b"", None, None],
        [Peek(UBInt8).build, 1, b"", None],
        [Peek(UBInt8).build, None, b"", None],
        [Peek(UBInt8).sizeof, None, 0, None],
        [Peek(VarInt).sizeof, None, 0, None],
        [Struct(Peek("a"/UBInt8), "b"/UBInt16).parse, b"\x01\x02", Container(a=1)(b=0x0102), None],
        [Struct(Peek("a"/UBInt8), "b"/UBInt16).build, dict(a=1,b=0x0102), b"\x01\x02", None],
        [Struct(Peek("a"/Byte), Peek("b"/UBInt16),).parse, b"\x01\x02", Container(a=1)(b=0x0102), None],
        [Struct(Peek("a"/Byte), Peek("b"/UBInt16),).build, dict(a=0,b=0x0102), b"", None],
        [Struct(Peek("a"/Byte), Peek("b"/UBInt16),).sizeof, None, 0, None],

        [Optional(ULInt32).parse, b"\x01\x00\x00\x00", 1, None],
        [Optional(ULInt32).build, 1, b"\x01\x00\x00\x00", None],
        [Optional(ULInt32).parse, b"?", None, None],
        [Optional(ULInt32).build, None, b"", None],
        # issue #104
        # [Optional(ULInt32).sizeof, None, 0, None],

        [Union("a"/UBInt16, "b"/Struct("b1"/UBInt8, "b2"/UBInt8)).parse, b"\x01\x02", Container(a=0x0102)(b=Container(b1=1)(b2=2)), None],
        [Union("a"/UBInt16, "b"/Struct("b1"/UBInt8, "b2"/UBInt8)).build, dict(a=0x0102,b=dict(b1=1,b2=2)), b"\x01\x02", None],
        [Union("sub1"/Struct("a"/UBInt8, "b"/UBInt8), "sub2"/Struct("c"/ULInt16), ).build, dict(sub1=dict(a=1,b=2)), b"\x01\x02", None],
        [Union("sub1"/Struct("a"/UBInt8, "b"/UBInt8), "sub2"/Struct("c"/ULInt16), ).build, dict(sub2=dict(c=3)), b"\x03\x00", None],
        [Union("a"/UBInt8, "b"/UBInt16, buildfrom=0).build, dict(a=1,b=2), b"\x01", None],
        [Union("a"/UBInt8, "b"/UBInt16, buildfrom=1).build, dict(a=1,b=2), b"\x00\x02", None],
        [Union(Embedded("sub1"/Struct("a"/Byte, "b"/Byte)), Embedded("sub2"/Struct("c"/UBInt16)), buildfrom="sub1").build, dict(a=1,b=2), b"\x01\x02", None],
        [Union(Embedded("sub1"/Struct("a"/Byte, "b"/Byte)), Embedded("sub2"/Struct("c"/UBInt16)), buildfrom="sub2").build, dict(c=3), b"\x00\x03", None],
        [Union("a"/Byte, "b"/PascalString(Byte), ).build, None, None, SelectError],
        [Union(Byte).sizeof, None, None, SizeofError],
        [Union(VarInt).sizeof, None, None, SizeofError],
        [Union(CString()).sizeof, None, None, SizeofError],

        [PrefixedArray(Byte,Byte).parse, b"\x03\x01\x02\x03", [1,2,3], None],
        [PrefixedArray(Byte,Byte).parse, b"\x00", [], None],
        [PrefixedArray(Byte,Byte).parse, b"", None, ArrayError],
        [PrefixedArray(Byte,Byte).parse, b"\x03\x01", None, ArrayError],
        [PrefixedArray(Byte,Byte).build, [1,2,3], b"\x03\x01\x02\x03", None],
        [PrefixedArray(Byte,Byte).sizeof, None, None, SizeofError],
        [PrefixedArray(Byte,Byte).sizeof, [1,1,1], 4, SizeofError],

        [Prefixed(Byte,ULInt16).parse, b"\x02\xff\xffgarbage", 65535, None],
        [Prefixed(Byte,ULInt16).build, 65535, b"\x02\xff\xff", None],
        [Prefixed(Byte,ULInt16).sizeof, None, None, SizeofError],
        [Prefixed(VarInt,GreedyBytes).parse, b"\x03abcgarbage", b"abc", None],
        [Prefixed(VarInt,GreedyBytes).build, b"abc", b'\x03abc', None],
        [Prefixed(VarInt,GreedyBytes).sizeof, None, None, SizeofError],

        [Prefixed(Byte,Compressed(GreedyBytes,"zlib")).parse, b'\x0cx\x9c30\xa0=\x00\x00\xb3q\x12\xc1???????????', b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", zlibcodecraises],
        [Prefixed(Byte,Compressed(GreedyBytes,"zlib")).build, b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", b'\x0cx\x9c30\xa0=\x00\x00\xb3q\x12\xc1', zlibcodecraises],
        [Prefixed(Byte,Compressed(CString(),"zlib")).parse, b'\rx\x9c30\xa0=`\x00\x00\xc62\x12\xc1??????????????', b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", zlibcodecraises],
        [Prefixed(Byte,Compressed(CString(),"zlib")).build, b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", b'\rx\x9c30\xa0=`\x00\x00\xc62\x12\xc1', zlibcodecraises],
        [Prefixed(Byte,Compressed(CString(),"zlib")).sizeof, None, None, SizeofError],

        [String(5).parse, b"hello", b"hello", None],
        [String(5).build, b"hello", b"hello", None],
        [String(5).parse, b"", None, StringError],
        [String(5).build, b"", b"\x00\x00\x00\x00\x00", None],
        [String(12, encoding="utf8").parse, b"hello joh\xd4\x83n", u"hello joh\u0503n", None],
        [String(12, encoding="utf8").build, u"hello joh\u0503n", b"hello joh\xd4\x83n", None],
        [String(12, encoding="utf8").sizeof, None, 12, None],
        [String(5).build, u"hello", None, StringError],  # missing encoding
        [String(10, padchar=b"X", paddir="right").parse, b"helloXXXXX", b"hello", None],
        [String(10, padchar=b"X", paddir="left").parse, b"XXXXXhello", b"hello", None],
        [String(10, padchar=b"X", paddir="center").parse, b"XXhelloXXX", b"hello", None],
        [String(10, padchar=b"X", paddir="right").build, b"hello", b"helloXXXXX", None],
        [String(10, padchar=b"X", paddir="left").build, b"hello", b"XXXXXhello", None],
        [String(10, padchar=b"X", paddir="center").build, b"hello", b"XXhelloXXX", None],
        [String(10, padchar=u"X", paddir="right", encoding="utf8").build, b"hello", b"helloXXXXX", None],
        [String(10, padchar=u"X", paddir="left", encoding="utf8").build, b"hello", b"XXXXXhello", None],
        [String(10, padchar=u"X", paddir="center", encoding="utf8").build, b"hello", b"XXhelloXXX", None],
        [String(5, trimdir="right").build, b"1234567890", b"12345", None],
        [String(5, trimdir="left").build, b"1234567890", b"67890", None],
        [String(5, padchar=b"X", paddir="left", encoding="utf8").sizeof, None, 5, None],
        [String(5).sizeof, None, 5, None],

        [PascalString().parse, b"\x05hello????????", b"hello", None],
        [PascalString().build, b"hello", b"\x05hello", None],
        [PascalString(encoding="utf8").parse, b"\x05hello", u"hello", None],
        [PascalString(encoding="utf8").build, u"hello", b"\x05hello", None],
        [PascalString(UBInt16).parse, b"\x00\x05hello????????", b"hello", None],
        [PascalString(UBInt16).build, b"hello", b"\x00\x05hello", None],
        [PascalString().sizeof, None, None, SizeofError],

        [CString().parse, b"hello\x00", b"hello", None],
        [CString(encoding="utf8").parse, b"hello\x00", u"hello", None],
        [CString().build, b"hello", b"hello\x00", None],
        [CString(encoding="utf8").build, u"hello", b"hello\x00", None],
        [CString(terminators=b"XYZ", encoding="utf8").parse, b"helloX", u"hello", None],
        [CString(terminators=b"XYZ", encoding="utf8").parse, b"helloY", u"hello", None],
        [CString(terminators=b"XYZ", encoding="utf8").parse, b"helloZ", u"hello", None],
        [CString(terminators=b"XYZ", encoding="utf8").build, u"hello", b"helloX", None],
        [CString().sizeof, None, None, SizeofError],

        [GreedyString().parse, b"hello\x00", b"hello\x00", None],
        [GreedyString().parse, b"", b"", None],
        [GreedyString().build, b"hello\x00", b"hello\x00", None],
        [GreedyString().build, b"", b"", None],
        [GreedyString(encoding="utf8").parse, b"hello\x00", u"hello\x00", None],
        [GreedyString(encoding="utf8").parse, b"", u"", None],
        [GreedyString(encoding="utf8").build, u"hello\x00", b"hello\x00", None],
        [GreedyString(encoding="utf8").build, u"", b"", None],
        [GreedyString().sizeof, None, None, SizeofError],

        # [ExprAdapter(UBInt8("expradapter"), 
        #     encoder = lambda obj, ctx: obj // 7, 
        #     decoder = lambda obj, ctx: obj * 7,
        #     ).parse, b"\x06", 42, None],
        # [ExprAdapter(UBInt8("expradapter"), 
        #     encoder = lambda obj, ctx: obj // 7, 
        #     decoder = lambda obj, ctx: obj * 7,
        #     ).build, 42, b"\x06", None],

        [LazyBound(lambda ctx: Byte).parse, b"\x01", 1, None],
        [LazyBound(lambda ctx: Byte).build, 1, b"\x01", None],
        [LazyBound(lambda ctx: Byte).sizeof, None, 1, None],

        # did this one come from some issue?
        [Struct("length" / Byte, "inner" / Struct("inner_length" / Byte, "data" / Bytes(lambda ctx: ctx._.length + ctx.inner_length))).parse, b"\x03\x02helloXXX", Container(length=3)(inner=Container(inner_length=2)(data=b"hello")), None],
        [Struct("length" / Byte, "inner" / Struct("inner_length" / Byte, "data" / Bytes(lambda ctx: ctx._.length + ctx.inner_length))).sizeof, Container(inner_length=2)(_=Container(length=3)), 7, None],

        [NoneOf(Byte,[4,5,6,7]).parse, b"\x08", 8, None],
        [NoneOf(Byte,[4,5,6,7]).parse, b"\x06", 8, ValidationError],

        [OneOf(Byte,[4,5,6,7]).parse, b"\x05", 5, None],
        [OneOf(Byte,[4,5,6,7]).parse, b"\x08", 5, ValidationError],
        [OneOf(Byte,[4,5,6,7]).build, 5, b"\x05", None],
        [OneOf(Byte,[4,5,6,7]).build, 8, None, ValidationError],

        [HexDump(Bytes(6)).parse, b'abcdef', '0000   61 62 63 64 65 66                                 abcdef\n', None],
        [HexDump(Bytes(6)).build, b'abcdef', b'abcdef', None],

        [OnDemand(Byte).parse(b"\x01garbage"), None, 1, None],
        [OnDemand(Byte).build, 1, b"\x01", None],
        [OnDemand(Byte).sizeof, None, 1, None],

        # issue #109
        # [OnDemandPointer(lambda ctx: 2, Byte).parse(b"\x01\x02\x03\x04"), None, 3, None],
        [OnDemandPointer(lambda ctx: 2, Byte).build, 1, b"\x00\x00\x01", None],
        [OnDemandPointer(lambda ctx: 2, Byte).sizeof, None, 0, None],

        [IpAddress.parse, b"\x7f\x80\x81\x82", "127.128.129.130", None],
        [IpAddress.build, "127.1.2.3", b"\x7f\x01\x02\x03", None],
        # issue #107
        # [IpAddress.build, "300.1.2.3", None, FieldError],
        [IpAddress.sizeof, None, 4, None],




        # [Buffered(UBInt8("buffered"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
        # [Buffered(GreedyRange(UBInt8("buffered")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", None, SizeofError],
        # [Buffered(UBInt8("buffered"), lambda x:x, lambda x:x, lambda x:x).build, 7, b"\x07", None],
        # [Buffered(GreedyRange(UBInt8("buffered")), lambda x:x, lambda x:x, lambda x:x).build, [7], None, SizeofError],

        # [Restream(UBInt8("restream"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
        # [Restream(GreedyRange(UBInt8("restream")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", [7], None],
        # [Restream(UBInt8("restream"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
        # [Restream(GreedyRange(UBInt8("restream")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", [7], None],

        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}).parse, b"\x03", "y", None],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}).parse, b"\x04", None, MappingError],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}, decdefault="foo").parse, b"\x04", "foo", None],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}, decdefault=Pass).parse, b"\x04", 4, None],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}).build, "y", b"\x03", None],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}).build, "z", None, MappingError],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}, encdefault=17).build, "foo", b"\x11", None],
        # [MappingAdapter(UBInt8("mappingadapter"), {2:"x",3:"y"}, {"x":2,"y":3}, encdefault=Pass).build, 4, b"\x04", None],

        # [FlagsAdapter(UBInt8("flagsadapter"), {"a":1,"b":2,"c":4,"d":8,"e":16,"f":32,"g":64,"h":128}).parse, b"\x81", FlagsContainer(a=True, b=False,c=False,d=False,e=False,f=False,g=False,h=True), None],
        # [FlagsAdapter(UBInt8("flagsadapter"), {"a":1,"b":2,"c":4,"d":8,"e":16,"f":32,"g":64,"h":128}).build, FlagsContainer(a=True, b=False,c=False,d=False,e=False,f=False,g=False,h=True), b"\x81", None],
    ]

    def test_suite(self):
        errors = []
        for i, (func, args, res, exctype) in enumerate(self.alltests):
            if type(args) is not tuple:
                args = (args,)
            try:
                r = func(*args)
            except:
                t, ex, tb = sys.exc_info()
                if exctype is None:
                    errors.append("%d::: %s" % (i, "".join(traceback.format_exception(t, ex, tb))))
                    continue
                if t is not exctype:
                    errors.append("%s: raised %r, expected %r" % (func, t, exctype))
                    continue
            else:
                if exctype is not None:
                    print("Testing: %r", (i, func, args, res, exctype))
                    errors.append("%s: expected exception %r" % (func, exctype))
                    continue
                if r != res:
                    errors.append("%s: returned %r, expected %r" % (func, r, res))
                    continue
        if errors:
            self.fail("\n=========================\n".join(str(e) for e in errors))


