import unittest

from construct.lib.py3compat import *


class TestAll(unittest.TestCase):

    def test(self):
        self.assertEqual(int2byte(5), b"\x05")
        self.assertEqual(byte2int(b"\x05"), 5)
        for i in range(256):
            self.assertEqual(byte2int(int2byte(i)), i)

        self.assertEqual(str2bytes("abc"), b"abc")
        self.assertEqual(bytes2str(b"abc"), "abc")
        self.assertEqual(bytes2str(str2bytes("abc123\n")), "abc123\n")
        self.assertEqual(str2bytes(bytes2str(b"abc123\n")), b"abc123\n")

        self.assertEqual(str2unicode("abc"), u"abc")
        self.assertEqual(unicode2str(u"abc"), "abc")
        self.assertEqual(unicode2str(str2unicode("abc123\n")), "abc123\n")
        self.assertEqual(str2unicode(unicode2str(u"abc123\n")), "abc123\n")

        self.assertEqual(list(iteratebytes(b"abc")), [97,98,99])
        for i in range(256):
            self.assertEqual(list(iteratebytes(int2byte(i))), [i])

