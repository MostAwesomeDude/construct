import unittest
from declarativeunittest import raises

from construct import *
from construct.lib.py3compat import *





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

