import unittest
from random import randint
from copy import copy

from construct.lib.container import Container, ListContainer


class TestContainer(unittest.TestCase):

    def test_getattr(self):
        c = Container(a=1)
        self.assertEqual(c["a"], c.a)

    def test_setattr(self):
        c = Container()
        c.a = 1
        self.assertEqual(c["a"], 1)

    def test_delattr(self):
        c = Container(a=1)
        del c.a
        self.assertFalse("a" in c)

    def test_update(self):
        c = Container(a=1)
        d = Container()
        d.update(c)
        self.assertEqual(d.a, 1)

    def test_eq_eq(self):
        c = Container(a=1)
        d = Container(a=1)
        self.assertEqual(c, d)

    def test_ne_wrong_type(self):
        c = Container(a=1)
        d = [("a", 1)]
        self.assertNotEqual(c, d)

    def test_ne_wrong_key(self):
        c = Container(a=1)
        d = Container(b=1)
        self.assertNotEqual(c, d)

    def test_ne_wrong_value(self):
        c = Container(a=1)
        d = Container(a=2)
        self.assertNotEqual(c, d)

    def test_copy(self):
        c = Container(a=1)
        d = c.copy()
        self.assertEqual(c, d)
        self.assertTrue(c is not d)

    def test_copy_module(self):
        c = Container(a=1)
        d = copy(c)
        self.assertEqual(c, d)
        self.assertTrue(c is not d)

    def test_bool_false(self):
        c = Container()
        self.assertFalse(c)

    def test_bool_true(self):
        c = Container(a=1)
        self.assertTrue(c)

    def test_in(self):
        c = Container(a=1)
        self.assertTrue("a" in c)

    def test_not_in(self):
        c = Container()
        self.assertTrue("a" not in c)

    def test_repr(self):
        c = Container(a=1, b=2)
        repr(c)

    def test_repr_recursive(self):
        c = Container(a=1, b=2)
        c.c = c
        repr(c)

    def test_str(self):
        c = Container(a=1, b=2)
        str(c)

    def test_str_recursive(self):
        c = Container(a=1, b=2)
        c.c = c
        str(c)
    
    def test_order(self):
        c = Container()
        while True:
            words = [("".join(chr(randint(65, 97)) for _ in range(randint(3,7))), i) for i in range(20)]
            if words != list(dict(words).keys()):
                break
        c.update(words)
        self.assertEqual([k for k, _ in words], list(c.keys()))

    def test_dict_arg(self):
        c = Container({'a': 1})
        d = Container(a=1)
        self.assertEqual(c, d)

    def test_multiple_dict_args(self):
        c = Container({'a': 1, 'b': 42}, {'b': 2})
        d = Container(a=1, b=2)
        self.assertEqual(c, d)

    def test_dict_and_kw_args(self):
        c = Container({'b': 42, 'c': 43}, {'a': 1, 'b': 2, 'c': 4}, c=3, d=4)
        d = Container(a=1, b=2, c=3, d=4)
        self.assertEqual(c, d)

class TestListContainer(unittest.TestCase):

    def test_str(self):
        l = ListContainer(range(5))
        str(l)

