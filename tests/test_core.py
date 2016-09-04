import unittest

from construct import *


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


class TestAligned(unittest.TestCase):

    def test_from_issue_76(self):
        def barLength(ctx):
            # print("Context of field2 is", ctx)
            return ctx.field1
        test1 = Struct("test1",
            Aligned(
                Struct("test2",
                    ULInt8("field1"),
                    Field("field2", barLength)
                ),
                modulus=4,
            )
        )
        self.assertEqual(test1.parse(b"\x02\xab\xcd\x00"), Container(test2=Container(field1=2,field2=b"\xab\xcd")))


class TestAnchor(unittest.TestCase):

    def test_from_issue_60(self):
        Header = Struct("header",
            UBInt8("type"),
            Switch("size", lambda ctx: ctx.type,
            {
                0: UBInt8("size"),
                1: UBInt16("size"),
                2: UBInt32("size")
            }),
            Anchor("length"),
        )
        self.assertEqual(Header.parse(b"\x00\x05"), Container(type=0, size=5, length=2))
        self.assertEqual(Header.parse(b"\x01\x00\x05"), Container(type=1, size=5, length=3))
        self.assertEqual(Header.parse(b"\x02\x00\x00\x00\x05"), Container(type=2, size=5, length=5))

        self.assertEqual(Header.build(Container(type=0, size=5)), b"\x00\x05")
        self.assertEqual(Header.build(Container(type=1, size=5)), b"\x01\x00\x05")
        self.assertEqual(Header.build(Container(type=2, size=5)), b"\x02\x00\x00\x00\x05")

    def test_subtract(self):
        Header = Struct("header",
            UBInt8("type"),
            Anchor("start"),
            Switch("size", lambda ctx: ctx.type,
            {
                0: UBInt8("size"),
                1: UBInt16("size"),
                2: UBInt32("size")
            }),
            Anchor("end", subtract="start"),
        )
        self.assertEqual(Header.parse(b"\x00\x05"), Container({'start': 1, 'end': 1, 'type': 0, 'size': 5}))
        self.assertEqual(Header.parse(b"\x01\x00\x05"), Container({'start': 1, 'end': 2, 'type': 1, 'size': 5}))
        self.assertEqual(Header.parse(b"\x02\x00\x00\x00\x05"), Container({'start': 1, 'end': 4, 'type': 2, 'size': 5}))

