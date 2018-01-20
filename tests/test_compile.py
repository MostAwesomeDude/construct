import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


class TestCompile(unittest.TestCase):

    def test_it(self):
        code = Int.compile()
        print(code)
        # assert 0
