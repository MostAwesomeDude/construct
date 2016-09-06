import unittest

from construct import BitField, BitStruct, Struct, Container
from construct import Bit, Flag, Nibble, Padding


class TestBitStruct(unittest.TestCase):

    def test(self):
        struct = BitStruct("bitstruct",
            BitField("a", 3),
            Flag("b"),
            Padding(3),
            Nibble("c"),
            BitField("d", 5),
        )
        self.assertEqual(struct.parse(b"\xe1\x1f"), Container(a=7)(b=False)(c=8)(d=31))
        self.assertEqual(struct.build(Container(a=7)(b=False)(c=8)(d=31)), b"\xe1\x1f")

    def test_nested(self):
        struct = BitStruct("bitstruct",
            BitField("a", 3),
            Flag("b"),
            Padding(3),
            Nibble("c"),
            Struct("sub",
                Nibble("d"),
                Bit("e"),
            )
        )
        self.assertEqual(struct.parse(b"\xe1\x1f"), Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1)))
        self.assertEqual(struct.build(Container(a=7)(b=False)(c=8)(sub=Container(d=15)(e=1))), b"\xe1\x1f")

