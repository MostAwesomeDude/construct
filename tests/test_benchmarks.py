# -*- coding: utf-8 -*-

from declarativeunittest import *
from construct import *
from construct.lib import *



def test_bytes_parse(benchmark):
    d = Bytes(100)
    benchmark(d.parse, bytes(100))

def test_bytes_build(benchmark):
    d = Bytes(100)
    benchmark(d.build, bytes(100))

def test_greedybytes_parse(benchmark):
    d = GreedyBytes
    benchmark(d.parse, bytes(100))

def test_greedybytes_build(benchmark):
    d = GreedyBytes
    benchmark(d.build, bytes(100))



def test_formatfield_parse(benchmark):
    d = FormatField(">", "L")
    benchmark(d.parse, bytes(4))

def test_formatfield_build(benchmark):
    d = FormatField(">", "L")
    benchmark(d.build, 0)

def test_bytesinteger_parse(benchmark):
    d = BytesInteger(4)
    benchmark(d.parse, bytes(4))

def test_bytesinteger_build(benchmark):
    d = BytesInteger(4)
    benchmark(d.build, 0)

def test_bitsinteger_parse(benchmark):
    d = Bitwise(BitsInteger(32, swapped=True))
    benchmark(d.parse, bytes(4))

def test_bitsinteger_build(benchmark):
    d = Bitwise(BitsInteger(32, swapped=True))
    benchmark(d.build, 0)

def test_varint_parse(benchmark):
    d = VarInt
    benchmark(d.parse, b'\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x04')

def test_varint_build(benchmark):
    d = VarInt
    benchmark(d.build, 2**64)



def test_struct_parse(benchmark):
    d = Struct("a"/Byte, "b"/Byte, "c"/Byte, "d"/Byte, "e"/Byte)
    benchmark(d.parse, bytes(5))

def test_struct_build(benchmark):
    d = Struct("a"/Byte, "b"/Byte, "c"/Byte, "d"/Byte, "e"/Byte)
    benchmark(d.build, dict(a=0, b=0, c=0, d=0, e=0))

def test_sequence_parse(benchmark):
    d = Sequence(Byte, Byte, Byte, Byte, Byte)
    benchmark(d.parse, bytes(5))

def test_sequence_build(benchmark):
    d = Sequence(Byte, Byte, Byte, Byte, Byte)
    benchmark(d.build, [0]*5)

def test_range_parse(benchmark):
    d = Array(100, Byte)
    benchmark(d.parse, bytes(100))

def test_range_build(benchmark):
    d = Array(100, Byte)
    benchmark(d.build, [0]*100)

def test_repeatuntil_parse(benchmark):
    d = RepeatUntil(lambda x,lst,ctx: len(lst)==20, Byte)
    benchmark(d.parse, bytes(20))

def test_repeatuntil_build(benchmark):
    d = RepeatUntil(lambda x,lst,ctx: len(lst)==20, Byte)
    benchmark(d.build, [0]*20)



def test_const_parse(benchmark):
    d = Const(bytes(4))
    benchmark(d.parse, bytes(4))

def test_const_build(benchmark):
    d = Const(bytes(4))
    benchmark(d.build, bytes(4))

def test_computed_parse(benchmark):
    d = Computed(this.entry)
    benchmark(d.parse, bytes(), entry=1)

def test_computed_build(benchmark):
    d = Computed(this.entry)
    benchmark(d.build, None, entry=1)

def test_rebuild_parse(benchmark):
    d = Rebuild(Int32ub, 0)
    benchmark(d.parse, bytes(4))

def test_rebuild_build(benchmark):
    d = Rebuild(Int32ub, 0)
    benchmark(d.build, None)

def test_default_parse(benchmark):
    d = Default(Int32ub, 0)
    benchmark(d.parse, bytes(4))

def test_default_build(benchmark):
    d = Default(Int32ub, 0)
    benchmark(d.build, None)

def test_check_parse(benchmark):
    d = Check(this.entry == 1)
    benchmark(d.parse, bytes(4), entry=1)

def test_check_build(benchmark):
    d = Check(this.entry == 1)
    benchmark(d.build, None, entry=1)

def test_focusedseq_parse(benchmark):
    d = FocusedSeq("num", Const(bytes(2)), "num"/Byte, Terminated)
    benchmark(d.parse, bytes(3))

def test_focusedseq_build(benchmark):
    d = FocusedSeq("num", Const(bytes(2)), "num"/Byte, Terminated)
    benchmark(d.build, 0)



def test_padded_parse(benchmark):
    d = Padded(4, Byte)
    benchmark(d.parse, bytes(4))

def test_padded_build(benchmark):
    d = Padded(4, Byte)
    benchmark(d.build, 0)

def test_aligned_parse(benchmark):
    d = Aligned(4, Byte)
    benchmark(d.parse, bytes(4))

def test_aligned_build(benchmark):
    d = Aligned(4, Byte)
    benchmark(d.build, 0)



def test_union_parse(benchmark):
    d = Union(0, "raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8])
    benchmark(d.parse, bytes(8))

def test_union_build(benchmark):
    d = Union(0, "raw"/Bytes(8), "ints"/Int32ub[2], "shorts"/Int16ub[4], "chars"/Byte[8])
    benchmark(d.build, dict(chars=[0]*8))

def test_select_parse(benchmark):
    d = Select(Int32ub, CString(encoding="utf8"))
    benchmark(d.parse, bytes(20))

def test_select_build(benchmark):
    d = Select(Int32ub, CString(encoding="utf8"))
    benchmark(d.build, "")

def test_switch_parse(benchmark):
    d = Switch(this.n, { 1:Int8ub, 2:Int16ub, 4:Int32ub })
    benchmark(d.parse, bytes(4), n=4)

def test_switch_build(benchmark):
    d = Switch(this.n, { 1:Int8ub, 2:Int16ub, 4:Int32ub })
    benchmark(d.build, 0, n=4)



def test_pointer_parse(benchmark):
    d = Pointer(8, Bytes(4))
    benchmark(d.parse, bytes(12))

def test_pointer_build(benchmark):
    d = Pointer(8, Bytes(4))
    benchmark(d.build, bytes(4))

def test_peek_parse(benchmark):
    d = Sequence(Peek(Int8ub), Peek(Int16ub))
    benchmark(d.parse, bytes(2))

def test_peek_build(benchmark):
    d = Sequence(Peek(Int8ub), Peek(Int16ub))
    benchmark(d.build, [0,0])

def test_rawcopy_parse(benchmark):
    d = RawCopy(Byte)
    benchmark(d.parse, bytes(1))

def test_rawcopy_build1(benchmark):
    d = RawCopy(Byte)
    benchmark(d.build, dict(data=bytes(1)))

def test_rawcopy_build2(benchmark):
    d = RawCopy(Byte)
    benchmark(d.build, dict(value=0))

def test_prefixed_parse(benchmark):
    d = Prefixed(Byte, GreedyRange(Byte))
    benchmark(d.parse, b"\x08"+bytes(8))

def test_prefixed_build(benchmark):
    d = Prefixed(Byte, GreedyRange(Byte))
    benchmark(d.build, [0]*8)

def test_prefixedarray_parse(benchmark):
    d = PrefixedArray(Byte, Byte)
    benchmark(d.parse, b"\x08"+bytes(8))

def test_prefixedarray_build(benchmark):
    d = PrefixedArray(Byte, Byte)
    benchmark(d.build, [0]*8)



def test_lazystruct_parse(benchmark):
    d = LazyStruct("a"/Byte, "b"/Byte, "c"/Byte, "d"/Byte, "e"/Byte)
    @benchmark
    def thecode():
        x = d.parse(bytes(5))
        [x.a, x.b, x.c, x.d, x.e]

def test_lazysequence_parse(benchmark):
    d = LazySequence(Byte, Byte, Byte, Byte, Byte)
    @benchmark
    def thecode():
        x = d.parse(bytes(5))
        [x[i] for i in range(5)]

def test_lazyrange_parse(benchmark):
    d = LazyRange(100, 100, Byte)
    @benchmark
    def thecode():
        x = d.parse(bytes(100))
        [x[i] for i in range(100)]



def test_flag_parse(benchmark):
    d = Flag
    benchmark(d.parse, bytes(1))

def test_flag_build(benchmark):
    d = Flag
    benchmark(d.build, False)

def test_enum_parse(benchmark):
    d = Enum(Byte, zero=0, one=1)
    benchmark(d.parse, bytes(1))

def test_enum_build(benchmark):
    d = Enum(Byte, zero=0, one=1)
    benchmark(d.build, 0)

def test_flagsenum_parse(benchmark):
    d = FlagsEnum(Byte, a=1, b=2, c=4, d=8)
    benchmark(d.parse, bytes(1))

def test_flagsenum_build(benchmark):
    d = FlagsEnum(Byte, a=1, b=2, c=4, d=8)
    benchmark(d.build, FlagsContainer(a=False, b=False, c=False, d=False))

def test_hex_parse(benchmark):
    d = Hex(GreedyBytes)
    benchmark(d.parse, bytes(100))

def test_hex_build(benchmark):
    d = Hex(GreedyBytes)
    benchmark(d.build, hexlify(bytes(100)))

def test_hexdump_parse(benchmark):
    d = HexDump(GreedyBytes)
    benchmark(d.parse, bytes(100))

def test_hexdump_build(benchmark):
    d = HexDump(GreedyBytes)
    benchmark(d.build, hexdump(bytes(100), 16))



def test_string_parse(benchmark):
    d = String(10, encoding="utf8")
    benchmark(d.parse, b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00\x00')

def test_string_build(benchmark):
    d = String(10, encoding="utf8")
    benchmark(d.build, u"Афон")

def test_pascalstring_parse(benchmark):
    d = PascalString(VarInt, encoding="utf8")
    benchmark(d.parse, b'\x08\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd')

def test_pascalstring_build(benchmark):
    d = PascalString(VarInt, encoding="utf8")
    benchmark(d.build, u"Афон")

def test_cstring_parse(benchmark):
    d = CString(encoding="utf8")
    benchmark(d.parse, b'\xd0\x90\xd1\x84\xd0\xbe\xd0\xbd\x00')

def test_cstring_build(benchmark):
    d = CString(encoding="utf8")
    benchmark(d.build, u"Афон")
