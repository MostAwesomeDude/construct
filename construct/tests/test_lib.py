import unittest

from construct.lib.binary import (int_to_bin, bin_to_int, swap_bytes,
    encode_bin, decode_bin)

class TestBinary(unittest.TestCase):
    def test_int_to_bin(self):
        self.assertEqual(int_to_bin(19, 5), b"\x01\x00\x00\x01\x01")

    def test_int_to_bin_signed(self):
        self.assertEqual(int_to_bin(-13, 5), b"\x01\x00\x00\x01\x01")

    def test_bin_to_int(self):
        self.assertEqual(bin_to_int(b"\x01\x00\x00\x01\x01"), 19)

    def test_bin_to_int_signed(self):
        self.assertEqual(bin_to_int(b"\x01\x00\x00\x01\x01", True), -13)

    def test_swap_bytes(self):
        self.assertEqual(swap_bytes(b"aaaabbbbcccc", 4), b"ccccbbbbaaaa")

    def test_encode_bin(self):
        self.assertEqual(encode_bin(b"ab"),
            b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")

    def test_decode_bin(self):
        self.assertEqual(decode_bin(
            b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"),
            b"ab")

    def test_decode_bin_length(self):
        self.assertRaises(ValueError, decode_bin, b"\x00")

