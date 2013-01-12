import unittest
import six
from construct import String, PascalString, CString, UBInt16


class TestString(unittest.TestCase):
    def test_parse(self):
        s = String("foo", 5)
        self.assertEqual(s.parse(six.b("hello")), six.u("hello"))

    def test_parse_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.parse(six.b("hello joh\xd4\x83n")), six.u("hello joh\u0503n"))

    def test_parse_padded(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="right")
        self.assertEqual(s.parse(six.b("helloXXXXX")), six.u("hello"))

    def test_parse_padded_left(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="left")
        self.assertEqual(s.parse(six.b("XXXXXhello")), six.u("hello"))

    def test_parse_padded_center(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="center")
        self.assertEqual(s.parse(six.b("XXhelloXXX")), six.u("hello"))

    def test_build(self):
        s = String("foo", 5)
        self.assertEqual(s.build(six.u("hello")), six.b("hello"))

    def test_build_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.build(six.u("hello joh\u0503n")), six.b("hello joh\xd4\x83n"))

    def test_build_padded(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="right")
        self.assertEqual(s.build(six.u("hello")), six.b("helloXXXXX"))

    def test_build_padded_left(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="left")
        self.assertEqual(s.build(six.u("hello")), six.b("XXXXXhello"))

    def test_build_padded_center(self):
        s = String("foo", 10, padchar=six.b("X"), paddir="center")
        self.assertEqual(s.build(six.u("hello")), six.b("XXhelloXXX"))


class TestPascalString(unittest.TestCase):
    def test_parse(self):
        s = PascalString("foo")
        self.assertEqual(s.parse(six.b("\x05hello")), six.u("hello"))

    def test_build(self):
        s = PascalString("foo")
        self.assertEqual(s.build(six.u("hello world")), six.b("\x0bhello world"))

    def test_parse_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.parse(six.b("\x00\x05hello")), six.u("hello"))

    def test_build_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.build(six.u("hello")), six.b("\x00\x05hello"))


class TestCString(unittest.TestCase):
    def test_parse(self):
        s = CString("foo")
        self.assertEqual(s.parse(six.b("hello\x00")), six.u("hello"))

    def test_build(self):
        s = CString("foo")
        self.assertEqual(s.build(six.u("hello")), six.b("hello\x00"))

    def test_parse_terminator(self):
        s = CString("foo", terminators=six.b("XYZ"))
        self.assertEqual(s.parse(six.b("helloX")), six.u("hello"))
        self.assertEqual(s.parse(six.b("helloY")), six.u("hello"))
        self.assertEqual(s.parse(six.b("helloZ")), six.u("hello"))

    def test_build_terminator(self):
        s = CString("foo", terminators=six.b("XYZ"))
        self.assertEqual(s.build(six.u("hello")), six.b("helloX"))

