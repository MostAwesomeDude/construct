import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


class TestCompile(unittest.TestCase):

    @pytest.mark.xfail(not PY3, reason="compiler supports PY3")
    def test_it(self):
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
        )

        dc = d.compile()
        print(dc.source)
        if not ontravis:
            dc.tofile("tests/compiled.py")

        data = bytes(1000)
        dc.parse(data)
        # assert dc.parse(data) == d.parse(data)
