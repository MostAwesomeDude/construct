from declarativeunittest import *
from construct.lib.hex import *


class TestHex(unittest.TestCase):

    def test_dump(self):
        for i in range(100):
            assert hexundump(hexdump(b"?"*i,32),32) == b"?"*i
