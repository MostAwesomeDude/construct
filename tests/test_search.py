import unittest
from declarativeunittest import raises

from construct import *



class TestSearch(unittest.TestCase):

    def setUp(self):
        self.s = Struct(
            "aa" / UBInt8,
            "ab" / Struct(
                "aba" / UBInt8,
                "abb" / UBInt8,
                "abc" / Struct(
                    "abca" / UBInt8,
                    "abcb" / Switch(lambda ctx: ctx.abca, {
                        1 : "abcb1" / Struct("abcb1a" / UBInt8),
                        2 : "abcb2" / Struct("abcb2a" / UBInt8),
                        3 : "abcb3" / Struct("abcb3a" / UBInt8),
                        4 : "abcb4" / Struct("abcb4a" / UBInt8),
                    }),
                ),
            ),
            "ac" / UBInt8,
            GreedyRange("ad" / Struct("ada" / UBInt8)),
        )

    def test_search_sanity(self):
        obj1 = self.s.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")

        self.assertEqual(obj1.search("bb"), None)
        self.assertNotEqual(obj1.search("abcb"), None)
        self.assertNotEqual(obj1.search("ad"), None)
        self.assertEqual(obj1.search("aa"), 0x11)
        self.assertEqual(obj1.search("aba"), 0x21)
        self.assertEqual(obj1.search("abb"), 0x22)
        self.assertEqual(obj1.search('ac'), 0x13)
        
    def test_search_functionality(self):
        obj1 = self.s.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")
        obj2 = self.s.parse(b"\x11\x21\x22\x03\x03\x13\x51\x52")

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
        obj1 = self.s.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")

        self.assertEqual(obj1.search_all("bb"), [])
        self.assertNotEqual(obj1.search_all("ad"), None)
        self.assertEqual(obj1.search_all("aa"), [0x11])
        self.assertEqual(obj1.search_all("aba"), [0x21])
        self.assertEqual(obj1.search_all("abb"), [0x22])
        self.assertEqual(obj1.search_all('ac'), [0x13])
        
    def test_search_all_functionality(self):
        obj1 = self.s.parse(b"\x11\x21\x22\x02\x02\x13\x51\x52")
        # Return all of them
        self.assertEqual(obj1.search_all("ada"), [0x51,0x52])

