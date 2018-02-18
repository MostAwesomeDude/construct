from declarativeunittest import *
from construct.lib.py3compat import *


def test_version():
    assert PY2 or PY3

def test_int_byte():
    assert int2byte(5) == b"\x05"
    assert int2byte(255) == b"\xff"
    assert byte2int(b"\x05") == 5
    assert byte2int(b"\xff") == 255
    assert all(byte2int(int2byte(i)) == i for i in range(256))

def test_str_bytes():
    assert str2bytes("abc") == b"abc"
    assert bytes2str(b"abc") == "abc"
    assert bytes2str(str2bytes("abc123\n")) == "abc123\n"
    assert str2bytes(bytes2str(b"abc123\n")) == b"abc123\n"

def test_str_unicode():
    assert str2unicode("abc") == u"abc"
    assert unicode2str(u"abc") == "abc"
    assert unicode2str(str2unicode("abc123\n")) == "abc123\n"
    assert str2unicode(unicode2str(u"abc123\n")) == "abc123\n"

def test_iteratebytes():
    assert list(iteratebytes(b"abc")) == [b"a", b"b", b"c"]
    assert all(list(iteratebytes(int2byte(i))) == [int2byte(i)] for i in range(256))

def test_iterateints():
    assert list(iterateints(b"abc")) == [97,98,99]
    assert all(list(iterateints(int2byte(i))) == [i] for i in range(256))
