import unittest

from construct import String, PascalString, CString, UBInt16, GreedyString
from construct import StringError


class TestString(unittest.TestCase):
    def test_parse(self):
        s = String("s", 5)
        self.assertEqual(s.parse(b"hello"), b"hello")

    def test_parse_utf8(self):
        s = String("s", 12, encoding="utf8")
        self.assertEqual(s.parse(b"hello joh\xd4\x83n"), u"hello joh\u0503n")

    def test_parse_padded_right(self):
        s = String("s", 10, padchar=b"X", paddir="right")
        self.assertEqual(s.parse(b"helloXXXXX"), b"hello")

    def test_parse_padded_left(self):
        s = String("s", 10, padchar=b"X", paddir="left")
        self.assertEqual(s.parse(b"XXXXXhello"), b"hello")

    def test_parse_padded_center(self):
        s = String("s", 10, padchar=b"X", paddir="center")
        self.assertEqual(s.parse(b"XXhelloXXX"), b"hello")

    def test_build(self):
        s = String("s", 5)
        self.assertEqual(s.build(b"hello"), b"hello")

    def test_build_utf8(self):
        s = String("s", 12, encoding="utf8")
        self.assertEqual(s.build(u"hello joh\u0503n"), b"hello joh\xd4\x83n")

    def test_build_missing_encoding(self):
        s = String("s", 5)
        self.assertRaises(StringError, s.build, u"hello")

    def test_build_padded_right(self):
        s = String("s", 10, padchar=u"X", paddir="right", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"helloXXXXX")
        s = String("s", 10, padchar=b"X", paddir="right", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"helloXXXXX")

    def test_build_padded_left(self):
        s = String("s", 10, padchar=u"X", paddir="left", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"XXXXXhello")
        s = String("s", 10, padchar=b"X", paddir="left", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"XXXXXhello")

    def test_build_padded_center(self):
        s = String("s", 10, padchar=u"X", paddir="center", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"XXhelloXXX")
        s = String("s", 10, padchar=b"X", paddir="center", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"XXhelloXXX")

    def test_build_too_long(self):
        s = String("string", 5, trimdir="right")
        self.assertEqual(s.build(b"1234567890"), b"12345")
        s = String("string", 5, trimdir="left")
        self.assertEqual(s.build(b"1234567890"), b"67890")

    def test_size(self):
        s = String("s", 5)
        self.assertEqual(s.sizeof(), 5)
        s = String("s", 12, encoding="utf8")
        self.assertEqual(s.sizeof(), 12)
        s = String("s", 10, padchar=u"X", paddir="left", encoding="utf8")
        self.assertEqual(s.sizeof(), 10)



class TestPascalString(unittest.TestCase):
    def test_parse(self):
        s = PascalString("s", encoding="utf8")
        self.assertEqual(s.parse(b"\x05hello"), u"hello")
        s = PascalString("s")
        self.assertEqual(s.parse(b"\x05hello"), b"hello")

    def test_build(self):
        s = PascalString("s", encoding="utf8")
        self.assertEqual(s.build(u"hello world"), b"\x0bhello world")
        s = PascalString("s")
        self.assertEqual(s.build(b"hello world"), b"\x0bhello world")

    def test_parse_custom_length_field(self):
        s = PascalString("s", lengthfield=UBInt16(None), encoding="utf8")
        self.assertEqual(s.parse(b"\x00\x05hello"), u"hello")

    def test_build_custom_length_field(self):
        s = PascalString("s", lengthfield=UBInt16(None), encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"\x00\x05hello")


class TestCString(unittest.TestCase):
    def test_parse(self):
        s = CString("s", encoding="utf8")
        self.assertEqual(s.parse(b"hello\x00"), u"hello")

    def test_build(self):
        s = CString("s", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"hello\x00")

    def test_parse_terminator(self):
        s = CString("s", terminators=b"XYZ", encoding="utf8")
        self.assertEqual(s.parse(b"helloX"), u"hello")
        self.assertEqual(s.parse(b"helloY"), u"hello")
        self.assertEqual(s.parse(b"helloZ"), u"hello")

    def test_build_terminator(self):
        s = CString("s", terminators=b"XYZ", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"helloX")


class TestGreedyString(unittest.TestCase):
    def test_parse(self):
        s = GreedyString("s", encoding="utf8")
        self.assertEqual(s.parse(b"hello\x00"), u"hello\x00")
        self.assertEqual(s.parse(b""), u"")

    def test_build(self):
        s = GreedyString("s", encoding="utf8")
        self.assertEqual(s.build(u"hello"), b"hello")

