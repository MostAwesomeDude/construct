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

import warnings
import traceback
import unittest
warnings.filterwarnings("ignore", category=DeprecationWarning)



all_tests = [
    #
    # constructs
    #
    [("string_name" / Byte).parse, b"\x00", 0, None],
    [(u"unicode_name" / Byte).parse, b"\x00", 0, None],
    [(b"bytes_name" / Byte).parse, b"\x00", 0, None],

    [Byte.parse, b"\x00", 0, None],

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

    [VarInt.parse, b"\x05", 5, None],
    [VarInt.parse, b"\x85\x05", 645, None],
    [VarInt.build, 5, b"\x05", None],
    [VarInt.build, 645, b"\x85\x05", None],
    [VarInt.parse, b"", None, FieldError],
    [VarInt.build, -1, None, ValueError],

    # [MetaArray(lambda ctx: 3, UBInt8("metaarray")).parse, b"\x01\x02\x03", [1,2,3], None],
    # [MetaArray(lambda ctx: 3, UBInt8("metaarray")).parse, b"\x01\x02", None, ArrayError],
    # [MetaArray(lambda ctx: 3, UBInt8("metaarray")).build, [1,2,3], b"\x01\x02\x03", None],
    # [MetaArray(lambda ctx: 3, UBInt8("metaarray")).build, [1,2], None, ArrayError],

    # [Range(3, 5, UBInt8("range")).parse, b"\x01\x02\x03", [1,2,3], None],
    # [Range(3, 5, UBInt8("range")).parse, b"\x01\x02\x03\x04", [1,2,3,4], None],
    # [Range(3, 5, UBInt8("range")).parse, b"\x01\x02\x03\x04\x05", [1,2,3,4,5], None],
    # [Range(3, 5, UBInt8("range")).parse, b"\x01\x02", None, RangeError],
    # [Range(3, 5, UBInt8("range")).build, [1,2,3], b"\x01\x02\x03", None],
    # [Range(3, 5, UBInt8("range")).build, [1,2,3,4], b"\x01\x02\x03\x04", None],
    # [Range(3, 5, UBInt8("range")).build, [1,2,3,4,5], b"\x01\x02\x03\x04\x05", None],
    # [Range(3, 5, UBInt8("range")).build, [1,2], None, RangeError],
    # [Range(3, 5, UBInt8("range")).build, [1,2,3,4,5,6], None, RangeError],

    # [RepeatUntil(lambda obj, ctx: obj == 9, UBInt8("repeatuntil")).parse, b"\x02\x03\x09", [2,3,9], None],
    # [RepeatUntil(lambda obj, ctx: obj == 9, UBInt8("repeatuntil")).parse, b"\x02\x03\x08", None, ArrayError],
    # [RepeatUntil(lambda obj, ctx: obj == 9, UBInt8("repeatuntil")).build, [2,3,9], b"\x02\x03\x09", None],
    # [RepeatUntil(lambda obj, ctx: obj == 9, UBInt8("repeatuntil")).build, [2,3,8], None, ArrayError],

    # [Struct("struct", UBInt8("a"), UBInt16("b")).parse, b"\x01\x00\x02", Container(a=1)(b=2), None],
    # [Struct("struct", UBInt8("a"), UBInt16("b"), Struct("inner", UBInt8("c"), UBInt8("d"))).parse, b"\x01\x00\x02\x03\x04", Container(a=1)(b=2)(inner=Container(c=3)(d=4)), None],
    # [Struct("struct", UBInt8("a"), UBInt16("b"), Embedded(Struct("inner", UBInt8("c"), UBInt8("d")))).parse, b"\x01\x00\x02\x03\x04", Container(a=1)(b=2)(c=3)(d=4), None],
    # [Struct("struct", UBInt8("a"), UBInt16("b")).build, Container(a=1)(b=2), b"\x01\x00\x02", None],
    # [Struct("struct", UBInt8("a"), UBInt16("b"), Struct("inner", UBInt8("c"), UBInt8("d"))).build, Container(a=1)(b=2)(inner=Container(c=3)(d=4)), b"\x01\x00\x02\x03\x04", None],
    # [Struct("struct", UBInt8("a"), UBInt16("b"), Embedded(Struct("inner", UBInt8("c"), UBInt8("d")))).build, Container(a=1)(b=2)(c=3)(d=4), b"\x01\x00\x02\x03\x04", None],

    # [Sequence("sequence", UBInt8("a"), UBInt16("b")).parse, b"\x01\x00\x02", [1,2], None],
    # [Sequence("sequence", UBInt8("a"), UBInt16("b"), Sequence("foo", UBInt8("c"), UBInt8("d"))).parse, b"\x01\x00\x02\x03\x04", [1,2,[3,4]], None],
    # [Sequence("sequence", UBInt8("a"), UBInt16("b"), Embedded(Sequence("foo", UBInt8("c"), UBInt8("d")))).parse, b"\x01\x00\x02\x03\x04", [1,2,3,4], None],
    # [Sequence("sequence", UBInt8("a"), UBInt16("b")).build, [1,2], b"\x01\x00\x02", None],
    # [Sequence("sequence", UBInt8("a"), UBInt16("b"), Sequence("foo", UBInt8("c"), UBInt8("d"))).build, [1,2,[3,4]], b"\x01\x00\x02\x03\x04", None],
    # [Sequence("sequence", UBInt8("a"), UBInt16("b"), Embedded(Sequence("foo", UBInt8("c"), UBInt8("d")))).build, [1,2,3,4], b"\x01\x00\x02\x03\x04", None],

    # [Switch("switch", lambda ctx: 5, {1:UBInt8("x"), 5:UBInt16("y")}).parse, b"\x00\x02", 2, None],
    # [Switch("switch", lambda ctx: 6, {1:UBInt8("x"), 5:UBInt16("y")}).parse, b"\x00\x02", None, SwitchError],
    # [Switch("switch", lambda ctx: 6, {1:UBInt8("x"), 5:UBInt16("y")}, default=UBInt8("x")).parse, b"\x00\x02", 0, None],
    # [Switch("switch", lambda ctx: 5, {1:UBInt8("x"), 5:UBInt16("y")}, include_key=True).parse, b"\x00\x02", (5, 2), None],
    # [Switch("switch", lambda ctx: 5, {1:UBInt8("x"), 5:UBInt16("y")}).build, 2, b"\x00\x02", None],
    # [Switch("switch", lambda ctx: 6, {1:UBInt8("x"), 5:UBInt16("y")}).build, 9, None, SwitchError],
    # [Switch("switch", lambda ctx: 6, {1:UBInt8("x"), 5:UBInt16("y")}, default=UBInt8("x")).build, 9, b"\x09", None],
    # [Switch("switch", lambda ctx: 5, {1:UBInt8("x"), 5:UBInt16("y")}, include_key=True).build, ((5, 2),), b"\x00\x02", None],
    # [Switch("switch", lambda ctx: 5, {1:UBInt8("x"), 5:UBInt16("y")}, include_key=True).build, ((89, 2),), None, SwitchError],

    # [Select("select", UBInt32("a"), UBInt16("b"), UBInt8("c")).parse, b"\x07", 7, None],
    # [Select("select", UBInt32("a"), UBInt16("b")).parse, b"\x07", None, SelectError],
    # [Select("select", UBInt32("a"), UBInt16("b"), UBInt8("c"), include_name=True).parse, b"\x07", ("c", 7), None],
    # [Select("select", UBInt32("a"), UBInt16("b"), UBInt8("c")).build, 7, b"\x00\x00\x00\x07", None],
    # [Select("select", UBInt32("a"), UBInt16("b"), UBInt8("c"), include_name=True).build, (("c", 7),), b"\x07", None],
    # [Select("select", UBInt32("a"), UBInt16("b"), UBInt8("c"), include_name=True).build, (("d", 7),), None, SelectError],

    # [Peek(UBInt8("peek")).parse, b"\x01", 1, None],
    # [Peek(UBInt8("peek")).parse, b"", None, None],
    # [Peek(UBInt8("peek")).build, 1, b"", None],
    # [Peek(UBInt8("peek"), performbuild=True).build, 1, b"\x01", None],
    # [Struct("peek", Peek(UBInt8("a")), UBInt16("b")).parse, b"\x01\x02", Container(a=1)(b=0x102), None],
    # [Struct("peek", Peek(UBInt8("a")), UBInt16("b")).build, dict(a=1,b=0x102), b"\x01\x02", None],
    # [Peek(UBInt16("peek")).sizeof, None, 2, None],
    # [Peek(UBInt64("peek")).sizeof, None, 8, None],
    # [Peek(VarInt("peek")).sizeof, None, None, SizeofError],
    # [Struct("struct",Peek(Byte("a")),Peek(UBInt16("b")),).parse, b"\x01\x02", Container(a=1)(b=258), None],
    # [Struct("struct",Peek(Byte("a")),Peek(UBInt16("b")),).build, dict(a=0,b=258), b"", None],

    # [Computed("computed", lambda ctx: "moo").parse, b"", "moo", None],
    # [Computed("computed", lambda ctx: "moo").build, None, b"", None],
    # [Struct("s", Computed("c", lambda ctx: None)).parse, b"", Container(c=None), None],
    # [Struct("s", Computed("c", lambda ctx: None)).build, Container(c=None), b"", None],
    # [Struct("s", Computed("c", lambda ctx: None)).build, Container(), b"", None],

    # [Anchor("anchor").parse, b"", 0, None],
    # [Anchor("anchor").build, None, b"", None],

    # [AnchorRange("anchorrange").parse, b"", 0, None],
    # [AnchorRange("anchorrange").build, None, b"", None],
    # [Struct("struct",AnchorRange("anchorrange"),Byte("a"),AnchorRange("anchorrange"),allow_overwrite=True).parse, b"\xff", Container(anchorrange=Container(offset1=0)(offset2=1)(length=1))(a=255), None],
    # [Struct("struct",AnchorRange("anchorrange"),Byte("a"),AnchorRange("anchorrange"),allow_overwrite=True).build, dict(a=255), b"\xff", None],

    # [LazyBound("lazybound", lambda: UBInt8("byte")).parse, b"\x02", 2, None],
    # [LazyBound("lazybound", lambda: UBInt8("byte")).build, 2, b"\x02", None],

    # [Pass.parse, b"", None, None],
    # [Pass.build, None, b"", None],

    # [Terminator.parse, b"", None, None],
    # [Terminator.parse, b"x", None, TerminatorError],
    # [Terminator.build, None, b"", None],

    # [Pointer(lambda ctx: 2, UBInt8("pointer")).parse, b"\x00\x00\x07", 7, None],
    # [Pointer(lambda ctx: 2, UBInt8("pointer")).build, 7, b"\x00\x00\x07", None],

    # # [OnDemand(UBInt8("ondemand")).parse(b"\x08").read, (), 8, None],
    # # [Struct("ondemand", UBInt8("a"), OnDemand(UBInt8("b")), UBInt8("c")).parse, b"\x07\x08\x09", Container(a=7)(b=LazyContainer(None, None, None, None))(c=9), None],
    # # [Struct("ondemand", UBInt8("a"), OnDemand(UBInt8("b"), advance_stream=False), UBInt8("c")).parse, b"\x07\x09", Container(a=7)(b=LazyContainer(None, None, None, None))(c=9), None],

    # # [OnDemand(UBInt8("ondemand")).build, 8, b"\x08", None],
    # # [Struct("ondemand", UBInt8("a"), OnDemand(UBInt8("b")), UBInt8("c")).build, Container(a=7)(b=8)(c=9), b"\x07\x08\x09", None],
    # # [Struct("ondemand", UBInt8("a"), OnDemand(UBInt8("b"), force_build=False), UBInt8("c")).build, Container(a=7)(b=LazyContainer(None, None, None, None))(c=9), b"\x07\x00\x09", None],
    # # [Struct("ondemand", UBInt8("a"), OnDemand(UBInt8("b"), force_build=False, advance_stream=False), UBInt8("c")).build, Container(a=7)(b=LazyContainer(None, None, None, None))(c=9), b"\x07\x09", None],

    # [Struct("reconfig", Reconfig("foo", UBInt8("bar"))).parse, b"\x01", Container(foo=1), None],
    # [Struct("reconfig", Reconfig("foo", UBInt8("bar"))).build, Container(foo=1), b"\x01", None],

    # [Buffered(UBInt8("buffered"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
    # [Buffered(GreedyRange(UBInt8("buffered")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", None, SizeofError],
    # [Buffered(UBInt8("buffered"), lambda x:x, lambda x:x, lambda x:x).build, 7, b"\x07", None],
    # [Buffered(GreedyRange(UBInt8("buffered")), lambda x:x, lambda x:x, lambda x:x).build, [7], None, SizeofError],

    # [Restream(UBInt8("restream"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
    # [Restream(GreedyRange(UBInt8("restream")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", [7], None],
    # [Restream(UBInt8("restream"), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", 7, None],
    # [Restream(GreedyRange(UBInt8("restream")), lambda x:x, lambda x:x, lambda x:x).parse, b"\x07", [7], None],

    # #
    # # adapters
    # #
    # [BitField("bitfield", 8).parse, b"\x01" * 8, 255, None],
    # [BitField("bitfield", 8).build, 255, b"\x01" * 8, None],
    # [BitField("bitfield", 8).build, -1, None, BitIntegerError],
    # [BitField("bitfield", 8, signed=True).parse, b"\x01" * 8, -1, None],
    # [BitField("bitfield", 8, signed=True).build, -1, b"\x01" * 8, None],
    # [BitField("bitfield", 8, swapped=True, bytesize=4).parse, b"\x01" * 4 + b"\x00" * 4, 0x0f, None],
    # [BitField("bitfield", 8, swapped=True, bytesize=4).build, 0x0f, b"\x01" * 4 + b"\x00" * 4, None],
    # [BitField("bitfield", lambda c: 8).parse, b"\x01" * 8, 255, None],
    # [BitField("bitfield", lambda c: 8).build, 255, b"\x01" * 8, None],

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

    # [Slicing(Array(4, UBInt8("elements")), 4, 1, 3, empty=0).parse, b"\x01\x02\x03\x04", [2,3], None],
    # [Slicing(Array(4, UBInt8("elements")), 4, 1, 3, empty=0).build, [2,3], b"\x00\x02\x03\x00", None],

    # [Indexing(Array(4, UBInt8("elements")), 4, 2, empty=0).parse, b"\x01\x02\x03\x04", 3, None],
    # [Indexing(Array(4, UBInt8("elements")), 4, 2, empty=0).build, 3, b"\x00\x00\x03\x00", None],

    # [Padding(4).parse, b"\x00\x00\x00\x00", None, None],
    # [Padding(4, strict=True).parse, b"\x00\x00\x00\x00", None, None],
    # [Padding(4, strict=True).parse, b"????", None, PaddingError],
    # [Padding(4).build, None, b"\x00\x00\x00\x00", None],
    # [Padding(4, strict=True).build, None, b"\x00\x00\x00\x00", None],
    # [lambda none: Padding(4, pattern=b"??"), None, None, PaddingError],

    # # [LengthValueAdapter(Sequence("lengthvalueadapter", UBInt8("length"), Field("value", lambda ctx: ctx.length))).parse, b"\x05abcde", b"abcde", None],
    # # [LengthValueAdapter(Sequence("lengthvalueadapter", UBInt8("length"), Field("value", lambda ctx: ctx.length))).build, b"abcde", b"\x05abcde", None],

    # # [TunnelAdapter(PascalString("data", encoding=ZlibCodec), GreedyRange(UBInt16("elements"))).parse, b"\rx\x9cc`f\x18\x16\x10\x00u\xf8\x01-", [3] * 100, None],
    # # [TunnelAdapter(PascalString("data", encoding=ZlibCodec), GreedyRange(UBInt16("elements"))).build, [3] * 100, b"\rx\x9cc`f\x18\x16\x10\x00u\xf8\x01-", None],

    # [Const(b"MZ").parse, b"MZ", b"MZ", None],
    # [Const(b"MZ").parse, b"ELF", None, ConstError],
    # [Const(b"MZ").build, None, b"MZ", None],
    # [Const(b"MZ").build, b"MZ", b"MZ", None],
    # [Const("const", b"MZ").parse, b"MZ", b"MZ", None],
    # [Const("const", b"MZ").parse, b"ELF", None, ConstError],
    # [Const("const", b"MZ").build, None, b"MZ", None],
    # [Const("const", b"MZ").build, b"MZ", b"MZ", None],
    # [Const(ULInt32("const"), 255).parse, b"\xff\x00\x00\x00", 255, None],
    # [Const(ULInt32("const"), 255).parse, b"\x00\x00\x00\x00", 255, ConstError],
    # [Const(ULInt32("const"), 255).build, None, b"\xff\x00\x00\x00", None],
    # [Const(ULInt32("const"), 255).build, 255, b"\xff\x00\x00\x00", None],

    # [ExprAdapter(UBInt8("expradapter"), 
    #     encoder = lambda obj, ctx: obj // 7, 
    #     decoder = lambda obj, ctx: obj * 7,
    #     ).parse, b"\x06", 42, None],
    # [ExprAdapter(UBInt8("expradapter"), 
    #     encoder = lambda obj, ctx: obj // 7, 
    #     decoder = lambda obj, ctx: obj * 7,
    #     ).build, 42, b"\x06", None],

    # #
    # # macros
    # #
    # [Aligned(UBInt8("aligned")).parse, b"\x01\x00\x00\x00", 1, None],
    # [Aligned(UBInt8("aligned")).build, 1, b"\x01\x00\x00\x00", None],
    # [Struct("aligned", Aligned(UBInt8("a")), UBInt8("b")).parse, b"\x01\x00\x00\x00\x02", Container(a=1)(b=2), None],
    # [Struct("aligned", Aligned(UBInt8("a")), UBInt8("b")).build, Container(a=1)(b=2), b"\x01\x00\x00\x00\x02", None],

    # [Bitwise(Field("bitwise", 8)).parse, b"\xff", b"\x01" * 8, None],
    # [Bitwise(Field("bitwise", lambda ctx: 8)).parse, b"\xff", b"\x01" * 8, None],
    # [Bitwise(Field("bitwise", 8)).build, b"\x01" * 8, b"\xff", None],
    # [Bitwise(Field("bitwise", lambda ctx: 8)).build, b"\x01" * 8, b"\xff", None],

    # [Union("union",
    #     UBInt32("a"),
    #     Struct("b", UBInt16("a"), UBInt16("b")),
    #     BitStruct("c", Padding(4), Octet("a"), Padding(4)),
    #     Struct("d", UBInt8("a"), UBInt8("b"), UBInt8("c"), UBInt8("d")),
    #     Embedded(Struct("q", UBInt8("e"))),
    #     ).parse,
    #     b"\x11\x22\x33\x44",
    #     Container(a=0x11223344)
    #         (b=Container(a=0x1122)(b=0x3344))
    #         (c=Container(a=0x12))
    #         (d=Container(a=0x11)(b=0x22)(c=0x33)(d=0x44))
    #         (e=0x11),
    #     None],
    # [Union("union",
    #     UBInt32("a"),
    #     Struct("b", UBInt16("a"), UBInt16("b")),
    #     BitStruct("c", Padding(4), Octet("a"), Padding(4)),
    #     Struct("d", UBInt8("a"), UBInt8("b"), UBInt8("c"), UBInt8("d")),
    #     Embedded(Struct("q", UBInt8("e"))),
    #     ).build,
    #     Container(a=0x11223344)
    #         (b=Container(a=0x1122)(b=0x3344))
    #         (c=Container(a=0x12))
    #         (d=Container(a=0x11)(b=0x22)(c=0x33)(d=0x44))
    #         (e=0x11),
    #     b"\x11\x22\x33\x44",
    #     None],
    # [Union("union",
    #     Struct("sub1", ULInt8("a"), ULInt8("b") ),
    #     Struct("sub2", ULInt16("c") ),
    #     ).build, dict(sub1=dict(a=1,b=2)), b"\x01\x02", None],
    # [Union("union",
    #     Struct("sub1", ULInt8("a"), ULInt8("b") ),
    #     Struct("sub2", ULInt16("c") ),
    #     ).build, dict(sub2=dict(c=3)), b"\x03\x00", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom=None,
    #     ).build, dict(a=1,b=2), b"\x01\x02", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom=None,
    #     ).build, dict(c=3), b"\x03\x00", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom=0,
    #     ).build, dict(a=1,b=2), b"\x01\x02", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom=1,
    #     ).build, dict(c=3), b"\x03\x00", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom="sub1",
    #     ).build, dict(a=1,b=2), b"\x01\x02", None],
    # [Union("union",
    #     Embed(Struct("sub1", ULInt8("a"), ULInt8("b") )),
    #     Embed(Struct("sub2", ULInt16("c") )),
    #     buildfrom="sub2",
    #     ).build, dict(c=3), b"\x03\x00", None],
    # [Union("nonematches",
    #     Byte("a"), PascalString("b"),
    #     ).build, None, None, SelectError],
    # [Union("samesize",
    #     Struct("both",ULInt8("a"),ULInt8("b")),
    #     ULInt16("c"),
    #     ).sizeof, None, 2, None],
    # [Union("mixedsize",
    #     Struct("both",ULInt8("a"),ULInt8("b")),
    #     ULInt32("c"),
    #     ).sizeof, None, 4, None],
    # [Union("somevariablesize",
    #     Struct("both",ULInt8("a"),ULInt8("b")),
    #     VarInt("c"),
    #     ).sizeof, None, None, SizeofError],

    # [Enum(UBInt8("enum"),q=3,r=4,t=5).parse, b"\x04", "r", None],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5).parse, b"\x07", None, MappingError],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5, _default_="spam").parse, b"\x07", "spam", None],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5, _default_=Pass).parse, b"\x07", 7, None],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5).build, "r", b"\x04", None],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5).build, "spam", None, MappingError],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5, _default_=9).build, "spam", b"\x09", None],
    # [Enum(UBInt8("enum"),q=3,r=4,t=5, _default_=Pass).build, 9, b"\x09", None],

    # [PrefixedArray(UBInt8("array"), UBInt8("count")).parse, b"\x03\x01\x01\x01", [1,1,1], None],
    # [PrefixedArray(UBInt8("array"), UBInt8("count")).parse, b"\x00", [], None],
    # [PrefixedArray(UBInt8("array"), UBInt8("count")).parse, b"", None, ArrayError],
    # [PrefixedArray(UBInt8("array"), UBInt8("count")).parse, b"\x03\x01\x01", None, ArrayError],
    # # Fixed: sizeof takes a context, not an obj.
    # [PrefixedArray(UBInt8("array"), UBInt8("count")).sizeof, [1,1,1], 4, SizeofError],
    # [PrefixedArray(UBInt8("array"), UBInt8("count")).build, [1,1,1], b"\x03\x01\x01\x01", None],

    # [IfThenElse("ifthenelse", lambda ctx: True, UBInt8("then"), UBInt16("else")).parse, b"\x01", 1, None],
    # [IfThenElse("ifthenelse", lambda ctx: False, UBInt8("then"), UBInt16("else")).parse, b"\x00\x01", 1, None],
    # [IfThenElse("ifthenelse", lambda ctx: True, UBInt8("then"), UBInt16("else")).build, 1, b"\x01", None],
    # [IfThenElse("ifthenelse", lambda ctx: False, UBInt8("then"), UBInt16("else")).build, 1, b"\x00\x01", None],

    # [Optional(ULInt32("int")).parse, b"\x01\x00\x00\x00", 1, None],
    # [Optional(ULInt32("int")).build, 1, b"\x01\x00\x00\x00", None],
    # [Optional(ULInt32("int")).parse, b"?", None, None],
    # [Optional(ULInt32("int")).build, None, b"", None],

    # [UBInt24('int24').parse, b"\x01\x02\x03", 0x010203, None],
    # [UBInt24('int24').build, 0x010203, b"\x01\x02\x03", None],
    # [Struct('struct', UBInt24('int24')).parse, b"\x01\x02\x03", Container(int24=0x010203), None],
    # [Struct('struct', UBInt24('int24')).build, Container(int24=0x010203), b"\x01\x02\x03", None],

    # [ULInt24('int24').parse, b"\x01\x02\x03", 0x030201, None],
    # [ULInt24('int24').build, 0x030201, b"\x01\x02\x03", None],
    # [Struct('struct', ULInt24('int24')).parse, b"\x01\x02\x03", Container(int24=0x030201), None],
    # [Struct('struct', ULInt24('int24')).build, Container(int24=0x030201), b"\x01\x02\x03", None],

    # [ByteSwapped(Bytes(None, 5)).parse, b"12345", b"54321", None],
    # [ByteSwapped(Bytes(None, 5)).build, b"12345", b"54321", None],
    # [ByteSwapped(Struct("struct",Byte("a"),Byte("b"))).parse, b"\x01\x02", Container(a=2)(b=1), None],
    # [ByteSwapped(Struct("struct",Byte("a"),Byte("b"))).build, Container(a=2)(b=1), b"\x01\x02", None],

    # # from Issue #70
    # [ByteSwapped(BitStruct("Example",
    #     Bit("flag1"),                   # bit 0
    #     Bit("flag2"),                   # bit 1
    #     Padding(2),                     # bits 03:02
    #     BitField("number", 16),         # bits 19:04
    #     Padding(4)                      # bits 23:20
    #     )).parse, b'\xd0\xbc\xfa', Container(flag1=1)(flag2=1)(number=0xabcd), None],

    # [Prefixed(Byte(None),ULInt16(None)).parse, b"\x02\xff\xffgarbage", 65535, None],
    # [Prefixed(Byte(None),ULInt16(None)).build, 65535, b"\x02\xff\xff", None],
    # [Prefixed(VarInt(None), GreedyBytes(None)).parse, b"\x03abcgarbage", b"abc", None],
    # [Prefixed(VarInt(None), GreedyBytes(None)).build, b"abc", b'\x03abc', None],

    # [Prefixed(Byte(None),Compressed(CString(None),"zlib")).parse, b'\rx\x9c30\xa0=`\x00\x00\xc62\x12\xc1??????????????', b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", zlibcodecraises],
    # [Prefixed(Byte(None),Compressed(CString(None),"zlib")).build, b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", b'\rx\x9c30\xa0=`\x00\x00\xc62\x12\xc1', zlibcodecraises],

    # [GreedyBytes(None).parse, b"123", b"123", None],
    # [GreedyBytes(None).build, b"123", b"123", None],

]


class TestAll(unittest.TestCase):
    def _run_tests(self, tests):
        errors = []
        for i, (func, args, res, exctype) in enumerate(tests):
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
        return errors

    def test_all(self):
        errors = self._run_tests(all_tests)
        if errors:
            self.fail("\n=========================\n".join(str(e) for e in errors))

