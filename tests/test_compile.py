import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


@pytest.mark.xfail(not PY3, reason="compiler supports PY3")
class TestCompile(unittest.TestCase):

    def test_it(self):
        shared = Struct()
        d = Struct(
            "num" / Byte,
            "bytes" / Bytes(this.num),
            # GreedyBytes
            "int8" / FormatField(">", "B"),
            "int16" / BytesInteger(16),
            "varint" / VarInt,
            "struct" / Struct("field" / Byte),
            "sequence" / Sequence(Byte, Byte),
            "array" / Array(5, Byte),
            "const1" / Const(bytes(4)),
            "const2" / Const(0, Int32ub),
            "computed" / Computed(this.num),
            "rebuild" / Rebuild(Byte, len_(this.array)),
            "default" / Default(Byte, 0),
            Check(this.num == 0),
            # Error,
            # If(False, Error),
            "focusedseq1" / FocusedSeq(0, Byte, Byte),
            "focusedseq2" / FocusedSeq("first", "first" / Byte, Byte),
            # Numpy
            "namedtuple" / NamedTuple("coord", "x y z", Byte[3]),

            "prefixedarray" / PrefixedArray(Byte, Byte),

            "shared1" / shared,
            "shared2" / shared,
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
