import unittest

from construct.lib.py3compat import *


class TestAll(unittest.TestCase):

    # def test_on_py2(self):
    #     if notPY3:
    #         self.assertEqual(int2byte(5), b"\x05")
    #         self.assertEqual(byte2int(b"\x05"), 5)
    #         self.assertEqual(str2bytes("abc"), b"abc")
    #         self.assertEqual(str2unicode("abc"), u"abc")
    #         self.assertEqual(bytes2str(b"abc"), "abc")

    # def test_on_py3(self):
    #     if PY3:
    #         self.assertEqual(int2byte(5), b"\x05")
    #         self.assertEqual(byte2int(b"\x05"), 5)
    #         self.assertEqual(str2bytes("abc"), b"abc")
    #         self.assertEqual(str2unicode("abc"), u"abc")
    #         self.assertEqual(bytes2str(b"abc"), "abc")

    def test(self):
        self.assertEqual(int2byte(5), b"\x05")
        self.assertEqual(byte2int(b"\x05"), 5)
        self.assertEqual(str2bytes("abc"), b"abc")
        self.assertEqual(str2unicode("abc"), u"abc")
        self.assertEqual(bytes2str(b"abc"), "abc")

        for i in range(256):
            self.assertEqual(byte2int(int2byte(i)), i)

