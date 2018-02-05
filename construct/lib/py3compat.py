import sys

PY = sys.version_info[:2]
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = '__pypy__' in sys.builtin_module_names
supportskwordered = PY >= (3,6) or PYPY
supportscompiler = PY >= (3,6)


if PY3:
    stringtypes = (bytes, str, )
    integertypes = (int, )
    unicodestringtype = str
    bytestringtype = bytes

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
        """Iterates though b'...' string yielding characters as b'...' characters. On PY2 iter is the same."""
        return map(int2byte, s)

    def iterateints(s):
        """Iterates though b'...' string yielding characters as ints. On PY3 iter is the same."""
        return s

    def reprbytes(b):
        if isinstance(b, bytes):
            return repr(b)[2:-1]
        if isinstance(b, str):
            return repr(b)[1:-1]


else:
    stringtypes = (str, unicode, )
    integertypes = (int, long, )
    unicodestringtype = unicode
    bytestringtype = str

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
        """Iterates though b'...' string yielding characters as b'...' characters. On PY2 iter is the same."""
        return s

    def iterateints(s):
        """Iterates though b'...' string yielding characters as ints. On PY3 iter is the same."""
        return map(byte2int, s)

    def reprbytes(b):
        if isinstance(b, str):
            return repr(b)[1:-1]
        if isinstance(b, unicode):
            return repr(b)[2:-1]
