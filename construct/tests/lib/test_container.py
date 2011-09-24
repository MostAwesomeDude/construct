import unittest

from construct.lib.container import Container

class TestContainer(unittest.TestCase):

    def test_in(self):
        c = Container(a=1)
        self.assertTrue("a" in c)

    def test_not_in(self):
        c = Container()
        self.assertTrue("a" not in c)
