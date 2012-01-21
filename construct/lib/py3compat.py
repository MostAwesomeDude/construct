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

    def int2byte(i):
        return bytes((i,))
else:
    import cStringIO
    StringIO = BytesIO = cStringIO.StringIO

    int2byte = chr



