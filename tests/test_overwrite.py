import unittest

from construct import Struct, Byte, Embedded, OverwriteError


class TestOverwrite(unittest.TestCase):
    def test_overwrite(self):
        s = Struct("s",
            Byte("a"),
            Byte("a"),
            allow_overwrite = True
        )
        self.assertEqual(s.parse(b"\x01\x02").a, 2)

        s = Struct("s",
            Byte("a"),
            Embedded(Struct("b",
                Byte("a"),
                allow_overwrite = True
            )),
        )
        self.assertEqual(s.parse(b"\x01\x02").a, 2)

        s = Struct("s",
            Embedded(Struct("b",
                Byte("a"),
            )),
            Byte("a"),
            allow_overwrite = True
        )
        self.assertEqual(s.parse(b"\x01\x02").a, 2)

    def test_no_overwrite(self):
        s = Struct("s",
            Byte("a"),
            Byte("a"),
        )
        self.assertRaises(OverwriteError, s.parse, b"\x01\x02")

        s = Struct("s",
            Byte("a"),
            Embedded(Struct("b",
                Byte("a"),
            )),
            allow_overwrite = True
        )
        self.assertRaises(OverwriteError, s.parse, b"\x01\x02")

        s = Struct("s",
            Embedded(Struct("b",
                Byte("a"),
                allow_overwrite = True
            )),
            Byte("a"),
        )
        self.assertRaises(OverwriteError, s.parse, b"\x01\x02")

