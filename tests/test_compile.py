import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


@pytest.mark.xfail(not supportscompiler, reason="compiler requires Python 3.4")
class TestCompile(unittest.TestCase):

    def test_all(self):
        d = Struct(
            "num" / Byte,

            "bytes1" / Bytes(4),
            "bytes2" / Bytes(this.num),
            "greedybytes" / Prefixed(Byte, GreedyBytes),
            "bitwise1" / Bitwise(BitsInteger(8, swapped=False)),
            "bitwise2" / Bitwise(BitsInteger(8, swapped=True)),

            "int8" / FormatField(">", "B"),
            "int16_1" / BytesInteger(16, swapped=True),
            "int16_2" / BytesInteger(16, swapped=False),
            "int16dynamic" / BytesInteger(this.num+1),
            "bitsinteger1" / Bitwise(BitsInteger(8, swapped=False)),
            "bitsinteger2" / Bitwise(BitsInteger(8, swapped=True)),
            "varint" / VarInt,

            "struct" / Struct("field" / Byte),
            "sequence1" / Sequence(Byte, Byte),
            "sequence2" / Sequence("num1" / Byte, "num2" / Byte),
            "array1" / Array(5, Byte),
            "array2" / Array(this.num, Byte),

            "const1" / Const(bytes(4)),
            "const2" / Const(0, Int32ub),
            "computed" / Computed(this.num),
            "rebuild" / Rebuild(Byte, len_(this.array1)),
            "default" / Default(Byte, 0),
            Check(this.num == 0),
            "error0" / If(False, Error),
            # "focusedseq1" / FocusedSeq(0, Byte, Byte),
            # "focusedseq2" / FocusedSeq("first", "first" / Byte, Byte),
            # "numpy_data" / Computed(b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"),
            # "numpy1" / RestreamData(this.numpy_data, Numpy),
            "numpy0" / If(False, Numpy),
            "namedtuple1" / NamedTuple("coord", "x y z", Byte[3]),
            "namedtuple2" / NamedTuple("coord", "x y z", Byte >> Byte >> Byte),
            "namedtuple3" / NamedTuple("coord", "x y z", "x"/Byte + "y"/Byte + "z"/Byte),

            "padding" / Padding(2),
            "paddedbyte" / Padded(4, Byte),
            "alignedbyte" / Aligned(4, Byte),

            "union1" / Union(None, "char"/Byte),
            "union2" / Union(0, "char"/Byte),
            "union3" / Union("char", "char"/Byte),
            "if1" / If(this.num == 0, Byte),
            "ifthenelse" / IfThenElse(this.num == 0, Byte, Byte),

            "seek0" / Seek(0, 1),
            "tell" / Tell,
            "pass1" / Pass,
            "terminated0" / Prefixed(Byte, Terminated),

            "byteswapped" / ByteSwapped(BytesInteger(8)),
            "prefixed" / Prefixed(Byte, GreedyBytes),
            "prefixedarray" / PrefixedArray(Byte, Byte),

            "flag" / Flag,

            "string1" / String(10),
            "string2" / String(10, encoding="utf8"),
            "pascalstring1" / PascalString(Byte),
            "pascalstring2" / PascalString(Byte, encoding="utf8"),
            "greedystring" / Prefixed(Byte, GreedyString()),
        )

        # d = Struct("num" / Byte)

        dc = d.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled.py")

        data = bytes(1000)
        d.testcompiled(data)

        # print(d.benchmark(data))
        # assert False
