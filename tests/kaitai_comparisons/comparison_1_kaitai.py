# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Comparison1Kaitai(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.count = self._io.read_u4le()
        self.items = [None] * (self.count)
        for i in range(self.count):
            self.items[i] = self._root.Item(self._io, self, self._root)


    class Item(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num1 = self._io.read_u1()
            self.num2_lo = self._io.read_u2le()
            self.num2_hi = self._io.read_u1()
            # tweaked
            self.num2
            self.flags = self._root.Item.Flags(self._io, self, self._root)
            self.fixedarray1 = [None] * (3)
            for i in range(3):
                self.fixedarray1[i] = self._io.read_u1()

            self.name1 = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf-8")
            self.len_name2 = self._io.read_u1()
            self.name2 = (self._io.read_bytes(self.len_name2)).decode(u"utf-8")

        class Flags(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.bool1 = self._io.read_bits_int(1) != 0
                self.num4 = self._io.read_bits_int(3)
                self.padding = self._io.read_bits_int(4)


        @property
        def num2(self):
            if hasattr(self, '_m_num2'):
                return self._m_num2 if hasattr(self, '_m_num2') else None

            self._m_num2 = ((self.num2_hi << 16) | self.num2_lo)
            return self._m_num2 if hasattr(self, '_m_num2') else None


data = open("blob","rb").read()
Comparison1Kaitai.from_bytes(data)

from timeit import timeit
parsetime = timeit(lambda: Comparison1Kaitai.from_bytes(data), number=1000)/1000
print("Timeit measurements:")
print("parsing:           {:.10f} sec/call".format(parsetime))
