import unittest

from construct.lib.binary import int_to_bin, bin_to_int, swap_bytes, encode_bin, decode_bin
from construct.lib.expr import Path


class TestBinary(unittest.TestCase):
    def test_int_to_bin(self):
        self.assertEqual(int_to_bin(19, 5), b"\x01\x00\x00\x01\x01")
        self.assertEqual(int_to_bin(19, 8), b'\x00\x00\x00\x01\x00\x00\x01\x01')
        self.assertEqual(int_to_bin(19, 3), b'\x00\x01\x01')

    def test_int_to_bin_signed(self):
        self.assertEqual(int_to_bin(-13, 5), b"\x01\x00\x00\x01\x01")
        self.assertEqual(int_to_bin(-13, 8), b"\x01\x01\x01\x01\x00\x00\x01\x01")

    def test_bin_to_int(self):
        self.assertEqual(bin_to_int(b"\x01\x00\x00\x01\x01"), 19)
        self.assertEqual(bin_to_int(b"10011"), 19)

    def test_bin_to_int_signed(self):
        self.assertEqual(bin_to_int(b"\x01\x00\x00\x01\x01", True), -13)
        self.assertEqual(bin_to_int(b"10011", True), -13)

    def test_swap_bytes(self):
        self.assertEqual(swap_bytes(b"aaaabbbbcccc", 4), b"ccccbbbbaaaa")
        self.assertEqual(swap_bytes(b"abcdefgh", 2), b"ghefcdab")
        self.assertEqual(swap_bytes(b"00011011", 2), b"11100100")

    def test_encode_bin(self):
        self.assertEqual(encode_bin(b"ab"),
            b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")

    def test_decode_bin(self):
        self.assertEqual(decode_bin(
            b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"),
            b"ab")

    def test_decode_bin_length(self):
        self.assertRaises(ValueError, decode_bin, b"\x00")


class TestExpr(unittest.TestCase):
    def test(self):
        path = Path("path")
        x = ~((path.foo * 2 + 3 << 2) % 11)
        self.assertEqual(x, 'not ((((this.foo * 2) + 3) >> 2) % 11)')
        self.assertFalse(x(dict(foo=7)))

