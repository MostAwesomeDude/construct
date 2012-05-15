import unittest

from construct import Flag

class TestFlag(unittest.TestCase):

    def test_parse(self):
        flag = Flag("flag")
        self.assertTrue(flag.parse("\x01"))

    def test_parse_flipped(self):
        flag = Flag("flag", truth=0, falsehood=1)
        self.assertFalse(flag.parse("\x01"))

    def test_parse_default(self):
        flag = Flag("flag")
        self.assertFalse(flag.parse("\x02"))

    def test_parse_default_true(self):
        flag = Flag("flag", default=True)
        self.assertTrue(flag.parse("\x02"))

    def test_build(self):
        flag = Flag("flag")
        self.assertEqual(flag.build(True), "\x01")

    def test_build_flipped(self):
        flag = Flag("flag", truth=0, falsehood=1)
        self.assertEqual(flag.build(True), "\x00")
