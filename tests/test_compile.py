from declarativeunittest import *
from construct import *
from construct.lib import *


@pytest.mark.xfail(not supportscompiler, reason="compiler requires Python 3.4")
class TestCompile(unittest.TestCase):

    def setUp(self):
        self.example = Struct(
            "num" / Byte,

            "bytes1" / Bytes(4),
            "bytes2" / Bytes(this.num),
            "greedybytes" / Prefixed(Byte, GreedyBytes),
            "bitwise1" / Bitwise(BitsInteger(8, swapped=False)),
            "bitwise2" / Bitwise(BitsInteger(8, swapped=True)),
            "bytewise1" / Bitwise(Bytewise(BytesInteger(16, swapped=True))),
            "bytewise2" / Bitwise(Bytewise(BytesInteger(16, swapped=False))),

            "formatfield" / FormatField(">", "B"),
            "bytesinteger1" / BytesInteger(16, swapped=True),
            "bytesinteger2" / BytesInteger(16, swapped=False),
            "bytesinteger3dynamic" / BytesInteger(this.num+1),
            "bitsinteger1" / Bitwise(BitsInteger(8, swapped=False)),
            "bitsinteger2" / Bitwise(BitsInteger(8, swapped=True)),
            "varint" / VarInt,
            "byte" / Byte,
            "float1" / Single,
            "float2" / Double,

            "string1" / String(10, encoding=StringsAsBytes),
            "string2" / String(10, encoding="utf8"),
            "pascalstring1" / PascalString(Byte, encoding=StringsAsBytes),
            "pascalstring2" / PascalString(Byte, encoding="utf8"),
            # CString
            "greedystring1" / Prefixed(Byte, GreedyString(encoding=StringsAsBytes)),
            "greedystring2" / Prefixed(Byte, GreedyString(encoding="utf8")),

            "flag" / Flag,
            # Enum
            # FlagsEnum
            # Mapping
            # SymmetricMapping

            "struct" / Struct("field" / Byte),
            "embeddedstruct" / Embedded(Struct("embeddedfield1" / Byte)),
            "sequence1" / Sequence(Byte, Byte),
            "sequence2" / Sequence("num1" / Byte, "num2" / Byte),
            "embeddedsequence1" / Sequence(Embedded(Sequence(Byte, Byte))),
            "embeddedsequence2" / Sequence(Embedded(Sequence("num1" / Byte, "num2" / Byte))),

            "array1" / Array(5, Byte),
            "array2" / Array(this.num, Byte),
            "range1" / Range(0, 5, Byte),
            "greedyrange0" / Prefixed(Byte, GreedyRange(Byte)),
            # RepeatUntil

            "const1" / Const(bytes(4)),
            "const2" / Const(0, Int32ub),
            "computed" / Computed(this.num),
            "rebuild" / Rebuild(Byte, len_(this.array1)),
            "default" / Default(Byte, 0),
            Check(this.num == 0),
            "error0" / If(False, Error),
            "focusedseq1" / FocusedSeq(1, Const(bytes(4)), Byte),
            "focusedseq2" / FocusedSeq("num", Const(bytes(4)), "num"/Byte),
            "numpy_data" / Computed(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"),
            "numpy1" / RestreamData(this.numpy_data, Numpy),
            "namedtuple1" / NamedTuple("coord", "x y z", Byte[3]),
            "namedtuple2" / NamedTuple("coord", "x y z", Range(3, 3, Byte)),
            "namedtuple3" / NamedTuple("coord", "x y z", Byte >> Byte >> Byte),
            "namedtuple4" / NamedTuple("coord", "x y z", "x"/Byte + "y"/Byte + "z"/Byte),

            "union1" / Union(None, "char"/Byte, "short"/Short, "int"/Int),
            "union2" / Union(1, "char"/Byte, "short"/Short, "int"/Int),
            "union3" / Union(0, "char1"/Byte, "char2"/Byte, "char3"/Byte),
            "union4" / Union("char1", "char1"/Byte, "char2"/Byte, "char3"/Byte),
            "unionembedded" / Union(None, Embedded(Struct("char"/Byte))),
            # Select
            # Optional
            "if1" / If(this.num == 0, Byte),
            "ifthenelse" / IfThenElse(this.num == 0, Byte, Byte),
            # Switch
            # StopIf

            "padding" / Padding(2),
            "paddedbyte" / Padded(4, Byte),
            "alignedbyte" / Aligned(4, Byte),
            # AlignedStruct
            # BitStruct
            # EmbeddedBitStruct

            # Pointer
            # Peek
            "seek0" / Seek(0, 1),
            "tell" / Tell,
            "pass1" / Pass,
            "terminated0" / Prefixed(Byte, Terminated),
            # Restreamed
            # Rebuffered

            "rawcopy1" / RawCopy(Byte),
            "rawcopy2" / RawCopy(RawCopy(RawCopy(Byte))),
            "bytesswapped" / ByteSwapped(BytesInteger(8)),
            "bitsswapped" / BitsSwapped(BytesInteger(8)),
            "prefixed" / Prefixed(Byte, GreedyBytes),
            "prefixedarray" / PrefixedArray(Byte, Byte),
            # RestreamData
            # Checksum
            # Compressed

            # LazyStruct
            # LazySequence
            # LazyRange
            # OnDemand
            # LazyBound

            # adapters and validators
        )

    def test_compiles(self):
        dc = self.example.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled.py")

    def test_parsesbuilds(self):
        d = self.example
        data = bytes(1000)
        d.testcompiled(data)

    # def test_benchmark_compiling(benchmark):
    #     d = benchmark.example
    #     benchmark(d.compile)

    # def test_benchmark_parse(benchmark):
    #     d = benchmark.example
    #     data = bytes(1000)
    #     benchmark(d.parse, data)

    # def test_benchmark_parse_compiled(benchmark):
    #     dc = benchmark.example.compile()
    #     data = bytes(1000)
    #     benchmark(dc.parse, data)

    # def test_benchmark_build(benchmark):
    #     d = benchmark.example
    #     data = bytes(1000)
    #     obj = d.parse(data)
    #     benchmark(d.build, obj)

    # def test_benchmark_build_compiled(benchmark):
    #     dc = benchmark.example.compile()
    #     data = bytes(1000)
    #     obj = dc.parse(data)
    #     benchmark(dc.build, obj)
