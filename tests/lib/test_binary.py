import unittest
from declarativeunittest import raises

from construct.lib.binary import *


class TestBinary(unittest.TestCase):
    def testall(self):

        assert integer2bits(19, 5) == b"\x01\x00\x00\x01\x01"
        assert integer2bits(19, 8) == b'\x00\x00\x00\x01\x00\x00\x01\x01'
        assert integer2bits(19, 3) == b'\x00\x01\x01'
        assert integer2bits(-13, 5) == b"\x01\x00\x00\x01\x01"
        assert integer2bits(-13, 8) == b"\x01\x01\x01\x01\x00\x00\x01\x01"
        self.assertRaises(ValueError, integer2bits, 19, 0)
        self.assertRaises(ValueError, integer2bits, 19, -1)
        self.assertRaises(ValueError, integer2bits, -19, 0)
        self.assertRaises(ValueError, integer2bits, -19, -1)

        assert integer2bytes(0, 4) == b"\x00\x00\x00\x00"
        assert integer2bytes(1, 4) == b"\x00\x00\x00\x01"
        assert integer2bytes(255, 4) == b"\x00\x00\x00\xff"
        assert integer2bytes(-1, 4) == b"\xff\xff\xff\xff"
        assert integer2bytes(-255, 4) == b"\xff\xff\xff\x01"
        self.assertRaises(ValueError, integer2bytes, 19, 0)
        self.assertRaises(ValueError, integer2bytes, 19, -1)
        self.assertRaises(ValueError, integer2bytes, -19, 0)
        self.assertRaises(ValueError, integer2bytes, -19, -1)

        assert bits2integer(b"\x01\x00\x00\x01\x01") == 19
        assert bits2integer(b"\x01\x00\x00\x01\x01", True) == -13
        assert bits2integer(b"10011") == 19
        assert bits2integer(b"10011", True) == -13

        for i in [-300,-255,-100,-1,0,1,100,255,300]:
            assert bits2integer(integer2bits(i,64),signed=(i<0)) == i
            assert bytes2integer(integer2bytes(i,8),signed=(i<0)) == i
            assert bits2bytes(integer2bits(i,64)) == integer2bytes(i,8)
            assert bytes2bits(integer2bytes(i,8)) == integer2bits(i,64)

        assert bytes2bits(b"ab") == b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"
        assert bytes2bits(b"") == b""

        assert bits2bytes(b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00") == b"ab"
        assert bits2bytes(b"") == b""
        self.assertRaises(ValueError, bits2bytes, b"\x00")
        self.assertRaises(ValueError, bits2bytes, b"\x00\x00\x00\x00\x00\x00\x00")

        assert swapbytes(b"aaaabbbbcccc", 4) == b"ccccbbbbaaaa"
        assert swapbytes(b"abcdefgh", 2) == b"ghefcdab"
        assert swapbytes(b"00011011", 2) == b"11100100"
        assert swapbytes(b"", 2) == b""
        self.assertRaises(ValueError, swapbytes, b"12345678", 7)
        self.assertRaises(ValueError, swapbytes, b"12345678", -4)

