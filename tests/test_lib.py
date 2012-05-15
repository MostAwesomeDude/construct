import unittest

from construct.lib.binary import (int_to_bin, bin_to_int, swap_bytes,
    encode_bin, decode_bin)

class TestBinary(unittest.TestCase):
    pass

    def test_int_to_bin(self):
        self.assertEqual(int_to_bin(19, 5), "\x01\x00\x00\x01\x01")

    def test_int_to_bin_signed(self):
        self.assertEqual(int_to_bin(-13, 5), "\x01\x00\x00\x01\x01")

    def test_bin_to_int(self):
        self.assertEqual(bin_to_int("\x01\x00\x00\x01\x01"), 19)

    def test_bin_to_int_signed(self):
        self.assertEqual(bin_to_int("\x01\x00\x00\x01\x01", True), -13)

    def test_swap_bytes(self):
        self.assertEqual(swap_bytes("aaaabbbbcccc", 4), "ccccbbbbaaaa")

    def test_encode_bin(self):
        self.assertEqual(encode_bin("ab"),
            "\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")

    def test_decode_bin(self):
        self.assertEqual(decode_bin(
            "\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"),
            "ab")

    def test_decode_bin_length(self):
        self.assertRaises(ValueError, decode_bin, "\x00")
