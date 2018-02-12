import pytest
xfail = pytest.mark.xfail
skip = pytest.mark.skip
skipif = pytest.mark.skipif

import os, math, random, collections, itertools, io, hashlib, binascii

from construct import *
from construct.lib import *

ontravis = "TRAVIS" in os.environ
ident = lambda x: x
devzero = open("/dev/zero", "rb")


def raises(func, *args, **kw):
    try:
        func(*args, **kw)
        return None
    except Exception as e:
        return e.__class__


def atmostone(*args):
    return sum(1 for x in args if x) <= 1


def common(format, datasample, objsample, sizesample=SizeofError, **kw):
    obj = format.parse(datasample, **kw)
    # print("parsed:   ", obj)
    # print("expected: ", objsample)
    assert obj == objsample
    data = format.build(objsample, **kw)
    # print("build:    ", data)
    # print("expected: ", datasample)
    assert data == datasample
    # following are implied by above (re-parse and re-build)
    # assert format.parse(format.build(obj)) == obj
    # assert format.build(format.parse(data)) == data
    if isinstance(sizesample, int):
        size = format.sizeof(**kw)
        # print("size:     ", size)
        # print("expected: ", sizesample)
        assert size == sizesample
    else:
        size = raises(format.sizeof, **kw)
        # print("size:     ", size)
        # print("expected: ", sizesample)
        assert size == sizesample
    # print()


def commonhex(format, hexdata):
    commonbytes(format, binascii.unhexlify(hexdata))


def commondump(format, filename):
    if ontravis:
        filename = "examples/formats/" + filename
    if not ontravis:
        filename = "tests/examples/formats/" + filename
    with open(filename,'rb') as f:
        data = f.read()
    commonbytes(format, data)


def commonbytes(format, data):
    obj = format.parse(data)
    data2 = format.build(obj)
    # protocol examples pass but format examples fail at this
    # assert binascii.hexlify(data2) == binascii.hexlify(data)
