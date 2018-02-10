import sys

PY = sys.version_info[:2]
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PYPY = '__pypy__' in sys.builtin_module_names

supportskwordered = PY >= (3,6) or PYPY
supportscompiler = PY >= (3,6)
supportsintenum = PY >= (3,4)
supportsintflag = PY >= (3,6)
try:
    import numpy
    supportsnumpy = True
except ImportError:
    supportsnumpy = False


if PY3:
    stringtypes = (bytes, str, )
    integertypes = (int, )
    unicodestringtype = str
    bytestringtype = bytes

    INT2BYTE_CACHE = {i:bytes((i,)) for i in range(256)}
    def int2byte(i):
        """Converts integer (0 through 255) into b'...' character."""
        return INT2BYTE_CACHE[i]

    def byte2int(b):
        """Converts b'...' character into integer (0 through 255)."""
        return ord(b)

    def str2bytes(s):
        """Converts '...' string into b'...' string. On PY2 they are equivalent."""
        return s.encode("utf8")

    def bytes2str(b):
        """Converts b'...' string into '...' string. On PY2 they are equivalent."""
        return b.decode("utf8")

    def str2unicode(s):
        """Converts '...' string into u'...' string. On PY3 they are equivalent."""
        return s

    def unicode2str(s):
        """Converts u'...' string into '...' string. On PY3 they are equivalent."""
        return s

    ITERATEBYTES_CACHE = {i:bytes((i,)) for i in range(256)}
    def iteratebytes(s):
        """Iterates though b'...' string yielding b'...' characters. On PY2 iter is the same."""
        return (ITERATEBYTES_CACHE[i] for i in s)

    def iterateints(s):
        """Iterates though b'...' string yielding integers. On PY3 iter is the same."""
        return s

    def reprbytes(b):
        """Trims b- u- prefix and both apostrophies."""
        if isinstance(b, bytes):
            return repr(b)[2:-1]
        if isinstance(b, str):
            return repr(b)[1:-1]


else:
    stringtypes = (str, unicode, )
    integertypes = (long, int, )
    unicodestringtype = unicode
    bytestringtype = str

    def int2byte(i):
        """Converts integer (0 through 255) into b'...' character."""
        return chr(i)

    def byte2int(s):
        """Converts b'...' character into integer (0 through 255)."""
        return ord(s)

    def str2bytes(s):
        """Converts '...' string into b'...' string. On PY2 they are equivalent."""
        return s

    def bytes2str(b):
        """Converts b'...' string into '...' string. On PY2 they are equivalent."""
        return b

    def str2unicode(b):
        """Converts '...' string into u'...' string. On PY3 they are equivalent."""
        return b.encode("utf8")

    def unicode2str(s):
        """Converts u'...' string into '...' string. On PY3 they are equivalent."""
        return s.decode("utf8")

    def iteratebytes(s):
        """Iterates though b'...' string yielding b'...' characters. On PY2 iter is the same."""
        return s

    def iterateints(s):
        """Iterates though b'...' string yielding integers. On PY3 iter is the same."""
        return (ord(c) for c in s)

    def reprbytes(b):
        """Trims b- u- prefix and both apostrophies."""
        if isinstance(b, str):
            return repr(b)[1:-1]
        if isinstance(b, unicode):
            return repr(b)[2:-1]
