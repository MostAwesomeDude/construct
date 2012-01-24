#-------------------------------------------------------------------------------
# py3compat.py
#
# Some Python2&3 compatibility code
#-------------------------------------------------------------------------------
import sys
PY3 = sys.version_info[0] == 3


if PY3:
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO

    def u(s):
        return s

    def int2byte(i):
        return bytes((i,))

    def byte2int(b):
        return b

    def str2bytes(s):
        return s.encode("latin-1")

    def str2unicode(s):
        return s

    def bytes2str(b):
        return b.decode('latin-1')

    def decodebytes(b, encoding):
        return bytes(b, encoding)

    advance_iterator = next
        
else:
    import cStringIO
    StringIO = BytesIO = cStringIO.StringIO

    int2byte = chr
    byte2int = ord

    def u(s):
        return unicode(s, "unicode_escape")

    def str2bytes(s):
        return s

    def str2unicode(s):
        return unicode(s, "unicode_escape")

    def bytes2str(b):
        return b

    def decodebytes(b, encoding):
        return b.decode(encoding)

    def advance_iterator(it):
        return it.next()

