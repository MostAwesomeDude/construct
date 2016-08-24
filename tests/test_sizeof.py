import unittest
from construct import Struct, UBInt8, Bytes, Container

def foo(ctx):
    print("!! %r" % (ctx,))
    return ctx._.length + ctx.inner_length

class TestSizeof(unittest.TestCase):
    def test(self):
        pstring = Struct("pstring", 
            UBInt8("length"),
            Struct("inner",
                UBInt8("inner_length"),
                Bytes("data", foo),
            )
        )
        obj = pstring.parse(b"\x03\x02helloXXX")
        print(repr(obj))
        self.assertEqual(obj, Container(length = 3, inner = Container(inner_length = 2, data = b"hello")))
        size = pstring._sizeof(Container(inner_length = 2, _ = Container(length = 3)))
        self.assertEqual(size, 7)

