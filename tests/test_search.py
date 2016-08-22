import unittest

from construct import Struct, UBInt8, Bytes, Container, Switch, GreedyRange

struct = Struct("a",
    UBInt8("aa"),
    Struct("ab",
        UBInt8("aba"),
        UBInt8("abb"),
        Struct("abc",
            UBInt8("abca"),
            Switch("abcb", lambda ctx: ctx.abca, {
                    1 : Struct("abcb1",
                            UBInt8("abcb1a")
                        ),
                    2 : Struct("abcb2",
                            UBInt8("abcb2a")
                        ),
                    3 : Struct("abcb3",
                            UBInt8("abcb3a")
                        ),
                    4 : Struct("abcb4",
                            UBInt8("abcb4a")
                        ),
                }
            ),
        ),
    ),
    UBInt8("ac"),
    GreedyRange(Struct('ad', UBInt8("ada")))
)

class TestSearch(unittest.TestCase):
    def test_search_sanity(self):
        obj1 = struct.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")

        self.assertEqual(obj1.search("bb"), None)
        self.assertNotEqual(obj1.search("abcb"), None)
        self.assertNotEqual(obj1.search("ad"), None)
        self.assertEqual(obj1.search("aa"), 0x11)
        self.assertEqual(obj1.search("aba"), 0x21)
        self.assertEqual(obj1.search("abb"), 0x22)
        self.assertEqual(obj1.search('ac'), 0x13)
        
    def test_search_functionality(self):
        obj1 = struct.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")
        obj2 = struct.parse(b"\x11\x21\x22\x03\x03\x13\x51\x52")

        self.assertEqual(obj1.search('abcb1a'), None)
        self.assertEqual(obj1.search('abcb3a'), None)
        self.assertEqual(obj1.search('abcb4a'), None)
        self.assertEqual(obj1.search('abcb2a'), 0x02)
        
        self.assertEqual(obj2.search('abcb1a'), None)
        self.assertEqual(obj2.search('abcb2a'), None)
        self.assertEqual(obj2.search('abcb4a'), None)
        self.assertEqual(obj2.search('abcb3a'), 0x03)
        # Return only the first one
        self.assertEqual(obj1.search("ada"), 0x51)
        
    def test_search_all_sanity(self):
        obj1 = struct.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")

        self.assertEqual(obj1.search_all("bb"), [])
        self.assertNotEqual(obj1.search_all("ad"), None)
        self.assertEqual(obj1.search_all("aa"), [0x11])
        self.assertEqual(obj1.search_all("aba"), [0x21])
        self.assertEqual(obj1.search_all("abb"), [0x22])
        self.assertEqual(obj1.search_all('ac'), [0x13])
        
    def test_search_all_functionality(self):
        obj1 = struct.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")
        # Return all of them
        self.assertEqual(obj1.search_all("ada"), [0x51,0x52])
