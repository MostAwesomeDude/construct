import unittest

from construct import String, PascalString, CString, UBInt16

class TestString(unittest.TestCase):

    def test_parse(self):
        s = String("foo", 5)
        self.assertEqual(s.parse("hello"), "hello")

    def test_parse_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.parse("hello joh\xd4\x83n"), u"hello joh\u0503n")

    def test_parse_padded(self):
        s = String("foo", 10, padchar="X", paddir="right")
        self.assertEqual(s.parse("helloXXXXX"), "hello")

    def test_parse_padded_left(self):
        s = String("foo", 10, padchar="X", paddir="left")
        self.assertEqual(s.parse("XXXXXhello"), "hello")

    def test_parse_padded_center(self):
        s = String("foo", 10, padchar="X", paddir="center")
        self.assertEqual(s.parse("XXhelloXXX"), "hello")

    def test_build(self):
        s = String("foo", 5)
        self.assertEqual(s.build("hello"), "hello")

    def test_build_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.build(u"hello joh\u0503n"), "hello joh\xd4\x83n")

    def test_build_padded(self):
        s = String("foo", 10, padchar="X", paddir="right")
        self.assertEqual(s.build("hello"), "helloXXXXX")

    def test_build_padded_left(self):
        s = String("foo", 10, padchar="X", paddir="left")
        self.assertEqual(s.build("hello"), "XXXXXhello")

    def test_build_padded_center(self):
        s = String("foo", 10, padchar="X", paddir="center")
        self.assertEqual(s.build("hello"), "XXhelloXXX")

class TestPascalString(unittest.TestCase):

    def test_parse(self):
        s = PascalString("foo")
        self.assertEqual(s.parse("\x05hello"), "hello")

    def test_build(self):
        s = PascalString("foo")
        self.assertEqual(s.build("hello world"), "\x0bhello world")

    def test_parse_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.parse("\x00\x05hello"), "hello")

    def test_build_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"))
        self.assertEqual(s.build("hello"), "\x00\x05hello")

class TestCString(unittest.TestCase):

    def test_parse(self):
        s = CString("foo")
        self.assertEqual(s.parse("hello\x00"), "hello")

    def test_build(self):
        s = CString("foo")
        self.assertEqual(s.build("hello"), "hello\x00")

    def test_parse_terminator(self):
        s = CString("foo", terminators="XYZ")
        self.assertEqual(s.parse("helloX"), "hello")
        self.assertEqual(s.parse("helloY"), "hello")
        self.assertEqual(s.parse("helloZ"), "hello")

    def test_build_terminator(self):
        s = CString("foo", terminators="XYZ")
        self.assertEqual(s.build("hello"), "helloX")
