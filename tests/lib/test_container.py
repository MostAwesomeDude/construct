import unittest
from declarativeunittest import raises

from construct import *
from construct.lib import *
from construct.lib.py3compat import *

from copy import copy
from random import randint, shuffle
def shuffled(alist):
    a = list(alist)
    shuffle(a)
    return a



class TestContainer(unittest.TestCase):
    def testall(self):

        c = Container(a=1)(b=2)(c=3)(d=4)
        assert c == Container(c)

        c = Container(a=1)
        assert c["a"] == 1
        assert c.a == 1
        assert raises(lambda: c.unknownkey) == AttributeError
        assert raises(lambda: c["unknownkey"]) == KeyError

        c = Container()
        c.a = 1
        assert c["a"] == 1
        assert c.a == 1
        c["a"] = 2
        assert c["a"] == 2
        assert c.a == 2

        c = Container(a=1)
        del c.a
        assert "a" not in c
        assert raises(lambda: c.a) == AttributeError
        assert raises(lambda: c["a"]) == KeyError
        assert c == Container()

        c = Container(a=1)
        del c["a"]
        assert "a" not in c
        assert raises(lambda: c.a) == AttributeError
        assert raises(lambda: c["a"]) == KeyError
        assert c == Container()

        c = Container(a=1)(b=2)(c=3)(d=4)
        d = Container()
        d.update(c)
        assert d.a == 1
        assert d.b == 2
        assert d.c == 3
        assert d.d == 4
        assert c == d
        assert c.items() == d.items()

        c = Container(a=1)(b=2)(c=3)(d=4)
        d = Container()
        d.update([("a",1),("b",2),("c",3),("d",4)])
        assert d.a == 1
        assert d.b == 2
        assert d.c == 3
        assert d.d == 4
        assert c == d
        assert c.items() == d.items()

        # issue #130
        # test pop popitem clear

        c = Container(a=1)(b=2)(c=3)(d=4)
        assert c.keys() == ["a","b","c","d"]
        assert c.values() == [1,2,3,4]
        assert c.items() == [("a",1),("b",2),("c",3),("d",4)]
        assert list(c.iterkeys()) == ["a","b","c","d"]
        assert list(c.itervalues()) == [1,2,3,4]
        assert list(c.iteritems()) == [("a",1),("b",2),("c",3),("d",4)]
        assert list(c) == c.keys()

        c = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        assert c == c
        assert c == d

        c = Container(a=1)(b=2)(c=3)
        d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
        assert c != d
        assert d != c

        c = Container(a=1)
        d = [("a" == 1)]
        assert c != d

        c = Container(a=1)
        d = Container(b=1)
        assert c != d

        c = Container(a=1)
        d = Container(a=2)
        assert c != d

        c = Container(a=1)
        d = c.copy()
        assert c == d
        assert c is not d

        c = Container(a=1)
        d = copy(c)
        assert c == d
        assert c is not d

        c = Container(a=1)(b=2)(c=3)(d=4)
        assert len(c) == 4
        assert c
        c = Container()
        assert len(c) == 0
        assert not c

        c = Container(a=1)
        assert "a" in c
        assert "b" not in c

        print("REGRESSION: recursion_lock() used to leave private keys.")
        c = Container()
        str(c); repr(c)
        assert not c

        c = Container()
        assert str(c) == "Container: "
        assert repr(c) == "Container()"
        assert eval(repr(c)) == c

        c = Container(a=1)(b=2)(c=3)
        assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = 3"
        assert repr(c) == "Container(a=1)(b=2)(c=3)"
        assert eval(repr(c)) == c

        c = Container(a=1)(b=2)(c=Container())
        assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = Container: "
        assert repr(c) == "Container(a=1)(b=2)(c=Container())"
        assert eval(repr(c)) == c

        c = Container(a=1)(b=2)
        c.c = c
        assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = <recursion detected>"
        assert repr(c) == "Container(a=1)(b=2)(c=<recursion detected>)"

        c = Container({'a': 1})
        d = Container(a=1)
        assert c == d

        c = Container({'a': 1, 'b': 42}, {'b': 2})
        d = Container(a=1, b=2)
        assert c == d

        c = Container({'b': 42, 'c': 43}, {'a': 1, 'b': 2, 'c': 4}, c=3, d=4)
        d = Container(a=1, b=2, c=3, d=4)
        assert c == d


class TestFlagsContainer(unittest.TestCase):

    def test_str(self):
        c = FlagsContainer(a=True, b=False, c=True, d=False)
        assert str(c)
        assert repr(c)

    def test_eq(self):
        c = FlagsContainer(a=True, b=False, c=True, d=False)
        d = FlagsContainer(a=True, b=False, c=True, d=False)
        assert c == d


class TestListContainer(unittest.TestCase):

    def test_str(self):
        l = ListContainer(range(5))
        assert str(l)
        assert repr(l)

        l = ListContainer(range(5))
        l.append(l)
        assert str(l)
        assert repr(l)

