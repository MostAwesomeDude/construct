import declarativeunittest

from construct.lib.py3compat import *


class TestAll(declarativeunittest.TestCase):
    alltests = [

        # issue #128
        # [PY26 != PY3],

        [int2byte(5), b"\x05"],
        [byte2int(b"\x05"), 5],
        [all(byte2int(int2byte(i)) == i for i in range(256))],

        [str2bytes("abc"), b"abc"],
        [bytes2str(b"abc"), "abc"],
        [bytes2str(str2bytes("abc123\n")), "abc123\n"],
        [str2bytes(bytes2str(b"abc123\n")), b"abc123\n"],

        [str2unicode("abc"), u"abc"],
        [unicode2str(u"abc"), "abc"],
        [unicode2str(str2unicode("abc123\n")), "abc123\n"],
        [str2unicode(unicode2str(u"abc123\n")), "abc123\n"],

        [list(iteratebytes(b"abc")), [b"a",b"b",b"c"]],
        [all(list(iteratebytes(int2byte(i))) == [int2byte(i)] for i in range(256))],

        [list(iterateints(b"abc")), [97,98,99]],
        [all(list(iterateints(int2byte(i))) == [i] for i in range(256))],

    ]

