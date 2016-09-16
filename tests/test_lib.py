import unittest

from construct.lib.binary import integer2bits, bits2integer, swapbitslines, bytes2bits, bits2bytes
from construct.lib.expr import Path


class TestBinary(unittest.TestCase):
    def test_int_to_bin(self):
        self.assertEqual(integer2bits(19, 5), b"\x01\x00\x00\x01\x01")
        self.assertEqual(integer2bits(19, 8), b'\x00\x00\x00\x01\x00\x00\x01\x01')
        self.assertEqual(integer2bits(19, 3), b'\x00\x01\x01')
        self.assertRaises(ValueError, integer2bits, 19, 0)
        self.assertRaises(ValueError, integer2bits, 19, -1)

    def test_int_to_bin_signed(self):
        self.assertEqual(integer2bits(-13, 5), b"\x01\x00\x00\x01\x01")
        self.assertEqual(integer2bits(-13, 8), b"\x01\x01\x01\x01\x00\x00\x01\x01")
        self.assertRaises(ValueError, integer2bits, -19, 0)
        self.assertRaises(ValueError, integer2bits, -19, -1)

    def test_bin_to_int(self):
        self.assertEqual(bits2integer(b"\x01\x00\x00\x01\x01"), 19)
        self.assertEqual(bits2integer(b"10011"), 19)

    def test_bin_to_int_signed(self):
        self.assertEqual(bits2integer(b"\x01\x00\x00\x01\x01", True), -13)
        self.assertEqual(bits2integer(b"10011", True), -13)

    def test_swapbitslines(self):
        self.assertEqual(swapbitslines(b"aaaabbbbcccc", 4), b"ccccbbbbaaaa")
        self.assertEqual(swapbitslines(b"abcdefgh", 2), b"ghefcdab")
        self.assertEqual(swapbitslines(b"00011011", 2), b"11100100")
        self.assertRaises(ValueError, swapbitslines, b"12345678", 7)
        self.assertRaises(ValueError, swapbitslines, b"12345678", -4)

    def test_encode_bin(self):
        self.assertEqual(bytes2bits(b"ab"), b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")
        self.assertEqual(bytes2bits(b""), b"")

    def test_decode_bin(self):
        self.assertEqual(bits2bytes(b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"), b"ab")
        self.assertEqual(bits2bytes(b""), b"")

    def test_decode_bin_length(self):
        self.assertRaises(ValueError, bits2bytes, b"\x00")
        self.assertRaises(ValueError, bits2bytes, b"\x00\x00\x00\x00\x00\x00\x00")

