import unittest
from declarativeunittest import raises, atmostone, alldifferent

from construct.lib.py3compat import *


class TestPy3compat(unittest.TestCase):

    def test_version(self):
        assert atmostone(PY2, PY3)
        assert atmostone(PY27, PY32, PY33, PY34, PY35, PY36)

    def test_int_byte(self):
        assert int2byte(5) == b"\x05"
        assert byte2int(b"\x05") == 5
        assert all(byte2int(int2byte(i)) == i for i in range(256))

    def test_str_bytes(self):
        assert str2bytes("abc") == b"abc"
        assert bytes2str(b"abc") == "abc"
        assert bytes2str(str2bytes("abc123\n")) == "abc123\n"
        assert str2bytes(bytes2str(b"abc123\n")) == b"abc123\n"

    def test_str_unicode(self):
        assert str2unicode("abc") == u"abc"
        assert unicode2str(u"abc") == "abc"
        assert unicode2str(str2unicode("abc123\n")) == "abc123\n"
        assert str2unicode(unicode2str(u"abc123\n")) == "abc123\n"

    def test_iteratebytes(self):
        assert list(iteratebytes(b"abc")) == [b"a", b"b", b"c"]
        assert all(list(iteratebytes(int2byte(i))) == [int2byte(i)] for i in range(256))

    def test_iterateints(self):
        assert list(iterateints(b"abc")) == [97,98,99]
        assert all(list(iterateints(int2byte(i))) == [i] for i in range(256))

