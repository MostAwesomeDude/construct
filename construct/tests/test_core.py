import unittest

from construct import Struct, Byte, MetaField, StaticField
from construct import FieldError

class TestStaticField(unittest.TestCase):

    def setUp(self):
        self.sf = StaticField("staticfield", 2)

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.sf.parse("ab"), "ab")

    def test_build(self):
        self.assertEqual(self.sf.build("ab"), "ab")

    def test_parse_too_short(self):
        self.assertRaises(FieldError, self.sf.parse, "a")

    def test_build_too_short(self):
        self.assertRaises(FieldError, self.sf.build, "a")

class TestMetaField(unittest.TestCase):

    def setUp(self):
        self.s = Struct("foo", Byte("length"),
            MetaField("data", lambda context: context["length"]))

    def test_trivial(self):
        pass

    def test_parse(self):
        c = self.s.parse("\x03ABC")
        self.assertEqual(c.length, 3)
        self.assertEqual(c.data, "ABC")

        c = self.s.parse("\x04ABCD")
        self.assertEqual(c.length, 4)
        self.assertEqual(c.data, "ABCD")
