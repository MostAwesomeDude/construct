import unittest

from construct import Struct, MetaField, StaticField, FormatField, Field
from construct import Container, Byte
from construct import FieldError, SizeofError


class TestStruct(unittest.TestCase):
    def test_build_from_nested_dicts(self):
        s = Struct(None, Struct('substruct1', Byte('field1')))
        self.assertEqual(s.build(dict(substruct1=dict(field1=5))), b'\x05')


class TestStaticField(unittest.TestCase):

    def setUp(self):
        self.sf = StaticField("staticfield", 2)

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.sf.parse(b"ab"), b"ab")

    def test_build(self):
        self.assertEqual(self.sf.build(b"ab"), b"ab")

    def test_parse_too_short(self):
        self.assertRaises(FieldError, self.sf.parse, b"a")

    def test_build_too_short(self):
        self.assertRaises(FieldError, self.sf.build, b"a")

    def test_sizeof(self):
        self.assertEqual(self.sf.sizeof(), 2)

    def test_field_parse(self):
        f = Field('name', 6)
        self.assertEqual(f.parse(b'abcdef'), b'abcdef')
        self.assertEqual(f.parse(b'12abcdef'), b'12abcd')
        

class TestFormatField(unittest.TestCase):

    def setUp(self):
        self.ff = FormatField("formatfield", "<", "L")

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.ff.parse(b"\x12\x34\x56\x78"), 0x78563412)

    def test_build(self):
        self.assertEqual(self.ff.build(0x78563412), b"\x12\x34\x56\x78")

    def test_parse_too_short(self):
        self.assertRaises(FieldError, self.ff.parse, b"\x12\x34\x56")

    def test_build_too_long(self):
        self.assertRaises(FieldError, self.ff.build, 9e9999)

    def test_sizeof(self):
        self.assertEqual(self.ff.sizeof(), 4)

class TestMetaField(unittest.TestCase):

    def setUp(self):
        self.mf = MetaField("metafield", lambda context: 3)

    def test_trivial(self):
        pass

    def test_parse(self):
        self.assertEqual(self.mf.parse(b"abc"), b"abc")

    def test_build(self):
        self.assertEqual(self.mf.build(b"abc"), b"abc")

    def test_parse_too_short(self):
        self.assertRaises(FieldError, self.mf.parse, b"ab")

    def test_build_too_short(self):
        self.assertRaises(FieldError, self.mf.build, b"ab")

    def test_sizeof(self):
        self.assertEqual(self.mf.sizeof(), 3)

class TestMetaFieldStruct(unittest.TestCase):

    def setUp(self):
        self.mf = MetaField("data", lambda context: context["length"])
        self.s = Struct("foo", Byte("length"), self.mf)

    def test_trivial(self):
        pass

    def test_parse(self):
        c = self.s.parse(b"\x03ABC")
        self.assertEqual(c.length, 3)
        self.assertEqual(c.data, b"ABC")

        c = self.s.parse(b"\x04ABCD")
        self.assertEqual(c.length, 4)
        self.assertEqual(c.data, b"ABCD")

    def test_sizeof_default(self):
        self.assertRaises(SizeofError, self.mf.sizeof)

    def test_sizeof(self):
        context = Container(length=4)
        self.assertEqual(self.mf.sizeof(context), 4)

