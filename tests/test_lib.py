import unittest

from construct.lib.binary import (int_to_bin, bin_to_int, swap_bytes,
    encode_bin, decode_bin)
import six

class TestBinary(unittest.TestCase):
    def test_int_to_bin(self):
        self.assertEqual(int_to_bin(19, 5), six.b("\x01\x00\x00\x01\x01"))
        self.assertEqual(int_to_bin(19, 8), six.b('\x00\x00\x00\x01\x00\x00\x01\x01'))
        self.assertEqual(int_to_bin(19, 3), six.b('\x00\x01\x01'))

    def test_int_to_bin_signed(self):
        self.assertEqual(int_to_bin(-13, 5), six.b("\x01\x00\x00\x01\x01"))
        self.assertEqual(int_to_bin(-13, 8), six.b("\x01\x01\x01\x01\x00\x00\x01\x01"))

    def test_bin_to_int(self):
        self.assertEqual(bin_to_int(six.b("\x01\x00\x00\x01\x01")), 19)
        self.assertEqual(bin_to_int(six.b("10011")), 19)

    def test_bin_to_int_signed(self):
        self.assertEqual(bin_to_int(six.b("\x01\x00\x00\x01\x01"), True), -13)
        self.assertEqual(bin_to_int(six.b("10011"), True), -13)

    def test_swap_bytes(self):
        self.assertEqual(swap_bytes(six.b("aaaabbbbcccc"), 4), six.b("ccccbbbbaaaa"))
        self.assertEqual(swap_bytes(six.b("abcdefgh"), 2), six.b("ghefcdab"))
        self.assertEqual(swap_bytes(six.b("00011011"), 2), six.b("11100100"))

    def test_encode_bin(self):
        self.assertEqual(encode_bin(six.b("ab")),
            six.b("\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"))

    def test_decode_bin(self):
        self.assertEqual(decode_bin(
            six.b("\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00")),
            six.b("ab"))

    def test_decode_bin_length(self):
        self.assertRaises(ValueError, decode_bin, six.b("\x00"))


if __name__ == "__main__":
    unittest.main()
    
