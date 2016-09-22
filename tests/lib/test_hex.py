import unittest
from declarativeunittest import raises

from construct.lib.hex import *


class TestHex(unittest.TestCase):

    def test_dump(self):
        assert hexundump(hexdump(b"",32),32) == b""
        assert hexundump(hexdump(b"??????????",32),32) == b"??????????"
