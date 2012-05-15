from construct.lib.py3compat import u
import unittest

from construct import String, PascalString, CString, UBInt16


class TestString(unittest.TestCase):
    def test_parse(self):
        s = String("foo", 5)
        self.assertEqual(s.parse(b"hello"), b"hello")

    def test_parse_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.parse(b"hello joh\xd4\x83n"), u("hello joh\u0503n"))

    def test_parse_padded(self):
        s = String("foo", 10, padchar=b"X", paddir="right")
        self.assertEqual(s.parse(b"helloXXXXX"), b"hello")

    def test_parse_padded_left(self):
        s = String("foo", 10, padchar=b"X", paddir="left")
        self.assertEqual(s.parse(b"XXXXXhello"), b"hello")

    def test_parse_padded_center(self):
        s = String("foo", 10, padchar=b"X", paddir="center")
        self.assertEqual(s.parse(b"XXhelloXXX"), b"hello")

    def test_build(self):
        s = String("foo", 5)
        self.assertEqual(s.build(b"hello"), b"hello")

    def test_build_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.build(u("hello joh\u0503n")), b"hello joh\xd4\x83n")

    def test_build_padded(self):
        s = String("foo", 10, padchar=b"X", paddir="right")
        self.assertEqual(s.build(b"hello"), b"helloXXXXX")

    def test_build_padded_left(self):
        s = String("foo", 10, padchar=b"X", paddir="left")
        self.assertEqual(s.build(b"hello"), b"XXXXXhello")

    def test_build_padded_center(self):
        s = String("foo", 10, padchar=b"X", paddir="center")
        self.assertEqual(s.build(b"hello"), b"XXhelloXXX")


class TestPascalString(unittest.TestCase):
    def test_parse(self):
        s = PascalString("foo")
        self.assertEqual(s.parse(b"\x05hello"), b"hello")

    def test_build(self):
        s = PascalString("foo")
        self.assertEqual(s.build(b"hello world"), b"\x0bhello world")

    def test_parse_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.parse(b"\x00\x05hello"), b"hello")

    def test_build_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.build(b"hello"), b"\x00\x05hello")


class TestCString(unittest.TestCase):
    def test_parse(self):
        s = CString("foo")
        self.assertEqual(s.parse(b"hello\x00"), b"hello")

    def test_build(self):
        s = CString("foo")
        self.assertEqual(s.build(b"hello"), b"hello\x00")

    def test_parse_terminator(self):
        s = CString("foo", terminators=b"XYZ")
        self.assertEqual(s.parse(b"helloX"), b"hello")
        self.assertEqual(s.parse(b"helloY"), b"hello")
        self.assertEqual(s.parse(b"helloZ"), b"hello")

    def test_build_terminator(self):
        s = CString("foo", terminators=b"XYZ")
        self.assertEqual(s.build(b"hello"), b"helloX")

