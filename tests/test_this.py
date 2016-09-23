import unittest, pytest, os
from declarativeunittest import raises
ontravis = 'TRAVIS' in os.environ

from construct import *
from construct.lib import *


class TestThis(unittest.TestCase):
    
    def testall(self):
        this_example = Struct(
            # straight-forward usage: instead of passing (lambda ctx: ctx["length"]) use this.length
            "length" / Int8ub,
            "value" / Bytes(this.length),
            # an example of nesting: '_' refers to the parent's scope
            "nested" / Struct(
                "b1" / Int8ub,
                "b2" / Int8ub,
                "b3" / Computed(this.b1 * this.b2 + this._.length),
            ),
            # and conditions work as expected
            "condition" / IfThenElse(
                this.nested.b1 > 50,
                "c1" / Int32ub,
                "c2" / Int8ub,
            ),
        )
        assert this_example.parse(b"\x05helloABXXXX") == Container(length=5)(value=b'hello')(nested=Container(b1=65)(b2=66)(b3=4295))(condition=1482184792)
        assert this_example.build(dict(length=5, value=b'hello', nested=dict(b1=65, b2=66), condition=1482184792)) == b"\x05helloABXXXX"


class TestPath(unittest.TestCase):

    def testall(self):
        path = Path("path")
        x = ~((path.foo * 2 + 3 << 2) % 11)
        assert str(x) == 'not ((((path.foo * 2) + 3) >> 2) % 11)'
        assert repr(x) == 'not ((((path.foo * 2) + 3) >> 2) % 11)'
        assert not x(dict(foo=7))

