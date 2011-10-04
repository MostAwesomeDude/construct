import unittest

from construct import Field, UBInt8
from construct import OneOf, NoneOf, HexDumpAdapter
from construct import ValidationError

class TestHexDumpAdapter(unittest.TestCase):

    def setUp(self):
        self.hda = HexDumpAdapter(Field("hexdumpadapter", 6))

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.hda.parse("abcdef"), "abcdef")

    def test_build(self):
        self.assertEqual(self.hda.build("abcdef"), "abcdef")

    def test_str(self):
        pretty = str(self.hda.parse("abcdef")).strip()
        offset, digits, ascii = [i.strip() for i in pretty.split("  ") if i]
        self.assertEqual(offset, "0000")
        self.assertEqual(digits, "61 62 63 64 65 66")
        self.assertEqual(ascii, "abcdef")

class TestNoneOf(unittest.TestCase):

    def setUp(self):
        self.n = NoneOf(UBInt8("foo"), [4, 5, 6, 7])

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.n.parse("\x08"), 8)

    def test_parse_invalid(self):
        self.assertRaises(ValidationError, self.n.parse, "\x06")

class TestOneOf(unittest.TestCase):

    def setUp(self):
        self.o = OneOf(UBInt8("foo"), [4, 5, 6, 7])

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.o.parse("\x05"), 5)

    def test_parse_invalid(self):
        self.assertRaises(ValidationError, self.o.parse, "\x08")

    def test_build(self):
        self.assertEqual(self.o.build(5), "\x05")

    def test_build_invalid(self):
        self.assertRaises(ValidationError, self.o.build, 9)
