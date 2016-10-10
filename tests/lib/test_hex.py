import unittest
from declarativeunittest import raises

from construct.lib.hex import *


class TestHex(unittest.TestCase):

    def test_dump(self):
        assert hexundump(hexdump(b"",32),32) == b""
        assert hexundump(hexdump(b"??????????",32),32) == b"??????????"
        for i in range(100):
            assert hexundump(hexdump(b"?"*i,32),32) == b"?"*i
        assert hexundump(hexdump(b"?"*100000,32),32) == b"?"*100000

