import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


class TestCompile(unittest.TestCase):

    @pytest.mark.xfail(not PY3, reason="compiler supports PY3")
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
        # assert dc.parse(data) == d.parse(data)
