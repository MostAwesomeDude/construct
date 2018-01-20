import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


class TestCompile(unittest.TestCase):

    def test_it(self):
        d = Struct(
            "bytes" / Bytes(this.num),
            # GreedyBytes
            "int8" / FormatField(">", "B"),
            "int16" / BytesInteger(16),
            "varint" / VarInt,
            "struct" / Struct("field" / Byte),
            "sequence" / Sequence(Byte, Byte),
        )

        dc = d.compile()
        print(dc.source)
        dc.tofile("tests/compiled.py")
        dc.parse(bytes(1000))

        # data = d.build(dict(inner=dict(num=1,data=bytes(1))))
        # assert dc.parse(data) == d.parse(data)
