# import unittest

# from construct import UBInt8, Struct, Container
# from construct import Range, Array, GreedyRange, OptionalGreedyRange
# from construct import ArrayError, RangeError


# class TestRange(unittest.TestCase):

#     def setUp(self):
#         self.c = Range(3, 7, UBInt8("foo"))
#         self.nested_range = Range(0, 100, Struct('report', UBInt8('id')))

#     def test_trivial(self):
#         pass

#     def test_parse(self):
#         self.assertEqual(self.c.parse(b"\x01\x02\x03"), 
#                          [1, 2, 3])
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04\x05\x06"),
#                          [1, 2, 3, 4, 5, 6])
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04\x05\x06\x07"),
#                          [1, 2, 3, 4, 5, 6, 7])
#         self.assertEqual(self.nested_range.parse(b'\x01\x02'),
#                          [Container(id=1), Container(id=2)])

#     def test_build(self):
#         self.assertEqual(self.c.build([1, 2, 3, 4]), b"\x01\x02\x03\x04")
#         self.assertEqual(self.nested_range.build([dict(id=i) for i in range(5)]), b'\x00\x01\x02\x03\x04')

#     def test_parse_undersized(self):
#         self.assertRaises(RangeError, self.c.parse, b'\x00')

#     def test_build_undersized(self):
#         self.assertRaises(RangeError, self.c.build, [1, 2])

#     def test_parse_oversized(self):
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08\x09"),
#                          [1, 2, 3, 4, 5, 6, 7])

#     def test_build_oversized(self):
#         self.assertRaises(RangeError, self.c.build, [1, 2, 3, 4, 5, 6, 7, 8])

#     def test_build_invalid_build_input(self):
#         self.assertRaises(RangeError, self.c.build, 0)
#         self.assertRaises(RangeError, self.nested_range.build, {'id': 1})

#     def test_unsane_constructor_min_max(self):
#         self.assertRaises(RangeError, Range, -2, 7, UBInt8("byte"))
#         self.assertRaises(RangeError, Range, -2, -7, UBInt8("byte"))
#         self.assertRaises(RangeError, Range, 2, -7, UBInt8("byte"))
#         self.assertRaises(RangeError, Range, 7, 2, UBInt8("byte"))


# class TestArray(unittest.TestCase):

#     def setUp(self):
#         self.c = Array(4, UBInt8("foo"))

#     def test_trivial(self):
#         pass

#     def test_parse(self):
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04"), [1, 2, 3, 4])
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04\x05\x06"),
#             [1, 2, 3, 4])

#     def test_build(self):
#         self.assertEqual(self.c.build([5, 6, 7, 8]), b"\x05\x06\x07\x08")

#     def test_build_oversized(self):
#         self.assertRaises(ArrayError, self.c.build, [5, 6, 7, 8, 9])

#     def test_build_undersized(self):
#         self.assertRaises(ArrayError, self.c.build, [5, 6, 7])


# class TestGreedyRange(unittest.TestCase):

#     def setUp(self):
#         self.c = GreedyRange(UBInt8("foo"))

#     def test_trivial(self):
#         pass

#     def test_empty_parse(self):
#         self.assertRaises(RangeError, self.c.parse, b"")

#     def test_parse(self):
#         self.assertEqual(self.c.parse(b"\x01"), [1])
#         self.assertEqual(self.c.parse(b"\x01\x02\x03"), [1, 2, 3])
#         self.assertEqual(self.c.parse(b"\x01\x02\x03\x04\x05\x06"),
#             [1, 2, 3, 4, 5, 6])

#     def test_empty_build(self):
#         self.assertRaises(RangeError, self.c.build, [])

#     def test_build(self):
#         self.assertEqual(self.c.build([1, 2]), b"\x01\x02")


# class TestOptionalGreedyRange(unittest.TestCase):

#     def setUp(self):
#         self.c = OptionalGreedyRange(UBInt8("foo"))

#     def test_trivial(self):
#         pass

#     def test_empty_parse(self):
#         self.assertEqual(self.c.parse(b""), [])

#     def test_parse(self):
#         self.assertEqual(self.c.parse(b"\x01\x02"), [1, 2])

#     def test_empty_build(self):
#         self.assertEqual(self.c.build([]), b"")

#     def test_build(self):
#         self.assertEqual(self.c.build([1, 2]), b"\x01\x02")

