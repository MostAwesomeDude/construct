import unittest

from construct import Flag
import six

class TestFlag(unittest.TestCase):

    def test_parse(self):
        flag = Flag("flag")
        self.assertTrue(flag.parse(six.b("\x01")))

    def test_parse_flipped(self):
        flag = Flag("flag", truth=0, falsehood=1)
        self.assertFalse(flag.parse(six.b("\x01")))

    def test_parse_default(self):
        flag = Flag("flag")
        self.assertFalse(flag.parse(six.b("\x02")))

    def test_parse_default_true(self):
        flag = Flag("flag", default=True)
        self.assertTrue(flag.parse(six.b("\x02")))

    def test_build(self):
        flag = Flag("flag")
        self.assertEqual(flag.build(True), six.b("\x01"))

    def test_build_flipped(self):
        flag = Flag("flag", truth=0, falsehood=1)
        self.assertEqual(flag.build(True), six.b("\x00"))

