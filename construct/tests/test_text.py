import unittest

from construct.text import Whitespace
from construct import RangeError

class TestWhitespace(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(Whitespace().parse(b" \t\t "), None)

    def test_parse_required(self):
        self.assertRaises(RangeError, Whitespace(optional=False).parse, b"X")

    def test_build(self):
        self.assertEqual(Whitespace().build(None), b" ")
