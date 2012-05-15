import unittest

from construct import BitField, BitStruct, Struct, Container
from construct import Bit, Flag, Nibble, Padding

class TestBitStruct(unittest.TestCase):

    def test_parse(self):
        struct = BitStruct("foo",
            BitField("a", 3),
            Flag("b"),
            Padding(3),
            Nibble("c"),
            BitField("d", 5),
        )
        self.assertEqual(struct.parse("\xe1\x1f"),
            Container(a=7, b=False, c=8, d=31))

    def test_parse_nested(self):
        struct = BitStruct("foo",
            BitField("a", 3),
            Flag("b"),
            Padding(3),
            Nibble("c"),
            Struct("bar",
                Nibble("d"),
                Bit("e"),
            )
        )
        self.assertEqual(struct.parse("\xe1\x1f"),
            Container(a=7, b=False, bar=Container(d=15, e=1), c=8))
