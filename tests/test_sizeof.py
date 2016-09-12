# import unittest

# from construct import Struct, UBInt8, Bytes, Container


# class TestSizeof(unittest.TestCase):

#     def test(self):
#         def func(ctx):
#             print("func context is %r" % (ctx,))
#             return ctx._.length + ctx.inner_length

#         pstring = Struct("pstring", 
#             UBInt8("length"),
#             Struct("inner",
#                 UBInt8("inner_length"),
#                 Bytes("data", func),
#             )
#         )
#         obj = pstring.parse(b"\x03\x02helloXXX")
#         print(repr(obj))
#         self.assertEqual(obj, Container(length=3)(inner=Container(inner_length=2)(data=b"hello")))
#         size = pstring._sizeof(Container(inner_length=2)(_=Container(length=3)))
#         self.assertEqual(size, 7)

