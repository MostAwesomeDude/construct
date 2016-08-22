import unittest
from construct import Struct, UBInt8, UBInt32, IfThenElse, Value, Field, Container
from construct import this


class TestThisExpressions(unittest.TestCase):
    
    this_example = Struct("this_example",
        # straight-forward usage: instead of passing (lambda ctx: ctx["length"]) use this.length
        UBInt8("length"),
        Field("value", this.length),
        
        # an example of nesting: '_' refers to the parent's scope
        Struct("nested",
            UBInt8("b1"),
            UBInt8("b2"),
            Value("b3", this.b1 * this.b2 + this._.length)
        ),
        
        # and conditions work as expected
        IfThenElse("condition", this.nested.b1 > 50,
            UBInt32("foo"),
            UBInt8("bar"),
        )
    )

    def test_parse(self):
        res = self.this_example.parse(b"\x05helloABXXXX")
        expected = Container(length = 5, value = b'hello', 
            nested = Container(b1 = 65, b2 = 66, b3 = 4295), 
            condition = 1482184792)
        self.assertEquals(res, expected)
    
    def test_build(self):
        obj = Container(length = 5, value = b'hello', 
            nested = Container(b1 = 65, b2 = 66, b3 = None), condition = 1482184792)
        data = self.this_example.build(obj)
        self.assertEquals(data, b"\x05helloABXXXX")

