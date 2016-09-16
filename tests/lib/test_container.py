import declarativeunittest

from construct import *
from construct.lib import *
from construct.lib.py3compat import *

from copy import copy
from random import randint, shuffle
def shuffled(alist):
    a = list(alist)
    shuffle(a)
    return a

import unittest
import traceback
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys




class TestAll(declarativeunittest.TestCase):
    def alltestsinteractive(self):

        c = Container(a=1)(b=2)(c=3)(d=4)
        yield [c, Container(c)]

        c = Container(a=1)
        yield [c["a"], 1]
        yield [c.a, 1]
        yield [lambda none: c.unknownkey, None, None, AttributeError]
        self.assertRaises(AttributeError, lambda: c.unknownkey)
        self.assertRaises(KeyError, lambda: c["unknownkey"])

        c = Container()
        c.a = 1
        yield [c["a"], 1]
        yield [c.a, 1]
        c["a"] = 2
        yield [c["a"], 2]
        yield [c.a, 2]

        c = Container(a=1)
        del c.a
        yield ["a" not in c]
        self.assertRaises(AttributeError, lambda: c.a)
        self.assertRaises(KeyError, lambda: c["a"])
        yield [c, Container()]

        c = Container(a=1)
        del c["a"]
        yield ["a" not in c]
        self.assertRaises(AttributeError, lambda: c.a)
        self.assertRaises(KeyError, lambda: c["a"])
        yield [c, Container()]

        c = Container(a=1)(b=2)(c=3)(d=4)
        d = Container()
        d.update(c)
        yield [d.a, 1]
        yield [d.b, 2]
        yield [d.c, 3]
        yield [d.d, 4]
        yield [c, d]
        yield [c.items(), d.items()]

        c = Container(a=1)(b=2)(c=3)(d=4)
        d = Container()
        d.update([("a",1),("b",2),("c",3),("d",4)])
        yield [d.a, 1]
        yield [d.b, 2]
        yield [d.c, 3]
        yield [d.d, 4]
        yield [c, d]
        yield [c.items(), d.items()]

        # issue #130
        # test pop popitem clear

        c = Container(a=1)(b=2)(c=3)(d=4)
        yield [c.keys(), ["a","b","c","d"]]
        yield [c.values(), [1,2,3,4]]
        yield [c.items(), [("a",1),("b",2),("c",3),("d",4)]]
        yield [list(c.iterkeys()), ["a","b","c","d"]]
        yield [list(c.itervalues()), [1,2,3,4]]
        yield [list(c.iteritems()), [("a",1),("b",2),("c",3),("d",4)]]
        yield [list(c), c.keys()]

        c = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        yield [c, c]
        yield [c, d]

        c = Container(a=1)(b=2)(c=3)
        d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        yield [c != d]
        yield [d != c]

        print("WARNING: dict randomizes key order so this test may fail unexpectedly if the order is correct by chance.")
        c = Container(a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10,k=11,l=12,m=13,n=14)
        yield [c != Container(shuffled(c.items()))]

        c = Container(a=1)
        d = [("a", 1)]
        yield [c != d]

        c = Container(a=1)
        d = Container(b=1)
        yield [c != d]

        c = Container(a=1)
        d = Container(a=2)
        yield [c != d]

        c = Container(a=1)
        d = c.copy()
        yield [c, d]
        yield [c is not d]

        c = Container(a=1)
        d = copy(c)
        yield [c, d]
        yield [c is not d]

        c = Container(a=1)(b=2)(c=3)(d=4)
        yield [len(c), 4]
        yield [c]
        c = Container()
        yield [len(c), 0]
        yield [not c]

        c = Container(a=1)
        yield ["a" in c]
        yield ["b" not in c]

        print("REGRESSION: recursion_lock() used to leave private keys.")
        c = Container()
        str(c); repr(c)
        yield [not c]

        c = Container()
        yield [str(c), "Container: "]
        yield [repr(c), "Container()"]
        yield [eval(repr(c)), c]

        c = Container(a=1)(b=2)(c=3)
        yield [str(c), "Container: \n    a = 1\n    b = 2\n    c = 3"]
        yield [repr(c), "Container(a=1)(b=2)(c=3)"]
        yield [eval(repr(c)), c]

        c = Container(a=1)(b=2)(c=Container())
        yield [str(c), "Container: \n    a = 1\n    b = 2\n    c = Container: "]
        yield [repr(c), "Container(a=1)(b=2)(c=Container())"]
        yield [eval(repr(c)), c]

        c = Container(a=1)(b=2)
        c.c = c
        yield [str(c), "Container: \n    a = 1\n    b = 2\n    c = <recursion detected>"]
        yield [repr(c), "Container(a=1)(b=2)(c=<recursion detected>)"]

        print("NOTE: dicts do not preserve order while eq does check it (by default).")
        print("However, only one entry is in order.")
        c = Container({'a': 1})
        d = Container(a=1)
        yield [c, d]
        yield [c.__eq__(d, skiporder=True)]
        yield [c.__eq__(d, skiporder=False)]

        print("NOTE: dicts do not preserve order while eq does check it (by default).")
        c = Container({'a': 1, 'b': 42}, {'b': 2})
        d = Container(a=1, b=2)
        yield [c.__eq__(d, skiporder=True)]

        print("NOTE: dicts do not preserve order while eq does check it (by default).")
        c = Container({'b': 42, 'c': 43}, {'a': 1, 'b': 2, 'c': 4}, c=3, d=4)
        d = Container(a=1, b=2, c=3, d=4)
        yield [c.__eq__(d, skiporder=True)]




class TestFlagsContainer(unittest.TestCase):

    def test_str(self):
        c = FlagsContainer(a=True, b=False, c=True, d=False)
        str(c)
        repr(c)

    def test_eq(self):
        c = FlagsContainer(a=True, b=False, c=True, d=False)
        d = FlagsContainer(a=True, b=False, c=True, d=False)
        self.assertEqual(c, d)


class TestListContainer(unittest.TestCase):

    def test_str(self):
        l = ListContainer(range(5))
        str(l)
        repr(l)

    def test_recursive_str(self):
        l = ListContainer(range(5))
        l.append(l)
        str(l)
        repr(l)


