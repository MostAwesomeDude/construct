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

            "int8" / FormatField(">", "B"),
            "int16a" / BytesInteger(16),
            "int16b" / BytesInteger(this.num),
            "varint" / VarInt,

            "struct" / Struct("field" / Byte),
            "sequence1" / Sequence(Byte, Byte),
            "sequence2" / Sequence("num1" / Byte, "num2" / Byte),
            "array1" / Array(5, Byte),
            "array2" / Array(this.num, Byte),

            "const1" / Const(bytes(4)),
            "const2" / Const(0, Int32ub),
            "computed" / Computed(this.num),
            "rebuild" / Rebuild(Byte, len_(this.array)),
            "default" / Default(Byte, 0),
            Check(this.num == 0),
            "error0" / If(False, Error),
            "focusedseq1" / FocusedSeq(0, Byte, Byte),
            "focusedseq2" / FocusedSeq("first", "first" / Byte, Byte),
            "numpy0" / If(False, Numpy),
            "namedtuple1" / NamedTuple("coord", "x y z", Byte[3]),
            "namedtuple2" / NamedTuple("coord", "x y z", Byte >> Byte >> Byte),
            # NamedTuple, cannot use factory on FIELDS object (non dict)
            # "namedtuple3" / NamedTuple("coord", "x y z", "x"/Byte + "y"/Byte + "z"/Byte),

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

            "prefixed" / Prefixed(Byte, GreedyBytes),
            "prefixedarray" / PrefixedArray(Byte, Byte),

            "flag" / Flag,

            "string1" / String(10),
            "string2" / String(10, encoding="utf8"),
            "pascalstring1" / PascalString(Byte),
            # "pascalstring2" / PascalString(Byte, encoding="utf8"),
            "greedystring" / Prefixed(Byte, GreedyString()),
        )

        dc = d.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled.py")

        data = bytes(1000)
        dc.parse(data)

    def test_numpy(self):
        d = Numpy
        dc = d.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled_numpy.py")
        data = b"\x93NUMPY\x01\x00F\x00{'descr': '<i8', 'fortran_order': False, 'shape': (3,), }            \n\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"
        dc.parse(data)

    def test_example1(self):
        d = Struct(
            "num8" / Int8ub,
            "num24" / Int24ub,
            "data" / Bytes(this.num8),
        )

        dc = d.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled_example1.py")

        data = bytes(1000)
        dc.parse(data)
