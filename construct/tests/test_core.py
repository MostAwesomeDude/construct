import unittest

from construct import Struct, Byte, MetaField

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
