"""
Some Python 2 & 3 compatibility code.
"""

import sys
PY3 = sys.version_info[0] == 3
PY26 = sys.version_info[:2] == (2,6)
PYPY = '__pypy__' in sys.builtin_module_names


if PY3:
    def int2byte(i):
        """Converts int (0 through 255) into b'...' character."""
        return bytes((i,))

    def byte2int(b):
        """Converts b'...' character into int (0 through 255)."""
        return ord(b)

    def str2bytes(s):
        """Converts '...' str into b'...' bytes. On PY2 they are equivalent."""
        return s.encode("utf8")

    def bytes2str(b):
        """Converts b'...' bytes into str. On PY2 they are equivalent."""
        return b.decode("utf8")

    def str2unicode(s):
        """Converts '...' str into u'...' unicode string. On PY3 they are equivalent."""
        return s

    def unicode2str(s):
        """Converts u'...' string into '...' str. On PY3 they are equivalent."""
        return s

    def iteratebytes(s):
        """Itarates though b'...' string yielding characters as ints. On PY3 iter is the same."""
        return s

else:
    def int2byte(i):
        """Converts int (0 through 255) into b'...' character."""
        return chr(i)

    def byte2int(s):
        """Converts b'...' character into int (0 through 255)."""
        return ord(s)

    def str2bytes(s):
        """Converts '...' str into b'...' bytes. On PY2 they are equivalent."""
        return s

    def bytes2str(b):
        """Converts b'...' bytes into str. On PY2 they are equivalent."""
        return b

    def str2unicode(b):
        """Converts '...' str into u'...' unicode string. On PY3 they are equivalent."""
        return b.encode("utf8")

    def unicode2str(s):
        """Converts u'...' string into '...' str. On PY3 they are equivalent."""
        return s.decode("utf8")

    def iteratebytes(s):
        """Itarates though b'...' string yielding characters as ints. On PY3 iter is the same."""
        for c in s:
            yield byte2int(c)

