import unittest
import hashlib
from hashlib import sha512

from construct import *
from construct.lib.py3compat import PY26, PY3, PYPY



class TestAnchor(unittest.TestCase):
    def test_from_issue_60(self):
        # closed issue #60
        Header = Struct(
            "type" / UBInt8,
            "size" / Switch(lambda ctx: ctx.type,
            {
                0: UBInt8,
                1: UBInt16,
                2: UBInt32,
            }),
            "length" / Anchor,
        )

        self.assertEqual(Header.parse(b"\x00\x05"), Container(type=0)(size=5)(length=2))
        self.assertEqual(Header.parse(b"\x01\x00\x05"), Container(type=1)(size=5)(length=3))
        self.assertEqual(Header.parse(b"\x02\x00\x00\x00\x05"), Container(type=2)(size=5)(length=5))

        self.assertEqual(Header.build(dict(type=0, size=5)), b"\x00\x05")
        self.assertEqual(Header.build(dict(type=1, size=5)), b"\x01\x00\x05")
        self.assertEqual(Header.build(dict(type=2, size=5)), b"\x02\x00\x00\x00\x05")

        HeaderData = Struct(
            Embedded(Header),
            "data" / Bytes(lambda ctx: ctx.size),
        )

        self.assertEqual(HeaderData.build(dict(type=0, size=5, data=b"12345")), b"\x00\x0512345")
        self.assertEqual(HeaderData.build(dict(type=1, size=5, data=b"12345")), b"\x01\x00\x0512345")
        self.assertEqual(HeaderData.build(dict(type=2, size=5, data=b"12345")), b"\x02\x00\x00\x00\x0512345")



    # def test_from_issue_71(self):
    #     # closed issue #71

    #     class ValidatePayloadLength(Validator):
    #         def _validate(self, obj, ctx):
    #             return ctx.payload_end - ctx.payload_start == ctx.payload_len == len(ctx.raw_payload)
    #     class ChecksumValidator(Validator):
    #         def _validate(self, obj, ctx):
    #             return sha512(ctx.raw_payload).digest() == obj

    #     Outer = Struct(
    #         'struct_type' / UBInt16,
    #         'payload_len' / UBInt16,

    #         'payload_start' / Anchor,
    #         'raw_payload' / Peek(String(lambda ctx: ctx.payload_len)),
    #         'name' / PascalString(),
    #         'occupation' / PascalString(),
    #         'payload_end' / Anchor,

    #         'serial' / UBInt16,

    #         'checksum' / ChecksumValidator(Bytes(64)),
    #         ValidatePayloadLength(Pass),
    #         Terminator,
    #     )
    #     Inner = Struct(
    #         'name' / PascalString(), 
    #         'occupation' / PascalString(),
    #     )

    #     payload = Inner.build(dict(name=b"unknown", occupation=b"worker"))
    #     payload_len = len(payload)
    #     checksum = sha512(payload).digest()
    #     Outer.build(dict(name=b"unknown", occupation=b"worker", raw_payload=payload, payload_len=payload_len, checksum=checksum, serial=12345, struct_type=9001))


class TestChecksum(unittest.TestCase):

    def test(self):
        def sha512(b):
            return hashlib.sha512(b).digest()
        struct = Struct(
            "fields" / RawCopy(Struct(
                "a" / Byte,
                "b" / Byte,
            )),
            "checksum" / Checksum(Bytes(64), sha512, "fields"),
        )

        c = sha512(b"\x01\x02")
        self.assertEqual(struct.parse(b"\x01\x02"+c), Container(fields=dict(data=b"\x01\x02", value=Container(a=1)(b=2), offset1=0, offset2=2, length=2))(checksum=c))
        self.assertEqual(struct.build(dict(fields=dict(data=b"\x01\x02"))), b"\x01\x02"+c)
        # issue #124
        # self.assertEqual(struct.build(dict(fields=dict(value=dict(a=1,b=2)))), b"\x01\x02"+c)


# class TestEmbedOptional(unittest.TestCase):

#     def test_from_issue_28(self):
#         def vstring(name, embed=True, optional=True):
#             lfield = "_%s_length" % name.lower()
#             s = Struct(name,
#                 ULInt8(lfield),
#                 String(name, lambda ctx: getattr(ctx, lfield)))
#             if optional:
#                 s = Optional(s)
#             if embed:
#                 s = Embed(s)
#             return s

#         def build_struct(embed_g=True, embed_h=True):
#             s = Struct(
#                 "mystruct",
#                 ULInt32("a"),
#                 ULInt8("b"),
#                 ULInt8("c"),
#                 BitStruct(
#                     "d",
#                     BitField("d_bit7", 1),
#                     BitField("d_bit6", 1),
#                     BitField("d_bit5", 1),
#                     BitField("d_bit4", 1),
#                     BitField("d_bit3", 1),
#                     BitField("d_bit2", 1),
#                     BitField("d_bit1", 1),
#                     BitField("d_bit0", 1)),
#                 BitStruct(
#                     "e",
#                     BitField("e_bit7", 1),
#                     BitField("e_bit6", 1),
#                     BitField("e_bit5", 1),
#                     BitField("e_bit4", 1),
#                     BitField("e_bit3", 1),
#                     BitField("e_bit2", 1),
#                     BitField("e_bit1", 1),
#                     BitField("e_bit0", 1)),
#                 BFloat32("f"),
#                 vstring("g", embed=embed_g),
#                 vstring("h", embed=embed_h),
#                 BitStruct(
#                     "i",
#                     BitField("i_bit7", 1),
#                     BitField("i_bit6", 1),
#                     BitField("i_bit5", 1),
#                     BitField("i_bit4", 1),
#                     BitField("i_bit3", 1),
#                     BitField("i_bit2", 1),
#                     BitField("i_bit1", 1),
#                     BitField("i_bit0", 1)),
#                 SBInt8("j"),
#                 SBInt8("k"),
#                 SBInt8("l"),
#                 LFloat32("m"),
#                 LFloat32("n"),
#                 vstring("o"),
#                 vstring("p"),
#                 vstring("q"),
#                 vstring("r"))
#             return s

#         data = b'\xc3\xc0{\x00\x01\x00\x00\x00HOqA\x12some silly text...\x00\x0e\x00\x00\x00q=jAq=zA\x02dB\x02%f\x02%f\x02%f'
#         print("\n\nNo embedding for neither g and h, i is a container --> OK")
#         print(build_struct(embed_g=False, embed_h=False).parse(data))
#         print("Embed both g and h, i is not a container --> FAIL")
#         print(build_struct(embed_g=True, embed_h=True).parse(data))
#         print("\n\nEmbed g but not h --> EXCEPTION")
#         print(build_struct(embed_g=True, embed_h=False).parse(data))
#         # When setting optional to False in vstring method, all three tests above work fine.


# class TestEmbeddedBitStruct(unittest.TestCase):

#     def test_from_issue_39(self):
#         s = Struct('test',
#             Byte('len'), 
#             EmbeddedBitStruct(BitField('data', lambda ctx: ctx.len)),
#         )
#         self.assertEqual(s.parse(b"\x08\xff"), Container(len=8)(data=255))
#         self.assertEqual(s.build(dict(len=8,data=255)), b"\x08\xff")
#         # self.assertRaises(SizeofError, s.sizeof)


# class TestLazyStruct(unittest.TestCase):

#     def test(self):
#         s = LazyStruct("lazystruct",
#             Byte("a"),
#             CString("b"),
#         )
#         obj = s.parse(b"\x01abc\x00")
#         self.assertEqual(obj.a, 1)
#         self.assertEqual(obj.b, b"abc")
#         self.assertEqual(obj, dict(a=1,b=b"abc"))
#         self.assertRaises(SizeofError, s.sizeof)


# class TestNumpy(unittest.TestCase):

#     def test(self):
#         if not PYPY:
#             import numpy
#             s = Numpy("numpy")
#             a = numpy.array([1,2,3], dtype=numpy.int64)
#             self.assertTrue(numpy.array_equal(s.parse(s.build(a)), a))

